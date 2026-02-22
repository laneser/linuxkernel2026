/* SPDX-License-Identifier: GPL-2.0 */
#ifndef KP_TIMSORT_SORT_H
#define KP_TIMSORT_SORT_H

#include <linux/list.h>
#include <linux/list_sort.h>

void klp_list_sort(void *priv, struct list_head *head, list_cmp_func_t cmp);

#endif /* KP_TIMSORT_SORT_H */
