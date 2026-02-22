// SPDX-License-Identifier: GPL-2.0
/*
 * bench_list_sort.c - benchmark kernel module for list_sort()
 *
 * Measures comparison count and wall-clock time for list_sort() across
 * multiple input patterns and sizes.  Results are printed to dmesg in
 * CSV format for post-processing.
 *
 * Usage: sudo insmod bench_list_sort.ko
 *   (module returns -EAGAIN so it auto-unloads after running)
 *
 * Output format (in dmesg):
 *   bench_list_sort: pattern,n,iter,comparisons,time_ns
 */

#define pr_fmt(fmt) "bench_list_sort: " fmt

#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/ktime.h>
#include <linux/list.h>
#include <linux/list_sort.h>
#include <linux/module.h>
#include <linux/random.h>
#include <linux/slab.h>

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Benchmark for list_sort() comparison count and timing");

#define BENCH_ITERATIONS	20

struct bench_element {
	struct list_head list;
	int value;
};

struct bench_ctx {
	unsigned long comparisons;
};

static int counting_cmp(void *priv, const struct list_head *a,
			const struct list_head *b)
{
	struct bench_ctx *ctx = priv;
	struct bench_element *ea = container_of(a, struct bench_element, list);
	struct bench_element *eb = container_of(b, struct bench_element, list);

	ctx->comparisons++;
	if (ea->value < eb->value)
		return -1;
	if (ea->value > eb->value)
		return 1;
	return 0;
}

/* Allocate n elements and add to head */
static struct bench_element *alloc_elements(int n)
{
	struct bench_element *elems;

	elems = kmalloc_array(n, sizeof(*elems), GFP_KERNEL);
	return elems;
}

static void build_list(struct list_head *head, struct bench_element *elems,
		       int n)
{
	int i;

	INIT_LIST_HEAD(head);
	for (i = 0; i < n; i++)
		list_add_tail(&elems[i].list, head);
}

/* Input pattern generators — set elems[i].value */
static void gen_sorted(struct bench_element *elems, int n)
{
	int i;

	for (i = 0; i < n; i++)
		elems[i].value = i;
}

static void gen_reverse(struct bench_element *elems, int n)
{
	int i;

	for (i = 0; i < n; i++)
		elems[i].value = n - 1 - i;
}

static void gen_random(struct bench_element *elems, int n)
{
	int i;

	for (i = 0; i < n; i++)
		elems[i].value = get_random_u32();
}

static void gen_partial_k(struct bench_element *elems, int n)
{
	/* 8 sorted segments spliced together */
	int i, k = 8;
	int seg_len = n / k;

	for (i = 0; i < n; i++) {
		int seg = i / seg_len;
		int pos = i % seg_len;
		/*
		 * Each segment is sorted within itself, but segments
		 * overlap in value ranges to force merges.
		 */
		elems[i].value = seg * 1000000 + pos;
	}
}

static void gen_pipe_organ(struct bench_element *elems, int n)
{
	int i, mid = n / 2;

	for (i = 0; i < mid; i++)
		elems[i].value = i;
	for (i = mid; i < n; i++)
		elems[i].value = n - 1 - i;
}

static void gen_push_front(struct bench_element *elems, int n)
{
	int i;

	/* Sorted, but move the last element to front */
	for (i = 0; i < n - 1; i++)
		elems[i + 1].value = i;
	elems[0].value = n - 1;
}

struct pattern_desc {
	const char *name;
	void (*generate)(struct bench_element *elems, int n);
};

static const struct pattern_desc patterns[] = {
	{ "sorted",     gen_sorted },
	{ "reverse",    gen_reverse },
	{ "random",     gen_random },
	{ "partial_8",  gen_partial_k },
	{ "pipe_organ", gen_pipe_organ },
	{ "push_front", gen_push_front },
};

static const int sizes[] = { 100, 500, 1000, 5000, 10000, 50000 };

static void run_bench(const struct pattern_desc *pat, int n)
{
	struct bench_element *elems;
	struct list_head head;
	struct bench_ctx ctx;
	int iter;
	ktime_t t_start, t_end;
	s64 elapsed_ns;

	elems = alloc_elements(n);
	if (!elems) {
		pr_err("Failed to allocate %d elements\n", n);
		return;
	}

	for (iter = 0; iter < BENCH_ITERATIONS; iter++) {
		/* Re-generate the pattern each iteration */
		pat->generate(elems, n);
		build_list(&head, elems, n);

		ctx.comparisons = 0;

		t_start = ktime_get();
		list_sort(&ctx, &head, counting_cmp);
		t_end = ktime_get();

		elapsed_ns = ktime_to_ns(ktime_sub(t_end, t_start));

		pr_info("%s,%d,%d,%lu,%lld\n",
			pat->name, n, iter,
			ctx.comparisons, elapsed_ns);
	}

	kfree(elems);
}

static int __init bench_list_sort_init(void)
{
	int i, j;

	pr_info("pattern,n,iter,comparisons,time_ns\n");

	for (i = 0; i < ARRAY_SIZE(patterns); i++) {
		for (j = 0; j < ARRAY_SIZE(sizes); j++) {
			run_bench(&patterns[i], sizes[j]);
			/* Let the system breathe between runs */
			cond_resched();
		}
	}

	pr_info("benchmark complete\n");

	/* Return -EAGAIN so the module auto-unloads */
	return -EAGAIN;
}

static void __exit bench_list_sort_exit(void)
{
}

module_init(bench_list_sort_init);
module_exit(bench_list_sort_exit);
