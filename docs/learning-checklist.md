# Linux Kernel 學習 Checklist

> 本模板定義所有學習項目，供個人進度檔（`.learning-progress.md`）使用。
> 設計依據見 [`ARC42.md`](ARC42.md) §5。
>
> **使用方式：**
> 1. 首次使用時，Claude 從本模板產生 `.learning-progress.md`
> 2. 學習過程中打勾並加註筆記（`<!-- 日期 備註 -->`）
> 3. 模板更新時，Claude 協助將新項目 merge 進個人進度

---

## A. 開發工具基礎

> 參照：[`gnu-linux-dev.md`](references/gnu-linux-dev.md)、[`git-with-github.md`](references/git-with-github.md)

### Git

- [ ] Git 基本操作（clone, add, commit, push, pull）
- [ ] Git branching 與 merge
- [ ] Git rebase 與 interactive rebase
- [ ] Git fetch + rebase 工作流程（與上游同步）
- [ ] 解決 merge/rebase conflict
- [ ] Commit message 七條規則（cbea.ms/git-commit）
- [ ] `git push --force` 的正確使用時機
- [ ] `.gitignore` 設定

### 編輯器與終端機

- [ ] VS Code 基本操作與擴充套件
- [ ] VS Code 除錯功能（launch.json, breakpoints）
- [ ] Vim 基本操作與 `.vimrc` 設定
- [ ] 終端機管理工具（Byobu / tmux）

### 建構工具

- [ ] Makefile 語法（target, dependency, recipe）
- [ ] Makefile 變數（`=`, `:=`, `?=`, `+=`）
- [ ] 自動化變數（`$@`, `$<`, `$^`, `$*`）
- [ ] Pattern rules（`%.o: %.c`）
- [ ] `.PHONY` 與自動產生依賴（`gcc -MMD`）

### 程式碼品質工具

- [ ] Cppcheck 靜態分析
- [ ] clang-format 程式碼格式化（K&R style, 4-space indent）
- [ ] GNU Aspell 拼字檢查
- [ ] Git hook 自動檢查流程（pre-commit）

---

## B. C 語言基礎

> 參照：課程 Week 2-4 教材

### 數值系統與位元運算

- [ ] 二進位表示法與補數
- [ ] 位元運算子（&, |, ^, ~, <<, >>）
- [ ] 位元運算技巧（判斷二的冪次、計算 popcount 等）
- [ ] IEEE 754 浮點數運算
- [ ] Bit-field 結構

### 指標與記憶體

- [ ] 指標基礎（pointer arithmetic, pointer to pointer）
- [ ] 動態記憶體配置（malloc, calloc, realloc, free）
- [ ] 記憶體對齊（alignment）
- [ ] 常見記憶體錯誤（buffer overflow, use-after-free, double-free）
- [ ] "Pointer to pointer" 技巧操作 linked list

### C 語言進階

- [ ] 前置處理器（macros, conditional compilation）
- [ ] 函式指標與 callback
- [ ] Variable arguments (`va_list`, `va_start`, `va_arg`)
- [ ] `typeof`、`container_of` 巨集
- [ ] C 語言的 undefined behavior
- [ ] C11 標準相關特性

---

## C. Lab0 Queue 實作

> 參照：[`linux2025-lab0.md`](references/linux2025-lab0.md) Part A、[`linux2023-lab0-review.md`](references/linux2023-lab0-review.md)

### Linux Kernel Linked List API

- [ ] 理解 `list_head` 結構（circular doubly-linked list）
- [ ] `INIT_LIST_HEAD`, `list_add`, `list_add_tail`
- [ ] `list_del`, `list_del_init`
- [ ] `list_for_each`, `list_for_each_safe`
- [ ] `list_entry`, `container_of`
- [ ] `list_empty`, `list_is_singular`
- [ ] `list_move`, `list_move_tail`, `list_splice`

### Queue 函式實作

- [ ] `q_new` — 建立空 queue
- [ ] `q_free` — 釋放 queue 記憶體
- [ ] `q_insert_head` — head 插入（LIFO）
- [ ] `q_insert_tail` — tail 插入（FIFO）
- [ ] `q_remove_head` — 取出 head 元素
- [ ] `q_remove_tail` — 取出 tail 元素
- [ ] `q_size` — 計算元素數量
- [ ] `q_delete_mid` — 刪除中間節點
- [ ] `q_delete_dup` — 消除已排序 queue 中的重複
- [ ] `q_swap` — 交換相鄰配對
- [ ] `q_reverse` — 反轉 queue
- [ ] `q_reverseK` — 以 K 個為一組反轉
- [ ] `q_sort` — 升序排列
- [ ] `q_ascend` — 移除違反遞增單調性的節點
- [ ] `q_descend` — 移除違反遞減單調性的節點
- [ ] `q_merge` — 合併已排序的 queue

### 測試與通過

- [ ] `make check` 基本驗證通過
- [ ] `make test` 完整測試通過
- [ ] `make SANITIZER=1 test` Address Sanitizer 通過

