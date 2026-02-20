# 2025 年 Linux 核心設計課程作業 —— kxo

> **原始出處：** <https://hackmd.io/@sysprog/linux2025-kxo>
> **子頁面：** kxo-a ~ kxo-f
> **擷取日期：** 2026-02-20
> **用途：** 課程作業 kxo 規格（2025 版，待更新為 2026）
> **主題：** 透過井字棋遊戲熟悉數值系統與核心程式設計
> **涵蓋度：** 摘要（約 5%）
> **省略內容：** Part A 核心模組開發環境設定、Part B 井字遊戲核心模組完整程式碼、Part C 並行處理與同步機制、Part D 資訊理論與 entropy 分析、Part E PRNG 實作與測試、Part F 完整繳交規格

---

## 概述

透過修改井字棋（Tic-Tac-Toe）遊戲，學習定點數運算、Linux kernel module 開發、並行處理、資訊理論與亂數產生器。最終目標是實作一個在 kernel space 運行的對奕模組，使用 MCTS 與 Negamax 等 AI 演算法。

**Repository：** <https://github.com/jserv/ttt>（user-space 版本）

---

## Part A：預期目標 + 定點數運算

> 原始出處：<https://hackmd.io/@sysprog/linux2025-kxo-a>

### 預期學習成果

- 透過實作學習定點數運算、位元運算、排程原理與 kernel 開發介面
- 了解經典 AI 概念（Negamax、RL、MCTS、TD Learning）

### 為何 Kernel 不用浮點數

- Kernel 無法無縫支援浮點數，需手動管理 FPU 暫存器
- CVE-2018-3665：Lazy FPU State 漏洞，利用 speculative execution 洩漏 FPU 暫存器中的加密金鑰
- 解決方案：使用**定點數運算**（fixed-point arithmetic）

### 定點數運算

- **Qm.f 表示法：** 如 Q23.8 使用 23-bit 整數 + 8-bit 小數
- 加減法：直接整數運算
- 乘法：結果右移 fractional bits
- 除法：被除數先左移再除

### Linux Load Average

- 每 5 秒以指數平滑計算 1/5/15 分鐘負載
- 公式：$\text{load}_t = n \times \alpha + (1-\alpha) \times \text{load}_{t-1}$
- `fixed_power_int()` 以 O(log n) 計算 $x^n$
- 結果儲存於 `avenrun[]`，用 `LOAD_INT()` / `LOAD_FRAC()` 提取

### Monte Carlo Tree Search (MCTS)

四步驟迭代：
1. **Selection** — 用 UCT 公式選擇最高價值節點
2. **Expansion** — 產生未拜訪的子節點
3. **Simulation** — 隨機模擬至終局
4. **Backpropagation** — 更新祖先統計

UCT 公式：$\frac{w_i}{n_i} + c\sqrt{\frac{\ln(N_i)}{n_i}}$（$c$ 通常取 $\sqrt{2}$）

### 定點數實作

- **整數開平方根：** 使用 quadratic residue 測試
- **對數：** 透過 Taylor 級數與二分搜尋逼近

---

## Part B：Linux Kernel Modules（ksort 範例）

> 原始出處：<https://hackmd.io/@sysprog/linux2025-kxo-b>

### 開發環境

- Kernel ≥ 5.15.0，Secure Boot 須關閉
- 套件：`linux-headers`, `util-linux`, `strace`, `gnuplot-nox`
- 不可用 root 帳號開發，使用 `sudo`

### ksort 字元裝置驅動

- 使用者透過 `/dev/sort` 與 kernel module 互動
- `open()` → `write()`（傳入未排序資料）→ `read()`（取回已排序資料）
- Kernel 端用 `copy_from_user()` / `copy_to_user()` 搬移資料
- `copy_to_user()` 約 22 ns/byte 的額外開銷

### file_operations 結構

```c
static const struct file_operations fops = {
    .read = sort_read,
    .write = sort_write,
    .open = sort_open,
    .release = sort_release,
    .owner = THIS_MODULE,
};
```

### Kernel 計時機制

- **jiffies** — 中斷計數，適合 timeout（精度較低）
- **hrtimer** — 高解析度計時器（Linux 2.6.16+），奈秒精度
- **ktime_t** — `ktime_get()`, `ktime_sub()`, `ktime_to_ns()`

### 效能分析環境設定

- CPU affinity：`taskset` 綁定特定核心
- `isolcpus` kernel 參數隔離 CPU
- 關閉 ASLR：`echo 0 > /proc/sys/kernel/randomize_va_space`
- 固定 CPU 頻率為 performance mode
- 關閉 Turbo Boost 與 SMT/Hyper-Threading
- 統計離群值移除：Z-score 過濾法

---

## Part C：Linux Kernel 並行處理（simrupt）

> 原始出處：<https://hackmd.io/@sysprog/linux2025-kxo-c>

### 中斷處理架構

- **Top half**（即時，atomic context）：確認中斷來源、排程延遲工作
- **Bottom half**（延遲處理）：透過 softirq、tasklet、workqueue 執行

### Softirq

- 透過 `ksoftirqd` kernel thread 執行（每 CPU 一個）
- 10 種類型：HI, TIMER, NET_TX, NET_RX, BLOCK, IRQ_POLL, TASKLET, SCHED, HRTIMER, RCU
- 監控：`/proc/softirqs`

