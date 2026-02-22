// SPDX-License-Identifier: GPL-2.0
/*
 * kp_timsort_sort.c - list_sort replacement with natural run detection
 *
 * Based on lib/list_sort.c from Linux 6.19.
 *
 * merge() and merge_final() are copied verbatim (with klp_ prefix) because
 * they are static in the original and thus inaccessible to livepatch modules.
 *
 * The main function klp_list_sort() replaces the per-element insertion loop
 * with natural run detection: instead of feeding one element at a time into
 * the merge tree, it scans for naturally ascending subsequences ("runs") and
 * feeds entire runs as units. This achieves O(n log r) comparisons where r
 * is the number of natural runs, while degenerating to the original O(n log n)
 * for fully random input.
 */

#include <linux/compiler.h>
#include <linux/kernel.h>
#include <linux/list.h>
#include <linux/list_sort.h>
#include "kp_timsort_sort.h"
#include "kp_timsort_stats.h"

/*
 * Comparison wrapper for instrumentation.
 * Wraps the caller's cmp function to count every comparison made.
 */
struct cmp_wrapper {
	list_cmp_func_t real_cmp;
	void *real_priv;
	unsigned long comparisons;
};

static int counting_cmp(void *priv, const struct list_head *a,
			const struct list_head *b)
{
	struct cmp_wrapper *w = priv;

	w->comparisons++;
	return w->real_cmp(w->real_priv, a, b);
}

/*
 * Copied from lib/list_sort.c merge().
 *
 * Returns a list organized in an intermediate format suited
 * to chaining of merge() calls: null-terminated, no reserved or
 * sentinel head node, "prev" links not maintained.
 */
__attribute__((nonnull(2,3,4)))
static struct list_head *klp_merge(void *priv, list_cmp_func_t cmp,
				   struct list_head *a, struct list_head *b)
{
	struct list_head *head, **tail = &head;

	for (;;) {
		/* if equal, take 'a' -- important for sort stability */
		if (cmp(priv, a, b) <= 0) {
			*tail = a;
			tail = &a->next;
			a = a->next;
			if (!a) {
				*tail = b;
				break;
			}
		} else {
			*tail = b;
			tail = &b->next;
			b = b->next;
			if (!b) {
				*tail = a;
				break;
			}
		}
	}
	return head;
}

/*
 * Copied from lib/list_sort.c merge_final().
 *
 * Combine final list merge with restoration of standard doubly-linked
 * list structure.  This approach duplicates code from merge(), but
 * runs faster than the tidier alternatives of either a separate final
 * prev-link restoration pass, or maintaining the prev links
 * throughout.
 */
__attribute__((nonnull(2,3,4,5)))
static void klp_merge_final(void *priv, list_cmp_func_t cmp,
			     struct list_head *head,
			     struct list_head *a, struct list_head *b)
{
	struct list_head *tail = head;
	u8 count = 0;

	for (;;) {
		/* if equal, take 'a' -- important for sort stability */
		if (cmp(priv, a, b) <= 0) {
			tail->next = a;
			a->prev = tail;
			tail = a;
			a = a->next;
			if (!a)
				break;
		} else {
			tail->next = b;
			b->prev = tail;
			tail = b;
			b = b->next;
			if (!b) {
				b = a;
				break;
			}
		}
	}

	/* Finish linking remainder of list b on to tail */
	tail->next = b;
	do {
		/*
		 * If the merge is highly unbalanced (e.g. the input is
		 * already sorted), this loop may run many iterations.
		 * Continue callbacks to the client even though no
		 * element comparison is needed, so the client's cmp()
		 * routine can invoke cond_resched() periodically.
		 */
		if (unlikely(!++count))
			cmp(priv, b, b);
		b->prev = tail;
		tail = b;
		b = b->next;
	} while (b);

	/* And the final links to make a circular doubly-linked list */
	tail->next = head;
	head->prev = tail;
}

/*
 * klp_list_sort - list_sort replacement with natural run detection
 * @priv: private data, opaque to list_sort(), passed to @cmp
 * @head: the list to sort
 * @cmp: the elements comparison function
 *
 * Drop-in replacement for list_sort().  The merge scheduling logic is
 * identical to the original: "count" tracks the number of sublists pushed
 * onto the pending stack, and merges are triggered by the same bit-counting
 * scheme.  The only difference is that each "unit" pushed is a natural
 * ascending run (possibly multiple elements) instead of a single element.
 *
 * For random input, most runs are length 1 and this degenerates to the
 * original algorithm.  For partially sorted input, longer runs reduce
 * the total number of merges needed.
 */
