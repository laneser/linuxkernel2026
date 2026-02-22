/* SPDX-License-Identifier: GPL-2.0 */
#ifndef KP_TIMSORT_STATS_H
#define KP_TIMSORT_STATS_H

#include <linux/atomic.h>

struct kp_sort_stats {
	atomic64_t call_count;
	atomic64_t total_elements;
	atomic64_t total_runs;
	atomic64_t total_comparisons;
	atomic64_t already_sorted;	/* cases where runs == 1 */
	atomic64_t asc_runs;		/* ascending runs detected */
	atomic64_t desc_runs;		/* descending runs (reversed) */
};

extern struct kp_sort_stats kp_stats;

int kp_timsort_stats_init(void);
void kp_timsort_stats_exit(void);

static inline void kp_stats_record(unsigned long elements, unsigned long runs,
				    unsigned long comparisons,
				    unsigned long asc_runs,
				    unsigned long desc_runs)
{
	atomic64_inc(&kp_stats.call_count);
	atomic64_add(elements, &kp_stats.total_elements);
	atomic64_add(runs, &kp_stats.total_runs);
	atomic64_add(comparisons, &kp_stats.total_comparisons);
	if (runs == 1)
		atomic64_inc(&kp_stats.already_sorted);
	atomic64_add(asc_runs, &kp_stats.asc_runs);
	atomic64_add(desc_runs, &kp_stats.desc_runs);
}

#endif /* KP_TIMSORT_STATS_H */
