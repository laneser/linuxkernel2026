> **原始出處：** https://hackmd.io/@sysprog/linux2026-basics
> **擷取日期：** 2026-04-17
> **用途：** 第三週作業 (basics) 完整要求
> **涵蓋度：** 完整
> **省略內容：** 無

---
title: 2026 年 Linux 核心設計課程作業 —— basics
image: https://i.imgur.com/robmeiQ.png
description: 做好探索 Linux 主體的準備
tags: linux2026
---

# 2026 年 [Linux 核心設計](https://wiki.csie.ncku.edu.tw/linux/schedule)課程作業: basics

> 主講人: [jserv](https://wiki.csie.ncku.edu.tw/User/jserv) / 課程討論區: [2026 年系統軟體課程](https://www.facebook.com/groups/system.software2026/)
:mega: 返回「[Linux 核心設計](https://wiki.csie.ncku.edu.tw/linux/schedule)」課程進度表

## :memo: 預期目標
* 充分檢視[第三、第四週教材](https://wiki.csie.ncku.edu.tw/linux/schedule)，從第一手材料理解 C 語言程式設計和 Linux 核心內部機制
* 觀摩學員[第二次作業的成果](https://hackmd.io/@sysprog/linux2026-homework2)並學習 code review 原則
* [軟體工程師要學會說故事](https://ruddyblog.wordpress.com/2016/06/18/)，從良性詳盡的批評開始

## 注意須知
* 凡[第三週測驗題](https://hackmd.io/@sysprog/linux2026-quiz3)超過 40 分的學員，請參閱 [kbox 專案](https://github.com/sysprog21/kbox) (搭配 [LKL: 重用 Linux 核心的成果閱讀](https://hackmd.io/@sysprog/linux-lkl)) 並發信件 ([依循指定格式]，並回覆下方「細讀〈LKL: 重用 Linux 核心的成果〉」指定的問題。其他學員則要比照第一次和第二次作業的風格，細讀教材、提問，和回覆指定的問題
* 進行 [kbox 專案](https://github.com/sysprog21/kbox)的學員至少要提交 2 個 pull request 並與授課教師協作 (code review 和參與討論)，其中至少一份要是 non-trivial 貢獻，參照 [GitHub Issues](https://github.com/sysprog21/kbox/issues)，且回覆指定的問題
* 所有學員都要依據指示，觀摩學員[第二次作業的成果](https://hackmd.io/@sysprog/linux2026-homework2)，審視並提出意見，也該針對同儕的意見，予以回應

:::warning
以下不是「重點提示」，而是你該在作業中充分回答的各式問題。不該用「是」和「否」這樣二元的答覆，每題值得你重新檢視 C 語言規格書、Linux 核心原始程式碼及其 git log、(原本你該翻閱的) 微積分、機率和統計教科書、數學推理，和設計實驗來確認你的認知。
這些問題也可能在你日後參加科技公司面試時出現，現在就進行對應的準備。
:::

## 細讀〈[LKL: 重用 Linux 核心的成果](https://hackmd.io/@sysprog/linux-lkl)〉
> 進行 kbox 專案的學員需要回覆以下，並紀錄你的提問

* Linux Kernel Library (LKL) 以數千行的 [`arch/lkl`](https://github.com/lkl/linux/tree/master/arch/lkl) 架構相關程式碼，將 Linux 核心編譯為使用者空間的函式庫 (`liblkl.a`)，使 FreeBSD、macOS、Windows 乃至 JavaScript 環境得以重用 Linux 的檔案系統、TCP/IP 堆疊與 `/proc` 介面。作業一的提問中，你已分析「若將 Linux 的 VFS 或 network stack 遷移至 userspace (類似 microkernel multi-server 模型)」的 context switch 數量變化、cache locality、fault isolation 與 worst-case latency。LKL 正是此遷移的極端案例：整個核心以函式庫的形式嵌入應用程式行程。以此為出發點：
    * (a) 閱讀 [`arch/lkl/include/uapi/asm/host_ops.h`](https://github.com/lkl/linux/blob/master/arch/lkl/include/uapi/asm/host_ops.h) 的 `struct lkl_host_operations`，此結構體定義 LKL 對主機作業系統的全部依賴：`thread_create`、`sem_alloc`/`sem_up`/`sem_down`、`mem_alloc`、`timer_set` 等。對照 Linux 核心正常運作時對硬體的依賴 (中斷控制器、MMU、計時器)，逐一分析 LKL 如何以主機作業系統的 POSIX API (參閱 [`tools/lkl/lib/posix-host.c`](https://github.com/lkl/linux/blob/master/tools/lkl/lib/posix-host.c) 的 `thread_create` 實作) 替代這些硬體抽象。建立對照表：中斷→信號或 eventfd、MMU→無 (LKL 無記憶體保護)、spinlock→主機 semaphore、timer→`timer_create()`/`timer_settime()`
    * (b) LKL 不啟用 `CONFIG_SMP`，在任何時刻只允許一個執行緒執行核心程式碼。此限制透過 semaphore 實作：`__switch_to()` (位於 [`arch/lkl/kernel/threads.c`](https://github.com/lkl/linux/blob/master/arch/lkl/kernel/threads.c)) 先以 `sem_up(next->sched_sem)` 喚醒目標執行緒，再以 `sem_down(current->sched_sem)` 阻塞自身。證明此機制等效於協同式多工 (cooperative multitasking) 的 coroutine 切換，與作業一分析的 `setjmp`/`longjmp` context switch 在控制流儲存策略上有何根本差異？提示：LKL 的 `__switch_to` 不儲存/恢復暫存器，而是依賴每個主機執行緒擁有獨立的 stack frame，semaphore 的 down/up 即隱含完整的上下文儲存
* 教材展示 LKL 搭配 FUSE 掛載 ext4 檔案系統的流程：`lkl_init()` → `lkl_start_kernel("mem=128M")` → `lkl_disk_add()` → `lkl_mount_dev()` → `lkl_opendir()`/`lkl_readdir()`。作業二分析 Linux 核心的 VFS 層如何以 `struct file_operations` 的函式指標實作多型。LKL 重用的正是同一套 VFS 程式碼，但 I/O 路徑完全不同：磁碟存取不經過 block device driver，而是透過 virtio 介面回呼至主機的 `read()`/`write()`。以此為出發點：
    * (a) 追蹤 LKL 中一次 `lkl_sys_read()` 的完整路徑：從系統呼叫入口 → VFS `vfs_read()` → ext4 的 `read_iter` → page cache → bio 提交 → virtio-blk → 主機端的 `pread()` 回呼。繪製此呼叫鏈的序列圖，標註哪些層級是 Linux 核心通用程式碼 (不因 LKL 而改變)、哪些是 [`arch/lkl`](https://github.com/lkl/linux/tree/master/arch/lkl) 的橋接層。以此解釋為何 LKL 僅需數千行架構相關程式碼即可重用整個 Linux 核心
    * (b) 設計實驗：編譯 LKL，以教材的 `readfs.c` 範例掛載 ext4 映像檔，以 `strace` 追蹤主機端的系統呼叫，統計一次 `lkl_sys_read()` 觸發多少次主機端的 `pread64()`/`read()`。比較相同操作在原生 Linux 核心 (直接掛載) 下的系統呼叫次數，量化 LKL 的額外間接層開銷
* LKL 允許在使用者空間對 Linux 核心程式碼進行模糊測試 (fuzzing)，可搭配 libFuzzer 使用。教材指出為使模糊測試行為更可預測 (deterministic)，可在 LKL 中引入特製的排程器，在同步處理機制 (spinlock、mutex) 前後插入 yield point。以此為出發點：
    * (a) 作業二分析 BPF verifier 的邊界檢查機制。LKL-based fuzzing 提供另一條核心測試路徑：直接在使用者空間以 AddressSanitizer (ASan) 和 libFuzzer 檢測核心程式碼的記憶體錯誤。比較 LKL fuzzing 與 syzkaller (在虛擬機器中模糊測試核心系統呼叫) 的架構差異：syzkaller 需要 VM 重啟來恢復狀態，LKL 可在行程內重置。從測試效率的角度分析各自的 executions/sec 上限
    * (b) 教材的 `cat_proc.c` 範例以 `lkl_sys_mount("none", "/proc", "proc", 0, 0)` 掛載 procfs 並走訪其內容。此範例展示 LKL 完整重用核心的 procfs 實作。閱讀輸出中 `/proc/stat` 與 `/proc/pagetypeinfo` 的內容，分析：LKL 環境中 `/proc/stat` 的 `cpu` 行只顯示一個 CPU (因為 `!CONFIG_SMP`)，`/proc/pagetypeinfo` 顯示 page block order = 10，即 1024 pages。LKL 以 `mem=128M` 啟動，計算其可用的 page 總數 ($128 \times 1024 \times 1024 / 4096 = 32768$ pages) 與 buddy allocator 的最大 order 配置，並對照 `/proc/buddyinfo` 的輸出驗證
* LKL 的設計凸顯 Linux 核心架構的模組化程度：`arch/` 目錄提供硬體抽象層，其餘程式碼 (VFS、network stack、記憶體管理、排程器) 鮮少依賴特定硬體。以此為出發點：
    * (a) 作業一提到 Linux 在 monolithic 架構下如何持續擴展，以及 abstraction preservation 的角色。LKL 的存在證明 Linux 核心的 HAL (Hardware Abstraction Layer) 足夠薄，使得將整個核心搬至使用者空間可行。然而 LKL 目前不支援 SMP，相關[雛形設計](https://github.com/lkl/linux/issues/370)尚未完成。分析 SMP 支援為何困難：LKL 以主機 semaphore 實作 [`__switch_to()`](https://github.com/lkl/linux/blob/master/arch/lkl/kernel/threads.c)，此模型假設同一時刻只有一個執行緒持有「核心執行權」。若要支援 $N$ 個虛擬 CPU 同時執行核心程式碼，需要什麼機制取代現有的全域 semaphore？從 per-CPU 資料結構 (`DEFINE_PER_CPU`)、RCU 的 grace period 偵測、以及 `local_irq_disable()` 的語意出發，分析 LKL 要支援 SMP 所需的最小改動集合
    * (b) 從數學的角度，LKL 的單執行緒模型可視為 $N = 1$ 的特例。作業一建立的 lock contention 模型中，$N = 1$ 時 contention 為零，spinlock 退化為 nop。驗證此推論：閱讀 LKL 的 spinlock 相關標頭檔 (如 [`arch/lkl/include/asm/`](https://github.com/lkl/linux/tree/master/arch/lkl/include/asm) 下的 spinlock 定義)，分析 `!CONFIG_SMP` 下 spinlock 是否仍保留 preemption disable 或 IRQ disable 語意，抑或完全退化為空操作。進一步推導：若 LKL 支援 SMP ($N > 1$)，其 lock contention 成本是否會高於原生 Linux 核心 (因為主機作業系統的 semaphore 比硬體 spinlock 慢)？建立比較模型並估算差異

## 研讀〈[Linux: 發展動態回顧](https://hackmd.io/@sysprog/linux-dev-review)〉
* Big Kernel Lock (BKL) 歷經約 15 年才從 Linux 核心移除。作業一的提問中，你已分析 monolithic 架構下 Linux 如何持續擴展，以及 $N$ 核系統中 spinlock 保護全域計數器的 coherence traffic 成長趨勢。以此為出發點：
    * (a) 從 git log 找出 BKL 移除歷程中的關鍵 commit (提示: `lock_kernel()`/`unlock_kernel()` 的呼叫點逐步被 fine-grained mutex 取代)，追蹤 VFS、network stack、tty 子系統各自何時脫離 BKL，並以 lock contention 模型量化 $N$ 核系統中 BKL 與 fine-grained lock 的 cache-line bouncing 成本差異
    * (b) 建立數學模型：假設 $N$ 個 CPU 以頻率 $f$ 競爭單一 spinlock，每次 cache-line transfer 成本為 $T_c$，推導 lock contention 的期望等待時間隨 $N$ 的增長階數，並對照 per-CPU 計數器 (如 `percpu_counter`) 的設計如何將此成本從 $O(N)$ 降至 $O(1)$。設計實驗以 `perf stat -e cache-misses,bus-cycles` 在多核系統上量測全域 atomic counter 與 per-CPU counter 的實際差異
* io_uring 以 submission queue (SQ) 與 completion queue (CQ) 的共享記憶體環形緩衝區避免每次 I/O 操作都進入核心模式，取代傳統 AIO。作業一中你已分析 context switch 數量變化與系統呼叫機制的成本。閱讀 [`io_uring/io_uring.c`](https://github.com/torvalds/linux/blob/master/io_uring/io_uring.c) 的 `io_submit_sqes()` 路徑，說明核心如何以 single `io_uring_enter()` 系統呼叫批次處理多個 SQE (Submission Queue Entry)。設計實驗：以 `fio` 工具分別在 `libaio` 與 `io_uring` 引擎下對同一 NVMe 裝置執行 4K 隨機讀取，以 `perf stat -e syscalls:sys_enter_*` 量測系統呼叫次數，建立 IOPS 與系統呼叫次數的關係模型，驗證 io_uring 的 batching 效果
    > 對照 [I/O 模型演化: Linux 的 io_uring](https://hackmd.io/@sysprog/iouring)
* eBPF 允許在核心中動態載入程式。作業二的提問中，你已分析 CVE-2021-33200 中 BPF verifier 對指標算術的邊界限制不足，導致攻擊者可繞過 `alu_limit` 檢查。進一步探討：
    * (a) 閱讀 [`kernel/bpf/verifier.c`](https://github.com/torvalds/linux/blob/master/kernel/bpf/verifier.c) 的 `check_alu_op()` 與 `adjust_reg_min_max_vals()`，追蹤 verifier 如何以 interval analysis 追蹤每個暫存器的 `[smin_value, smax_value]` 與 `[umin_value, umax_value]`，並說明此 abstract interpretation 在 ALU32 操作後如何更新值域。對比作業二分析的 `BIT()` 與 `GENMASK()` 在位移量邊界的編譯期檢查，BPF verifier 的邊界檢查是在執行期前的靜態驗證
    * (b) 設計一段 BPF 程式 (使用 `bpf_prog_test_run`)，刻意觸發 verifier 拒絕載入的邊界條件 (如陣列越界存取)，觀察 verifier 的錯誤訊息，並與作業二分析的 UBSan 位移檢查機制進行對比
* PREEMPT_RT 將 Linux 核心轉變為可搶佔式即時系統。作業一提到排程器的映射函數 $f : (P, t) \rightarrow C$ 與 worst-case latency 分析。閱讀 [`kernel/irq/manage.c`](https://github.com/torvalds/linux/blob/master/kernel/irq/manage.c) 的 `__setup_irq()`，說明 PREEMPT_RT 如何將 hardirq handler 轉為 threaded interrupt handler (以 `IRQF_ONESHOT` 旗標)，使中斷處理可被高優先權行程搶佔。設計實驗：在同一硬體上分別以 `CONFIG_PREEMPT_NONE` 與 `CONFIG_PREEMPT_RT` 編譯核心，以 [cyclictest](https://wiki.linuxfoundation.org/realtime/documentation/howto/tools/cyclictest/start) 量測 worst-case latency 並繪製延遲直方圖。以作業一建立的延遲期望值模型 $E[T] = T_{pf} \cdot p + T_{normal} \cdot (1-p)$ 為基礎，擴充為包含搶佔延遲項 $T_{preempt}$ 與中斷延遲項 $T_{irq}$ 的完整模型 $E[T] = T_{normal} + p_{pf} \cdot T_{pf} + p_{irq} \cdot T_{irq} + p_{preempt} \cdot T_{preempt}$，以實驗資料擬合各參數
    > 對照 [PREEMPT\_RT 作為邁向硬即時作業系統的機制](https://hackmd.io/@sysprog/preempt-rt)

## 細讀〈[有限體算術與 $2^k$ 索引：Linux 核心對數學封閉性與硬體成本的權衡](https://hackmd.io/@sysprog/BJ7DvyPtWg)〉
* X25519 橢圓曲線密碼學 (在質數體 $\text{GF}(2^{255}-19)$ 上運算) 與雜湊表索引 (在環 $\mathbb{Z}/2^k\mathbb{Z}$ 上運算) 存在根本性的設計取捨。作業一要求證明 $(\mathbb{Z}/2^k\mathbb{Z}, +)$ 為阿貝爾群但 $(\mathbb{Z}/2^k\mathbb{Z}, \times)$ 非群，作業二分析 `GOLDEN_RATIO_64` 在環論語境中的可逆性。以此為出發點：
    * (a) 以擴充歐幾里得演算法實際求出 `GOLDEN_RATIO_64` ($= \text{0x61C8864680B583EB}$) 在 $\mathbb{Z}/2^{64}\mathbb{Z}$ 中的乘法反元素 $C^{-1}$，撰寫程式驗證 $C \cdot C^{-1} \equiv 1 \pmod{2^{64}}$。接著，證明即使乘法在環中可逆，`hash_64(val, bits) = (val * C) >> (64 - bits)` 的右移操作丟棄 $64 - \text{bits}$ 個低位元，使得每個輸出值對應 $2^{64-\text{bits}}$ 個 preimage，故整體函數不可逆。將丟棄的位元數量與 preimage 集合大小的關係以精確的數學式表達
    * (b) X25519 以 Fiat-Crypto 的 10-limb representation (交替 25/26 位元邊界) 延遲進位傳播，使中間乘積在 52 位元內以 `u64` 安全累加。作業二分析 `mul_u64_u32_shr` 在 32 位元平台的部分積累加與 carry propagation。比較兩者的分解策略：X25519 的延遲進位消除資料相依的分支 (constant-time 需求)，CFS 排程器的立即進位確保每步結果可用於後續計算 (確定性需求)。從 [`lib/crypto/curve25519-fiat32.c`](https://github.com/torvalds/linux/blob/master/lib/crypto/curve25519-fiat32.c) 找出 `fe_mul_ttt()` 的實作 (Fiat-Crypto 產生的程式碼以 `ttt`/`tlt`/`tll` 後綴區分 tight/loose field element 的輸入組合)。注意此檔案是針對無高效 128 位元乘法的 32 位元平台設計，以 `u64` 部分積累加避免溢位，而非使用 `u128`。對比 `lib/crypto/curve25519-hacl64.c` (64 位元平台版本，使用 `u128` 累加)，並與 `include/linux/math64.h` 的 32 位元 fallback 路徑在溢位處理策略上進行對比
* 作業二分析 `hash_32()` 使用黃金比例常數與 Three-gap theorem 的數學背景，以及 hash collision 攻擊對系統效能的影響。雜湊函數取高位元作為 bucket index 而非低位元，因為乘法散列的高位元攜帶更充分的混合資訊。以此為出發點：
    * (a) 從數論的角度，證明 $\{K \cdot \phi \bmod 1 : K = 0, 1, \ldots, n-1\}$ 將 $[0, 1)$ 切分為至多三種不同長度的間隔 (Three-gap theorem)。以 Python 或 C 程式產生 $n = 1024$ 個點的分布，繪製 gap histogram，驗證此定理並與使用 `0x80000000` (非黃金比例) 作為乘數時的分布進行對比
    * (b) 乘法雜湊對 HashDoS 攻擊脆弱，因為乘數 $C$ 公開，攻擊者可構造碰撞。從 Linux 核心的 git log 找出從 `jhash` 遷移至 `siphash` 的關鍵 commit (提示: 搜尋 `net/ipv4/` 與 `fs/` 下的 hash function 替換)，分析 `siphash` 以密鑰混合如何使攻擊者無法預測碰撞，並閱讀 [`lib/siphash.c`](https://github.com/torvalds/linux/blob/master/lib/siphash.c) 說明其 2-4 round 架構的計算成本與 `jhash` 的差異

## 細讀〈[最大公因數特性和實作考量](https://hackmd.io/@sysprog/gcd-impl)〉
* `perf` 量測顯示歐幾里得演算法中除法運算約佔 28% 的 CPU cycles。作業二分析 `DIV_ROUND_UP`、`do_div`，以及將除法轉換為乘法與位移的技巧。以此為出發點：
    * (a) 閱讀 [`lib/math/gcd.c`](https://github.com/torvalds/linux/blob/master/lib/math/gcd.c) 的 binary GCD 實作，追蹤其如何以 `__ffs()` (count trailing zeros) 取代重複除以 2 的操作。從 git log 找出將歐幾里得演算法替換為 binary GCD 的 commit，擷取其中的 benchmark 資料。設計實驗：以隨機 32 位元整數對作為輸入，分別量測歐幾里得演算法與 binary GCD 的 cycles/operation (使用 `rdtsc` 或 `perf stat`)，並以 `perf record -e cpu/event=0xc4,umask=0x00/` 追蹤 division µop 的數量差異
    * (b) binary GCD 的最壞情況迭代次數與 Fibonacci 數列相關：連續 Fibonacci 數 $(F_n, F_{n+1})$ 使歐幾里得演算法達到最大遞迴深度，binary GCD 則在 $a, b$ 的二進位表示交替為 0 和 1 時最差。推導 binary GCD 對 $w$ 位元輸入的最壞迭代次數上界 $2w$，並以實驗驗證
* 作業一提到 $a^{-1} \equiv a^{p-2} \pmod{p}$ (費馬小定理) 可用於計算有限體中的反元素。GCD 與擴充歐幾里得演算法提供另一條求反元素的路徑。比較兩者在 Linux 核心密碼學子系統 ([`crypto/`](https://github.com/torvalds/linux/tree/master/crypto)) 中的應用：
    * (a) 費馬小定理需要模指數運算 ($O(\log p)$ 次模乘)，擴充歐幾里得演算法需要 $O(\log p)$ 次除法/位移。在 constant-time 需求下，模指數的固定迭代次數使其更易實現 timing-safe 的程式碼，而擴充歐幾里得的迭代次數依賴輸入，需額外 padding。從 `crypto/ecc.c` 的 `vli_mod_inv()` 追蹤核心選擇哪種方法，並分析其 constant-time 保證
    * (b) 核心在多個子系統中使用 `gcd()` (如時間子系統的 `clk_rate` 簡化、排程器的權重參數正規化)。設計實驗：以 Linux 核心中實際出現的 nice 值對應權重 (nice 0 = 1024, nice -20 = 88761 等) 作為 GCD 輸入，量測 `lib/math/gcd.c` 的迭代次數分布，並與隨機輸入的分布進行比較

## 細讀〈[從 Revolution OS 看作業系統生態系統變化](https://hackmd.io/@sysprog/revolution-os-note)〉
* `MODULE_LICENSE("GPL")` 與核心模組的授權宣告機制。Linux 核心要求每個可載入模組以 `MODULE_LICENSE()` 巨集宣告其授權條款。閱讀 [`include/linux/module.h`](https://github.com/torvalds/linux/blob/master/include/linux/module.h) 中 `MODULE_LICENSE` 的展開邏輯，以及 `kernel/module/main.c` 中 `license_is_gpl_compatible()` 的判斷流程。當模組未宣告 GPL 相容授權時，核心會在 `dmesg` 輸出 "loading out-of-tree module taints kernel" 並設定 `TAINT_PROPRIETARY_MODULE` 旗標，而此 tainted 狀態會導致 `EXPORT_SYMBOL_GPL` 匯出的符號對該模組不可見，OOPS 回報中也會標記 taint flag 使得社群拒絕協助除錯。從 [`include/linux/export.h`](https://github.com/torvalds/linux/blob/master/include/linux/export.h) 追蹤 `EXPORT_SYMBOL_GPL` 與 `EXPORT_SYMBOL` 的差異如何在符號解析階段 (`resolve_symbol()`) 生效。設計實驗：撰寫二個核心模組，一個宣告 `MODULE_LICENSE("GPL")`、另一個宣告 `MODULE_LICENSE("Proprietary")`，觀察後者嘗試呼叫 GPL-only 符號時 `insmod` 的錯誤訊息與 `dmesg` 輸出
    > 對照 [Linux 核心模組運作原理](https://hackmd.io/@sysprog/linux-kernel-module)
* Microsoft Hyper-V 的 GPL 之旅。2009 年社群發現 Microsoft 的 Hyper-V Linux integration components 使用 GPL 授權的核心標頭檔與符號卻以閉源形式散布，違反 GPL v2 條款。在壓力下 Microsoft 被迫將 Hyper-V Linux integration code 以 GPL v2 釋出，這是 Microsoft 首次向 Linux 核心貢獻程式碼。此後 Microsoft 逐步成為核心的主要貢獻者之一：從 `drivers/hv/` 的 Hyper-V VMBus 驅動到 `fs/cifs/` 的 SMB 用戶端、`net/mptcp/` 的 Multipath TCP，乃至 `tools/testing/selftests/` 的測試基礎設施。從 git log 追蹤此歷程：
    * (a) 找出 2009 年 Hank Janssen 提交的初始 Hyper-V commit series，觀察其程式碼品質 (當時被社群大量批評並要求重寫)
    * (b) 以 `git log --author="@microsoft.com" --oneline | wc -l` 統計 Microsoft 員工迄今的 commit 數量，以 `git log --author="@microsoft.com" --shortstat` 估算變更的程式碼行數，並列出 Microsoft 貢獻最多的五個子系統。此案例如何證明 GPL 的 copyleft 機制，即便最初抗拒開放原始碼的企業，一旦依賴 Linux 核心生態系統，終將被迫參與並受益於社群協作模式？
* BSD 的 `struct vnode` 與 Linux 的 `struct inode` + `struct dentry` 分離設計構成 VFS 的關鍵分歧。Linus Torvalds 在 1991 年釋出 Linux 核心時，BSD 正面臨 AT&T 訴訟。從技術面分析：4.4BSD 以單一 `struct vnode` 同時承擔路徑名稱與 inode 語意，Linux 則將路徑查詢結果快取於 `struct dentry`、將檔案中繼資料獨立為 `struct inode`。此分離使 Linux 的 dentry cache (dcache) 可獨立於 inode 回收，高頻路徑查詢 (`open()`, `stat()`) 命中 dcache 時無需觸及儲存媒介的 inode。閱讀 [`fs/dcache.c`](https://github.com/torvalds/linux/blob/master/fs/dcache.c) 的 `__d_lookup_rcu()`，說明 RCU 如何在無鎖條件下完成 dcache 查詢，分析此設計如何成為 Linux 檔案系統效能的關鍵優勢。將此 VFS 設計差異與 GPL 授權的生態系統效應結合：BSD 的寬鬆授權允許閉源衍生 (如 macOS 的 VFS 層基於 BSD)，而 GPL 迫使所有 VFS 改進回饋至主線。從 `fs/` 下的 git log 統計近 5 年新增的檔案系統數量，佐證 copyleft 對生態系統多樣性的影響
* 閱讀 Linux 核心的 [`MAINTAINERS`](https://github.com/torvalds/linux/blob/master/MAINTAINERS) 檔案，以 `scripts/get_maintainer.pl` 對近 3 個月的 commit 進行分析：
    * (a) 統計前 10 大活躍子系統的 commit 數量與維護者人數，計算每位維護者平均的 review 負擔
    * (b) 從 `Documentation/process/submitting-patches.rst` 出發，追蹤一個 patch 從提交到合併的完整流程，即開發者 → 子系統維護者 → linux-next 整合樹 → Linus 的主線樹，並說明此階層式 review 模型如何在不依賴中央化 CI 的前提下維持程式碼品質

## 細讀〈[浮點數運算](https://hackmd.io/@sysprog/c-floating-point)〉
* IEEE 754 的表示法與運算陷阱中，catastrophic cancellation (二個相近數值相減導致有效位數大幅流失) 尤為重要。作業二分析 MIPS FPU 軟體模擬器的 sticky-bit 截斷與 round-to-even，以及 `float32_to_float16` 的 denormalized 路徑。以此為出發點：
    * (a) Linux 核心的計時子系統以 `s64` (帶號 64 位元整數) 儲存奈秒級時間戳。`ktime_sub()` 計算二個時間戳的差值時，定點數減法不會出現 catastrophic cancellation，因為整數減法的相對誤差為零 (結果精確)。證明此性質：對 $a, b \in \mathbb{Z}$，$a - b$ 在整數算術下精確無誤差，而 IEEE 754 浮點數減法 $\text{fl}(a - b)$ 在 $|a - b| \ll |a|$ 時相對誤差可達 $O(1)$。以此解釋為何 Linux 核心的時間子系統選擇整數奈秒而非浮點秒
    * (b) subnormal numbers 在某些處理器上造成 denormal penalty (Intel 的 SSE 路徑可能降速 100 倍)。閱讀 [`arch/x86/kernel/fpu/xstate.c`](https://github.com/torvalds/linux/blob/master/arch/x86/kernel/fpu/xstate.c) 的 FPU context switch 機制，說明 `fpstate` 如何儲存與恢復 MXCSR 暫存器 (含 FTZ/DAZ 旗標)。設計實驗：撰寫使用者空間程式分別在 FTZ=0 (denormal 正常處理) 與 FTZ=1 (denormal flush to zero) 模式下執行大量 subnormal 運算，以 `perf stat` 量測 cycles 差異，並驗證核心的 FPU context switch 正確恢復每個行程獨立的 MXCSR 設定
* USS Yorktown 癱瘓、Ariane 5 爆炸等真實案例說明數值錯誤的嚴重後果。作業二分析 Boeing 787 的 32 位元計數器在約 248 天 overflow。從 Linux 核心的角度延伸：
    * (a) 閱讀 [`kernel/time/clocksource.c`](https://github.com/torvalds/linux/blob/master/kernel/time/clocksource.c) 的 `clocks_calc_mult_shift()`，此函式在給定的 `from` (Hz)、`to` (Hz) 與 `maxsec` (最大不溢位秒數) 約束下選擇最大的 `shift` 值以最大化定點精度。推導 `mult` 與 `shift` 的選擇如何決定「在不溢位的前提下可表示的最長時間間隔」，並以 TSC 頻率 3 GHz、`maxsec = 600` 為例，計算最佳的 `mult`/`shift` 值與對應的奈秒精度。此設計與 IEEE 754 的 exponent/fraction 位元分配有粗略的類比，兩者都是在固定位元預算下的精度與範圍的權衡
    * (b) 設計一份 Linux 核心中可能受數值精度問題影響的子系統清單 (至少涵蓋 scheduler、timekeeping、networking、DRM/KMS)，針對每個子系統記錄其數值表示法的選擇與精度保證，以及在 git log 中是否存在因數值問題而修正的 commit
* Linux 核心的 `lib/math/div64.c` 在 32 位元平台上處理 64÷32 除法。閱讀 `div_u64_rem()` 的實作：在 64 位元平台上直接以原生除法完成，但在 32 位元平台上退化至 `__div64_32()` 的軟體模擬路徑。追蹤 `__div64_32()` 的演算法，它將 64 位元被除數拆為高 32 位元與低 32 位元，以兩次 32 位元除法完成計算。分析此拆解的數學基礎：設 $N = N_H \cdot 2^{32} + N_L$，$D$ 為 32 位元除數，則 $\lfloor N / D \rfloor = \lfloor N_H / D \rfloor \cdot 2^{32} + \lfloor ((N_H \bmod D) \cdot 2^{32} + N_L) / D \rfloor$。證明此恆等式成立，並說明為何第二次除法的被除數 $(N_H \bmod D) \cdot 2^{32} + N_L$ 保證不超過 $D \cdot 2^{32} - 1$，使得商能以 32 位元表示。進一步探討以 Newton-Raphson reciprocal approximation 加速除法的可能性：推導 Newton-Raphson 迭代 $x_{n+1} = x_n (2 - D \cdot x_n)$ 如何以乘法逼近 $1/D$，每次迭代將精度位元數翻倍

## 細讀〈[並行程式設計: 排程器原理](https://hackmd.io/@sysprog/concurrency-sched)〉
* 從 coroutine 出發逐步建構排程器的設計原理：以 `setjmp`/`longjmp` 與 `ucontext` 實作使用者空間 context switch。作業一分析 fork-join 模型的 DAG 表示與 Amdahl's law 的關係，以及 `int *foo(void) { int x = 10; return &x; }` 的未定義行為與 storage duration。以此為出發點：
    * (a) C99 §7.13.2.1 規定 `longjmp` 後，自動儲存期 (auto storage duration) 且未宣告為 `volatile` 的區域變數，若在 `setjmp` 與 `longjmp` 之間被修改，其值 indeterminate。撰寫測試程式在 `-O0` 與 `-O2` 下驗證此行為差異 (提示: 編譯器可能將區域變數快取於暫存器，`longjmp` 恢復暫存器後其值回到 `setjmp` 時的狀態)。解釋 Linux 核心為何以 `switch_to()` 巨集 (定義於 `arch/x86/include/asm/switch_to.h`) 而非 `setjmp`/`longjmp` 實作 context switch，因為核心需要精確控制 FPU 狀態、TLS (`fs` 段暫存器)、per-CPU 變數、以及 stack canary 的切換，`setjmp` 僅儲存 callee-saved registers，無法涵蓋這些需求
    * (b) 閱讀 `arch/x86/include/asm/switch_to.h` 的 `__switch_to_asm` 與 [`arch/x86/kernel/process_64.c`](https://github.com/torvalds/linux/blob/master/arch/x86/kernel/process_64.c) 的 `__switch_to()`，列出 context switch 過程中依序切換的所有 CPU 狀態 (sp、ip、FPU、segment registers、per-CPU 基底位址、debug registers)，並估算每項切換操作的 cycles 成本
* [Google 的 ghOSt 框架](https://research.google/pubs/ghost-fast-and-flexible-user-space-delegation-of-linux-scheduling/)將 CPU 排程決策從核心模式移至使用者空間。作業一提到若將 VFS 或 network stack 遷移至 userspace 時的 context switch 數量變化、cache locality、fault isolation 與 worst-case latency。將此分析框架套用至 ghOSt：
    * (a) ghOSt 的使用者空間 CPU 排程器透過 eBPF hook 與共享記憶體佇列 (status word) 與核心互動，每次排程決策需要至少一次核心→使用者空間→核心的往返。以作業一的延遲模型為基礎，推導 ghOSt 的排程延遲下界 $T_{ghost} \geq T_{ctx} \cdot 2 + T_{decision}$，其中 $T_{ctx}$ 為單次 context switch 成本、$T_{decision}$ 為使用者空間排程策略的計算時間，並分析在 $T_{decision}$ 極小時，此額外延遲是否仍可容忍
    * (b) 作業二分析 PELT 使用 EWMA 並以 `mul_u64_u32_shr()` 完成定點數乘法。從 Linux v0.01 的 150ms timeslice round-robin 到 CFS 的 `vruntime` 再到 EEVDF 的 eligible/deadline 計算，追蹤排程器精度需求的演進。閱讀 [`kernel/sched/fair.c`](https://github.com/torvalds/linux/blob/master/kernel/sched/fair.c) 中 EEVDF 的 `pick_eevdf()` 與 `entity_eligible()`，以作業一探討的 lag 有界性證明 ($\sum_i \text{Lag}_i(t) = 0$) 為基礎，說明 EEVDF 如何以 deadline 排序取代 CFS 的純 `vruntime` 排序來改善 tail latency
* CFS 的 `vruntime` 以 `u64` 奈秒計數器記錄每個排程實體的虛擬執行時間。分析 `vruntime` wraparound 問題：$2^{64}$ 奈秒約為 $2^{64} / (10^9 \times 3600 \times 24 \times 365.25) \approx 584.5$ 年，實務上不會溢位，但排程器內部仍以帶號差值比較 `vruntime`。閱讀 [`kernel/sched/fair.c`](https://github.com/torvalds/linux/blob/master/kernel/sched/fair.c) 的 `min_vruntime()` 與 `max_vruntime()`，說明其如何以 `(s64)(vruntime - min_vruntime) < 0` 的帶號比較處理潛在的 wraparound。注意當前 mainline 的 `entity_before()` 已改為比較 EEVDF 的 `deadline` 而非 `vruntime`，但 `vruntime` 的帶號差值比較仍存在於 `min_vruntime()` 等輔助函式中。此技巧的數學基礎在於二補數減法的 modular arithmetic 性質：只要任意二個 `vruntime` 的差距不超過 $2^{63}$，帶號比較即能正確判定大小關係。證明此不變量在正常排程運作下成立 (提示：`min_vruntime` 持續推進，所有就緒態行程的 `vruntime` 與 `min_vruntime` 的差距受權重比與排程週期約束，遠小於 $2^{63}$)。進一步追蹤 `entity_before()` 在 EEVDF 中如何以相同的帶號比較技巧作用於 `deadline` 欄位，並分析 `avg_vruntime()` → `update_entity_lag()` → `entity_eligible()` → `pick_eevdf()` 的完整呼叫鏈

## 細讀〈[C 語言: 函式呼叫](https://hackmd.io/@sysprog/c-function)〉
* System V AMD64 ABI 的 calling convention 與 stack frame 配置。作業一分析 `int *foo(void) { int x = 10; return &x; }` 的未定義行為、`void f(int a[10])` 與 `void f(int *a)` 的 ABI 差異，以及 call-by-value 的機制。以此為出發點：
    * (a) 函式 prologue (`push rbp; mov rbp, rsp; sub rsp, N`) 建立 stack frame。在 Linux 核心中，`CONFIG_FRAME_POINTER` 啟用時 GCC 以 `-fno-omit-frame-pointer` 保留 frame pointer chain，但此選項增加暫存器壓力 (x86-64 損失 `rbp`)。核心自 v4.14 引入 ORC unwinder (`CONFIG_UNWINDER_ORC`)，以編譯期產生的 `.orc_unwind` section 取代執行期 frame pointer chain。閱讀 [`scripts/orc/`](https://github.com/torvalds/linux/tree/master/scripts) 的 ORC 產生工具與 [`arch/x86/kernel/unwind_orc.c`](https://github.com/torvalds/linux/blob/master/arch/x86/kernel/unwind_orc.c) 的 unwinder 實作，說明 ORC 如何以查表 (每個指令位址對應一組 sp/fp 偏移) 取代 frame pointer traversal，並從 git log 找出 ORC 引入的 commit 以了解其在核心 profiling (`perf record`) 中的精確度改善
    * (b) Linux 核心的系統呼叫以 `struct pt_regs` 傳遞暫存器狀態。閱讀 [`arch/x86/entry/entry_64.S`](https://github.com/torvalds/linux/blob/master/arch/x86/entry/entry_64.S) 的 `entry_SYSCALL_64`，追蹤使用者空間的 `rdi`, `rsi`, `rdx`, `r10`, `r8`, `r9` 如何被儲存至 `pt_regs` 結構體，以及 `SYSCALL_DEFINE` 巨集 (定義於 [`include/linux/syscalls.h`](https://github.com/torvalds/linux/blob/master/include/linux/syscalls.h)) 如何展開為系統呼叫的進入點，以及 x86 架構特有的 `pt_regs` wrapper (定義於 `arch/x86/include/asm/syscall_wrapper.h`) 如何從 `struct pt_regs` 擷取參數並轉交給泛型的系統呼叫函式。注意 x86-64 的 syscall ABI 使用 `r10` 而非 `rcx` 作為第四個參數 (因為 `syscall` 指令以 `rcx` 儲存返回位址)，此差異如何反映在 `pt_regs` 的欄位順序中
* `setjmp`/`longjmp` 可跨越多個函式邊界執行非區域跳躍。作業一分析 strict aliasing rule 與 type punning 的安全性。在 Linux 核心中，`setjmp` 的角色被 `switch_to()` + `schedule()` 取代，但核心的 kprobes 機制 ([`kernel/kprobes.c`](https://github.com/torvalds/linux/blob/master/kernel/kprobes.c)) 以 `setjmp`-like 的方式儲存暫存器狀態以實現動態追蹤。閱讀 `arch/x86/kernel/kprobes/core.c` 的 `kprobe_int3_handler()`，說明其如何儲存 `pt_regs` 並在探測點觸發 callback 後恢復原始執行流程。對比 `setjmp`/`longjmp` 僅儲存 callee-saved registers，kprobes 需要完整的 `pt_regs` 快照。從 `perf probe` 的角度，設計實驗以 kprobes 追蹤 `vfs_read()` 的呼叫次數與參數值

## 細讀〈[C 語言: 前置處理器應用](https://hackmd.io/@sysprog/c-preprocessor)〉
* C 前置處理器的 stringification、token pasting、`_Generic`，以及 Linux 核心中巨集的大量應用。作業二分析 `BIT(N)`/`GENMASK(h, l)` 如何避免有號位移的未定義行為、`BUILD_BUG_ON_ZERO` 的位元欄位技巧，以及 `container_of` 的 object model 假設。以此為出發點：
    * (a) `__stringify(x)` 巨集需要兩層展開 (`#define __stringify_1(x...) #x` + `#define __stringify(x...) __stringify_1(x)`)，原因在於 C 語言規格要求 `#` 運算子在參數替換之前執行 stringification，因此若只有一層，巨集參數不會被展開。撰寫測試程式驗證此行為 (`#define FOO 42` 後 `__stringify(FOO)` 應產生 `"42"` 而非 `"FOO"`)，並從 C99 §6.10.3.2 引述規範性文字
    * (b) 閱讀 Linux 核心 v6.x 中重新設計的 [`include/linux/minmax.h`](https://github.com/torvalds/linux/blob/master/include/linux/minmax.h)，追蹤 `__types_ok()` 如何以 `__builtin_choose_expr` 與 `__is_constexpr()` 在編譯期偵測 signed/unsigned 混合比較，此設計直接呼應作業二分析的 signed/unsigned 隱式轉型陷阱 (CWE-195)。從 git log 找出此巨集重新設計的 commit (提示: 2024 年 Linus Torvalds 親自重寫 `min()`/`max()`)，分析舊版 `min_t()` 強制轉型可能吞噬的 warning
* 以巨集實現物件導向設計模式。作業一探討 Linux 核心的 VFS 與 network stack 如何以抽象層支撐演化。從 VFS 層出發：`struct file_operations` 以函式指標模擬 vtable，各檔案系統以 designated initializer (`.read = ext4_file_read_iter`) 填入實作。閱讀 [`fs/ext4/file.c`](https://github.com/torvalds/linux/blob/master/fs/ext4/file.c) 的 `ext4_file_operations` 定義，追蹤 `vfs_read()` 如何透過 `f->f_op->read_iter` 間接呼叫。此模式等效於 C++ 的虛擬函式分派 (virtual dispatch)，但以 C 語言的前置處理器與結構體手動實現。設計實驗：撰寫核心模組 (或使用者空間模擬)，以函式指標表實現兩種不同的「檔案系統」讀取行為，以 `perf stat -e branch-misses` 量測間接呼叫 (`f->f_op->read`) 的 branch prediction 命中率與直接呼叫的差異

## 細讀〈[C 語言: goto 和流程控制](https://hackmd.io/@sysprog/c-control-flow)〉
* `goto` 在 Linux 核心中的合理使用，主要用於集中式錯誤處理與資源釋放。作業一分析 `free(ptr)` 後指標值變為 indeterminate 的 UB，以及物件生命週期結束後解參考指標的未定義行為。以此為出發點：
    * (a) Linux 核心的驅動程式典型 `goto` 模式：`goto err_free_irq; ... err_free_irq: free_irq(irq, dev); err_free_mem: kfree(dev);` 以反向順序釋放資源。此模式的正確性依賴標籤的嚴格反向排列，若開發者在 `err_free_irq` 後意外跳至 `err_free_mem` 之前的位置 (遺漏一層釋放)，會造成記憶體洩漏。從 git log 搜尋 `goto` 相關的 resource leak 修正 (提示: `drivers/` 下以 "fix leak" 與 "goto" 為關鍵字)，找出至少二個實際案例，分析錯誤模式並說明 Coccinelle semantic patch (`scripts/coccinelle/free/`) 如何自動偵測此類缺陷
    * (b) Linux 核心自 v6.x 引入的 `guard()` 巨集 (定義於 [`include/linux/cleanup.h`](https://github.com/torvalds/linux/blob/master/include/linux/cleanup.h)) 以 `__attribute__((cleanup))` 實現 scope-based 鎖釋放，可取代 `goto err_unlock` 模式。閱讀 `cleanup.h` 的 `DEFINE_GUARD()` 展開式，說明其如何在變數離開作用域時自動呼叫 `mutex_unlock()`，以及此設計在 C 語言 (而非 C++) 中的侷限，因為 C 沒有析構子語意，`__attribute__((cleanup))` 是 GCC extension
* computed goto (GCC `&&label` 擴充) 與 Duff's device。作業二分析 SWAR 技巧中的 loop unrolling 與 branchless 設計。以此為出發點：
    * (a) Linux 核心的 BPF 直譯器 ([`kernel/bpf/core.c`](https://github.com/torvalds/linux/blob/master/kernel/bpf/core.c)) 使用 computed goto 實作 dispatch table，每個 BPF opcode 對應一個 `&&label`，直譯器以 `goto *jumptable[opcode]` 分派。相較於 `switch-case`，computed goto 避免集中式跳轉表查詢，每個 opcode handler 的結尾直接 `goto *jumptable[next_op]`，使分支預測器對每個 handler→handler 的轉移建立獨立的預測紀錄。閱讀 `___bpf_prog_run()` 的 dispatch 邏輯 (搜尋 `CONT` 或 `goto select_insn` 等控制流巨集)，說明其展開後的控制流程。設計實驗：撰寫使用者空間的簡易 bytecode 直譯器，分別以 `switch-case` 與 computed goto 實作 dispatch，以 `perf stat -e branch-misses` 量測 1M 次 dispatch 的 branch miss rate 差異
    * (b) Simon Tatham 的 `switch-case` coroutine 技巧，本質上是 stackless coroutine 的手動實作。C 語言規格允許 `case` 標籤出現在 `switch` 內任何子語句中 (包含 `while` 或 `for` 迴圈內)。從 Linux 核心找出使用此技巧或類似手法的非同步 I/O 路徑 (提示: `fs/cifs/connect.c` 的 `cifs_demultiplex_thread` 或 `drivers/` 下的 state machine)，分析其如何跨越函式呼叫保存狀態

## 細讀〈[C 語言程式設計技巧](https://hackmd.io/@sysprog/c-trick)〉
* 以 C 語言實現 OOP、`__attribute__((cleanup))` 的 RAII 模式、designated initializer，以及 `container_of`，這些技巧在 Linux 核心中隨處可見。作業二分析 `container_of` 的 object model 依賴，以及 `typeof`、`offsetof` 在核心中的角色。以此為出發點：
    * (a) Linux 核心的裝置模型以「繼承式結構體」搭配 `container_of` 實現多型，例如 `struct pci_dev` 内嵌 `struct device`，`struct device` 内嵌 `struct kobject`。閱讀 [`drivers/base/core.c`](https://github.com/torvalds/linux/blob/master/drivers/base/core.c) 的 `device_release()`，追蹤 `kobject_put()` 如何透過 `kobj->ktype->release` 間接呼叫上層結構體的釋放函式，此呼叫路徑需要從 `kobject *` 反向取得 `struct device *` (經由 `container_of`)，再從 `struct device *` 取得 `struct pci_dev *`。繪製記憶體布局圖說明 `container_of` 的指標算術，並與 C++ 的多重繼承 vptr 機制在指標調整上進行對比
    * (b) `__attribute__((cleanup))` 實現 RAII。閱讀 [`include/linux/cleanup.h`](https://github.com/torvalds/linux/blob/master/include/linux/cleanup.h) 的 `__free()` 巨集以及 `guard(mutex)` 的展開式，設計實驗：在核心模組中分別以傳統 `goto err_unlock` 與 `guard(mutex)` 實現臨界區保護，比較二者的組合語言輸出，觀察 `guard()` 是否引入額外的 function call overhead (cleanup handler)？在 hot path 上此開銷是否可量測？
* 匿名結構體/union 在型別設計中的應用。作業一探討 Linux 核心的 abstraction preservation。閱讀 [`include/linux/skbuff.h`](https://github.com/torvalds/linux/blob/master/include/linux/skbuff.h) 的 `struct sk_buff`，找出其匿名 union 如何讓同一記憶體區域在不同網路層 (L2/L3/L4) 提供不同的 header 存取介面 (如 `skb->protocol` vs. `ip_hdr(skb)->saddr`)。以 `pahole` 工具分析 `struct sk_buff` 的完整記憶體布局，計算其 padding 浪費與 cache line 佔用情況，並從 git log 找出近年縮減 `sk_buff` 大小的 commit

## 細讀〈[Linux 核心的紅黑樹](https://hackmd.io/@sysprog/linux-rbtree)〉
* `rb_node` 結構與紅黑樹的實作細節。作業一探討 linked list traversal 的 cache locality 問題，作業二分析 hlist 的 `pprev` pointer tagging 設計。以此為出發點：
    * (a) `rb_node` 將 parent pointer 與 color bit 打包在 `unsigned long __rb_parent_color` 中，利用 `struct rb_node` 的 alignment 保證最低位元為零。作業二分析此 pointer tagging 技巧在紅黑樹中的應用。延伸證明：設 `struct rb_node` 包含至少一個指標成員，故在 64 位元架構上 `sizeof(struct rb_node) >= 8`，`alignof(struct rb_node) >= 8`。從 C11 §6.2.8 的 alignment 規則出發，證明任何 `rb_node *` 的值 modulo 8 必為 0，因此低 3 位元皆可安全使用 (核心實際只使用 bit 0 存放顏色)。若某假想架構以 `packed` 屬性將 `rb_node` 壓縮至 1-byte alignment，此技巧如何失效？以 `__attribute__((packed))` 撰寫測試程式驗證
    * (b) 作業一分析 linked list 的 O(1) 插入在實際硬體上可能比陣列慢 (cache 效應)。將此分析延伸至樹狀結構：紅黑樹的每次查詢沿路徑走訪 $O(\log n)$ 個節點，每個節點可能不在同一 cache line。Linux 核心在 VMA 管理中以 [Maple Tree](https://docs.kernel.org/core-api/maple_tree.html) 取代紅黑樹。Maple Tree 以 B-tree 風格將多個 entry 打包在單一節點 (每個 node 佔一至二個 cache line)，大幅提升 cache locality。從 git log 找出 Maple Tree 取代 rbtree 的 commit series (提示: 2022 年 Liam Howlett 的 patchset)，閱讀 [`include/linux/maple_tree.h`](https://github.com/torvalds/linux/blob/master/include/linux/maple_tree.h) 的 `struct maple_node`，分析其 slot 數量如何對應 cache line 大小。設計實驗：以使用者空間實作簡化版的 rbtree 與 B-tree (fan-out = 16)，以隨機查詢 $10^6$ 個元素的 latency 分布 (以 `perf stat -e cache-misses` 量測) 驗證 cache 行為差異
* 作業二分析 `hlist_head`/`hlist_node` 的 `pprev` 設計如何消除刪除首節點的特殊情況，正如 Linus Torvalds 所強調的 "good taste"。閱讀 `lib/rbtree.c` 的 `__rb_erase_augmented()`，分析紅黑樹刪除後的平衡修復 (`____rb_erase_color`) 中是否仍存在無法消除的特殊情況。紅黑樹的修復需區分四種 case (兄弟節點為紅/黑、侄子節點的顏色組合)，且左右子樹對稱，核心以 `__rb_rotate_set_parents()` 統一處理旋轉以減少重複程式碼。分析此設計是否達到「消除特殊情況」的目標，或只是將特殊情況以對稱性壓縮
* Linux 核心的 augmented rbtree 機制用於 interval tree ([`include/linux/interval_tree.h`](https://github.com/torvalds/linux/blob/master/include/linux/interval_tree.h))。在標準紅黑樹中，查詢「所有與 $[lo, hi]$ 重疊的區間」需走訪全部 $n$ 個節點 ($O(n)$)。interval tree 在每個節點額外維護 `__subtree_last` 欄位，記錄該子樹中所有區間右端點的最大值。閱讀 [`include/linux/interval_tree_generic.h`](https://github.com/torvalds/linux/blob/master/include/linux/interval_tree_generic.h) 的 `INTERVAL_TREE_DEFINE` 巨集，追蹤 `interval_tree_iter_first()` 與 `interval_tree_iter_next()` 的查詢邏輯：當節點的 `__subtree_last < lo` 時，整棵子樹可被剪枝。分析此剪枝如何將查詢時間從 $O(n)$ 降至 $O(\log n + k)$，其中 $k$ 為實際重疊的區間數。推導此複雜度界限的數學證明 (提示：在平衡樹上，每層至多走訪常數個不含結果的節點 (因為 `__subtree_last` 的傳播保證若左子樹無結果則可跳過)。從 `mm/interval_tree.c` 找出此資料結構在 VMA 管理中的應用場景 (如 `anon_vma_interval_tree` 用於 reverse mapping)

## 細讀〈[C 編譯器原理和案例分析](https://hackmd.io/@sysprog/c-compiler-construction)〉
* AMaCC (不到 2000 行的自我編譯 C 編譯器) 為案例，涵蓋 lexer、parser、中間表示、以及 ARM 程式碼產生。作業二分析 GCC 的 `-fstrict-aliasing`/`-fno-strict-overflow` 如何影響編譯結果，以及 UBSan 的位移檢查。以此為出發點：
    * (a) AMaCC 這類簡易編譯器不進行 type-based alias analysis 或 value range propagation，因此不會因 UB 產生令人意外的最佳化，UB exploitation 是 SSA-based 最佳化 (如 GCC 的 tree-ssa 與 LLVM 的 InstCombine) 的產物。設計一段 C 程式碼包含有號溢位 UB (`int x = INT_MAX; x + 1`)，分別以 AMaCC (或其他簡易編譯器如 `tcc`) 與 GCC `-O2` 編譯執行，觀察行為差異，並從 compiler theory 的角度解釋為何 SSA 的 value numbering 與 range propagation 是觸發 UB exploitation 的必要條件
    * (b) Linux 核心的 eBPF JIT ([`arch/x86/net/bpf_jit_comp.c`](https://github.com/torvalds/linux/blob/master/arch/x86/net/bpf_jit_comp.c)) 將 BPF bytecode 轉譯為原生 x86-64 指令，屬於三種執行模型中的 JIT 路徑。閱讀 `do_jit()` 的翻譯迴圈，追蹤 `BPF_ALU64_REG(BPF_ADD, ...)` 如何映射至 x86 `add` 指令。與 AMaCC 的 codegen 比較：AMaCC 從 AST 直接產生機械碼，eBPF JIT 從已驗證的 bytecode 翻譯，後者的安全性來自 verifier 的前置靜態檢查。從 Spectre v1 防禦的角度，說明 eBPF JIT 如何在條件分支後插入 `lfence` 或以 array index masking 防止推測執行越界存取 (提示: 搜尋 `opt_hard_wire_dead_code_branches` 與 `fixup_bpf_calls`)
* 符號表與 ELF 重定位。作業二探討 CRC 計算的 $\text{GF}(2)$ 多項式運算。Linux 核心模組 (`.ko`) 以 ELF relocatable object 的形式存在，`insmod` 時由 [`kernel/module/main.c`](https://github.com/torvalds/linux/blob/master/kernel/module/main.c) 的模組載入器執行重定位。閱讀 `apply_relocate_add()` (架構相關，如 `arch/x86/kernel/module.c`) 的重定位邏輯，說明 `R_X86_64_PC32` 與 `R_X86_64_PLT32` 重定位型別的計算方式。`CONFIG_MODVERSIONS` 以 `genksyms` 工具為每個 exported symbol 計算 CRC 校驗碼 (儲存於 `__versions` section)，模組載入時核心比對此 CRC 確保 ABI 相容。從 `scripts/genksyms/` 的原始碼追蹤 CRC 的計算方法，說明其與作業二分析的 CRC 多項式運算的關係，以及為何 struct layout 變更會改變 CRC 值

## 細讀〈[C 語言: 未定義行為](https://hackmd.io/@sysprog/c-compiler-optimization)〉
* 現代編譯器利用 UB 進行激進最佳化。作業二深入分析 strict aliasing (C99 6.5 §7)、有號位移溢位 (C99 6.5.7 §4)、以及 `-fno-strict-aliasing`/`-fno-strict-overflow` 在核心中的必要性。以此為出發點：
    * (a) C99 引入的 `restrict` 關鍵字告知編譯器二個指標不重疊，允許更激進的最佳化 (如向量化)。Linux 核心極少使用 `restrict`。閱讀 `lib/string.c` 的 `memcpy()` 與 `memmove()` 實作，說明兩者的語意差異 (前者假設不重疊、後者處理重疊)。在核心語境下，若函式簽名加上 `restrict` 但呼叫端意外傳入重疊指標，行為為 UB，編譯器可能假定不重疊而省略安全的反向複製路徑。以 GCC `-O2 -ftree-vectorize` 編譯一段含 `restrict` 的 `memcpy` 替代品，觀察是否產生 SIMD 指令，並對比不含 `restrict` 時的差異
    * (b) 核心的 [`include/linux/compiler.h`](https://github.com/torvalds/linux/blob/master/include/linux/compiler.h) 以 `__builtin_unreachable()` 標記不應到達的路徑 (如 `switch` 的 `default` case)。閱讀 `BUG()` 巨集的展開式：在 `CONFIG_BUG` 啟用時觸發 `ud2` (x86 非法指令)，停用時退化為 `unreachable()`。設計程式碼展示 `unreachable()` 的危險：若標記實際可到達的路徑，GCC 會省略後續所有程式碼 (dead code elimination)，導致控制流落入相鄰函式的機械碼中。以 `objdump -d` 驗證此行為
* SSA 形式在常數傳播與死碼消除中扮演關鍵角色。作業二的 `int_size_is_w` 函式展示有號位移 UB 如何導致條件分支被消除。設計一組最小化 C 程式碼 (每段不超過 10 行)，展示 GCC `-O2` 下至少三種不同類型的 UB exploitation：
    * (a) 有號溢位，`if (x + 1 > x)` 被最佳化為 `if (true)`
    * (b) 空指標解參考，`int *p = ...; int val = *p; if (p == NULL) { /* 此分支被消除 */ }`
    * \(c) 位移超出範圍，`1 << 32` 在 32 位元 `int` 上。對每段程式碼以 `gcc -O2 -S` 產生組合語言，標示被消除或改變的指令，並對照 C99 規格書中對應的條款 (6.5 §5 有號溢位、6.5.3.2 §4 空指標解參考、6.5.7 §3 位移範圍)。進一步分析：Linux 核心的 `-fno-strict-overflow` 與 `-fwrapv` 能防禦 (a) 但無法防禦 \(c)，只有 `BIT()` 巨集搭配 `unsigned long` 才是位移 UB 的正解

## 細讀〈[錯誤更正碼 (ECC) 介紹和實作考量](https://hackmd.io/@sysprog/linux-ecc)〉
* 從 Shannon 的資訊理論出發：Hamming code、BCH code、Reed-Solomon code 的數學基礎。作業一探討有限域 $\text{GF}(2^8)$ 與 AES 的關聯，作業二分析 CRC 在 $\text{GF}(2)$ 上的多項式除法與 SWAR 實作。以此為出發點：
    * (a) CRC 以 $\text{GF}(2)[x]$ 上的多項式模運算偵錯，Reed-Solomon 以 $\text{GF}(2^8)[x]$ 上的多項式糾錯。兩者的代數結構差異在於底層的 coefficient field：$\text{GF}(2)$ 只有 $\{0, 1\}$ 二個元素，運算極為簡單 (XOR/AND)；$\text{GF}(2^8)$ 有 256 個元素，乘法需要多項式乘法再模不可約多項式。閱讀 [`lib/reed_solomon/reed_solomon.c`](https://github.com/torvalds/linux/blob/master/lib/reed_solomon/reed_solomon.c) 的 `init_rs_gfp()` 與底層的 `init_rs_internal()`，追蹤其如何以 `rs->index_of[]` (log table) 與 `rs->alpha_to[]` (antilog table) 將乘法轉為加法 ($a \cdot b = \alpha^{\log_\alpha a + \log_\alpha b}$)，避免逐位元的多項式乘法。撰寫使用者空間程式以此查表法實作 $\text{GF}(2^8)$ 乘法，並驗證 $a \cdot a^{-1} = 1$ 對所有非零 $a$ 成立
    * (b) 作業一提到 `hweight_long()` (Hamming weight) 的次可加性 $\text{hw}(a \oplus b) \leq \text{hw}(a) + \text{hw}(b)$。Hamming distance $d(x, y) = \text{hw}(x \oplus y)$ 決定碼的錯誤偵測/更正能力：最小距離 $d_{min}$ 的碼可偵測 $d_{min} - 1$ 個錯誤、更正 $\lfloor (d_{min} - 1)/2 \rfloor$ 個錯誤。閱讀 `include/linux/bitops.h` 的 `hweight_long()` SWAR 實作 (作業二已分析 SWAR 原理)，設計實驗：以 `hweight_long()` 計算隨機 (7,4) Hamming code 字碼間的距離分布，驗證最小距離確為 3
* EDAC (Error Detection And Correction) 子系統用於監控硬體 ECC 記憶體錯誤。閱讀 [`drivers/edac/edac_mc.c`](https://github.com/torvalds/linux/blob/master/drivers/edac/edac_mc.c) 的 `edac_mc_handle_error()`，追蹤 correctable error (CE) 與 uncorrectable error (UE) 的計數與通報路徑 (經由 `edac_raw_mc_handle_error()` 累加至 `mci->ce_count`/`mci->ue_count`)。以作業一探討的機率模型為基礎：假設 CE 發生率為 $\lambda_{ce}$ (events/hour)，且 CE 為 UE 的前兆 (研究顯示出現 CE 的 DIMM 之 UE 機率增加 $10 \times$)，建立 DIMM 失效的連續時間 Markov 模型 (healthy → CE → UE 三態)，推導 UE 發生前的期望時間，並說明 Linux 的 `ras-daemon` 如何以 CE 頻率趨勢觸發預防性 DIMM 替換
* NAND flash 的 ECC 需求與 BCH 碼。Linux 核心的 `drivers/mtd/nand/` 子系統以 BCH (Bose-Chaudhuri-Hocquenghem) 碼保護 NAND flash 資料完整性。BCH 碼的糾錯能力 $t$ (可糾正的錯誤位元數) 與碼字長度 $n = 2^m - 1$ 及所需 parity 位元數 $r$ 之間滿足關係 $r \leq m \cdot t$。閱讀 [`lib/bch.c`](https://github.com/torvalds/linux/blob/master/lib/bch.c) 的 `bch_init()`，追蹤其如何依據使用者指定的 $m$ (Galois field order) 與 $t$ (糾錯強度) 建構生成多項式 $g(x)$。對於典型的 NAND flash 配置，如 512 位元組 (4096 位元) 資料頁面配 4-bit ECC ($m = 13, t = 4$)，計算所需的 parity 位元數 $r = m \cdot t = 52$ 位元 (7 位元組)，驗證 spare area 是否足夠容納。說明 BCH 碼的設計保證 (designed distance)：$t$-bit 糾錯碼的最小距離至少為 $d_{min} \geq 2t + 1$。此為 BCH bound，不同於適用所有線性碼的 Singleton bound $d \leq n - k + 1$。分別以 BCH bound 與 Singleton bound 計算上述 $m=13, t=4$ 配置的理論極限。進一步比較 BCH 與 Reed-Solomon 在 NAND flash 場景的取捨：BCH 以位元為單位糾錯、RS 以符號 (symbol) 為單位。當錯誤模式為隨機位元翻轉 (如 MLC/TLC NAND 的 retention error) 時，BCH 的效率較高；當錯誤為突發型 (burst error) 時，RS 的符號糾錯更具優勢

## 細讀〈[CS:APP 第 2 章](https://hackmd.io/@sysprog/CSAPP-ch2)〉
* CS:APP 第 2 章的核心概念：二進位表示、二補數、位元運算、浮點數。作業二以 CS:APP 習題為基礎設計五道核心題組 (位元組替換、位移 UB、寬乘法、半精度浮點轉換、位元級浮點除法)。以此為出發點：
    * (a) 選擇 CS:APP Practice Problem 2.32 (two's complement subtraction 的 `tsub_ok` 函式) 與 Practice Problem 2.49 (浮點可精確表示的最大整數)，仿照作業二的 Part 1/Part 2 格式，自行設計「Part 2: Linux 核心應用」的延伸題。Part 2 須以 Linux 核心原始程式碼中的實際案例為基礎 (提示：`include/linux/time.h` 或 `kernel/time/` 下的 `timespec64_sub()` 涉及二補數溢位處理 (當 nsec 相減為負時的借位邏輯)，`drivers/gpu/drm/amd/display/dc/dml/` 的色彩空間計算涉及浮點精度限制)
    * (b) signed/unsigned 混合運算的隱式轉型陷阱。作業二已分析此議題在 `access_ok()` 與緩衝區溢位中的影響。綜合作業一至三的分析，從 Linux 核心 git log 找出至少三個因 signed/unsigned 混合運算而引入的漏洞 (參考 [CWE-195](https://cwe.mitre.org/data/definitions/195.html): Signed to Unsigned Conversion Error)，歸納共通模式，如使用者空間傳入的 signed 值在未檢驗下直接與 unsigned 常數比較，並以 `include/linux/overflow.h` 的 `check_add_overflow()` 為例，提出系統性的防禦策略
* 作業二已實作 `float32_to_float16` 的完整轉換邏輯。從 Linux 核心的 [`include/uapi/drm/drm_fourcc.h`](https://github.com/torvalds/linux/blob/master/include/uapi/drm/drm_fourcc.h) 找出 fp16 像素格式的定義 (如 `DRM_FORMAT_XRGB16161616F`)。GPU 驅動程式在禁止浮點運算的核心環境中以純整數位元操作處理 fp16 色彩值。閱讀 [`drivers/gpu/drm/amd/display/dc/dml/dcn20/display_mode_vba_20.c`](https://github.com/torvalds/linux/blob/master/drivers/gpu/drm/amd/display/dc/dml/dcn20/display_mode_vba_20.c) 的定點數運算範例。設計一個 fp16 → 8-bit sRGB 的純整數轉換函式：
    * (a) 先以位元操作擷取 sign/exponent/fraction (如同作業二的 `float32_to_float16` 的反向操作)
    * (b) 以定點數乘法實現 $\gamma$ correction ($\approx x^{1/2.2}$，可用查表或二次多項式近似)
    * \(c) 以 round-to-even 捨入至 8 位元。撰寫驗證程式以所有 65536 個 fp16 數值窮舉測試，比較與使用者空間 `float` 計算結果的差異

## 回顧第四和第五週測驗
針對「Linux 核心設計」[第 4 週測驗題](https://hackmd.io/@sysprog/linux2026-quiz4)和[第 5 週測驗題](https://hackmd.io/@sysprog/linux2026-quiz5)，檢視自身的認知並充分回答所有延伸問題。

## :penguin: 作業要求
* [HackMD](https://hackmd.io/) 筆記作為開發紀錄，必須嚴格依循上方的「筆記書寫規範」，且符合如下:
	* 標題格式固定為 ==2026q1 Homework2 (basics)==，其中 "basics" 是小寫，**2026q1** 表示「2026 年第 1 季」
	* 共筆內容的第二行則為 **contributed by < `你的GitHub帳號名稱` >**，務必確保你的 GitHub 帳號是有效的
	* 共筆內容的第三行僅留換行符號，第四行是 ==`{%hackmd NrmQUGbRQWemgwPfhzXj6g %}`== 並確保「作業書寫規範」正確顯示
* 課程助教預計在 3 月 27 日，針對每位選課的學員，從 ==[Homework2 作業區](https://hackmd.io/@sysprog/linux2026-homework2)== 挑出 5 位學員，逐一發信通知，若你在 3 月 28 日中午尚未收到如此的信件，請聯繫授課教師，當然若你願意額外評論其他同學，也歡迎。針對其他學員的開發紀錄，請編輯內文，加上 `Reviewed by 你的GitHub帳號名稱` 的段落，參見: [示範的 Review-1](https://hackmd.io/@r36EKfH2TwalEWG_fUuSyg/linux2024-homework1) 和 [示範的 Review-2](https://hackmd.io/@jason50123/linux2024-homework1)，你的總結意見要寫在共筆的最上方，僅次於 "contributed by"。要從以下方面探討:
    - 回覆給定題目的完整程度、是否參照權威材料去解讀和推理、是否設計實驗去驗證、論述和後續討論，落實上述 "Code Review" 提出的原則
	- 實驗設計的不足處、涵蓋程度是否全面，以及後續的改進空間
	- 共筆行文是否流暢且具體，結構規劃是否清晰，且以第一手材料為主要依循，並細緻驗證 $\to$ 台大電機系李宏毅教授對於 ChatGPT 的看法是，要善用人工智慧的成果，一旦人們得以善用，人類的書寫不該比 GPT 一類的大語言模型差。
	- 斟酌在選定的 GitHub repository 留下 code review 意見。
	- 嘗試回覆學員提出的問題。
	    > :information_source: 及早提交對學員的意見並藉由 HackMD 平台互動
	    > :warning: 不必擔心得罪人而刻意用委婉或模糊的詞彙，如此非但不利於有效溝通，還可能導致真正的訊息丟失。關鍵是不要過分拘謹於形式，若因你沒有直接說出問題，導致他人錯失學習機會，那才是真正的失禮 —— **真誠地分享你的專業知識，讓溝通能夠達到共鳴，才是真正展現禮貌的方式**。
* 應適時回應授課教師和其他同學在你羅列於 [Homework2 作業區](https://hackmd.io/@sysprog/linux2026-homework2) 的共筆中所做的評語意見、建議，和提問。你可趁這個機會，在其他學員的共筆提交相關疑惑
* 填寫 [Google 表單](https://forms.gle/AJELh8SgxFUeKPom6)，填入個人資訊和你建立的 HackMD 筆記的超連結，並回答指定問題。一旦系統確認你的提交內容，你的作業預期會出現「[作業區](https://hackmd.io/@sysprog/linux2026-homework3)」
    > :warning: 不用等到作業完成才填寫表單，當你開始進行作業時，即可填寫表單，系統會進行必要的檢查工作。某些問題的回答較費時，務必及早開始
* 本課程鼓勵學員相互觀摩，從而進行良性互動及批評，但要注意以下:
    * 當你參照其他學員作業的材料時，應該指明出處並加上對應的超連結
    * 善用 HackMD 的留言功能，在其他學員的筆記內文，留下你的想法、指出錯誤，和提及你對此的改進等等
* 截止日期：
    * Apr 18, 2026 25:59 (含) 之前