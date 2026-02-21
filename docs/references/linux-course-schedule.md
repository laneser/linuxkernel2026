# Linux 核心設計 (Spring 2026) — 課程表

> **原始出處：** <https://wiki.csie.ncku.edu.tw/linux/schedule>
> **擷取日期：** 2026-02-21
> **用途：** 課程完整路線圖與每週主題
> **涵蓋度：** 完整

---

## 課程資訊

**授課教師：** Jim Huang (黃敬群) `<jserv.tw@gmail.com>`

**聯絡：**
- Facebook 粉絲頁：<https://www.facebook.com/JservFans>
- 討論區：<https://www.facebook.com/groups/system.software2025/>
- 課程信箱：`<embedded.master2015@gmail.com>`
- [線上講座系列](https://hackmd.io/@sysprog/linux-kernel-internal)

**時間：**
- 週二 15:20-18:10（實體）
- 週四 19:30-21:00（作業檢討/線上測驗/討論）

**期末成果展：** 2026 年 6 月 27 日

**評分：**
- 隨堂測驗 20%（取最佳 12 次）
- 個人作業 + 報告 + 期末專題 30%
- 自我評量 50%

**成績登錄前提：**
- 隨堂測驗：Jun 19 前至少 2 次課堂互動
- 作業：Jun 7 前至少 1 次一對一討論
- 自我評量：Jul 3, 12:00 PM 前完成

---

## 每週大綱

### Week 1 (Feb 24, 26)：自我誠實 & 基礎
- 課程導覽與期望（[課程介紹影片](https://youtu.be/7Rij1IZqazM)）
- [資訊科技詞彙翻譯](https://hackmd.io/@sysprog/it-vocabulary)
- C 指標、linked list 實作
- Linux 作業系統概念
- [GNU/Linux 開發工具](https://hackmd.io/@sysprog/gnu-linux-dev/)
- 作業一，截止 Mar 11
- [Quiz 1](https://hackmd.io/@sysprog/linux2025-quiz1)

### Week 2 (Mar 3, 5)：C 語言程式設計
- [數值系統](https://hackmd.io/@sysprog/c-numerics)
- [位元運算](https://hackmd.io/@sysprog/c-bitwise)
- [Linux kernel hash table 實作](https://hackmd.io/@sysprog/linux-hashtable)
- [C 語言規格與安全](https://hackmd.io/@sysprog/c-std-security)
- 記憶體管理、對齊、硬體特性
- Bit-field 結構
- 作業二，截止 Mar 17
- [Quiz 2](https://hackmd.io/@sysprog/linux2025-quiz2)

### Week 3 (Mar 10, 12)：數值系統 & C 程式設計
- [Linux 開發回顧](https://hackmd.io/@sysprog/linux-dev-review)
- 最大公因數性質
- [浮點數運算](https://hackmd.io/@sysprog/c-floating-point)
- [並行排程原理](https://hackmd.io/@sysprog/concurrency-sched)
- [函式呼叫](https://hackmd.io/@sysprog/c-function)
- [遞迴](https://hackmd.io/@sysprog/c-recursion)
- [前置處理器](https://hackmd.io/@sysprog/c-preprocessor)
- [goto 與控制流程](https://hackmd.io/@sysprog/c-control-flow)
- [C 程式設計技巧](https://hackmd.io/@sysprog/c-trick)
- 作業三，截止 Apr 11
- [Quiz 3](https://hackmd.io/@sysprog/linux2025-quiz3)

### Week 4 (Mar 17, 19)：數值系統 & 編譯器
- 貢獻程式碼至 Linux kernel
- [Linux kernel red-black trees](https://hackmd.io/@sysprog/linux-rbtree)
- [CS:APP Chapter 2 重點](https://hackmd.io/@sysprog/CSAPP-ch2)
- [C 編譯器建構](https://hackmd.io/@sysprog/c-compiler-construction)
- [Undefined behavior](https://hackmd.io/@sysprog/c-undefined-behavior)
- [編譯器最佳化原理](https://hackmd.io/@sysprog/c-compiler-optimization)
- [Error correction codes (ECC)](https://hackmd.io/@sysprog/r1wrjOp6a)
- 作業四，截止 Apr 15
- [Quiz 4](https://hackmd.io/@sysprog/linux2025-quiz4)

### Week 5 (Mar 24, 26)：Code Review
- 學生作業審查
- [Quiz 5](https://hackmd.io/@sysprog/linux2025-quiz5)

### Week 6 (Mar 31, Apr 2)：C Runtime/Linker & fork/exec
- [亂數分布與 modulo bias](https://hackmd.io/@sysprog/BkSydKkaJg)
- [動態連結器](https://hackmd.io/@sysprog/c-dynamic-linkage)
- [連結器與執行檔](https://hackmd.io/@sysprog/c-linker-loader)
- [C runtime (CRT)](https://hackmd.io/@sysprog/c-runtime)
- ["Everything is a file" 哲學](https://hackmd.io/@sysprog/io-universality)
- [UNIX fork/exec 系統呼叫](https://hackmd.io/@sysprog/unix-fork-exec)
- 作業五，截止 Apr 23
- [Quiz 6](https://hackmd.io/@sysprog/linux2025-quiz6)

### Week 7 (Apr 7, 9)：Process & CPU Scheduling
- 註：Apr 7 為線上課程
- [Euler number 與連續變化](https://hackmd.io/@sysprog/S1lBrHrp1e)
- [Linux 排程機制](https://hackmd.io/@sysprog/linux-scheduler)
- [Linux process 實作](https://hackmd.io/@sysprog/linux-process)
- [Linux system calls](https://hackmd.io/@sysprog/linux-syscall)
- [vDSO：快速系統呼叫](https://hackmd.io/@sysprog/linux-vdso)
- 電子書發放：*Demystifying the Linux CPU Scheduler* (Ch. 1)

### Week 8 (Apr 14, 16)：Concurrency & Linux 同步
- [並行概念](https://hackmd.io/@sysprog/concurrency)
- [Concurrency Primer 導讀](https://hackmd.io/@sysprog/concurrency-primer)
- CS:APP Chapter 12 (Concurrency, Synchronization, Thread-Level Parallelism)
- [Linux 同步機制](https://hackmd.io/@sysprog/linux-sync)
- *Demystifying the Linux CPU Scheduler* (Sections 2.1-2.2.2)
- [Quiz 8](https://hackmd.io/@sysprog/linux2025-quiz8)

### Week 9 (Apr 21, 23)：futex & Server 開發
- [Thread Local Storage (TLS)](https://chao-tic.github.io/blog/2018/12/25/tls)
- [POSIX Thread 相容實作](https://hackmd.io/@sysprog/concurrency-thread-package)
- [事件驅動 I/O 模型演進](https://hackmd.io/@sysprog/linux-io-model)
- [RCU 同步機制](https://hackmd.io/@sysprog/linux-rcu)
- [eBPF 觀察 OS 行為](https://hackmd.io/@sysprog/linux-ebpf)
- 作業六 (ktcp)，截止 May 16
- [Quiz 9](https://hackmd.io/@sysprog/linux2025-quiz9)

### Week 10 (Apr 28, 30)：現代微處理器
- [C11/C++11 並行模型](https://docs.google.com/presentation/d/1IndzU1LDyHcm1blE0FecDyY1QpCfysUm95q_D2Cj-_U/edit?usp=sharing)
- 產業動態：Google Axion Processors, SiFive
- [CPU 基礎與設計](https://hackmd.io/@sysprog/cpu-basics)
- [Linux 中斷處理](https://hackmd.io/@sysprog/linux-interrupt)
- [多核心與 spinlocks](https://hackmd.io/@sysprog/multicore-locks)
- [Quiz 10](https://hackmd.io/@sysprog/linux2025-quiz10)

### Week 11 (May 5, 7)：作業回顧 & 期末專題
- [2025 期末專題](https://hackmd.io/@sysprog/S18kgVDJex)
- 期末專題：個人或兩人一組（兩人組難度較高）
- 自 Week 12 起遷至新大樓 65203 教室
- [Quiz 11](https://hackmd.io/@sysprog/linux2025-quiz11)

### Week 12 (May 12, 14)：微處理器 & 記憶體管理
- [Mutex Lock 輕量實作](https://hackmd.io/@sysprog/concurrency-mutex)
- [Reference counting](https://hackmd.io/@sysprog/concurrency-reference-count)
- *Demystifying the Linux CPU Scheduler* (Sections 2.4, 3.2, 3.4, 4.1-4.2)
- [CS:APP Chapter 6 重點](https://hackmd.io/@sysprog/CSAPP-ch6)
- [CPU caches](https://lwn.net/Articles/252125/)
- [CS:APP Chapter 9 重點](https://hackmd.io/@sysprog/CSAPP-ch9)
- [Quiz 12](https://hackmd.io/@sysprog/linux2025-quiz12)

### Week 13 (May 19, 21)：記憶體管理 & Device Drivers
- [Linux 記憶體管理](https://hackmd.io/@sysprog/linux-memory)
- [POSIX Shared Memory](http://logan.tw/posts/2018/01/07/posix-shared-memory/)
- [共享記憶體機制](https://hackmd.io/@sysprog/linux-shared-memory)
- [/dev/mem device](https://hackmd.io/@sysprog/linux-mem-device)
- [物件導向 C 程式設計](https://hackmd.io/@sysprog/c-oop)
- [核心中的設計模式](https://lwn.net/Articles/444910/)
- [串流 I/O 與例外處理](https://hackmd.io/@sysprog/c-stream-io)
- [CS:APP Chapter 10 重點](https://hackmd.io/@sysprog/CSAPP-ch10)
- [Device driver 介面與模型](https://github.com/gregkh/presentation-driver-model)
- [Device Tree](https://events.static.linuxfound.org/sites/events/files/slides/petazzoni-device-tree-dummies.pdf)
- [Linux timers](https://hackmd.io/@sysprog/linux-timer)
- [Linux scalability](https://hackmd.io/@sysprog/linux-scalability)
- [Cache-oblivious 資料結構](https://rcoh.me/posts/cache-oblivious-datastructures/)
- [Quiz 13](https://hackmd.io/@sysprog/linux2025-quiz13)

### Week 14 (May 26, 28)：Virtual Memory & 虛擬化
- [記憶體模型](https://mes0903.github.io/memory/memory_model/)
- [Linux Copy-On-Write](https://hackmd.io/@linD026/Linux-kernel-COW-content)
- [嵌入式虛擬化](https://www.slideshare.net/jserv/mobile-virtualization)
- [KVM：Linux 虛擬化基礎建設](https://hackmd.io/@sysprog/linux-kvm)
- [LKL：重用 Linux kernel](https://hackmd.io/@sysprog/linux-lkl)
- 自我評量開放（Jun 20）

### Week 15 (Jun 2, 4)：網路封包處理 & 多核心
- [slab 記憶體配置器](https://hackmd.io/@sysprog/linux-slab)
- [Linux kernel 網路](https://hackmd.io/@rickywu0421/BJxD_3989)
- [semu：簡化 RISC-V 模擬器](https://hackmd.io/@sysprog/Skuw3dJB3)
- [userfaultfd 記憶體外部化](http://ftp.ntu.edu.tw/pub/linux/kernel/people/andrea/userfaultfd/userfaultfd-LSFMM-2015.pdf)
- [Linux 處理網路封包的方式](https://www.slideshare.net/DevopsCon/how-linux-processes-your-network-packet-elazar-leibovich)
- [Kernel 封包截取技術](https://www.slideshare.net/ennael/kernel-recipes-2015-kernel-packet-capture-technologies)
- [PACKET_MMAP](https://www.kernel.org/doc/Documentation/networking/packet_mmap.txt)
- [Linux 多核心](https://youtu.be/UNI6Mbqryv0) / [SMP OS](https://wiki.csie.ncku.edu.tw/embedded/11-smp_os.pdf)
- [CPU cache coherence 與 spinlock scalability](https://hackmd.io/@sysprog/linux-spinlock-scalability)
- [Quiz 15](https://hackmd.io/@sysprog/linux2025-quiz15)

### Week 16 (Jun 9, 11)：程式碼最佳化 & 多核心架構
- *Demystifying the Linux CPU Scheduler* (Sections 2.4-2.5, 3.4, 4.2-4.4)
- [Binary search 在現代硬體上的最佳化](https://hackmd.io/@RinHizakura/BJ-Zjjw43)
- [CS:APP Chapter 5 重點](https://hackmd.io/s/SyL8m4Lnm)
- [Linux scalability 議題](https://hackmd.io/@sysprog/linux-scalability)
- [Memory ordering in Linux](http://www.rdrop.com/users/paulmck/scalability/paper/LinuxMM.2017.04.08b.Barcamp.pdf)
- [Quiz 16](https://hackmd.io/@sysprog/linux2025-quiz16)

### Week 17 (Jun 16, 18)：Real-Time Linux 基礎
- [Linux timers](https://hackmd.io/@sysprog/linux-timer)
- [2038 年時間問題](https://events19.linuxfoundation.org/wp-content/uploads/2017/12/The-End-of-Time-19-Years-to-Go-Arnd-Bergmann-Linaro-Ltd.pdf)
- [Real-time scheduling on Linux](https://eci.intel.com/docs/3.2/development/performance/rt_scheduling.html)
- [PREEMPT_RT for hard real-time](https://hackmd.io/@sysprog/preempt-rt)
- [Linux kernel preemption](https://hackmd.io/@sysprog/linux-preempt)
- [Task isolation on PREEMPT_RT](https://ossna2022.sched.com/event/11NtQ)
- [Linux and Zephyr on same SoC](https://events19.linuxfoundation.org/wp-content/uploads/2017/12/Linux-and-Zephyr-%E2%80%9CTalking%E2%80%9D-to-Each-Other-in-the-Same-SoC-Diego-Sueiro-Sepura-Embarcados.pdf)
- [Quiz 17](https://hackmd.io/@sysprog/linux2025-quiz17)

### Week 18 (Jun 23, 25)：多核心 & Rust 程式設計
- [Linux kernel preemption](https://hackmd.io/@sysprog/linux-preempt)
- [RTMux multiplexer](https://elinux.org/images/a/a4/Huang--rtmux_a_thin_multiplexer_to_provide_hard_realtime_applications_for_linux.pdf) / [EVL](https://evlproject.org/)
- Memory barriers
- [Rust for Linux 研究](https://hackmd.io/@hank20010209/SJmVNPMQ2)
- [撰寫 Rust kernel modules](https://hackmd.io/@sysprog/Sk8IMQ9S2)
- [Quiz 18](https://hackmd.io/@sysprog/linux2025-quiz18)

### Week 19 (Jun 30)：Rust & Kernel Debugging
- 自我評量截止：Jul 3, 12:00 PM
- 期末成果展與專題審查
- 最後一堂課：Jul 1, 19:30
- [Rust for Linux 研究](https://hackmd.io/@hank20010209/SJmVNPMQ2)
- [The Rust Programming Language](https://rust-lang.tw/book-tw/)（繁體中文）
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
- [C vs. Rust](http://www-verimag.imag.fr/~mounier/Enseignement/Software_Security/19RustVsC.pdf)

### Week 20 (Jul 7)：總回顧 & 評量
- Peer review 截止：Jul 8, 12:00 PM（至少 5 個專題）
- 回應截止：Jul 4, 12:00 PM
- [課程自我評量指南](https://hackmd.io/@sysprog/linux2024-assessment)
- [期末成果展](https://hackmd.io/@sysprog/linux2025-showcase)
- [專題審查](https://hackmd.io/@sysprog/linux2025-projects)

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
