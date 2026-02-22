// SPDX-License-Identifier: GPL-2.0
/*
 * kp_timsort_stats.c - debugfs instrumentation for kp_timsort
 *
 * Exposes sorting statistics under /sys/kernel/debug/kp_timsort/:
 *   stats  - read sorting statistics summary
 *   reset  - write to clear all counters
 */

#include <linux/debugfs.h>
#include <linux/seq_file.h>
#include "kp_timsort_stats.h"

struct kp_sort_stats kp_stats;

static struct dentry *stats_dir;

static int stats_show(struct seq_file *m, void *v)
{
	s64 calls = atomic64_read(&kp_stats.call_count);

	seq_printf(m, "call_count:       %lld\n", calls);
	seq_printf(m, "total_elements:   %lld\n",
		   atomic64_read(&kp_stats.total_elements));
	seq_printf(m, "total_runs:       %lld\n",
		   atomic64_read(&kp_stats.total_runs));
	seq_printf(m, "total_comparisons:%lld\n",
		   atomic64_read(&kp_stats.total_comparisons));
	seq_printf(m, "already_sorted:   %lld\n",
		   atomic64_read(&kp_stats.already_sorted));
	seq_printf(m, "asc_runs:         %lld\n",
		   atomic64_read(&kp_stats.asc_runs));
	seq_printf(m, "desc_runs:        %lld\n",
		   atomic64_read(&kp_stats.desc_runs));

	if (calls > 0) {
		seq_printf(m, "avg_elements:     %lld\n",
			   atomic64_read(&kp_stats.total_elements) / calls);
		seq_printf(m, "avg_runs:         %lld\n",
			   atomic64_read(&kp_stats.total_runs) / calls);
		seq_printf(m, "avg_comparisons:  %lld\n",
			   atomic64_read(&kp_stats.total_comparisons) / calls);
	}

	return 0;
}
DEFINE_SHOW_ATTRIBUTE(stats);

static ssize_t reset_write(struct file *file, const char __user *buf,
			    size_t count, loff_t *ppos)
{
	atomic64_set(&kp_stats.call_count, 0);
	atomic64_set(&kp_stats.total_elements, 0);
	atomic64_set(&kp_stats.total_runs, 0);
	atomic64_set(&kp_stats.total_comparisons, 0);
	atomic64_set(&kp_stats.already_sorted, 0);
	atomic64_set(&kp_stats.asc_runs, 0);
	atomic64_set(&kp_stats.desc_runs, 0);
	return count;
}

static const struct file_operations reset_fops = {
	.write = reset_write,
	.llseek = noop_llseek,
};

int kp_timsort_stats_init(void)
{
	stats_dir = debugfs_create_dir("kp_timsort", NULL);
	if (IS_ERR(stats_dir))
		return PTR_ERR(stats_dir);

	debugfs_create_file("stats", 0444, stats_dir, NULL, &stats_fops);
	debugfs_create_file("reset", 0200, stats_dir, NULL, &reset_fops);

	return 0;
}

void kp_timsort_stats_exit(void)
{
	debugfs_remove_recursive(stats_dir);
}