__attribute__((nonnull(2,3)))
void klp_list_sort(void *priv, struct list_head *head, list_cmp_func_t cmp)
{
	struct list_head *list = head->next, *pending = NULL;
	size_t count = 0;	/* Number of runs in pending */
	size_t n_elements = 0;
	unsigned long n_asc_runs = 0, n_desc_runs = 0;
	struct cmp_wrapper wrapper = {
		.real_cmp = cmp,
		.real_priv = priv,
		.comparisons = 0,
	};

	if (list == head->prev)	/* Zero or one elements */
		return;

	/* Convert to a null-terminated singly-linked list. */
	head->prev->next = NULL;

	do {
		size_t bits;
		struct list_head **tail = &pending;
		struct list_head *run_tail;
		struct list_head *next_list;
		size_t run_len = 1;
		int descending = 0;

		/* Find the least-significant clear bit in count */
		for (bits = count; bits & 1; bits >>= 1)
			tail = &(*tail)->prev;
		/* Do the indicated merge */
		if (likely(bits)) {
			struct list_head *a = *tail, *b = a->prev;

			a = klp_merge(&wrapper, counting_cmp, b, a);
			/* Install the merged result in place of the inputs */
			a->prev = b->prev;
			*tail = a;
		}

		/*
		 * Natural run detection: scan for a maximal monotonic
		 * run from the input.  We detect both ascending (cmp <= 0)
		 * and strictly descending (cmp > 0) runs.
		 *
		 * Descending uses strict inequality (> 0, not >= 0) to
		 * preserve sort stability: equal elements stay in their
		 * original order even after the run is reversed.
		 */
		run_tail = list;
		if (run_tail->next &&
		    counting_cmp(&wrapper, run_tail, run_tail->next) > 0) {
			/* Strictly descending run */
			descending = 1;
			while (run_tail->next &&
			       counting_cmp(&wrapper, run_tail,
					    run_tail->next) > 0) {
				run_tail = run_tail->next;
				run_len++;
			}
		} else {
			/* Ascending run (includes single elements) */
			while (run_tail->next &&
			       counting_cmp(&wrapper, run_tail,
					    run_tail->next) <= 0) {
				run_tail = run_tail->next;
				run_len++;
			}
		}
		n_elements += run_len;

		/* Snip the run from the remaining input */
		next_list = run_tail->next;
		run_tail->next = NULL;

		if (descending) {
			/*
			 * Reverse the singly-linked run in-place so it
			 * becomes ascending.  After reversal, 'prev' is
			 * the new head and the original 'list' is the tail.
			 */
			struct list_head *prev = NULL, *curr = list, *tmp;

			while (curr) {
				tmp = curr->next;
				curr->next = prev;
				prev = curr;
				curr = tmp;
			}
			run_tail = list;	/* original head is now tail */
			list = prev;		/* reversed list head */
			n_desc_runs++;
		} else {
			n_asc_runs++;
		}

		/* Push this run onto the pending stack */
		list->prev = pending;
		pending = list;
		list = next_list;
		count++;
	} while (list);

	/* End of input; merge together all the pending lists. */
	list = pending;
	pending = pending->prev;
	if (!pending) {
		/*
		 * Single run — input was already sorted (or a single
		 * reversed run).  Just restore the doubly-linked list.
		 */
		struct list_head *tail = head;

		while (list) {
			tail->next = list;
			list->prev = tail;
			tail = list;
			list = list->next;
		}
		tail->next = head;
		head->prev = tail;
		goto done;
	}
	for (;;) {
		struct list_head *next = pending->prev;

		if (!next)
			break;
		list = klp_merge(&wrapper, counting_cmp, pending, list);
		pending = next;
	}
	/* The final merge, rebuilding prev links */
	klp_merge_final(&wrapper, counting_cmp, head, pending, list);
done:
	/* Record instrumentation data */
	kp_stats_record(n_elements, count, wrapper.comparisons,
			n_asc_runs, n_desc_runs);
}
