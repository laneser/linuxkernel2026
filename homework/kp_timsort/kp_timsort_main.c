// SPDX-License-Identifier: GPL-2.0
/*
 * kp_timsort_main.c - Livepatch module for list_sort natural run detection
 *
 * This module uses kernel livepatch to replace list_sort() with
 * klp_list_sort(), which adds natural run detection to exploit
 * pre-existing order in the input.  When loaded, all kernel callers
 * of list_sort() transparently use the improved version.
 *
 * debugfs interface at /sys/kernel/debug/kp_timsort/ provides
 * instrumentation data (comparison counts, run distributions) for
 * empirical analysis of sorting behavior under real workloads.
 */

#define pr_fmt(fmt) KBUILD_MODNAME ": " fmt

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/livepatch.h>
#include "kp_timsort_sort.h"
#include "kp_timsort_stats.h"

static struct klp_func funcs[] = {
	{
		.old_name = "list_sort",
		.new_func = klp_list_sort,
	}, { }
};

static struct klp_object objs[] = {
	{
		/* name being NULL means vmlinux */
		.funcs = funcs,
	}, { }
};

static struct klp_patch patch = {
	.mod = THIS_MODULE,
	.objs = objs,
};

static int __init kp_timsort_init(void)
{
	int ret;

	ret = kp_timsort_stats_init();
	if (ret) {
		pr_err("failed to initialize debugfs: %d\n", ret);
		return ret;
	}

	ret = klp_enable_patch(&patch);
	if (ret) {
		pr_err("failed to enable livepatch: %d\n", ret);
		kp_timsort_stats_exit();
		return ret;
	}

	pr_info("loaded — list_sort() patched with natural run detection\n");
	return 0;
}

static void __exit kp_timsort_exit(void)
{
	kp_timsort_stats_exit();
	pr_info("unloaded\n");
}

module_init(kp_timsort_init);
module_exit(kp_timsort_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Livepatch: list_sort with natural run detection");
MODULE_INFO(livepatch, "Y");