---

## D. 測試與分析工具

> 參照：[`linux2025-lab0.md`](references/linux2025-lab0.md) Part B、[`gnu-linux-dev.md`](references/gnu-linux-dev.md) Perf 章節

### Valgrind

- [ ] Valgrind 基本用法（`valgrind --tool=memcheck`）
- [ ] 理解記憶體洩漏分類（definitely/indirectly/possibly lost, still reachable）
- [ ] 偵測無效記憶體存取（invalid read/write, use-after-free）
- [ ] `make valgrind` 通過零錯誤

### Massif

- [ ] Massif 記憶體使用分析（`valgrind --tool=massif`）
- [ ] `ms_print` 視覺化分析結果

### GDB

- [ ] GDB 基本操作（break, run, step, next, print, backtrace）
- [ ] 搭配 VS Code 除錯
- [ ] 編譯時加入 `-g -fno-omit-frame-pointer`

### Perf

- [ ] Perf 安裝與權限設定（`perf_event_paranoid`）
- [ ] `perf stat` 統計分析（cycles, instructions, cache misses）
- [ ] `perf record` + `perf report` 取樣分析
- [ ] Call graph 解讀（caller-based vs callee-based）
- [ ] 效能瓶頸定位與迭代改善

---

## E. 數學與統計

> 參照：[`linux2025-lab0.md`](references/linux2025-lab0.md) Part D

### 亂數與 Shuffle

- [ ] Fisher–Yates shuffle 演算法
- [ ] Pearson's chi-squared 檢定（驗證均勻性）
- [ ] PRNG 概念與測試（ent, dieharder）
- [ ] 機率觀點 vs 資訊理論觀點

### 常數時間分析

