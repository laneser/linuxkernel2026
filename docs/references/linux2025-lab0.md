# 2025 年 Linux 核心設計課程作業 —— lab0

> **原始出處：** <https://hackmd.io/@sysprog/linux2025-lab0>
> **擷取日期：** 2026-02-19
> **用途：** 課程第一份作業規格（2025 版，待更新為 2026）
> **子頁面：** lab0-a ~ lab0-f
> **涵蓋度：** 摘要（約 4%）
> **省略內容：** Part A 完整 Git hook 設定與 clang-format 流程、Part B Valgrind 完整範例與 signal handling、Part C web server 程式碼與 select() I/O 多工、Part D Fisher-Yates shuffle 與統計檢定數學推導、Part E list_sort.c 演算法深入分析（原文最長約 2800 行）、Part F 完整繳交規格

---

## 概述

改寫自 CMU Introduction to Computer Systems 課程第一份作業，擴充 GNU/Linux 開發工具的使用並強化自動分析機制。

**相關 Repository：** <https://github.com/sysprog21/lab0-c>

---

## Part A：預期目標 + 開發環境設定

> 原始出處：<https://hackmd.io/@sysprog/linux2025-lab0-a>

### 預期學習成果

- 記憶體管理基礎
- 基於指標的資料結構建構
- 字串操作技巧
- 關鍵操作的效能最佳化
- 強健的錯誤處理（含 NULL pointer 情境）
- Linux kernel API 的 linked list 模式

### 開發環境

**作業系統：** Ubuntu Linux 24.04 LTS 或更新版本

**工具安裝：**
```shell
$ sudo apt install build-essential git-core valgrind
$ sudo apt install cppcheck clang-format wamerican aspell colordiff
```

**Repository 管理：**
- Fork `sysprog21/lab0-c`，確保 repository 名稱為 `lab0-c`
- 使用 GitHub sync fork 與上游同步
- `git clone https://github.com/YOUR-USERNAME/lab0-c`

### Queue 實作

需實作以下操作：

| 函式 | 功能 |
|------|------|
| `q_new` | 建立空 queue |
| `q_free` | 釋放 queue 記憶體 |
| `q_insert_head` | 在 head 插入元素 (LIFO) |
| `q_insert_tail` | 在 tail 插入元素 (FIFO) |
| `q_remove_head` | 取出 head 元素 |
| `q_remove_tail` | 取出 tail 元素 |
| `q_size` | 計算目前元素數量 |
| `q_delete_mid` | 刪除中間節點 |
| `q_delete_dup` | 消除已排序 queue 中的重複 |
| `q_swap` | 交換相鄰配對 |
| `q_reverse` | 反轉 queue 順序 |
| `q_reverseK` | 以 K 個節點為一組反轉 |
| `q_sort` | 升序排列 |
| `q_ascend` / `q_descend` | 移除違反單調性的節點 |
| `q_merge` | 合併已排序的 queue |

### 建構與測試

```shell
$ make                    # 編譯
$ make check              # 基本驗證
$ make test               # 完整測試套件
$ make SANITIZER=1 test   # 啟用 Address Sanitizer
```

### 程式碼風格

- 4 空格縮排（無 tab）
- 每行最多 80 字元
- K&R brace style
- 使用 `clang-format -i *.{c,h}` 格式化

### Git Hook 自動檢查

- Commit message 是否符合七條規則
- C 程式碼格式一致性
- GNU Aspell 拼字檢查
- Cppcheck 靜態分析
- **嚴禁使用 `--no-verify` 跳過 hook**

---

## Part B：Valgrind + 自動測試程式

> 原始出處：<https://hackmd.io/@sysprog/linux2025-lab0-b>

### Valgrind 記憶體分析

Valgrind 在 user space 運作，透過 Dynamic Binary Instrumentation (DBI) 追蹤程式行為。使用 shadow values 技術維護暫存器與記憶體的複本。

**基本用法：**
```shell
$ valgrind --tool=<toolname> <program>
```

**記憶體洩漏分類：**
- **definitely lost** — 真正的記憶體洩漏
- **indirectly lost** — 結構成員的洩漏，修復 parent 即可解決
- **possibly lost** — 指標移至已配置區塊中間
- **still reachable** — 未釋放但仍有有效指標的記憶體

**Case 1 — 記憶體洩漏偵測：**
```c
void func(void) {
    char *buff = malloc(10);  // 未 free → definitely lost
}
```

**Case 2 — 無效記憶體存取：**
- Invalid write（超出 buffer 邊界）
- Invalid read（存取已 free 或越界的記憶體）
- Double-free 與 use-after-free

### qtest 自動測試框架

qtest 提供：
1. 偵測非預期終止（segfault）
2. 設定計時器進行 timeout 偵測
3. 透過 Valgrind 監控記憶體配置/釋放
4. 可擴展的約束架構
5. 驗證時間複雜度（如 O(1) 操作）

**記憶體管理追蹤** — 使用 function hooking 以 `test_malloc`/`test_free` 取代標準函式：
- Header magic: `0xdeadbeef`
- Footer magic: `0xbeefdead`
- 初始化填充: `0x55`

### 信號處理與例外管理

```c
signal(SIGSEGV, sigsegv_handler);  // 無效記憶體參考
signal(SIGALRM, sigalrm_handler);  // Timeout
```

使用 `sigsetjmp()`/`siglongjmp()` 實現非區域跳躍，確保信號遮罩正確恢復。

**執行 Valgrind 分析：**
```shell
$ make valgrind
```

---

## Part C：整合網頁伺服器