### Tasklet

- 建構於 softirq 之上，可動態配置
- 同一 tasklet 不會在不同 CPU 上同時執行
- 不同 tasklet 可在不同 CPU 上並行

### Workqueue

- 透過 kernel thread（worker thread）執行，可休眠、可被搶佔
- `queue_work()` 將 work item 排入 workqueue
- 與 tasklet 差異：workqueue 在 process context 執行

### KFIFO

- Kernel 的環形 FIFO 緩衝區
- Single Producer–Single Consumer 無需額外鎖
- `kfifo_in()` / `kfifo_out()` / `kfifo_alloc()` / `kfifo_free()`

### Fast Circular Buffer

- 大小為 2 的冪次，用 bitwise 操作取代模數運算
- `CIRC_CNT()`, `CIRC_SPACE()`, `CIRC_CNT_TO_END()`, `CIRC_SPACE_TO_END()`

### 記憶體屏障

- `READ_ONCE()` — 強制 atomic read
- `smp_rmb()` — 讀屏障，確保 index 讀取先於內容讀取
- `smp_wmb()` — 寫屏障，確保內容寫入先於指標更新

### simrupt 資料流

```
timer handler → process_data()（模擬中斷）
  → update_simrupt_data()（產生 ASCII 資料）
  → fast_buf_put()（寫入 circular buffer）
  → tasklet_schedule()（觸發 tasklet）
  → simrupt_tasklet_func()（排入 workqueue）
  → simrupt_work_func()（worker thread 執行）
  → fast_buf_get()（從 circular buffer 讀取）
  → produce_data()（寫入 kfifo）
  → userspace 從 /dev/simrupt 讀取
```

---

## Part D：對奕的核心模組

> 原始出處：<https://hackmd.io/@sysprog/linux2025-kxo-d>

### 模組架構

- 衍生自 simrupt，實作 MCTS 與 Negamax 兩種 AI 在不同 CPU 上對奕
- 遊戲邏輯完全在 kernel space 運行
- 透過 `/dev/kxo` 與 user space 互動

### 棋盤表示

- **字元陣列：** 空格 / 'O' / 'X'
- **位元編碼（最佳化）：** 每個位置用 32-bit nibble 編碼勝利條件
  - `move_masks[9] = {0x40040040, 0x20004000, ...}`
  - 勝利偵測：`(board + 0x11111111) & 0x88888888`

### Popcount 最佳化

- 從 naive O(k) 到 constant-time `popcount_branchless()`
- 使用 nibble 計算 + parallel summation + magic constant 乘法
- GCC 提供 `__builtin_popcount()` 內建函式

### Modulo-3 無除法

- 利用 $2^k \equiv (-1)^k \pmod{3}$ 性質
- 透過 popcount 實作，避免昂貴的除法指令

### sysfs 控制介面

- `DEVICE_ATTR_RW()` 暴露 kernel module 狀態
- 使用者可透過 sysfs 觸發 restart、pause、resume
- reader-writer lock 保護並行存取

### 同步挑戰

- 多 CPU 執行時 mutex + turn 變數不足
- 需使用 memory ordering（acquire/release semantics）確保跨 CPU 一致性

---

## Part E：資訊理論與亂數產生器

> 原始出處：<https://hackmd.io/@sysprog/linux2025-kxo-e>

### Shannon Entropy

- 資訊量：$-\lg(p(E))$，低機率事件攜帶更多資訊
- Shannon entropy：$H(X) = -\sum p^X(\eta) \cdot \lg(p^X(\eta))$
- 最大 entropy 出現在均勻分布

### Linear Feedback Shift Register (LFSR)

- **Fibonacci LFSR：** 反饋 taps 透過 XOR 控制最左位元
- **Galois LFSR：** 內部 XOR 操作
- Kernel 實作：`lib/random32.c`，使用 $x^{64} + x^{61} + x^{34} + x^9 + 1$

### Scrambled Linear Generators

- 結合線性引擎與非線性 scrambler
- **xoroshiro128+** 與 **xoshiro256** 系列
- xoshiro** 統計品質最佳（chi-square 信心度 88.75%）

### Fisher-Yates Shuffle 實驗

- 標準 `rand()/srand()` 的限制：RAND_MAX ≈ 32,767、LCG 可預測性
- 關鍵發現：每次 shuffle 前重新 seed 才能確保迭代間獨立性
- 用 chi-squared 檢定驗證均勻分布

---

## Part F：作業要求

> 原始出處：<https://hackmd.io/@sysprog/linux2025-kxo-f>

### 核心任務

1. **縮減 user-kernel 通訊成本**，允許並行對奕
2. **實作 coroutine**（非 POSIX thread）對應 AI₁、AI₂ 與鍵盤事件
3. **多局顯示：** 持續觀看電腦對電腦
   - Ctrl-P：暫停/恢復顯示（計算不停）
   - Ctrl-Q：退出
4. **負載機制：** 類似 Linux load average，用定點數量測 AI 排程負載
5. **即時顯示：** 持續更新的時間顯示（含秒數）
6. **User-space 算繪：** 將棋盤繪製從 kernel 移至 user space，用 bitops 最小化通訊
7. **強化學習：** 移植 jserv/ttt 的 RL 至 kernel module，支援動態切換
8. **開發紀錄：** 於 HackMD 提交

**截止日期：** 2025 年 4 月 11 日