- [ ] Welch's t-test 原理
- [ ] fix-vs-random 測試策略
- [ ] 論文：[Dude, is my code constant time?](https://eprint.iacr.org/2016/1123.pdf)

### Shannon Entropy

- [ ] Shannon entropy 公式與意義
- [ ] `shannon_entropy.c` 定點數運算分析
- [ ] `log2_lshift16.h` 預計算 log2 實作
- [ ] Linux kernel `fs/btrfs/compression.c` 中的 entropy 計算參考
- [ ] 改進精確度的數學分析

---

## F. Linux Kernel 鏈結串列排序

> 參照：[`linux2025-lab0.md`](references/linux2025-lab0.md) Part E

### `lib/list_sort.c` 分析

- [ ] Bottom-up merge sort 原理與 cache 友善設計
- [ ] 2:1 合併策略與 `count` 二進位表示
- [ ] `merge()` 穩定性保證
- [ ] `list_sort()` 完整流程走讀

### Timsort

- [ ] Timsort 演算法原理
- [ ] 為 linked list 實作 kernel-style Timsort
- [ ] [CPython listsort 文件](https://github.com/python/cpython/blob/main/Objects/listsort.txt) 研讀
- [ ] 各種資料分布的效能測試

### 學術論文

- [ ] Panny & Prodinger (1995) — Bottom-up Mergesort 分析
- [ ] Chen, Hwang & Chen (1999) — Queue-mergesort 成本分布
- [ ] Golin & Sedgewick (1993) — Queue-Mergesort 基礎
- [ ] 比較論文描述與目前 kernel 程式碼的差異

---

## G. 系統程式設計

> 參照：[`linux2025-lab0.md`](references/linux2025-lab0.md) Part C

### I/O 多工

- [ ] `select(2)` 系統呼叫
- [ ] Non-blocking socket（`fcntl` + `O_NONBLOCK`）
- [ ] qtest 中 `cmd_select()` 的實作分析

### 信號處理

- [ ] `signal(7)` — SIGSEGV, SIGALRM 等
- [ ] `sigsetjmp()` / `siglongjmp()` 非區域跳躍
- [ ] qtest 中的 timeout 偵測機制

### Web Server 整合

- [ ] lab0-c web server 實作
- [ ] HTTP 請求處理（URL path → queue 命令）
- [ ] Web server 與 linenoise CLI 共存

---

## H. Code Review 與技術寫作

> 參照：[`linux2025-review.md`](references/linux2025-review.md)

### Code Review

- [ ] 觀看：[Amazing Code Reviews: Creating a Superhero Collective](https://youtu.be/ly86Wq_E18o)
- [ ] 理解 software peer review 流程
- [ ] 練習建設性批評與技術溝通

### 技術寫作

- [ ] [Google Technical Writing Courses](https://developers.google.com/tech-writing) 研讀
- [ ] 中文技術文件撰寫慣例（術語規範、格式）
- [ ] 使用精確術語（參照 [`it-vocabulary.md`](references/it-vocabulary.md)）

### 職涯思考

- [ ] 研讀：[Teach Yourself Programming in Ten Years](https://norvig.com/21-days.html)

---

## I. 課程週次教材

> 參照：[`linux-course-schedule.md`](references/linux-course-schedule.md)
> 每週教材細節請查閱課程表原始連結。

### 第一階段：基礎（Week 1-4）

- [ ] Week 1 — Linked list 實作、Linux 作業系統概念、GNU/Linux 開發工具
- [ ] Week 2 — C 語言數值系統、位元運算、kernel hash table、記憶體對齊
- [ ] Week 3 — GCD 實作、IEEE 754 浮點數、並行排程原理、遞迴與前置處理器
- [ ] Week 4 — 貢獻程式碼至 kernel、red-black trees、C 編譯器最佳化、undefined behavior、ECC

### 第二階段：系統程式設計（Week 5-9）

- [ ] Week 5 — Code review 實戰
- [ ] Week 6 — 亂數分布、動態連結器/載入器、CRT、fork/exec
- [ ] Week 7 — Linux 排程機制、process state、system calls、vDSO
- [ ] Week 8 — 並行概念與 atomics、CS:APP Ch.12、Linux 同步原語
- [ ] Week 9 — TLS、POSIX Thread、I/O 模型、RCU、eBPF

### 第三階段：硬體與核心（Week 10-14）

- [ ] Week 10 — C11 並行模型、現代處理器設計、中斷處理、多核心 spinlocks
- [ ] Week 11 — 作業回顧、期末專題構想
- [ ] Week 12 — Lightweight mutex、reference counting、CS:APP Ch.6（CPU caches）、skip lists
- [ ] Week 13 — Linux 記憶體管理、POSIX shared memory、OO in C、device drivers、device tree
- [ ] Week 14 — 記憶體模型、COW、嵌入式虛擬化、KVM、LKL

### 第四階段：進階主題（Week 15-20）

- [ ] Week 15 — slab allocator、kernel 網路、semu（RISC-V）、userfaultfd、cache coherence
- [ ] Week 16 — 演算法最佳化、binary search、CS:APP Ch.5、memory barriers
- [ ] Week 17 — Linux timers、2038 問題、real-time 排程、PREEMPT_RT
- [ ] Week 18 — RTMux、ARM memory barriers、Rust kernel modules
- [ ] Week 19 — Kernel panic 分析、Rust for Linux
- [ ] Week 20 — 期末專題 peer review、自我評量

---

## J. 核心教材書籍

> 參照：[`linux-course-schedule.md`](references/linux-course-schedule.md) 核心教材

- [ ] CS:APP Chapter 5 — Optimizing Program Performance
- [ ] CS:APP Chapter 6 — The Memory Hierarchy (CPU caches)
- [ ] CS:APP Chapter 10 — System-Level I/O
- [ ] CS:APP Chapter 12 — Concurrent Programming
- [ ] *Demystifying the Linux CPU Scheduler* — Ch.1, §2.1-2.2.2
- [ ] *Concurrency Primer*
- [ ] *每位程式開發者都該有的記憶體知識*

---

## K. Linux Kernel Module Programming Guide (LKMPG)

> 參照：[`lkmpg.md`](references/lkmpg.md)（Week 13 起使用）
> 線上版：<https://sysprog21.github.io/lkmpg/>

- [ ] Ch.4 — Hello World（第一個 kernel module）
- [ ] Ch.5 — Preliminaries（編譯、載入、卸載）
- [ ] Ch.6 — Character Device Drivers
- [ ] Ch.7 — The /proc Filesystem
- [ ] Ch.8 — sysfs: Interacting with your module
- [ ] Ch.9 — Talking To Device Files
- [ ] Ch.10 — System Calls
- [ ] Ch.11 — Blocking Processes and Threads
- [ ] Ch.12 — Synchronization
- [ ] Ch.15 — Scheduling Tasks
- [ ] Ch.16 — Interrupt Handlers

---

## L. Linux 核心模組運作原理

> 參照：[`linux-kernel-module.md`](references/linux-kernel-module.md)
> 原始出處：<https://hackmd.io/@sysprog/linux-kernel-module>
> 與 LKMPG 互補——LKMPG 側重入門教學，本文側重底層機制。

### 基礎與環境

- [ ] Kernel headers 安裝與 Secure Boot 設定
- [ ] Hello World module 編譯、載入（insmod）、卸載（rmmod）

### 內部機制

- [ ] MODULE_* 巨集展開流程（MODULE_INFO → __MODULE_INFO → `.modinfo` ELF section）
- [ ] Module 載入 syscall 流程（`finit_module` → `load_module` → `do_init_module`）
- [ ] `module_init()` 函式別名機制（alias → `init_module`）
- [ ] `.ko` 檔案的 ELF 結構分析（readelf, objdump）

### 實作範例

- [ ] fibdrv — Fibonacci 數列 character device module
- [ ] Sysfs 整合（`/sys/module/` 目錄結構）

### 進階主題

- [ ] 可自我隱藏的 kernel module（lkm-hidden）
- [ ] `kallsyms_lookup_name`、`list_del`、`rb_erase`、`kobject_del` 的運用