> 原始出處：<https://hackmd.io/@sysprog/linux2025-lab0-c>

### I/O 多工與 `select()`

使用 `select()` 同時監控 stdin 輸入與 socket 連線，避免 `read` 阻塞。

**關鍵實作：**

1. 設定 non-blocking socket：
```c
int flags = fcntl(listenfd, F_GETFL);
fcntl(listenfd, F_SETFL, flags | O_NONBLOCK);
```

2. 修改 `cmd_select()` 函式處理 stdin 和 listening socket

3. HTTP 請求處理：將 URL path 的 `/` 轉為空格作為命令

4. 回傳 HTTP 200 OK 與正確的 headers

**favicon.ico 問題解決：**
```html
<link rel="shortcut icon" href="#">
```

**測試：**
```bash
./qtest
cmd> web
# 另一個 terminal：
curl http://localhost:9999/new
curl http://localhost:9999/ih/1
```

---

## Part D：亂數 + 論文閱讀

> 原始出處：<https://hackmd.io/@sysprog/linux2025-lab0-d>

### Fisher–Yates Shuffle 實作

1. 取得 queue size
2. 隨機選取 0 到 (len-1) 的 index
3. 將該 index 的值與最後一個未選取元素交換
4. 遞減 len 並重複

### Pearson's Chi-Squared 檢定

驗證 shuffle 均勻性：

$$X^2 = \sum_{i=1}^n \frac{(O_i - E_i)^2}{E_i}$$

1,000,000 次 shuffle 3 個元素的結果：X² = 1.769，自由度 = 5，p-value ≈ 0.8-0.9。p > 0.05，無法拒絕 H₀（均勻分布）。

### 亂數的兩個觀點

**機率觀點：** 各結果等機率、統計獨立 — $X \sim^{iid} U[a,b]$

**資訊理論觀點：** 以 entropy 衡量 — $S = -\sum P(x_i) \log_b P(x_i)$

最大 entropy 出現在均勻分布：$S_{\max} = \log_b n$

### 偽亂數產生器 (PRNG)

PRNG $G: \{0,1\}^\ell \to \{0,1\}^n$ 需「欺騙」所有統計測試。

**測試工具：**
- `ent` — 計算 entropy
- `dieharder` — 全面性統計測試套件

### 常數時間分析（Welch's t-test）

驗證操作是否為 O(1)，使用 fix-vs-random 策略：

$$t = \frac{\bar{X_0} - \bar{X_1}}{\sqrt{\frac{s^2_1}{N_1} + \frac{s^2_2}{N_2}}}$$

lab0-c 中的兩個測試：
- `is_insert_tail_const()` — 測試 append 是否為常數時間
- `is_size_const()` — 測試取得 queue size 是否為常數時間

**關鍵論文：** [Dude, is my code constant time?](https://eprint.iacr.org/2016/1123.pdf)

---

## Part E：Linux 核心的鏈結串列排序

> 原始出處：<https://hackmd.io/@sysprog/linux2025-lab0-e>

### `lib/list_sort.c` — Bottom-Up Merge Sort

**為何用 bottom-up？** 持續合併小的已排序 run，讓資料留在 cache 更久，避免 top-down 方式的 cache thrashing。

### 2:1 合併策略

未排序 list 維持 2:1 大小比例，確保 $3 \times 2^k$ 個元素能放入 L1 cache。

**合併時機判斷：**
- `count + 1` 為 $2^k$（二的冪次）→ **不合併**
- `count + 1` 非二的冪次 → **執行合併**

### 核心元件

- **`list_sort()`** — 將雙向鏈結串列轉為單向，依 `count` 的二進位表示進行合併
- **`merge()`** — 逐元素比較兩個已排序 list，對相等元素優先取自第一個 list（保持穩定性）

### 最佳性證明

`list_sort` 的 merge tree 所有 leaves 都位於最底兩層 — 這是最佳 merge sort 的必要條件。

### 學術參考

1. Panny & Prodinger (1995) — Bottom-up Mergesort 分析
2. Chen, Hwang & Chen (1999) — Queue-mergesort 成本分布
3. Golin & Sedgewick (1993) — Queue-Mergesort 基礎

---

## Part F：作業要求

> 原始出處：<https://hackmd.io/@sysprog/linux2025-lab0-f>

### Repository 設定

- Fork [sysprog21/lab0-c](https://github.com/sysprog21/lab0-c)
- 確認 git log 可見指定的 commit

### 核心實作

- 修改 `queue.[ch]` 通過 `make test`
- 使用 "pointer to pointer" 技巧操作 linked list
- 研讀 2023 年 lab0 檢討以取得詳細指引

### 進階要求

- 實作 `shuffle` 命令（Fisher–Yates 演算法）
- 使用 entropy 概念分析亂數分布
- 支援多種 PRNG 實作（選做 Xorshift）
- 統計分析 shuffle 品質

### 程式碼品質與分析

- 啟用 Address Sanitizer 與 Valgrind 偵測記憶體錯誤
- 使用 Massif 視覺化分析記憶體使用
- 研讀 `console.c` 中的 `select()` 實作
- 理解 CS:APP 的 RIO 封包概念

### 開發紀錄（HackMD 筆記）

- 標題格式：`==2025q1 Homework1 (lab0)==`
- 署名行含 GitHub 帳號
- 中英文間適當空格
- 避免使用圖片呈現程式碼輸出
- 使用中性語言
- 記錄關鍵洞見而非完整程式碼

### 截止日期

2025 年 3 月 11 日（越早提交、越多 code review 活動者得分越高）
