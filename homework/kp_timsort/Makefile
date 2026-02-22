# SPDX-License-Identifier: GPL-2.0
#
# kp_timsort - Livepatch module replacing list_sort with natural run detection
#
# Requires: CONFIG_LIVEPATCH=y CONFIG_DYNAMIC_FTRACE=y
#

obj-m := kp_timsort.o
kp_timsort-y := kp_timsort_main.o kp_timsort_sort.o kp_timsort_stats.o

KDIR ?= /lib/modules/$(shell uname -r)/build

all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean
