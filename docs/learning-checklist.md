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

## B. 第一週作業：Warm-up

> 參照：[`warmup.md`](references/warmup.md)
> 繳交期限：3 月 11 日

### 筆記書寫規範

- [ ] 熟悉 HackMD 共筆格式要求（無 `[TOC]`、無自訂 CSS、程式碼不加行號）
- [ ] 掌握中文技術文件撰寫慣例（全形標點、書名號、術語規範）
- [ ] 理解 AI 工具使用規範（標示來源、指出謬誤、漸進更新）

### 探討〈資訊科技詞彙翻譯〉

> 參照：[`it-vocabulary.md`](references/it-vocabulary.md)

- [ ] "render" 在電腦圖學語境中為何應強調「如實呈現」？「渲染」喪失什麼意涵？Linux 核心中 "render" 出現在哪些場景？
- [ ] 說明 constant 與 immutable 的差異，並探討程式設計中的關鍵考量
- [ ] 比較 concurrent 與 parallel 的語意差異，說明為何「並行」較貼近 concurrent 的本意
- [ ] 撰寫 Linux 核心文件時，如何區分 process, thread, task, job 等術語？

### 細讀〈GNU/Linux 開發工具〉

> 參照：[`gnu-linux-dev.md`](references/gnu-linux-dev.md)

- [ ] 確保 Linux 系統已正確安裝，且每天使用
- [ ] 學習 HackMD 操作，能正確使用 LaTeX（波函數、密度矩陣）
- [ ] 學習 git 操作，依據教學錄影實際練習，知曉 `git rebase` 操作

### 探討〈解讀計算機編碼〉

> 參照：[`binary-representation.md`](references/binary-representation.md)、[`n1256-c99.md`](references/n1256-c99.md)

- [ ] 為何計算機加法在固定 $k$ 位元下，本質等價於 $\mathbb{Z}/2^k\mathbb{Z}$ 上的加法？
- [ ] 為何「允許溢位」反而保證封閉性？不允許溢位會破壞哪些群的性質？
- [ ] 為何 $2^k$ 不為質數時，乘法不形成群？找出 Linux 核心相關程式碼
- [ ] 為何 $x \% 2^n \equiv x \& (2^n - 1)$ 僅對 unsigned 或非負整數安全？從 CVE/CWE 找相關資安議題
- [ ] 為何 sign extension 僅在「跨圓環」搬移時才有意義？從數學觀點一般化證明
- [ ] 為何 Linux 核心中 unsigned overflow 是 defined behavior，但 signed overflow 是 UB？
- [ ] 為何 Linux 核心大量使用 unsigned long 作為時間計數器？
- [ ] 若模數改為質數 $p$，是否可構成有限域？和 AES 中 $GF(2^8)$ 有何關聯？
- [ ] 二補數構成環但非域，對除法有何限制？找出 Linux 核心對應案例
- [ ] 二補數的設計是否本質上是種 algebraic encoding？
- [ ] 若將系統時間設計於 $\mathbb{Z}/2^{64}$ 上，其安全極限為何？
- [ ] 證明 $(\mathbb{Z}/2^k\mathbb{Z}, +)$ 為阿貝爾群，但 $(\mathbb{Z}/2^k\mathbb{Z}, \times)$ 非群

### 探討〈你所不知道的 C 語言：指標篇〉

> 參照：[`c-pointer.md`](references/c-pointer.md)、[`n1256-c99.md`](references/n1256-c99.md)

- [ ] 根據 C99 對 object 的定義，分析 `int *foo(void) { int x = 10; return &x; }` 是否為 UB
  - `static int x = 10;` 的差異、storage duration 與 lifetime 的區別
- [ ] 分析 `sizeof(a)` vs `sizeof(p)`：array decay、`&a` 與 `a` 型態差異、Graphviz 記憶體示意圖
- [ ] 分析 `(int *)&x[0]` 的 pointer arithmetic 與 strict aliasing 問題
- [ ] 解釋 call-by-value 下指標修改行為，繪製 stack frame 示意圖
- [ ] 依據 C99 6.3.2.1 解釋 `(********puts)("Hello")` 的 function designator 轉換規則
- [ ] 從「儲存-執行模型」解釋 `char *p = (char *)&a`，為何 C 語言可視為 assembly 的語法抽象
- [ ] 分析 opaque pointer 與 incomplete type 如何達成 binary compatibility
- [ ] 構造 object lifetime 結束但 dereference 為 UB 的案例，用 C99 lifetime 定義解釋
- [ ] 分析 strict aliasing violation（`int *p = (int *)&f`）、`memcpy` 替代方案、`unsigned char *` 例外
- [ ] 比較 `void f(int a[10])` vs `void f(int *a)` vs `void g(int (*a)[10])` 的 ABI 差異

