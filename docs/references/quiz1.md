> **原始出處：** https://hackmd.io/@sysprog/linux2026-quiz1
> **擷取日期：** 2026-02-26
> **用途：** 2026q1 第 1 週測驗題
> **涵蓋度：** 完整
> **省略內容：** 無

---
tags: linux2026
---

# [2026q1](https://wiki.csie.ncku.edu.tw/linux/schedule) 第 1 週測驗題
> [作答表單: 測驗 1 到 5](https://forms.gle/zk22Wc7dgFKbKwnd7)
> [作答表單: 測驗 6 到 9](https://forms.gle/L6k5EQ6Q8S9yEDW76)

:::warning
:warning: 回答延伸問題時，務必優先以[課程教材](https://wiki.csie.ncku.edu.tw/linux/schedule)為主要出處，隨後參照 C 語言規格書、Linux 核心原始程式碼及其 git log 和 LKML (Linux Kernel Mailing-List)，和權威素材 (如 GCC 和 glibc 手冊，但絕對不是 CSDN 或者尋常的網路日誌/筆記)
AI 工具是輔助性質，可用來撰寫測試程式碼和收集資訊，但主要的推測、查證、分析，和討論，都該由人類進行。
:::

### 測驗 `1`
Linux 核心的時間換算以右移代替除法 (例如右移 10 位元等同除以 1024)，但右移會丟棄低位，高頻事件下誤差逐步累積。下列程式以 `remainder` 保存每輪尚未湊滿進位的碎片，扮演整數版 Kahan 補償變數的角色：
```c
u64 sum = 0;
u64 remainder = 0;  /* Kahan-style corr: carry the bits truncated in the previous iteration */

for (int i = 0; i < 1000; i++) {
    remainder += loads[i];
    sum       += remainder >> 10;
    remainder &= __甲__;  /* (1) Bit mask to retain the low 10 bits. */
}
```

:::success
延伸問題:
- [ ] 在 Linux 核心排程器找對應手法
1. 在 `kernel/sched/pelt.c` 中，指出哪個欄位扮演累積碎片的角色，並說明其作用及範圍
2. 針對 `___update_load_sum()`，解釋它如何用右移避免昂貴除法 (並解說在經典的 x86-64 和 Arm64 處理器中，除法運算的成本)，及這一步會截斷哪些位元
3. 逐步解釋何以上述程式碼可避免高頻事件下的誤差累積，考量因素有
    - 先把本次 `delta` 加回 `sa->period_contrib`
    - 用 `periods = delta / 1024` 算跨過多少個完整的 1ms 週期
    - 用 `delta %= 1024` 把尚未湊滿 1ms的碎片存回 `sa->period_contrib`
    - 探討該 `period_contrib` 在效果上等價於上述題目中 `remainder` 的作用、為何選擇 1024 (注意: 這是工程取捨)，並參照 git log 以得知 Linux 核心開發者的考量
4. 對照上述迴圈內的程式碼與 PELT 的 `period_contrib` 設計，回答下列問題
    - `remainder` 保留的是低 10 位元的負載碎片
    - PELT 的 `period_contrib` 保留的是哪種碎片
    - 二者在避免系統性低估上，數學上同一類型的原因為何

- [ ] 把 Linux 核心相關程式碼移植成獨立運作的程式碼 (standalone userspace program)

5. 撰寫 userspace C 程式，重現 PELT 的碎片補償並充分模擬，需求
    - 以 `now_ns` 當輸入事件時間戳記序列，事件間隔刻意採用非 1024ns 的整數倍
    - 先只做 `delta >>= 10` 後直接換算，不保留碎片，然後仿照 `accumulate_sum()` 維護 `period_contrib`
    - 模擬在 100 萬次事件後，不同手法對於跨過多少個 1ms 週期的差距
    - 解釋差距的符號與成因 (以統計學的觀點陳述)，參照 git log 和 LKML，羅列 Linux 核心開發者的考量
:::


### 測驗 `2`
Kahan summation 實作的 `corr = (t - sum) - y` 依賴浮點數不滿足 `__乙__` 律的特性追蹤捨入誤差。GCC 在 `-O3 -ffast-math` 下允許浮點重排，可能把此式視為恆等於零而消去。
以 GCC 為例，其編譯選項 `-ffast-math` 允許假設浮點數滿足數學上的 `__丙__` 律。

:::success
延伸問題:
- [ ] 證明 IEEE 754 二進位浮點數不滿足結合律

請在 binary64 下構造三個數 $a,b,c$，使得
$$
(a+b)+c \ne a+(b+c)
$$

解釋哪一步發生 rounding，並指出該 rounding 對應哪一個 guard / round / sticky bit 狀態，參照 IEEE 754 規格解說

為何 Kahan summation 的
$$
corr = (t - sum) - y
$$

能追蹤誤差？用 IEEE 754 的正規化 (normaliation) + 尾數截斷機制說明
* $t = sum + y$ 時實際儲存的尾數少哪幾些位元
* $(t - sum)$ 為何只保留被捨入後的高位
* $(t - sum) - y$ 如何重建被截斷的低位

以 ULP 單位來量化該誤差。

若 rounding mode 改為 toward zero，Kahan 是否仍正確？
分別分析
1. round-to-nearest-even
2. toward zero
3. toward +∞
4. toward −∞

說明哪幾種模式下，Kahan 的補償項可能偏向單側誤差。

- [ ] IEEE 754 規格細節與極端值

倘若 $sum$ 與 $y$ 的 exponent 相差超過 53:
1. 為何 $t = sum + y$ 會直接等於 $sum$
2. 此時 corr 等於多少
3. Kahan 是否仍能補償

請以 subnormal 邊界為例，說明 gradual underflow 在此的作用。

假設給定的硬體 (如 x86-64) 具備將
$$
t = sum + y
$$
用 FMA 重寫成單一指令執行路徑

分析
1. 若 FMA 只做一次 rounding，誤差是否更小
2. Kahan 是否還需要
3. 若編譯器在 `-ffast-math` 下啟用 contraction，是否改變語意

- [ ] `-ffast-math` 實際開啟哪些子選項

查閱 [GCC 文件](https://gcc.gnu.org/onlinedocs/)，指出 `-fassociative-math`, `-fno-signed-zeros`, `-fno-trapping-math`, `-freciprocal-math` 裡頭何者直接導致
$$
(t - sum) - y \equiv 0
$$
在最佳化過程中會被消去。

將 Kahan 誤差界寫成數學式。對於 n 次加法，證明
* naive summation 誤差界為 $O(n\epsilon)$
* Kahan summation 為 $O(\epsilon)$

其中 $\epsilon = 2^{-53}$，請完整推導。

- [ ] 深入掌握浮點數標準和原理
使用 IEEE 754 的 exact rounding 定理，證明
$$
fl(a+b) = (a+b)(1+\delta), \quad |\delta| \le \epsilon
$$

並用此式重新推導 Kahan 的補償公式。在 Linux 核心原始程式碼找到上述浮點運算 (注意: 核心其實使用定點數，但有相似原理) 誤差考量的程式碼，並充分探討。
:::

### 測驗 `3`
在 32 位元二補數系統上，`abs(-2147483648)` 的結果是 `__丁__`

:::success
延伸問題:
在 GCC/glibc 手冊中，找到對應描述並充分探討其考量。
:::

### 測驗 `4`
延伸測驗 `1`，以 `loads[i] = 100`(固定常數)、執行 1000 次迴圈為例，比較有無補償的結果：
```c
/* Without compensation: discard the remainder on every iteration. */
u64 sum_naive = 0;
for (int i = 0; i < 1000; i++)
    sum_naive += (u64)100 >> 10;
```

無補償版本執行後 `sum_naive = __戊__`，有補償版本執行後 `sum = __己__`

:::success
延伸問題:
解釋程式碼行為並推廣為更通用的數學形式。
:::

### 測驗 `5`
Linux `timekeeping.c` 以同樣的補償結構追蹤次奈秒 (sub-nanosecond) 精度：
```c
/* Accumulate the full fixed-point product; no truncation here. */
tk->tkr_mono.xtime_nsec += delta_cycles * mult;
/* Extract whole nanoseconds; retain the sub-ns fraction for the next round. */
nsec_delta = tk->tkr_mono.xtime_nsec >> shift;
tk->tkr_mono.xtime_nsec &= (1ULL << shift) - 1;
```

`xtime_nsec` 的作用類似測驗 `1` 中 `__庚__` 變數的角色，以保留尚未湊滿整數的碎片。`mult / 2^shift` 是每個 CPU cycle 對應 `__辛__` 的近似轉換係數 (填時間單位)。

:::success
延伸問題:
1. 參照 [Linux 核心文件](https://docs.kernel.org/) (注意: 字字珠璣，不要花太多心思在二手材料)，解讀 timekeeping 的作用，並探討為何 timekeeping 不直接使用 float/double 一類的浮點數型態，也說明 `struct tk_read_base` 中 `mult` 與 `shift` 的設計目的
2. `xtime_nsec` 為何必須保留 sub-ns fraction，分析
    * 每次都直接截斷低位會產生何種長期漂移
    * 在高頻 clocksource 下誤差成長速率如何
    * 倘若給定的 CPU (單核) 時脈為 4GHz，每秒大約幾次 cycle 累積會溢出 1ns，務必用數學式推導誤差上界
3. `xtime_nsec` 的 bit width 如何決定？判定 `shift` 的典型範圍：最大可能值、為何必須保證 `(1ULL << shift)` 不會 overflow，該設計是否隱含某種 clocksource 頻率上限
4. 將上述程式碼表示成數學式，令
    $$
    T = \sum_i \Delta c_i \cdot \frac{mult}{2^{shift}}
    $$
    證明若每次都 truncation，誤差界為 $O(n)$，且保留 fraction 後誤差界為常數上界
5. 若 delta_cycles 極大，分析
    * 乘法是否可能 overflow
    * 為何 Linux 核心使用 128-bit 中間值
    * 在 32 位元硬體架構是否有額外處理
6. 若 shift 過小，則會發生精度不足、fraction 太快溢出，和 mult 變大導致乘法風險，推導最佳 shift 範圍條件。
:::

### 測驗 `6`
Linux 核心的 PELT 以 $1024 /mu s$ 為單位更新週期計數，時間片段 `deltas[i]` 不規則，需保存碎片供下輪累積：
```c
u32 periods_passed = 0;
u32 period_contrib = 0;

for (int i = 0; i < 1000; i++) {
    u32 delta = deltas[i] + period_contrib;
    periods_passed += delta / 1024;
    period_contrib  = __A__;
}
```
不得有除法。

:::success
延伸問題
1. 在 Linux 核心 [sched/pelt.c](https://github.com/torvalds/linux/blob/master/kernel/sched/pelt.c) 中找出與上述對應的程式碼片段，並指出哪個欄位對應 `period_contrib` 及為何 PELT 的時間單位是 1024 µs，隨後探討:
    * 1024 µs 與 1ms 的差距是否重要
    * 若改為 1000 µs，會破壞哪些最佳化並對 CPU 排程帶來哪些衝擊
2. 倘若不保存 `period_contrib`，證明長期誤差界為 $O(n)$，並推導 1 秒內在 1 kHz 更新頻率下可能的最壞誤差。倘若保留 `period_contrib`，證明誤差界為常數上界 $< 1024$，並說明為何不會隨時間線性成長。探討現行 Linux 核心程式碼中，前述誤差界對於排程行為的影響
3. 倘若 `deltas[i]` 永遠小於 1024，`periods_passed` 何時才會增加？是否可能導致延遲更新？PELT 是否允許這種延遲？
4. PELT 不只計數週期，還會做 exponential decay，解釋
    * `periods_passed` 如何影響 load_avg 的衰減
    * 若 `period_contrib` 設計錯誤，會如何扭曲負載估計
    * 對照〈[從熱力學第二定律到系統軟體：機率、資訊熵與現代作業系統的大融通](https://hackmd.io/@sysprog/from-entropy-to-os)〉，探討 PELT 的物理意義
5. 倘若 `delta` 接近 `UINT_MAX`，分析 `delta + period_contrib` 是否可能 overflow、Linux 核心是否依賴 wraparound 語意，而若改為 64 位元是否更安全？Linux 核心程式碼設計的考量是什麼？搭配 git log 和 LKML 討論來解讀
6. 倘若 `deltas[i]` 非單調 (monotonic)，例如允許時間倒退 (由使用者或事件去變更系統時間)，充分回答 (附上數學分析和推論) 以下:
    * Linux 核心如何防止負 delta？
    * PELT 是否假設單調時鐘？
    * 在時鐘訊號源不穩定時會發生什麼？
7. 若將上述 1024 改為 2048，精度是否改變？衰減曲線是否改變？load average 半衰期是否改變？這些對於 Linux 核心 CPU 排程的衝擊是什麼？務必量化分析並進行實際測量
:::

### 測驗 `7`
在理想實數模型下討論 EWMA，更新式定義為：
$$
s_t = (1 - \alpha)\,s_{t-1} + \alpha\,x_t, \quad 0 < \alpha \le 1
$$

展開遞迴式，將 EWMA 展開 $k$ 步：
$$
s_t = (1-\alpha)^k s_{t-k} + \alpha \sum_{i=0}^{k-1} (1-\alpha)^i x_{t-i}
$$

歷史樣本 $x_{t-i}$ 的權重為 `__B__`，從 $s_0$ 展開至 $s_t$ 時，初值 $s_0$ 的係數為 `__C__`。

:::success
延伸問題:
- [ ] 回顧原理
令 $\alpha = 1/2^w$，推導 half-life：
$$
(1-\alpha)^k = \frac12
$$

求 $k$ 的近似。

當 $w$ 增加 1 時：
* 收斂速度變化比例為何？
* 對雜訊抑制能力的影響？

- [ ] CPU 排程器的考量
Linux scheduler 的 PELT 也是 EWMA 形式的衰減，為何 PELT 需要保存 period_contrib，而 RSSI 不需要？搭配原始程式碼、git log 和 LKML 等權威素材來討論。提示：
* 時間粒度不規則
* delta 不固定
* 右移轉換單位

若移除 PELT 的 remainder，會造成什麼偏差？
:::

### 測驗 `8`
在 Linux 核心的 [include/linux/average.h](https://github.com/torvalds/linux/blob/master/include/linux/average.h)，`struct ewma` 的 `weight_rcp` 的倒數形式 $2^w$ 中，$\alpha$ = `__D__`。
以 `DECLARE_EWMA(speed, 10, 8)` 為例 ($f = 10$，$w = 3$，$\alpha = 1/8$)，
`ewma_add()` 的 `>> w` 右移前被捨去的低位餘數 $r = N \bmod 2^w$ 最大為 `__E__`，對應誤差上界 `__F__` KB/s。`ewma_read()` 的 `>> f` 截斷誤差嚴格小於 `__G__` KB/s。

:::success
延伸問題:
`DECLARE_EWMA(name, f, w)` 在 Linux 核心的內部實作為
```c
avg = avg - (avg >> w) + (val << f);
```

推導其與
$$
s_t = (1-\alpha)s_{t-1} + \alpha x_t
$$

在定點數的等價關係，並解釋 `<< f` 與 `>> f` 的作用和考量，對照 objdump 輸出，分析 CPU 指令的延遲成本。

針對 $\alpha = 1/2^w$ 的設定
* 若改為 $\alpha = 1/10$ 是否仍可無除法實作
* 探討除法在 CPU 排程器的成本
:::

### 測驗 `9`
在 Linux 核心原始程式碼中，針對 Qualcomm-Atheros `ath9k` 晶片的 Wi-Fi 裝置驅動程式，其追蹤 [RSSI](https://en.wikipedia.org/wiki/Received_signal_strength_indicator) 使用 `DECLARE_EWMA(rssi, 10, 8)`，回答以下:
- $\alpha$ = `__H__`
- $I_\text{max}$ (RSSI 最大值約 100) = `__I__`
- 若 RSSI 從穩定的 50 突然降至 10，第 1 輪更新後 $s_1 = `__J__`，讀回值為 `__K__`

:::success
延伸問題:
WiFi RSSI 常以 dBm 表示，實際功率為
$$
P_\text{mW} = 10^{\frac{\text{RSSI}}{10}}
$$

為何對 RSSI (dB 尺度) 做 EWMA 與對線性功率做 EWMA 不等價？
* 推導對 dB 做 EWMA 等價於對線性功率做什麼運算
* 說明是否會導致物理意義上的偏差

RSSI 通常範圍約 -100 到 0 dBm。倘若 RSSI 使用無號整數表示 0~100，是否存在資訊損失？若連續輸入 0 (如異常狀況)，EWMA 是否會在有限步內歸零？推導理論需要多少步使值 `< 1`。

WiFi roaming 判斷常使用 RSSI threshold。倘若 $\alpha$ 太小 → 平滑但慢，而 $\alpha$ 太大 → 敏感但抖動
* 推導從 60 降到 40 所需步數為 $\alpha$ 的函數
* 若 beacon interval = 100 ms，估算實際反應時間
* 討論 Linux 核心裝置驅動程式為何選 $1/8$ 而非 $1/16$
:::

參考題解
:::spoiler
甲: `(1ULL << 10) - 1`，等價 `1023` 或 `0x3FF`；保留低的 10 個位元
乙/丙: 結合律，`-ffast-math` 允許浮點重排 (reassociation)
丁: undefined behavior，`INT_MIN` (即 `-2147483648`)，C 標準語意屬未定義行為，常見實作為此值
戊: 0，`100 >> 10 = 0`；每次增量為零
己: 97，$\lfloor 100000 / 1024 \rfloor = 97$
庚: `remainder`，保留尚未湊滿整數奈秒的碎片
辛: ns，`mult / 2^shift` ≈ 每 cycle 對應的奈秒數
A: `delta&1023`，即 `delta % 1024`
B: $\alpha (1-\alpha)^i$
C: $(1-\alpha)^t$
D: $1/2^w$
E: 7，$2^w - 1 = 7$，以 $w = 3$ 為例；右移前餘數 $r$ 的最大值
F: $7/8192 \approx 0.00085$，$(2^w-1)/2^{f+w}$；每 internal 單位截斷 $< 1/2^w$，轉 KB/s 須再除 $2^f$
G: 1，嚴格小於 1 KB/s，與 $f$ 無關
K: 45，$\lfloor 45.0 \times 1024 \rfloor \gg 10 = 45$
:::