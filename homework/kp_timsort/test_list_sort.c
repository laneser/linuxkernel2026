// SPDX-License-Identifier: GPL-2.0
/*
 * test_list_sort.c - Test module to exercise list_sort and verify stats
 *
 * Creates lists with known patterns (sorted, reverse, random) and calls
 * list_sort() to verify the instrumentation works and measure run detection.
 * Results are printed to dmesg.
 *
 * Usage: sudo insmod test_list_sort.ko && sudo rmmod test_list_sort
 *        dmesg | grep test_list_sort
 */

#define pr_fmt(fmt) "test_list_sort: " fmt

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/list.h>
#include <linux/list_sort.h>
#include <linux/slab.h>
#include <linux/random.h>

struct test_entry {
	struct list_head list;
	int value;
};

static int test_cmp(void *priv, const struct list_head *a,
		    const struct list_head *b)
{
	struct test_entry *ea = container_of(a, struct test_entry, list);
	struct test_entry *eb = container_of(b, struct test_entry, list);

	return ea->value > eb->value;
}

static void fill_sorted(struct list_head *head, struct test_entry *entries,
			 int n)
{
	int i;

	INIT_LIST_HEAD(head);
	for (i = 0; i < n; i++) {
		entries[i].value = i;
		list_add_tail(&entries[i].list, head);
	}
}

static void fill_reverse(struct list_head *head, struct test_entry *entries,
			  int n)
{
	int i;

	INIT_LIST_HEAD(head);
	for (i = 0; i < n; i++) {
		entries[i].value = n - 1 - i;
		list_add_tail(&entries[i].list, head);
	}
}

static void fill_random(struct list_head *head, struct test_entry *entries,
			 int n)
{
	int i;

	INIT_LIST_HEAD(head);
	for (i = 0; i < n; i++) {
		entries[i].value = get_random_u32() % (n * 10);
		list_add_tail(&entries[i].list, head);
	}
}

/* Partially sorted: k sorted runs concatenated */
static void fill_partial(struct list_head *head, struct test_entry *entries,
			  int n, int runs)
{
	int i, run_size = n / runs;

	INIT_LIST_HEAD(head);
	for (i = 0; i < n; i++) {
		int run_idx = i / run_size;
		int pos_in_run = i % run_size;

		entries[i].value = run_idx * 1000 + pos_in_run;
		list_add_tail(&entries[i].list, head);
	}
}

static int verify_sorted(struct list_head *head)
{
	struct test_entry *prev = NULL;
	struct test_entry *entry;

	list_for_each_entry(entry, head, list) {
		if (prev && prev->value > entry->value)
			return 0;
		prev = entry;
	}
	return 1;
}

static void run_test(const char *name, struct list_head *head,
		     struct test_entry *entries, int n,
		     void (*fill)(struct list_head *, struct test_entry *, int))
{
	fill(head, entries, n);
	list_sort(NULL, head, test_cmp);
	pr_info("%-20s n=%-5d sorted=%s\n", name, n,
		verify_sorted(head) ? "OK" : "FAIL");
}

#define TEST_N 1000

static int __init test_init(void)
{
	struct test_entry *entries;
	LIST_HEAD(head);

	entries = kmalloc_array(TEST_N, sizeof(*entries), GFP_KERNEL);
	if (!entries)
		return -ENOMEM;

	pr_info("=== Starting list_sort tests (n=%d) ===\n", TEST_N);
	pr_info("Check /sys/kernel/debug/list_sort/stats for run data\n");

	run_test("already_sorted", &head, entries, TEST_N,
		 fill_sorted);
	run_test("reverse_sorted", &head, entries, TEST_N,
		 fill_reverse);
	run_test("random", &head, entries, TEST_N,
		 fill_random);
	run_test("random_2", &head, entries, TEST_N,
		 fill_random);

	/* Partially sorted tests */
	fill_partial(&head, entries, TEST_N, 10);
	list_sort(NULL, &head, test_cmp);
	pr_info("%-20s n=%-5d runs=10 sorted=%s\n",
		"partial_10_runs", TEST_N,
		verify_sorted(&head) ? "OK" : "FAIL");

	fill_partial(&head, entries, TEST_N, 100);
	list_sort(NULL, &head, test_cmp);
	pr_info("%-20s n=%-5d runs=100 sorted=%s\n",
		"partial_100_runs", TEST_N,
		verify_sorted(&head) ? "OK" : "FAIL");

	pr_info("=== Tests complete ===\n");

	kfree(entries);
	return -EAGAIN;	/* fail load so module auto-unloads */
}

static void __exit test_exit(void)
{
}

module_init(test_init);
module_exit(test_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Test module for list_sort instrumentation");