### 探討〈linked list 和非連續記憶體〉

> 參照：[`c-linked-list.md`](references/c-linked-list.md)

- [ ] 從詞彙翻譯角度探討 "linked list" 為何翻譯為「鏈結串列」，「串列」詞源在哪？
- [ ] 分析 `struct ListNode **indir = &head;` 的型別語意，說明為何是「指標的指標」而非「雙指標」
- [ ] 分析 `free(*indir)` 的 lifetime 問題、AddressSanitizer 偵測、`-O3` 下的指令 reorder
- [ ] 為何 linked list traversal 難以被 hardware prefetcher 預測？`__builtin_prefetch` 是否一定改善效能？從 git log 探討 Linux 核心 List API 棄置 prefetcher 的考量
- [ ] 分析 Linux `list_sort`：為何是 stable？為何不用 quicksort？為何 merge sort 適合 linked list？
- [ ] `list_sort` 延遲合併策略：推導 worst-case comparison 次數，建立數學上界
- [ ] 鏈結串列新增 O(1) vs 陣列 O(n)，但實際硬體上陣列可能更快——解釋並量化分析

### 細讀〈Linux: 作業系統術語及概念〉

> 參照：[`linux-concepts.md`](references/linux-concepts.md)

- [ ] 頻繁觸發系統呼叫是否等同繞過 user/kernel 隔離？分析 CPU privilege level、page table、syscall 機制
- [ ] fork-join 模型：推導 $n$ 個 fork 點與 $m$ 個 join 點下的最大並行行程數上界
- [ ] fork-join 抽象為 DAG：critical path 與 Amdahl's law 的關係
- [ ] 比較 Mach microkernel 與 Linux（NPTL 前後）在 scheduling abstraction 上的差異
- [ ] 若將 VFS/network stack 遷移至 userspace：分析 context switch、cache locality、fault isolation、worst-case latency
- [ ] page fault 延遲期望值模型：$T_{pf}$、機率 $p$
- [ ] $N$ 核系統全域計數器 spinlock：估算 coherence traffic 與 lock contention 成長趨勢
- [ ] CPU 排程器多對多映射 $f : (P, t) \rightarrow C$ 是否為時間函式？翻閱經典論文探討
- [ ] 「卡比吸入能力」比喻：分析 abstraction preservation、backward compatibility、scalability、real-time

### 探討〈從熱力學第二定律到系統軟體〉

> 參照：[`from-entropy-to-os.md`](references/from-entropy-to-os.md)

- [ ] 將三項宏觀穩定條件改寫為可被拒絕的統計假說（$H_0, H_1$、ADF/KPSS/KS 檢定）
- [ ] 指出 i.i.d. 假設在 CPU 排程追蹤何時不成立（CI、顯著水準、Type I/II error）
- [ ] M/G/1 P-K 公式：推導 $E[W_q]$ 對 $E[S^2]$ 的敏感度，證明 $\rho \to 1$ 時的發散階數
  - 構造 lognormal 與 Pareto 分佈比較 tail latency
- [ ] EEVDF lag 有界性：流體模型下 $\sum_i Lag_i(t) = 0$，離散 slice 誤差界限，request length 縮放
- [ ] 熵率分析：對 `sched_wakeup`/`sched_switch` 事件建立 n-gram 模型，比較負載 regime change 前後
- [ ] 改進數學嚴格性：區分「方法論類比」與「數學等價」，明確適用範圍與失效條件

### 誠實面對期初考題

> 參照：[`quiz1.md`](references/quiz1.md)、[`floating-point-intro.md`](references/floating-point-intro.md)、[`floating-point.md`](references/floating-point.md)

- [ ] 測驗 1：右移取代除法的誤差補償（`remainder` 扮演 Kahan 補償變數）
  - 在 `kernel/sched/pelt.c` 找對應手法，分析 `period_contrib`
  - 移植 PELT 碎片補償為 standalone userspace 程式並模擬
- [ ] 測驗 2：Kahan summation 依賴浮點數不滿足結合律的特性
  - IEEE 754 結合律不成立的構造與證明
  - 不同 rounding mode 下 Kahan 是否仍正確
- [ ] 測驗 3：`abs()` 對 INT_MIN 的未定義行為
- [ ] 測驗 4-5：定點數運算與時間子系統精度
- [ ] 測驗 6：PELT `period_contrib` 的誤差界分析
- [ ] 測驗 7-9：EWMA 理論與 Linux 核心實作（WiFi RSSI 追蹤）

---

## C. C 語言基礎

> 參照：課程教材、[`n1256-c99.md`](references/n1256-c99.md)

