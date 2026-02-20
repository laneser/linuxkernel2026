# Linux 核心設計 (Spring 2026) — 課程表

> **原始出處：** <https://wiki.csie.ncku.edu.tw/linux/schedule>
> **擷取日期：** 2026-02-19
> **用途：** 課程完整路線圖與每週主題
> **涵蓋度：** 完整

---

## 課程資訊

**授課教師：** Jim Huang (黃敬群) `<jserv.tw@gmail.com>`

**時間：**
- 週二 15:20-18:10（實體）
- 週四 19:30-21:00（作業檢討/線上測驗/討論）

**評分：**
- 隨堂測驗 20%（取最佳 12 次）
- 個人作業 + 報告 + 期末專題 30%
- 自我評量 50%

---

## 每週大綱

### Week 1 (Feb 24, 26)：自我誠實 & 基礎
- 課程導覽與期望
- Linked list 實作（記憶體與演算法）
- Linux 作業系統概念
- GNU/Linux 開發工具介紹
- 作業一，截止 Mar 11
- [Quiz 1](https://hackmd.io/@sysprog/linux2025-quiz1)

### Week 2 (Mar 3, 5)：C 語言程式設計
- C 語言的數值系統
- 位元運算
- Linux kernel hash table 實作
- 記憶體管理與對齊
- Bit-field 結構
- 作業二，截止 Mar 17
- [Quiz 2](https://hackmd.io/@sysprog/linux2025-quiz2)

### Week 3 (Mar 10, 12)：數值系統 & C 程式設計
- 最大公因數實作
- 浮點數運算 (IEEE 754)
- 並行程式設計：排程原理
- 函式呼叫與遞迴
- 前置處理器與控制流程
- 作業三，截止 Apr 11
- [Quiz 3](https://hackmd.io/@sysprog/linux2025-quiz3)

### Week 4 (Mar 17, 19)：數值系統 & 編譯器
- 貢獻程式碼至 Linux kernel
- Linux kernel red-black trees
- C 編譯器建構與最佳化
- C 語言的 undefined behavior
- Error correction codes (ECC)
- 作業四，截止 Apr 15
- [Quiz 4](https://hackmd.io/@sysprog/linux2025-quiz4)

### Week 5 (Mar 24, 26)：Code Review
- 學生作業審查
- [Quiz 5](https://hackmd.io/@sysprog/linux2025-quiz5)

### Week 6 (Mar 31, Apr 2)：C Runtime/Linker & fork/exec
- 亂數分布
- 動態連結器與載入器
- C runtime (CRT)
- "Everything is a file" 哲學
- UNIX fork/exec 系統呼叫
- 作業五，截止 Apr 23
- [Quiz 6](https://hackmd.io/@sysprog/linux2025-quiz6)

### Week 7 (Apr 7, 9)：Process & CPU Scheduling
- Euler numbers 與連續變化
- Linux 排程機制
- Process state 與 task 結構
- System calls 與 vDSO
- 電子書發放：*Demystifying the Linux CPU Scheduler* (Ch. 1)
- User-Mode Linux 測試環境

### Week 8 (Apr 14, 16)：Concurrency & Linux 同步
- 並行概念與 atomics
- CS:APP Chapter 12 (Concurrency)
- Linux 同步原語
- *Demystifying the Linux CPU Scheduler* (Sections 2.1-2.2.2)
- [Quiz 8](https://hackmd.io/@sysprog/linux2025-quiz8)

### Week 9 (Apr 21, 23)：futex & Server 開發
- Thread Local Storage (TLS)
- POSIX Thread 實作
- I/O 模型演進
- RCU 同步機制
- eBPF 觀察 OS 行為
- 作業：ktcp，截止 May 16
- [Quiz 9](https://hackmd.io/@sysprog/linux2025-quiz9)

### Week 10 (Apr 28, 30)：現代微處理器
- C11/C++11 並行模型
- 產業動態 (Google Axion, ARM 處理器)
- 現代處理器設計原則
- 中斷處理
- 多核心 spinlocks
- [Quiz 10](https://hackmd.io/@sysprog/linux2025-quiz10)

### Week 11 (May 5, 7)：作業回顧 & 期末專題
- 作業審查
- 期末專題構想
- [2024 期末專題](https://hackmd.io/@sysprog/linux2024-projects)
- [Quiz 11](https://hackmd.io/@sysprog/linux2025-quiz11)

### Week 12 (May 12, 14)：微處理器 & 記憶體管理
- Lightweight Mutex Lock 實作
- Reference counting 模式
- CS:APP Chapter 6 (CPU caches)
- CPU cache 記憶體階層
- Skip lists 與 cache-oblivious 演算法
- [Quiz 12](https://hackmd.io/@sysprog/linux2025-quiz12)

### Week 13 (May 19, 21)：記憶體管理 & Device Drivers
- Linux 記憶體管理介紹
- POSIX shared memory
- Linux /dev/mem device
- 物件導向 C 程式設計
- CS:APP Chapter 10 (System-Level I/O)
- Device driver 介面與模型
- Device Tree, Timers, Scalability
- [Quiz 13](https://hackmd.io/@sysprog/linux2025-quiz13)

### Week 14 (May 26, 28)：Virtual Memory & 虛擬化
- 記憶體模型語意
- Copy-On-Write (COW)
- 嵌入式虛擬化
- KVM 基礎建設
- Linux Kernel Library (LKL)

### Week 15 (Jun 2, 4)：網路封包處理 & 多核心
- slab 記憶體配置器
- Linux kernel 網路
- RISC-V 系統模擬器 (semu)
- userfaultfd 記憶體外部化
- Linux 處理網路封包的方式
- Kernel 封包截取技術
- Linux 多核心
- Cache coherence 與 spinlock scalability
- [Quiz 15](https://hackmd.io/@sysprog/linux2025-quiz15)

### Week 16 (Jun 9, 11)：程式碼最佳化 & 多核心架構
- 現代硬體上的演算法設計
- Binary search 最佳化
- CS:APP Chapter 5
- Linux scalability 議題
- Memory barriers 與 ordering
- [Quiz 16](https://hackmd.io/@sysprog/linux2025-quiz16)

### Week 17 (Jun 16, 18)：Real-Time Linux 基礎
- Linux timers 與管理
- 2038 時間問題
- Real-time 排程
- PREEMPT_RT 機制
- Linux kernel preemption
- [Quiz 17](https://hackmd.io/@sysprog/linux2025-quiz17)

### Week 18 (Jun 23, 25)：多核心 & Rust 程式設計
- Linux preemption 機制
- RTMux real-time multiplexer
- ARM Linux 中的 memory barriers
- Rust 語言採用 (Android, Diem/Libra)
- 撰寫 Rust kernel modules
- [Quiz 18](https://hackmd.io/@sysprog/linux2025-quiz18)

### Week 19 (Jun 30)：Rust & Kernel Debugging
- Linux kernel panic 分析
- Rust for Linux 研究
- Rust 語言資源
- C vs. Rust 比較
- [Quiz 19](https://hackmd.io/@sysprog/linux2024-quiz19)

### Week 20 (Jul 7)：總回顧 & 評量
- 期末專題 peer review（至少 5 個專題）
- 自我評量完成
- 課程反思
- [期末成果展](https://hackmd.io/@sysprog/linux2025-showcase)

---

## 核心教材

- Computer Systems: A Programmer's Perspective (CS:APP)
- *Demystifying the Linux CPU Scheduler*
- *Concurrency Primer*
- *Linux Kernel Module Programming Guide*
- *每位程式開發者都該有的記憶體知識*

## 參考資源

- [GNU/Linux 開發工具](https://hackmd.io/@sysprog/gnu-linux-dev/)
- [資訊科技詞彙翻譯](https://hackmd.io/@sysprog/it-vocabulary)
- [線上講座系列](https://hackmd.io/@sysprog/linux-kernel-internal)

---

**授權：** [Creative Commons BY-SA 3.0 Taiwan](https://creativecommons.org/licenses/by-sa/3.0/tw/)
