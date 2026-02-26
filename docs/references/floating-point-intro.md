> **原始出處：** https://hackmd.io/@sysprog/B1dc2oq_Wx
> **擷取日期：** 2026-02-26
> **用途：** 初步解讀浮點數（第 1 週測驗相關教材）
> **涵蓋度：** 完整
> **省略內容：** 無

# 初步解讀浮點數
> 資料整理: [jserv](https://wiki.csie.ncku.edu.tw/User/jserv)
> 續集: [留意浮點數運算的陷阱](https://hackmd.io/@sysprog/floating-point)

## 前言
本文探討：
- 為什麼 `float` 加總會失準
- FP32 (IEEE 754 single precision) 在整數區間的可表示性
- `roundTiesToEven` 造成的誤差型態與週期
- Kahan summation algorithm 的補償機制與限制

## 問題的根源

```c
#include <stdio.h>

int main(void) {
    float sum = 0.0f;
    for (int i = 0; i < 10000; ++i) sum += i + 1;
    printf("Sum: %f\n", sum);
}
```

執行結果是 `Sum: 50002896.000000`，與 $1 + 2 + 3 + \cdots + 10000$ 的精確結果 $50005000$ 相差 $2104$。

並非加法有誤，而是：
- `float` 只能保存有限位元 (FP32 有效精度約 24 個二進位位元，含 hidden bit)
- 並非每個整數都能以 `float` 精確表示
- 每次相加都可能發生捨入 (rounding)
- 誤差在長迴圈中逐步累積

## IEEE 754 單精度浮點數格式

單精度浮點數 (`float`) 以 32 位元儲存，各資料欄位規劃如下：

```
 31  30        23 22                              0
┌────┬──────────┬──────────────────────────────────┐
│ S  │ Exponent │            Mantissa              │
└────┴──────────┴──────────────────────────────────┘
  1b     8b                   23b
```

數值由以下公式決定(適用於 normalized finite values，即 $1 \leq E \leq 254$；$E = 0$ 為 subnormals，$E = 255$ 保留給 infinities 與 NaN)：
$$
\text{value} = (-1)^{S} \times 1.\text{mantissa} \times 2^{E - 127}
$$

指數欄位 $E$ 以 127 為 bias 儲存 (stored exponent = actual exponent + 127)。公式中「1.」前的隱含 1 稱為 hidden bit，不佔任何欄位，但使有效數字 (significand) 實際達到 24 位元精度 (1 hidden bit + 23 mantissa bits)。

以整數 $10$ 為例：
$$
(10)_{10} = (1010)_{2} = 1.01_{2} \times 2^{3}
$$

$$
S = 0,\quad E = 3 + 127 = 130 = (10000010)_{2},\quad \text{mantissa} = 01\underbrace{000\cdots0}_{21}
$$

## 整數的精度邊界

並非每個整數都能以單精度浮點數精確表示。24 位元的有效精度意味著，若某整數的二進位表示在最高有效位 (MSB) 與最低有效位 (LSB) 之間相距超過 23 個位元，低位無法完整保留，會依捨入規則近似為鄰近的可表示值。

精度邊界位於 $2^{24} = 16777216$：

```
0 ................................. 2^24-1    2^24    2^24+1
|-----------------------------------|---------|--------|
all representable exactly                        from here, not every integer is representable
```

在區間 $[2^{24},\ 2^{25})$ 中，FP32 的整數間距 (ULP; units of least precision) 變為 2，只有偶數能精確表示：

```
... 16777216   16777218   16777220   16777222 ...
      ●           ●           ●           ●
      |     ✗     |     ✗     |     ✗     |
   16777217    16777219    16777221    16777223   (odd numbers not representable)
```

以下程式展示精度臨界附近的轉換行為：

```c
#include <stdio.h>

int main(void) {
    int nums[4] = {0x400001, 0x800001, 0x1000001, 0x8000007};
    float f;
    for (int i = 0; i < 4; ++i) {
        f = nums[i];
        printf("nums[%d] = %d, f = %.2f\n", i, nums[i], f);
    }
}
```

參考輸出:
```
nums[0] = 4194305,   f = 4194305.00    ← MSB-LSB gap = 22, representable exactly
nums[1] = 8388609,   f = 8388609.00    ← gap = 23, right at the precision limit
nums[2] = 16777217,  f = 16777216.00   ← gap = 24, exceeds limit; trailing 1 lost, rounds down
nums[3] = 134217735, f = 134217728.00  ← gap = 27, exceeds limit; low 4 bits lost, rounds down
```

以 `nums[2]` 和 `nums[3]` 為例，以二進位觀察可直接看出精度損失的原因：

```
0x1000001 = 16777217 = 2^24 + 1：

  位元位置：  24  23  22 ···  2   1   0
  二進位值：   1   0   0 ···  0   0   1
              │   └────── mantissa 23b ──┘ ← trailing 1 lost, rounds down
              └── hidden bit

  stored:  1.00000000000000000000000₂ × 2^24 = 16777216
```

```
0x8000007 = 134217735 = 2^27 + 7：

  位元位置：  27  26  25 ···  4   3   2   1   0
  二進位值：   1   0   0 ···  0   0   1   1   1
              │   └──── mantissa 23b ────┘ ←4b→ overflow, rounds down
              └── hidden bit

  stored:  1.00000000000000000000000₂ × 2^27 = 134217728
```

### 連續整數的精確表示範圍

ULP 隨數值增大而成倍放大，這也是為什麼加總愈來愈大時，後續加入的小量難以發揮作用：

```
interval              integer gap (ULP)
[2^23, 2^24)         1
[2^24, 2^25)         2
[2^25, 2^26)         4
[2^26, 2^27)         8
[2^k,  2^(k+1))      2^(k-23)
```

- $[0,\ 2^{24}]$ 範圍內的所有整數均可精確表示，最多需要 24 個有效位元，恰在精度上限之內。
- $[2^{k},\ 2^{k+1}-1]$ 範圍內，只有 $2^{k-23}$ 的倍數可精確表示。

## roundTiesToEven 捨入規則

IEEE 754 §4.3.1 定義 `roundTiesToEven`：
> The floating-point number nearest to the infinitely precise result shall be delivered; if the two nearest floating-point numbers bracketing an unrepresentable infinitely precise result are equally near, the one with an even least significant digit shall be delivered.

無法精確表示的數值，取最近的可表示值；若兩側距離相等，則取 mantissa LSB 為 `0` 的那一方。此設計使大量運算中的捨入誤差期望值趨近於零。

以 $16777219 = (1000000000000000000000011)_{2}$ 為例：可表示的相鄰值為 $16777218$ 和 $16777220$，距離均為 $1$。$16777218$ 的 mantissa LSB 為 `1`，$16777220$ 的 mantissa LSB 為 `0`，依 `roundTiesToEven` 取 $16777220$。

## 誤差的規律性

在 $[2^{24},\ 2^{25}-1]$ 範圍內，ULP = 2，奇數均被捨入至相鄰偶數，捨入誤差以 $[0, -1, 0, +1]$ 為週期循環：

```
16777216 → 16777216 (  0)
16777217 → 16777216 ( -1)
16777218 → 16777218 (  0)
16777219 → 16777220 ( +1)   ← roundTiesToEven: equidistant, pick the value with LSB = 0
16777220 → 16777220 (  0)
16777221 → 16777220 ( -1)
16777222 → 16777222 (  0)
16777223 → 16777224 ( +1)   ← roundTiesToEven: equidistant, pick the value with LSB = 0
```

在 $[2^{25},\ 2^{26}-1]$ 範圍內，ULP = 4，捨入誤差以 $[0, -1, -2, +1, 0, -1, +2, +1]$ 為週期循環：

```
33554432 → 33554432 (  0)
33554433 → 33554432 ( -1)
33554434 → 33554432 ( -2)   ← roundTiesToEven: equidistant, pick the value with LSB = 0
33554435 → 33554436 ( +1)
33554436 → 33554436 (  0)
33554437 → 33554436 ( -1)
33554438 → 33554440 ( +2)   ← roundTiesToEven: equidistant, pick the value with LSB = 0
33554439 → 33554440 ( +1)
33554440 → 33554440 (  0)
```

## 累加誤差的起始位置

$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$ 首次超過 $2^{24}$ 時，浮點數加法開始失準。臨界點估算：

$$
\frac{n(n+1)}{2} \leq 2^{24} \implies n \approx \sqrt{2 \times 2^{24}} \approx 5792.6
$$

驗算：
- $n = 5792$：$\dfrac{5792 \times 5793}{2} = 16776528 < 2^{24}$，仍在精確範圍。
- $n = 5793$：精確值 $\dfrac{5793 \times 5794}{2} = 16782321$，浮點數加總實際得到 $16782320$，誤差首次出現。

因此，迴圈執行至第 $5793$ 次加法時開始失準，之後誤差逐步累積，最終造成上述 $2104$ 的偏差。

## Kahan Summation Algorithm

Kahan summation algorithm 的目標不是讓 `float` 變成精確數學，而是把每一步加法中因捨入丟掉的低位誤差暫存起來，在下一輪嘗試補回：

```
每一輪的資料流：

     x(本輪加數)
     |
     v
  [x - corr] = y ─────────────────────┐
                                      │
sum ─────────────────────────────> (+) ──→ t(含捨入的實際結果)
  ↑                                   │
  │                                   ↓
  └────────── corr ←── (t - sum) - y
              (實際加入量 - 預期加入量 = 本輪被捨去的低位)
```

```c
float sum  = 0.0f;
float corr = 0.0f;  /* corrective value for rounding error */

for (int i = 0; i < 10000; ++i) {
    float x = (float)(i + 1);
    float y = x - corr;        /* apply previous correction to current addend */
    float t = sum + y;         /* low bits may be rounded away */
    corr = (t - sum) - y;      /* recover lost bits */
    sum  = t;
}
```

各變數的語意：
* `x` : 本輪的原始加數。
* `y` : 本輪欲加入的值，已扣除上輪被捨去的低位量
* `t` : 加法後的實際結果，若 `sum` 遠大於 `y`，`y` 的低位在相加時可能被捨去
* `corr` : 本輪實際加入量 `(t - sum)` 與預期加入量 `y` 的差，即本輪被捨去的低位部分，用於下輪修正，也就是說，將上一輪加法的捨入誤差補回到本輪加數中，這是補償 (compensation)

corr = (t - sum) - y 記錄的是「上一輪實際加進去的量」和「原本預期加的量」之差 (有正有負)，`corr` 的計算式寫為 `(t - sum) - y` 而非 `t - (sum + y)`，原因在於 `sum + y` 本身即觸發 rounding error 的運算，直接計算 `t - (sum + y)` 通常會得到 `0.0`，補償機制完全失效。這與以 `L + (R - L) / 2` 代替 `(L + R) / 2` 迴避整數溢位的技巧性質相同：數學等價的算式，在有限精度運算中可能產生截然不同的結果。

此補償機制在 `|sum| >= |y|` 時能最穩定地捕捉誤差，對應 Fast2Sum 的精確分解條件。在本文的情境中，`sum` 隨迴圈推進逐漸增大，進入失準區間後遠大於每個加數，`(t - sum) - y` 能有效捕捉被捨去的低位；即便初期 `sum` 尚小，Kahan 仍有補償效果，只是提取精度略有差異。`|sum| >= |y|` 是讓補償最穩定的有利條件，而非 Kahan 演算法運作的絕對前提。

## 演算法的限制

### 無法創造不存在的可表示數

若最終結果本身就無法以 `float` 精確表示，Kahan 也無法讓 `sum` 突然變得可表示。例如，將迴圈初始值改為 `float sum = 1.0f`，預期結果 $50005001$ 超出 `float` 的表示能力，無論補償機制多精確，輸出仍為 $50005000$。

### 加數本身已失真時，補償能力下降

Kahan 的補償前提是 `y = x - corr` 本身不發生 rounding error。若加數 `x` 在進入迴圈前就已因精度不足而失真，那些更低位的資訊根本沒有進入運算流程，`corr` 自然也無從補救。

當 `i >= 0x1000000`(約 $1.67 \times 10^7$)時，ULP 已增大到 2 以上，`(i + 1)` 本身不再保證可精確表示，演算法無法保證結果的正確性。使用前必須明確限制輸入範圍。

### 最後一輪 `corr != 0` 時的殘差

若迴圈結束後 `corr` 不為零，該誤差不會自動加回 `sum`。即便在迴圈外補做 `sum -= corr`，這一步仍是浮點運算，若目標值不可表示，最終仍會被捨入到鄰近值。

### 編譯器最佳化可能使補償機制失效

在 C/C++ 中，開啟激進的浮點最佳化選項 (如 GCC/Clang 的 `-ffast-math` 或 `-Ofast`) 時，編譯器假設浮點加法符合結合律，可將 `t = sum + y` 視為精確，進而把整個序列 `corr = (t - sum) - y` 等價展開為 `(sum + y - sum) - y`，直接折疊成 `0.0f`，補償機制完全失效。保護方式是對含有 Kahan 的翻譯單元單獨不加 `-ffast-math` / `-fassociative-math`，而非依賴 `#pragma GCC optimize` 等效果因編譯器版本而異的機制。

## 實務建議

```
需求                     建議
─────────────────────────────────────────────
一般統計、資料處理         至少用 double 累加
大量 float 輸入            float 輸入 + double accumulator
高可靠數值計算             Kahan / Neumaier / pairwise summation
整數金額、計數             優先整數或定點
```

Kahan 適合長序列加總、大小量混合但未嚴重超出格式精度極限的場景。若面對極端動態範圍、嚴重消去 (catastrophic cancellation)，或需要可重現的高精度科學計算，應考慮更高精度格式或專門的數值方法。

---

## Linux 核心中的補償機制實例

把被截去的微小誤差暫存，再遞延補回並非 Kahan summation 獨有的手法。在 Linux 核心空間 (kernel space) 中，因保存與還原 FPU 暫存器對 context switch 帶來顯著延遲，核心程式碼原則上不使用浮點數。相同的補償思想因此以整數形式出現在多個關鍵子系統中。

### 時鐘子系統的整數補償：`xtime_nsec`

Linux 核心的時間轉換公式為：
```
nanoseconds = (cycles × mult) >> shift
```

右移 `shift` 位等同於整數除法，每次計算都會丟棄餘數。若直接累加：

```c
/* naive approach: right-shift each time; remainder is permanently lost */
system_ns += (delta_cycles * mult) >> shift;
```

在每秒數百萬次時鐘中斷下，這些微小的截斷誤差逐步累積，最終導致可量測的時間漂移。

Linux 核心的對策是在 `struct tk_read_base` 中引入 `xtime_nsec`，以 fixed-point 形式儲存未經右移的完整積，只在需要讀取奈秒數值時才執行位移，低位的次奈秒分數位留在原處繼續參與下一輪累加：

```c
/* kernel/time/timekeeping.c conceptual pseudocode */
tk->tkr_mono.xtime_nsec += delta_cycles * mult;    /* accumulate the full fixed-point product, no truncation */

/* shift only when needed: extract whole nanoseconds; sub-ns fraction carries over */
nsec_delta = tk->tkr_mono.xtime_nsec >> shift;     /* whole nanoseconds */
tk->tkr_mono.xtime_nsec &= (1ULL << shift) - 1;   /* retain the fixed-point fraction */
```

對照 Kahan 演算法的作用：

```
Kahan's corr           ↔   low-order bits in xtime_nsec
low bits lost each round  ↔   sub-ns fixed-point fraction truncated each shift
carried forward next round  ↔   next delta_cycles accumulates into the same field
```

`xtime_nsec` 相當於整數版本的 `corr`，確保即使是次奈秒級的時間碎片，也不會因頻繁中斷而被累計遺失。

### tools/perf 中的 Welford's Online Algorithm

Linux 核心原始程式碼的 `tools/perf` 運行於使用者空間 (user space)，可合法使用 `double`。在統計效能事件 (IPC、cache miss 率等) 的變異數時，演算法的選擇直接決定數值計算的可靠性。

#### 基礎公式與其隱患

教科書常見的單遍 (one-pass) 母體變異數計算公式：
$$
\text{Var} = \frac{\sum x_i^2}{N} - \left(\frac{\sum x_i}{N}\right)^2
$$

此式等價於：
$$
N \cdot \text{Var} = \sum x_i^2 - \frac{(\sum x_i)^2}{N}
$$

只需一輪走訪即可同時累積 $\sum x_i$ 與 $\sum x_i^2$，看似高效。問題在於最後一步：當取樣值本身很大、彼此差異卻極小時，$\sum x_i^2$ 與 $(\sum x_i)^2 / N$ 都是天文數字，且極為接近。相減後的差值，亦即我們真正需要的變異數分子遠小於二個運算元本身。一旦超出浮點格式的有效精度，相近的大數相減會使所有有效位被消去，即 catastrophic cancellation (災難性消去)。樣本變異數只需將分母改為 $N - 1$，但二者共用危險的中間值 $\sum x_i^2 - (\sum x_i)^2 / N$，該陷阱同樣無從迴避。

#### 數值危機

取三筆效能計數：$x_1 = 10001$，$x_2 = 10002$，$x_3 = 10003$，均值 $\bar{x} = 10002$(母體變異數 $= 2/3$，樣本變異數 $= 1$)。

基礎公式的關鍵中間計算：
$$
\sum x_i^2 - N\bar{x}^2 = (10001^2 + 10002^2 + 10003^2) - 3 \times 10002^2 = 300120014 - 300120012 = 2
$$

以 `float` (mantissa 23b，ULP 在此量級為 $2^{28-23} = 32$) 計算時：

```
300120014 → 300120000(捨入至最近的 32 倍數，距離 14 < 16)
300120012 → 300120000(同樣被捨入，距離 12 < 16)

相減：300120000 − 300120000 = 0   ← 精確差值 2 被完全吃掉
```

$300120014$ 與 $300120012$ 的差距 2 遠小於此區間的 ULP 32，兩者被捨入至同一個可表示值，相減後精確答案蕩然無存。

`double` 擁有更高精度(有效位約 $10^{15}$)，但效能工具量測的 CPU 週期計數動輒達 $10^9$，對數百萬筆取樣累積平方和時，$\sum x_i^2$ 可輕易逼近 $10^{24}$；`double` 在此量級的整數解析度約為 $10^8$，相減結果誤差可能跨越數個量級，最終導致變異數嚴重失真，甚至出現負值。

#### Welford's Online Algorithm：從根本迴避龐大中間值

`tools/perf/util/stat.c` 改用 [Welford's online algorithm](https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance)，只維護二個隨樣本遞增更新的變數：
* `mean` : 走訪到目前為止的執行均值。
* `M2` : 各取樣值對均值的平方偏差累積量；最終樣本變異數 $= M2 / (n - 1)$。

每接收一筆新值 $x$，按以下順序更新：
1. $\delta_1 = x - \text{mean}_\text{old}$(對舊均值的偏差)
2. $\text{mean}_\text{new} = \text{mean}_\text{old} + \delta_1 / n$
3. $\delta_2 = x - \text{mean}_\text{new}$(對新均值的偏差)
4. $M2 \mathrel{+}= \delta_1 \times \delta_2$

$M2$ 每步增加的是二個偏差量的乘積，遠小於 $x^2$，從根本上消除讓中間值膨脹到超出精度範圍的可能。

Linux 原始程式碼：

```c
/* tools/perf/util/stat.c */
void update_stats(struct stats *stats, u64 val)
{
    double delta;
    stats->n++;
    delta = val - stats->mean;               /* delta1: deviation from the old mean */
    stats->mean += delta / stats->n;         /* update the mean */
    stats->M2   += delta * (val - stats->mean); /* delta1 * delta2; M2 increment */
}

double variance_stats(struct stats *stats)
{
    if (stats->n < 2)
        return 0.0;
    return stats->M2 / (stats->n - 1);      /* sample variance */
}
```

注意第三行：`val - stats->mean` 用的是已更新後的 `mean`($\text{mean}_\text{new}$)，計算的是 $\delta_2$，而非重複使用 `delta`($\delta_1$)。順序不可顛倒：必須先更新均值，再用新均值計算第二個偏差，才符合 Welford 公式的數學等價性。

#### 與 Kahan 的結構類比

`delta = val - mean` 類比 Kahan summation 的 `y = x - corr`，都是先求出與已知基準量的差，再把微小量疊加回去：

```
Kahan                               Welford
────────────────────────────────────────────────────────────────
y    = x - corr                     delta  = val - mean_old
t    = sum + y                      mean  += delta / n
corr = (t - sum) - y                M2    += delta × (val - mean_new)
(corrects truncated bits after the fact)  (avoids large intermediate values upfront)
```

Kahan 在加法已完成後回補被截去的低位；Welford 則是從一開始就拒絕讓中間值膨脹。前者是事後補救，後者是事先預防，但主體精神相同：永遠只操作差值，而非直接操作累積的大數。

## 延伸練習

### 練習: 整數補償累加器 (對標 timekeeping)

情境：在無法使用 FPU 的 Linux 核心環境中，以 `u64` 實作一個帶有餘數補償的累加器。

任務：給定陣列 `u32 loads[]` 與縮放因子 `shift = 10`。先演示每次迴圈執行 `sum += loads[i] >> shift` 所造成的截斷誤差，再改寫程式碼，在迴圈內維護 `remainder` 變數，展示重構後如何達成零誤差。

傳統截斷法，每次直接丟棄低 10 位元，誤差逐輪累積：
```c
u64 sum = 0;

for (int i = 0; i < N; ++i)
    sum += (u64)loads[i] >> 10;   /* discard the low 10 bits */
```

核心補償法，模擬 `xtime_nsec` 的「先累積、再提取」策略：
```c
u64 sum       = 0;
u64 remainder = 0;   /* Kahan-style corr: carry the bits truncated in the previous iteration */

for (int i = 0; i < N; ++i) {
    remainder += (u64)loads[i];          /* accumulate the full raw value */
    sum       += remainder >> 10;        /* extract the integer part ready to carry over */
    remainder &= (1ULL << 10) - 1;       /* keep the low 10 bits; carry over to the next iteration */
}
```

補償法截斷總量恆為零。

### 練習: 編譯器最佳化對 Kahan 的破壞 (-ffast-math)

情境：驗證 Kahan 演算法在 `-ffast-math` 下的失效機制。

1. 撰寫本文的 Kahan summation 程式，分別以下列選項編譯並比較結果：
```
gcc -O2              kahan.c -o kahan_safe
gcc -O3 -ffast-math  kahan.c -o kahan_broken
```

2. 檢視組合語言輸出 (`gcc -S -ffast-math kahan.c`)，說明 `-ffast-math` 允許編譯器將浮點數視為精確實數，進而把 `corr = (t - sum) - y` 中的 `t = sum + y` 展開代入，得出 `(sum + y - sum) - y`，經代數相消折疊成 `0.0f`

以下為標準 Kahan 函式的 AArch64 參考輸出 (GCC)：
```c
float kahan_sum(const float *a, int n) {
    float sum = 0.0f, corr = 0.0f;
    for (int i = 0; i < n; ++i) {
        float y = a[i] - corr;
        float t = sum + y;
        corr = (t - sum) - y;
        sum  = t;
    }
    return sum;
}
```

`gcc -O2`，嚴格 IEEE 754，`corr` 正常更新：
```c
kahan_loop:                         ; s0 = sum, s1 = corr
    ldr     s2, [x0], #4            ; s2 = *a++        (a[i])
    fsub    s3, s2, s1              ; s3 = a[i] - corr (y)
    fadd    s4, s0, s3              ; s4 = sum + y      (t)
    fsub    s5, s4, s0              ; s5 = t - sum
    fsub    s1, s5, s3              ; s1 = (t-sum) - y  (new corr)
    fmov    s0, s4                  ; s0 = t            (new sum)
    subs    w1, w1, #1
    b.ne    kahan_loop
```

`gcc -O3 -ffast-math`，`corr` 可能被代數化簡消去 (實際輸出因 GCC 版本與目標而異)：

```asm
kahan_loop:                         ; s0 = sum, s1 degraded to a load register
    ldr     s1, [x0], #4            ; s1 = *a++
    fadd    s0, s0, s1              ; s0 = sum + a[i]   (compensation path eliminated)
    subs    w1, w1, #1
    b.ne    kahan_loop
```

FP 算術指令從 4 條(3 × `fsub` + 1 × `fadd`)降為 1 條(`fadd`)；`s3`、`s5` 及所有 `fsub` 消去，`s1` 不再保存 `corr` 而退化為單純的載入暫存器，補償機制在此版本中失效。

3. 對抗 `-ffast-math` 破壞 Kahan 的可靠做法是對該翻譯單元明確禁用 `-fassociative-math`；`READ_ONCE()` / `WRITE_ONCE()` 則是不同層面的工具：底層為 `volatile` 轉型，主要約束編譯器對記憶體存取的合併、重讀與撕裂行為，無法可靠地阻止代數化簡。查閱 Linux 核心 `Makefile` 中對 `-ffast-math` 的明確排除 (`-fno-fast-math` / `-fno-associative-math`)，說明 Linux 核心開發者為何對此施加約束，以及這與 `READ_ONCE()`、`barrier()` 防止編譯器重排記憶體存取的設計哲學有何共通之處——兩者都是「在特定語意邊界上約束編譯器的最佳化假設」，只是目標層次不同。

## 結語

浮點誤差的本質不是真正的錯誤，而是肇因於在有限位元下的捨入。Kahan summation algorithm 的價值，在於每步把被捨掉的低位誤差記錄下來，盡量在後續計算中補回，但它仍受限於浮點格式本身的可表示能力，無法突破格式的精度上限。這個思想並不侷限於浮點數：從 Linux 核心時鐘子系統的 `xtime_nsec` 到 `tools/perf` 的 Welford 演算法，補償被截斷的微小誤差、遞延到後續還清，是驅動當代系統軟體底層演算法設計的反覆出現的主題。

以整數逼近浮點衰減的 EWMA，則以另一種視角體現同樣的工程哲學：在整數的約束下，以合理的近似保留最有價值的資訊。相關設計與 PELT 在排程器中的應用。