### 數值系統與位元運算

- [ ] 二進位表示法與二補數
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

## D. Linux Kernel 鏈結串列排序

> 參照：[`c-linked-list.md`](references/c-linked-list.md)

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

## E. 測試與分析工具

> 參照：[`gnu-linux-dev.md`](references/gnu-linux-dev.md)

### Valgrind

- [ ] Valgrind 基本用法（`valgrind --tool=memcheck`）
- [ ] 理解記憶體洩漏分類（definitely/indirectly/possibly lost, still reachable）
- [ ] 偵測無效記憶體存取（invalid read/write, use-after-free）

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

## F. Code Review 與技術寫作

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

## G. 課程週次教材

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

## H. 核心教材書籍

> 參照：[`linux-course-schedule.md`](references/linux-course-schedule.md) 核心教材

- [ ] CS:APP Chapter 5 — Optimizing Program Performance
- [ ] CS:APP Chapter 6 — The Memory Hierarchy (CPU caches)
- [ ] CS:APP Chapter 10 — System-Level I/O
- [ ] CS:APP Chapter 12 — Concurrent Programming
- [ ] *Demystifying the Linux CPU Scheduler* — Ch.1, §2.1-2.2.2
- [ ] *Concurrency Primer*
- [ ] *每位程式開發者都該有的記憶體知識*

---

## I. Linux Kernel Module Programming Guide (LKMPG)

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

## J. Linux 核心模組運作原理

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

---

## K. Introduction to Linux Kernel Driver Programming

> 參照：[`intro-kernel-driver-programming.md`](references/intro-kernel-driver-programming.md)
> 原始 PDF：[Bootlin / Michael Opdenacker (Linux Foundation)](https://events19.linuxfoundation.org/wp-content/uploads/2017/12/Introduction-to-Linux-Kernel-Driver-Programming-Michael-Opdenacker-Bootlin-.pdf)

### Device Model 架構

- [ ] 理解 device model 三大結構（`bus_type`, `device_driver`, `device`）
- [ ] Bus driver 的角色（以 USB 為例：adapter driver + device driver 配對）
- [ ] Driver 開發三步驟：宣告裝置 → 註冊 hook → 向 bus core 註冊
- [ ] `probe()` 與 `remove()` 函式的工作流程

### Platform Devices 與 Device Tree

- [ ] Platform bus 概念（非自動偵測裝置的處理方式）
- [ ] Device Tree 結構（`.dts` vs `.dtsi`、`compatible` 屬性）
- [ ] Pin multiplexing 概念
- [ ] Device Tree bindings 查找方式

### I2C Driver 範例

- [ ] I2C driver 的 `probe()` / `remove()` 實作分析
- [ ] 三種裝置配對方式（I2C name、DT compatible、ACPI ID）
- [ ] Framework 結構與 bus 結構的互相引用模式

---

## L. Linux 中斷處理與現代架構考量

> 參照：[`linux-interrupt.md`](references/linux-interrupt.md)
> 原始出處：<https://hackmd.io/@sysprog/linux-interrupt>

### 硬體中斷基礎

- [ ] PIC 機制（IRQ → vector 轉譯、優先級、masking）
- [ ] Edge-triggered vs Level-triggered 差異

### 上半部與下半部

- [ ] Top half 設計原則（快速、不可阻塞、hardware-critical）
- [ ] Bottom half 三種機制選擇（softirq / tasklet / workqueue）

### Softirq

- [ ] `softirq_action` 結構與 `__do_softirq()` 流程
- [ ] `ksoftirqd` 每 CPU 一個執行緒的設計
- [ ] `local_irq_disable()` / `local_irq_enable()` 的使用時機

### Tasklet

- [ ] Tasklet 與 softirq 的關係（建構於 softirq 之上）
- [ ] `tasklet_schedule()` / `tasklet_hi_schedule()` 使用方式
- [ ] 同一 tasklet 不會在不同 CPU 並行的保證

### Workqueue

- [ ] `create_workqueue()` / `schedule_work()` API
- [ ] Workqueue vs Tasklet 差異（process context vs atomic context）
- [ ] 可休眠（sleep）的延遲處理應用場景

### Threaded Interrupts 與 PREEMPT_RT

- [ ] Threaded interrupt 概念（sleeping spinlock 支援）
- [ ] PREEMPT_RT patch 的中斷處理策略
- [ ] Linux 2.6.30 合併的 threaded interrupt API

### 虛擬化與中斷（GIC-400）

- [ ] ARM GIC-400 四大組件（Distributor, CPU interface, GICH, GICV）
- [ ] TrustZone 整合與安全中斷
- [ ] Hypervisor 虛擬中斷控制機制
