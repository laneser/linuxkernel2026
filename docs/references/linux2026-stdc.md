> **原始出處：** https://hackmd.io/@sysprog/linux2026-stdc
> **擷取日期：** 2026-03-22
> **用途：** 第二週作業 (stdc) 完整要求
> **涵蓋度：** 完整
> **省略內容：** 無

---
title: 2026 年 Linux 核心設計課程作業 —— stdc
image: https://i.imgur.com/robmeiQ.png
description: 做好探索 Linux 主體的準備
tags: linux2026
---

# 2026 年 [Linux 核心設計](https://wiki.csie.ncku.edu.tw/linux/schedule)課程作業: stdc

> 主講人: [jserv](https://wiki.csie.ncku.edu.tw/User/jserv) / 課程討論區: [2026 年系統軟體課程](https://www.facebook.com/groups/system.software2026/)
:mega: 返回「[Linux 核心設計](https://wiki.csie.ncku.edu.tw/linux/schedule)」課程進度表

==[解說錄影](https://youtu.be/WBMLZFd9qwI)==

## :memo: 預期目標
* 充分檢視[第二週教材](https://wiki.csie.ncku.edu.tw/linux/schedule)，從第一手材料理解 C 語言程式設計
* 觀摩學員[第一次作業的成果](https://hackmd.io/@sysprog/linux2026-homework1)並學習 code review 原則
* [軟體工程師要學會說故事](https://ruddyblog.wordpress.com/2016/06/18/)，從良性詳盡的批評開始
* 工程師也許無法賺大錢，但一定要做大事 (開發的資訊系統給數千萬人每天用，當然是大事)，為了這樣的目標，提高自身素養

## :rocket: 檢查清單
* 參照 [2026-03-03/10 問答簡記](https://hackmd.io/p87SQ6WpT-ehlVhXglXk9w)，回顧課程問答並檢視「飛蛾撲火」的「科學解釋」存在的謬誤，引以為戒
* 畢業前就該證明自己能解決工程難題，掌握你能觸及的細節，並貫徹溝通能力、跨文化協作與對品質的自我約束
* 「誠實面對自己」不是口號，是面對 Linux 核心原始程式碼的浩瀚無涯，最深刻的領域

## :flashlight: Code Review
> 錄影: [Amazing Code Reviews: Creating a Superhero Collective](https://youtu.be/ly86Wq_E18o)

- [ ] 寫程式的人

良好的程式碼審閱文化往往從程式碼本身的品質開始。保持程式碼簡潔是一項基本原則。KISS（Keep It Small and Simple）提醒開發者避免過度複雜的實作。當一段程式碼逐漸膨脹到數百行時，就應重新檢視設計是否需要拆分。經驗上，單一函式或程式碼區塊若接近 200 行，往往已超出人類在短時間內能有效理解的範圍。

簡潔的程式碼讓閱讀者在第一時間掌握主要邏輯。這種可讀性並不只是風格問題，而是降低錯誤與盲點的重要機制。在大型資訊系統中，沒有任何人能同時記住所有模組、變數與控制流程。過長或過度複雜的程式碼會讓審閱者失去整體視角，使注意力停留在局部細節，而忽略系統層級的設計問題。

版本控制工具也應該用來維持程式碼結構的清晰。例如透過 git branch 管理不同開發方向，利用 git cherry-pick 挑選必要變更，並透過互動式 rebase 重新整理 commit 歷史。良好的 commit 結構可以讓審閱者理解每個變更的動機與脈絡，也讓未來的維護者更容易追蹤問題來源。

- [ ] 審閱者的角度

程式碼審閱的主體目標不是盲目挑出錯誤，而是思考如何讓程式碼更好。審閱者應以「我們如何讓這段程式碼更好」為出發點，而不是單純指出問題。這種態度將審閱視為合作過程，而非批評個人能力。

在健康的工程文化中，批評並不是負面的行為。重要的是批評的對象必須是程式碼，而不是作者。清楚說明審閱意圖可以避免誤解，也能讓討論更聚焦於技術本身。

正向回饋同樣重要。當審閱者指出良好的設計或清晰的實作時，能提升團隊的信心與動力，也有助於建立共同的品質標準。

審閱時應避免預設作者的動機。假設對方沒有閱讀文件、或假設對方刻意忽略某些原則，往往會讓討論偏離技術問題。比較有效的方式是直接指出觀察到的問題，並詢問設計考量。

- [ ] 範例

其中一個常見問題是評論過於簡短，沒有清楚說明問題。例如只問「bool 還是 int」，雖然指出型別選擇可能有問題，但沒有說明為何這是一個問題，也沒有提供建議。這樣的評論容易造成困惑，作者可能無法理解審閱者真正關心的是語意表達、效能，還是 API 設計。

另一個常見情況是評論缺乏動機與具體說明。例如只寫「請閱讀 [Google Python style guidelines](https://google.github.io/styleguide/pyguide.html)」。這樣的回應既沒有指出違反哪一條規範，也沒有說明為何這段程式碼需要修改。更糟的是，它可能暗示作者沒有閱讀文件，容易造成不必要的摩擦。

在某些情境下，簡短的評論是合理的。如果審閱者與作者都具備相似經驗，或之前已討論過同類問題，簡潔建議即可。例如指出應避免單一字元變數，並建議使用 board_size 或 size。這樣的評論直接且具體。

較好的審閱範例通常具備幾個特徵。首先會說明動機，例如為何要採用某種寫法。其次使用「我們」這樣的語氣，強調團隊合作。最後會提出可行的解決方案，而不是單純下達命令。例如建議將題目描述移至 Markdown 文件，並說明這樣做能改善排版並方便分享。

- [ ] 討論

有效的程式碼審閱需要控制討論範圍。過多或過長的討論往往降低效率。理想情況下，討論應聚焦於單一主題，避免在同一串對話中不斷切換議題。

參與討論的人數也應適度。過多參與者會讓意見分散，難以形成結論。通常由理解相關模組、或在該領域具備經驗的工程師參與審閱，能更有效率地找出問題並提出可行建議。

> Google 公司提供的 [Technical Writing Courses](https://developers.google.com/tech-writing) $\to$ ==Every engineer is also a writer.==

- [ ] 技術寫作的主體目標

技術文件的首要目標是讓讀者快速理解內容，而不是展現語言技巧。

清晰表示讀者可以迅速理解句子所表達的意思，而不需要反覆閱讀。簡潔則表示去除不必要的詞語與冗餘結構，使資訊密度提高。技術文件若過於冗長，讀者往往會跳過段落，甚至直接放棄閱讀。

在大型軟體系統中，文件與程式碼同樣重要。清楚的文件能降低團隊溝通成本，使工程師在沒有同步討論的情況下仍能理解系統設計。這也是 "Every engineer is also a writer" 的語境。

- [ ] 句子層級的寫作原則

技術寫作首先必須改善句子的可讀性。主動語態通常優於被動語態。主動語態更直接，也更容易指出動作的主體。例如
> The system writes the log file.

比
> The log file is written by the system.

更清楚。

句子應盡量只包含一個主要概念。如果一個句子同時描述多個邏輯關係，理解難度會快速上升。將複雜句拆分成數個簡單句，往往能顯著提升可讀性。

技術寫作也應避免冗長的開場語。例如
* This is to say that
* It should be noted that
* In order to

這些詞語通常不提供實際資訊，只會增加句子長度。

- [ ] 動詞與語意精確度

技術文件中的動詞應該具體且明確。模糊動詞會降低句子的資訊密度。

例如 perform, handle, deal with 這類動詞往往過於抽象。更好的做法是直接描述具體行為，例如 compute, parse, allocate, send 等。

具體動詞能讓讀者更清楚理解程式的行為，也能減少誤解。

- [ ] 術語與名詞一致性

技術文件必須保持術語一致。同一概念若在不同段落使用不同名稱，會增加理解成本。

例如若文件使用 thread 表示執行單位，就不應在其他段落突然改用 worker 或 task，除非這些詞確實表示不同概念。

另一個常見問題是過度使用代名詞。像 it, this, that 等詞若沒有明確指涉對象，讀者往往需要回頭尋找前文。技術文件通常應直接使用名詞，以避免歧義。

- [ ] 段落結構

每個段落應只討論一個主題，而且開頭句應該直接說明該段落的重點。這種句子通常稱為 topic sentence。

良好的段落結構可以讓讀者透過快速掃描理解文件內容，即使沒有逐字閱讀也能掌握主要概念。

段落之間應保持邏輯順序，例如先介紹背景，再說明問題，最後描述解決方案。清楚的結構能降低讀者理解系統的負擔。

- [ ] 清單與資訊結構

當一段文字包含多個並列概念時，清單通常比長句更容易閱讀。

如果項目之間存在順序關係，例如操作步驟，應使用編號。若順序不重要，則使用項目清單。

清單中的項目應保持語法一致。例如所有項目都以動詞開頭，或都以名詞片語開頭。這種平行結構能顯著提高可讀性。

- [ ] 讀者導向寫作

技術寫作的一個重要概念是讀者導向。作者在開始寫作之前，應先明確思考以下:
* 讀者是誰
* 讀者已經知道什麼
* 讀者需要知道什麼

這與程式設計中的抽象層概念相似。文件應該提供符合讀者知識層級的資訊，而不是將所有細節都放在同一份文件中。

工程師常遇到的問題是所謂的 knowledge curse。作者因為過於熟悉系統，會假設讀者也了解同樣的背景知識，導致文件省略必要說明。

- [ ] 自我編輯與修訂

寫作是一個反覆修訂的過程。初稿通常只是想法的整理，而不是最終版本。

有效的修訂通常包含幾個步驟。刪除冗餘文字、縮短過長句子、重新排列段落、檢查術語一致性，以及確認讀者能理解每一個步驟。這個過程與程式碼重構非常類似。好的文件往往經過多次修訂，逐步變得更清晰。

- [ ] 技術寫作與工程文化

在工程團隊中推動技術寫作訓練，目的並不是讓工程師成為作家，而是讓工程師能更清楚表達技術思想。

在大型軟體專案中，程式碼只是系統的一部分。設計文件、API 文件、commit message、code review comment 都屬於技術溝通。清楚的寫作能讓系統設計更容易被理解，也能讓工程成果被更多人使用與維護。

:::warning
以下不是「重點提示」，而是你該在作業中充分回答的各式問題。不該用「是」和「否」這樣二元的答覆，每題值得你重新檢視 C 語言規格書、Linux 核心原始程式碼及其 git log、(原本你該翻閱的) 微積分、機率和統計教科書、數學推理，和設計實驗來確認你的認知。
這些問題也可能在你日後參加科技公司面試時出現，現在就進行對應的準備。
:::

## 思索〈[分析「快慢指標」](https://hackmd.io/@sysprog/ry8NwAMvT)〉
* 設計實驗並在 GNU/Linux 比較文中二個演算法的 cache 行為。
    * 如何在 Linux 上建立長度可控制的鏈結串列（例如 $10^4$、$10^6$、$10^8$）？
    * 如何避免節點在記憶體中連續配置（例如使用 `malloc` + 隨機排列）？
    * 如何使用 [perf stat](https://hackmd.io/@sysprog/linux-perf) 測量： `perf stat -e cache-references,cache-misses,cycles,instructions`
    * 思考 cache miss rate 是否隨 linked list 長度增加而擴大？
* 如何觀察 temporal locality？
    * 如何使用 `perf record` + `perf report` 分析 memory access pattern？
    * 是否可以利用 `perf c2c` 分析 cache line 使用？
* 在 Linux 核心程式碼中，有哪些 commit 明確提到 cache locality，並類似本文的方式提出改進？(提示: slab, rbtree, runqueue)
* Linux 核心存在大量 linked list traversal，是否有對應的 commit 改進節點走訪的效率？請探討並提出自己的改進方案 (之後可貢獻回 Linux 核心)
* 如何建立數學模型來預測 traversal latency？例如 $T = N \times (L_{mem} + L_{miss})$，其中 $L_{mem}$ = memory latency 和 $L_{miss}$ = cache miss penalty，當建立理想模型後，對照上述的 perf 結果並進行分析

## 細讀〈[你所不知道的 C 語言：數值系統篇](https://hackmd.io/@sysprog/c-numerics)〉
* 教材以 `0.1 + 0.2 ≠ 0.3` 作為引言，說明電腦的數值表示問題，援引 IEEE 754 規格和你在電腦上的實驗，充分回答以下:
    * 為何十進位的 `0.1` 無法在二進位浮點數中精確表示？用 Graphviz 或類似的向量繪圖表示法，清晰展現數值表示的過程和限制
    * IEEE-754 單精度或雙精度為例，說明 sign, exponent, mantissa 在表示 `0.1` 時會發生什麼情況。
    * 文中指出浮點數加法不具有結合律，從 Linux 核心的原始程式碼 (事實上使用定點數，但具備浮點數運算的特性) git log 找出對應的浮點數運算考量並充分討論
* 針對 balanced ternary 和 radix economy
    * 電腦科學家 Donald E. Knuth 在《The Art of Computer Programming》第 2 卷說 "Perhaps the prettiest number system of all is the balanced ternary notation"，其背景考量是什麼？Knuth 是否有對應的著作進一步探討？
    * 為何 balanced ternary 中求負數只需「符號反轉」？與二補數 (two's complement) 表示法相比，分析計算成本、硬體實作，和數值對稱性。建立數學模型並討論
    * 說明為什麼低位元量化 (例如 ternary / 1-bit LLM) 在 AI 硬體中具有潛在優勢。參照提及的論文，描述其關鍵考量 $\to$ 歡迎協作 [BitMamba.c](https://github.com/jserv/bitmamba.c)
* 算術運算可完全以數位邏輯實作，分析 $x + y = (x \oplus y) + ((x \& y) << 1)$ 並回答：
    * 參閱數位邏輯教科書 (善用圖書館資源)，在硬體加法器中 `x ^ y` 和 `x & y` 各代表什麼訊號？並摘錄書中對應的描述，探討其應用場景
    * 為何 `(x+y)/2` 可能造成 overflow？又為何 $(x \& y) + ((x \oplus y) >> 1)$ 可避免 overflow
    * 在 Linux 核心中，為何這類 bit-level reasoning 對於效能與正確性非常重要？在 git log 找出對應的改進和修正
* `x & (x - 1)` 可用來檢測什麼數值性質？給出數學推導，說明為何此技巧成立。Linux 核心中有哪些場景會利用 power-of-two (2 的冪，[不是「冪次」](https://hackmd.io/@sysprog/it-vocabulary)) 性質？為何 power-of-two 對於系統效能特別重要？
* `((X) - 0x01010101) & ~(X) & 0x80808080` 技巧可用於 `strlen()` 的實作，回答：
    * 該巨集偵測的是什麼資料？為何該運算可一次檢測 4 個位元組？為何這比逐 byte 檢查更有效率？
    * 在 Linux 核心原始程式碼中找出類似 word-at-a-time 手法的案例，並充分進行效能分析
* 教材提及若干真實案例，以 Boeing 787 的[軟體缺失案例](https://hackmd.io/@sysprog/software-failure)來說，為何 32 位元計數器在約 248 天會 overflow？參照 FAA (Federal Aviation Administration ) 和相關官方事故分析報告進行探討
    * 在 Linux 核心的 git log 找出類似的 integer overflow 案例並探討
    * 在 C 語言規格書列舉相關整數範圍的規範和實作考量

## 細讀〈[你所不知道的 C 語言: bitwise 操作](https://hackmd.io/@sysprog/c-bitwise)〉
* 為何 Linux 核心程式碼通常會將用以描述硬體狀態 (例如 [x86 的 CR 系列暫存器](https://wiki.osdev.org/CPU_Registers_x86)) 的旗標 (flag) 型態定義為 unsigned 整數，而非 signed 整數？從 padding bits、trap representation 與 C 語言標準行為說明原因
* 若錯誤地使用 signed int 來儲存旗標並進行位移運算，可能出現哪些實作相依（implementation-defined）或未定義（undefined）行為？結合右移與負數的例子說明，搭配 C 語言規格書描述
* 在 Linux 核心中，若某個欄位同時承載 pointer 與 flags（例如最低幾個 bit 作為 flag），程式設計者通常會如何利用 bitwise 操作來拆解這些資訊？參照〈[Linux 核心的紅黑樹](https://hackmd.io/@sysprog/linux-rbtree)〉並在 Linux 核心原始程式碼找出更多案例。若程式碼在不同架構（例如 32-bit 與 64-bit）上編譯，這種技巧可能帶來哪些可攜性問題？請討論 alignment 與 pointer size 的影響
* 當 signed 與 unsigned 整數混合運算時，signed 數值會轉換為 unsigned，導致意外結果，例如比較運算結果顛倒。分析以下程式片段可能導致無窮迴圈:
    ```c
    int n = 10;
    for (int i = n - 1; i - sizeof(char) >= 0; i--)
        printf("%d\n", i);
    ```
    * 以 C 語言規格，逐步說明此程式產生無窮迴圈的原因，特別是 sizeof 的型態與整數提升（integer promotion）的影響
    * 若這段程式出現在 Linux 核心的 memory allocator 或 buffer traversal 程式碼中，可能造成什麼類型的 bug？在 git log 找出類似案例並探討
* 教材展示影像處理程式中使用 bitwise 操作拆解 RGBA pixel，將此概念延伸到 Linux 系統軟體：
    * 若 framebuffer driver 使用 32-bit RGBA pixel 格式，請說明如何用 bitwise 操作快速取得 R、G、B、A 四個分量，並在 Linux 核心原始程式碼找出類似的案例 (提示: V4L2)
    * 為何程式常用位移與遮罩（mask）而非結構體欄位來解析 pixel？從 C 語言規格來探討
    * 若要在 CPU cache 與記憶體頻寬受限的嵌入式系統中處理影像，位元操作與 lookup table 為何能顯著改善效能？
* 推導為何 $abs(n) = ((n >> 31) ^ n) - (n >> 31)$ 能正確計算絕對值，回答:
    * 這種 branchless 技巧在 Linux 核心程式碼中特別重要？提供數學分析和產生的機械碼作為解說
    * 在現代 CPU 的 branch predictor 與 pipeline 存在的情況下，branchless 寫法仍然有優勢嗎？請分析可能的情境。搭配 Linux 核心的 git log 來解說

## 分析〈[類神經網路的 ReLU 及其常數時間實作](https://hackmd.io/@sysprog/constant-time-relu)〉
* 教材提及利用 `union` 與位移運算實作 ReLU 的方法，其概念是利用浮點數與整數共用記憶體，藉由檢查 sign bit 判斷輸入是否為負數，並建立遮罩完成條件選擇，回答以下:
    * 該實作依賴 `int32_t` 的算術右移行為來複製 sign bit。請說明為何在大多數現代處理器上此方法可行，但在 C 語言標準層面仍存在未完全保證的行為。列舉 C 語言規格書內容和處理器指令的語意 (semantics)
    * 在 Linux 核心中，若要撰寫類似依賴位元語義的程式碼，通常會如何避免 implementation-defined behavior？請舉出 Linux 核心中常見的做法，例如使用特定型別、巨集或輔助用函式
    * 倘若 ReLU 函式需要被納入 Linux 核心的數值處理路徑中，例如某種 AI 推論模組，請討論 Linux 核心開發者是否會接受 union 型別轉換的寫法，還是傾向其他方式。說明理由並提出替代實作
* 藉由位元操作可達成 branchless 計算，即避免使用條件分支來判斷 `x < 0` 的情況，回答以下:
    * 在現代 CPU pipeline 中，branchless 實作可能比條件分支更快。說明造成此現象的原因，並討論 branch predictor 在其中的角色。設計實驗並用 perf 驗證
    * [Linux 核心中的 `min()` 和 `max()` 巨集](https://hackmd.io/@sysprog/linux-macro-minmax)如何實作，其考量是什麼？
    * 考慮上述程式碼在具備 SIMD 的處理器使用，如 AVX 或 RISC-V Vector extension (RVV)，branchless 設計會可帶來什麼額外優勢？提供程式碼和相關分析
* ReLU 其一特性是產生稀疏輸出，也就是負值會被截斷為零，導致許多節點沒有貢獻。在 Linux 核心中，找出類似稀疏化帶來效能優勢的案例 (提示: git log) 並充分探討
* 利用 union 共享記憶體，使 `float` 與 `int32_t` 可直接存取相同位元表示，該技巧本質是種 type punning。請解釋 strict aliasing rule 與此技巧之間的關係。
    * 在 GCC 或 Clang 編譯 Linux 核心時，為何 Linux 核心程式碼仍能安全地使用某些 type punning 手法
    * 若在使用者空間程式中需要安全地取得浮點數的 sign bit，請提出至少二種做法，並比較其可攜性與效能

## 分析〈[從 √2 的存在談開平方根的快速運算](https://hackmd.io/@sysprog/sqrt)〉
* 在 Linux 核心中，由於浮點運算通常不可用，許多數值計算必須使用整數或固定點數實作，例如 `int_sqrt()` 或 digit-by-digit 類型的平方根演算法。回答以下:
    * 假設你要在 Linux 核心中實作 `isqrt()` 函式，用來計算 32 位元整數的平方根。分析以下在核心環境中的可行性與成本: 1) 二分逼近法; 2) 牛頓法; 3) digit-by-digit 方法
    * 在 Linux 核心環境中不能使用浮點數的情況下，牛頓法需要哪些改寫才能安全使用？詳盡探討固定點數或整數除法可能帶來的誤差來源，以及迭代停止條件該如何設計
* Linux 核心常要求演算法具備 [predictable execution time](https://en.wikipedia.org/wiki/Worst-case_execution_time)，比較二分逼近法和牛頓法在最壞情況執行時間 (WCET) 上的差異，並說明何者更適合即時 (real-time) 系統。
* 假設輸入值來自不可信來源 (例如網路封包解析)，設計安全版本的 `isqrt()`，並說明如何避免整數溢位、除以零，和無限迴圈
* 教材說明固定點定理以及 contraction mapping 條件，並指出若函數導數滿足 $|g'(x)| < 1$，則迭代序列會收斂到唯一固定點。將此概念延伸到系統程式設計的情境：
    * 在 Linux 核心中，許多子系統藉由 feedback control 調整系統狀態，如 CPU frequency scaling, TCP congestion control, memory reclaim 等，選擇其中一機制，說明其更新規則為何可視為固定點迭代過程。提供數學模型和對應程式碼分析
    * 設計自動調整 CPU load balancing 參數的機制，請提出簡單的迭代更新公式，並分析其收斂條件
* 教材討論固定點迭代的收斂階數 (order of convergence)，並指出牛頓法具有二次收斂，而一般固定點迭代通常只有線性收斂。假設數值演算法每次迭代的成本為 (C)，而收斂速率可為線性收斂和二次收斂，在實際系統中何者可能更有效率，並考慮每次迭代的計算成本、分支預測，及 cache locality
* 在 Linux 核心中，有些演算法會刻意避免 division，而改用 bit shift 或查表。說明：
   * 為何 division 在某些架構上特別昂貴，搭配 git log 來解讀
   * 這如何影響數值演算法設計
* 針對 digit-by-digit 的平方根計算方法，該方法只需加減與位移運算 。為何該方法特別適合 Linux 核心？若你要為 RISC-V 架構設計新的 `sqrt` 指令，digit-by-digit 方法與牛頓法何者更適合作為硬體微架構 (microarchitecture) 的基礎？請說明原因。
* 教材展示某些固定點迭代可能會發散甚至產生 `nan` 的案例，回答:
    * 在系統程式設計中，數值演算法發散可能造成哪些實際問題，例如 scheduler decision 和 network congestion control，以 Linux 核心原始程式碼進行探討
    * 說明為何在 Linux 核心程式碼有時會加入保護式界限(clamping)，並舉例說明其與數值穩定性的關係

## 探討〈[Linux 核心原始程式碼的整數除法](https://hackmd.io/@sysprog/linux-intdiv)〉
* 針對 `#define DIV_ROUND_UP(n, d) (((n) + (d) - 1) / (d))`，回答以下:
    * 說明為何 `((n)+(d)-1)/d` 在 `n` 與 `d` 為正整數時可以實作上取整除法。請以歐幾里得除法表示式 `n = dq + r`，其中 `0 ≤ r < d`，以嚴謹的數學推導此巨集的正確性
    * 若 `n` 或 `d` 可能為負數，該巨集可能出現錯誤結果。請設計可在 Linux 核心中安全使用、同時仍盡量避免分支的版本，並說明設計考量
* Linux 核心原始程式碼提供 `do_div` 巨集，可在一次操作中取得 64 位元整數除法的商與餘數。回答以下：
    * 在某些架構 (例如部分 Arm 平台，缺乏 FPU) 上，編譯器可能將 64 位元除法轉換為呼叫 `__aeabi_uldivmod`。說明為何 Linux 核心會刻意避免依賴這類 libgcc 函式
    * 假設你正在實作 Linux 核心中的時間子系統，需要頻繁將奈秒 (ns) 轉換為毫秒 (ms)，討論以下實作方式的優缺點： a) 使用一般 `/` 運算子; b) 使用 `do_div`; c) 將除法轉換為乘法與位移
* Linux 核心 `vsprintf` 中的十進位轉換實作會避免直接使用除法，而改用乘法與查表方式來提升效能。回答以下:
    * 為何 `/proc` 與 `/sys` 的輸出效能會影響整體系統效能？以實際的測試來說明
    * 假設你需要在 Linux 核心中實作頻率統計 (histogram) 輸出函式，每秒可能被呼叫數十萬次，則直接使用 `sprintf` 可能帶來哪些效能問題？為何查表法能改善效能？
* 某些特殊常數除數可以讓編譯器將除法完全轉換為單一乘法，例如： `⌊n / 274177⌋ = (n × 67280421310721) >> 64`，回答以下:
    * 為何這類除數被稱為「理想除數」？說明其數學背景
    * 假設 Linux 核心 scheduler 需要頻繁計算某個比例值，如 `scaled = load / 274177`，分析使用上述技巧可能帶來的效益與風險
    * 若你是編譯器設計者，會如何在最佳化階段自動偵測並套用此類轉換？

## 細讀〈[Linux 核心的 hash table 實作](https://hackmd.io/@sysprog/linux-hashtable)〉
* Linux 核心在雜湊表 bucket 中使用 hlist_head / hlist_node，而不是一般的 doubly-linked list。其節點結構如 `struct hlist_node { struct hlist_node *next, **pprev; }`，不難見到，`pprev` 不是指向前一個節點，而是指向「指向目前節點的指標」。該設計讓刪除節點時不需要知道 list head。回答下列問題：
    * 若改用典型雙向連結串列 (prev / next)，當刪除 bucket 中的首個節點時，為何必須額外傳入 list head？用 Graphviz 繪製指標關係圖說明原因
    * 說明 hlist 的設計如何消除上述特殊情況。解釋 `__hlist_del()` 的行為並探討其效益
* Linux 核心在 `hash_32()` 中使用乘法雜湊 `val * GOLDEN_RATIO_32 >> (32 - bits)`，其中 `GOLDEN_RATIO_32 = 0x61C88647` 是黃金比例相關常數。探討以下：
    * 解釋為什麼 Linux hash 函數會取「高位元」作為 bucket index，而不是低位元
    * 若 bucket 數量為 `2^p`，說明右移 `(32 - p)` 的數學意義
    * 假設系統中 key 值具有模式 `K, K + d, K + 2d, K + 3d, ...`，例如連續的 file descriptor 或 PID。說明為何使用 golden ratio 乘法可以減少 clustering。
* 設計實驗程式（使用 C 或 Python 皆可)，比較以下對 hash 分布的影響: 0x61C88647, 0x80000000, 0x12345678, 0x54061094 等常數，說明實驗結果與文件中的觀察是否一致。要求：
    * key 範圍：0 ~ 10000
    * bucket 數量：1024
    * 繪製 bucket occupancy 分布圖
    * 分析 collision 與 clustering 情形
* hlist 的其中一個設計目標是減少記憶體開銷，因為 bucket head 只需要一個指標，而不是雙向鏈結串列的二個指標。回答以下:
    * 假設 hash table 有 1,048,576 個 buckets，在 64 位元系統中，分別使用 `struct list_head` 和 `struct hlist_head`，需要多少記憶體？
    * 若該 hash table 用於 networking subsystem（例如 connection tracking），bucket 數量非常大但每個 bucket 的元素數量通常很少，說明為何 hlist 是更合理的設計
    * hlist 無法在 O(1) 時間取得 tail，討論在什麼情況下 Linux 核心仍會選擇 `list_head` 而非 `hlist`
    * 舉出 Linux 核心中二個實際使用 hash table 的子系統（例如 dentry cache、routing table 或 TCP connection lookup），並分析其 bucket collision 的行為會如何影響系統效能
* Linux 的雜湊表的設計實際結合三個層面的考量：1) 雜湊函數的統計性質; 2) 資料結構的記憶體布局; 3) CPU cache 與指標操作成本。回答以下：
    * 若 bucket collision 過多，查找時間將從期望的 $O(1)$ 退化為 $O(n)$，在 Linux 核心中，這種退化可能造成哪些實際系統效應？
    * 假設某個攻擊者可以控制輸入 key（例如 HTTP header 或網路封包欄位），並刻意製造大量 hash collision。說明這種攻擊如何影響系統效能，並舉出 Linux 或其他系統曾出現的類似案例 (提示: git log)
    * 設計改進方案，使雜湊表在碰撞過多時仍能維持穩定性能，應適度考慮 bucket resize, alternate hashing, tree-based bucket, randomized hashing 等手法，並分析這些方法在 Linux 核心中的可行性 (後續可提交貢獻到 Linux 核心)
* 教材提到 Fibonacci hashing 與 Three-gap theorem 的數學背景。回答以下:
    * 為何 Linux 核心實作 hash 函數時，偏好使用整數運算與 bit shift，而非浮點運算？
    * 將數學式 $h(K) = \lfloor m (KA - \lfloor KA \rfloor) \rfloor$ 轉換為 Linux 核心實際程式碼形式並解釋每個步驟對應的位元操作
    * 若系統由 32 位元架構改為 64 位元架構，hash 函數應如何調整？
* 把 `GOLDEN_RATIO_64` 放回環論語境，探討可逆性與雜湊不可逆性的差異
    * 在環 $R=\mathbb{Z}/2^{64}\mathbb{Z}$ 中，判定 `GOLDEN_RATIO_64` 是否為 unit。必須給出判定條件與理由 (提示: 奇偶性與 $\gcd(C,2^{64})$)
    * 若它可逆，說明你如何以擴展歐幾里得演算法求出 $C^{-1}\bmod 2^{64}$，隨後解釋即使乘法在 $R$ 中可逆，為何 `hash_64(val,bits)` 依然不可逆。你必須指出右移取高位元等價於丟棄資訊、丟棄的位元數量與 preimage 的大小關係，並把這點連結到雜湊表只需要分布性，而不需要可逆性

## 細讀〈[為什麼要深入學習 C 語言？](https://hackmd.io/@sysprog/c-standards)〉
* 在 Linux 核心原始程式碼和 git log，找出，哪些「編譯器行為差異」會被視為 bug，而非「容忍實作差」的案例
* object 與 pointer 的視角如何影響核心中的 API 契約？教材提及 object 是執行時期中「資料儲存區域」的語意單元，pointer 只是其存取表達 ，也點出 `void *` 與字元型別指標在表示法與對齊需求的一致性。回答以下：
    * Linux 核心的 `copy_from_user` 一類的函式中，若以「object 邊界」定義安全，應該如何表達契約？
    * 針對核心常見的巨集，如 `container_of`，從 object model 觀點分析它倚賴哪些假設、哪些假設其實屬於 compiler extension？
* 教材列出 C23 候選特徵例如 `typeof`, `call_once`, `char8_t`, `unreachable` 單參數 `_Static_assert` C++11 風格 attribute 二補數強制 binary literal `_BitInt` `#elifdef` 等，回答以下:
    * 從 GCC 手冊 (不能參照其他二手材料！) 挑出「核心早已有 GNU extension 對應物」的特徵，例如 `typeof` 對應 `__typeof__`,  `unreachable` 對應 `__builtin_unreachable`,  attribute 對應 `__attribute__`
    * 探討 `_BitInt(N)` 是否能改善 Linux 核心在不同處理器架構中，位元精準資料結構與 ABI 表述

## 探討〈[基於 C 語言標準研究與系統程式安全議題](https://hackmd.io/@sysprog/c-std-security)〉
* 文件提及 integer conversion rank 和 usual arithmetic conversions，在系統程式設計中，混合使用 `signed` 與 `unsigned` 型別是緩衝區溢位（buffer overflow）的常見根源。回答以下:
    * 參考 C11 標準 §6.3.1.8 (Usual arithmetic conversions)，當一個 `signed long` (64-bit) 與一個 `unsigned int` (32-bit) 進行二元運算（如比較大小或加法）時，標準規定具體會發生什麼轉型？這與 `signed int` 和 `unsigned int` 的情況有何不同？
    * 在 Linux 核心的歷史漏洞中，常見於 `access_ok(type, addr, size)` 或類似的記憶體範圍檢查巨集。假設開發者寫出 `if (user_len < 0 || user_len > MAX_LEN)`，但 `MAX_LEN` 被定義為 `unsigned` 常數，而 `user_len` 是 `signed`
    * 請編譯器（如 GCC）在產生組合語言時，會使用邏輯比較（`CMP` 指令後接 `JA/JB`）還是算術比較（`JG/JL`）？這如何導致負數的 `user_len` 繞過檢查並在後續 `copy_from_user` 中造成巨大的 kernel heap overflow？
    * 結合文件提到的 "wraparound"，當攻擊者控制 `size` 參數造成 integer underflow，這在核心層級（kernel space）的 `kmalloc(size)` 配置中，與使用者層級的 `malloc` 行為有何本質上的不同 (考量到 SLUB 配置器的行為)？
* C11 §6.2.4.2 關於物件生命週期的定義是，當物件生命週期結束，指標的值變為不確定 (indeterminate)，回答以下:
    * 在現代 C 語言編譯器模型（如 LLVM 的 [PNVI-ae-udi 模型](https://inria.hal.science/hal-02089907/file/n2363.pdf)）中，即使兩個指標 `p` (已釋放) 和 `q` (新配置) 的記憶體地址（數值）相同，它們在語意上是否相等？
    * 討論 Alias Analysis（別名分析）如何利用 "Strict Aliasing Rule" 或 "Object Lifetime" 假設，認定對 `q` 的寫入不會影響 `p` 指向的內容，進而對程式碼進行激進的最佳化 (例如刪除看似多餘的 null check)
    * 考慮以下程式碼:
    ```c
    if (ptr)
        free(ptr); // Object lifetime ends here
    // ... 複雜邏輯 ...
    if (ptr) // 攻擊點
        ptr->func_table->execute();
    ```
    根據 C 標準，存取已釋放的 `ptr` 是 Undefined Behavior (UB)。編譯器是否有權力假設「UB 永遠不會發生」，進而直接移除第二個 `if (ptr)` 的檢查（Dead Code Elimination），導致該程式碼無條件執行？這對漏洞防護機制的實作有何啟示？
* 文件分析 Exim 郵件伺服器自訂的 `store_pool` 機制，及 `store_extend` 函數邏輯錯誤導致的 UAF。回答以下:
    * Exim 選擇實作自己的 Block/Pool 管理器，而非直接依賴 `glibc` 的 `malloc/free`。從 Heap Layout 的角度分析，Exim 的這種連續記憶體 (chunking) 策略，與 `glibc` 的 `ptmalloc`（使用 bins, chunks, boundary tags）相比，哪種結構在發生 overflow 時更容易被利用來進行 "House of Spirit" 或 "Unlink Exploit" 類的攻擊？
    * Exim 的 `store_release` 只是移動指標，並未真正清除資料。這與 Linux 的 [RCU (Read-Copy-Update)](https://hackmd.io/@sysprog/linux-rcu) 機制中的 "Grace Period" 有何異同？
    * 該漏洞的關鍵在於 `store_extend` 失敗後，程式邏輯誤以為舊區塊仍有效，但實際上指標已指向被釋放 (或即將被重用) 的區域。對照 Linux 核心的 `krealloc` 函式實作，當 `krealloc` 原地擴充（resize in place）失敗而必須移動記憶體時，如何處理舊指標？Linux 核心如何避免類似 Exim 這種「舊指標指向已釋放區域」的 race condition？
* 文件 UAF 的緩解措施及 `stack-use-after-scope`。然而，開發者常嘗試手動清除敏感資料 (如密碼或 Key)，回答以下:
    * 依據 C11 §5.1.2.3 (Program execution) 的 "As-if" 規則，編譯器只需要保證「可觀察行為」（Observable Behavior）一致。若開發者在函式返回前處理 `memset(password, 0, len);`，隨後變數 `password` 脫離 Scope。解釋為何在較高的編譯器最佳化級別（`-O2` 或 `-O3`，編譯器會將這行 `memset` 視為無用程式碼並刪除？
    * 比較 C11 Annex K 引入的 `memset_s` 及 Linux 核心中的 `memzero_explicit`。這些函式在實作層面上使用哪些技巧 (例如 `volatile` 關鍵字或 memory barrier) 來強迫編譯器保留清除指令？這與文件中提到的「物件生命週期」概念有何衝突與妥協？

## 探討〈[你所不知道的 C 語言：記憶體管理、對齊及硬體特性](https://hackmd.io/@sysprog/c-memory)〉
* C 語言規格指出 `void *` 可與任何物件指標互相轉換，並且其 representation 與 alignment requirement 與 `char *` 相同，但 ISO C 不允許直接對 `void *` 進行 pointer arithmetic。從 C 語言型別系統與記憶體模型的角度，說明以下：
    * 為何 C 語言需要 `void *` 這種「無型別指標」(提示: C 語言規格書)？這種設計如何支援泛型資料結構（例如 `malloc`、鏈結串列、資料容器函式庫）？
    * 為何 ISO C 不允許對 `void *` 進行 pointer arithmetic，這反映什麼設計考量？
    * 為何 `void *` 可安全轉換為 `int *` 再轉回，但 `void *` 與 `void **` 的轉換卻可能導致未定義行為？
* Linux 核心程式碼中少用 `void *` arithmetic，而是轉型為 `char *` 或其他型別後再計算位址。說明考量因素並分析其與 strict aliasing rule 的關聯
* `malloc` 可能回傳有效指標，但實際的實體記憶體尚未配置，只有在程式首次存取該記憶體時才會真正配置 page。回答以下:
    * 說明虛擬記憶體 (virtual memory) 的基本概念，及為何使用者行程只能看到虛擬位址，硬體設計者的考量是什麼？
    * 解釋 demand paging 的運作流程，包含 page fault 發生後 Linux 核心需要進行的主要步驟
    * 為何 `malloc()` 的回傳值無法直接對應到保證記憶體一定可用？在什麼情況下首次存取記憶體可能觸發 OOM？
    * Linux 的 memory overcommit policy 為何允許系統配置超過實體記憶體容量的虛擬記憶體？該設計在伺服器系統與高效能運算環境中有哪些優缺點？以 Linux 核心原始程式碼內附的文件和原始程式碼進行解讀
* CPU 存取資料通常以 word 或 cache line 為單位，若資料未對齊可能需要多次記憶體讀取或額外硬體操作，回答以下：
    * 為何 CPU 偏好對齊的記憶體存取？以 4-byte integer 為例，說明 aligned 與 unaligned access 的差異，搭配 Graphviz 繪製記憶體佈局圖
    * 若一個 4-byte integer 位於 address `0x01`，CPU 可能需要執行哪些額外操作才能完成存取？
    * 為何 x86(-64) 架構通常允許 unaligned access，而某些 RISC 架構（如 ARM 或 RISC-V）可能需要額外指令甚至觸發例外？
    * Linux 核心提供 `get_unaligned()` 與 `put_unaligned()` 等工具函式，其設計目的為何？在跨平台核心程式碼中為何重要？
* 由於結構體與指標通常具有 alignment 保證，因此位址的最低幾個 bit 永遠為 0，可被用作額外資訊，例如在 [lock-free linked list](https://hackmd.io/@sysprog/concurrency) 中標記節點已被邏輯刪除。
    * 為何 alignment 可保證某些位元永遠為 0？若系統保證 8-byte alignment，最低幾個 bit 可以安全使用？
    * 為何 lock-free linked list 常使用 logical deletion 而非立即刪除節點？
    * pointer tagging 如何協助實作這種邏輯刪除機制？
    * Linux 核心中哪些資料結構或同步機制使用類似技術 (提示: RCU 或其他 lock-free container)？
* 說明 glibc `malloc` 設計的關鍵原理與其在多執行緒環境中的限制：
    * 為何 `malloc` 需要 arena 機制？它如何減少多執行緒競爭？
    * 為何 thread arena 通常使用 `mmap()` 而不是 `brk()` 取得記憶體？
    * 為何 fastbin 在 `free()` 時不會立即合併 chunk，而 small bin 與 large bin 則會？
    * 為何在[高度並行](https://hackmd.io/@sysprog/concurrency)伺服器程式中，glibc malloc 可能成為效能瓶頸？這也是為何出現 jemalloc、tcmalloc 等 allocator 的原因
* 教材提及的記憶體配置器屬於使用者空間的實作，但 Linux 核心並不使用 glibc `malloc`，而有自己的記憶體配置器，如 slub 與 `kmalloc()`。
    * 為何 Linux 核心不能直接使用 glibc `malloc`？
    * `kmalloc()` 與 `vmalloc()` 在記憶體配置方式與位址連續性方面有何不同？
    * slab / slub 為何對核心資料結構特別重要？
    * Linux 核心環境中，記憶體配置器的設計為何特別強調 deterministic behavior 與 cache locality？搭配 git log 來說明 Linux 核心的相關演化

## 細讀〈[C 語言的 bit field](https://hackmd.io/@sysprog/c-bitfield)〉
* 考慮以下程式：
    ```c
    struct { signed int a : 1; } obj = { .a = 1 };
    if (obj.a == 1) puts("one"); else puts("not one");
    ```
    教材中指出，輸出結果會是 `"not one"`，因為 `1-bit signed` 在二補數系統中只能表示 `{0, -1}`。因此當 `1` 被存入時，bit pattern `1` 會被解讀為 `-1`。 回答：
    * 為何 `signed int : 1` 只能表示 `{0, -1}`？自 C 語言規格書找出對應的描述
    * 若改為 `struct { unsigned int a : 1;};`，其語意會如何改變？
    * Linux 核心原始程式碼如何使用 C bit-field 來表示旗標？為何還有 set_bit(), clear_bit(), test_bit() 等操作？
* 說明在 Linux 核心中使用 bit-field 需要考慮到 1) ABI; 2) 編譯器差異; 3) 記憶體 layout 不可預測。並搭配 git log 舉例說明這些考量
* 教材提到 zero-width bit-field: `int : 0;`，其作用是強制下個 bit-field 對齊到新的 storage unit，分析以下:
    ```c
    struct foo {
        int a : 3;
        int b : 2;
        int : 0;
        int c : 4;
        int d : 3;
    };
    ```
    回答以下:
    * 在 C 語言標準中，`int : 0` 的語意是什麼？
    * 為何 `c` 與 `d` 可能落在不同的記憶體區域？
    * 為何在不同編譯器（例如 gcc 和 clang）中結果可能不同？
    * 以 C 語言規格的觀點，解釋教材聲明的「`c` 和 `d` 可能指向不同記憶體區域，因此結果可能不穩定」的根本原因
* Linux 核心在結構對齊上幾乎不用 zero-width bit-field，而是使用 `__aligned()` 或 `__attribute__((aligned))`，回答以下：
    * 為何 Linux 核心避免使用 zero-width bit-field？
    * 若在 Linux 核心中使用 bit-field 進行硬體暫存器映射，可能會出現什麼問題？以 memory-mapped IO (MMIO) 暫存器操作為例說明

* 教材提及 Linux 核心的技巧 `#define BUILD_BUG_ON_ZERO(e) (sizeof(struct { int:(-!!(e)); }))`，從 C 語言規格的角度回答以下:
    * `!!(e)` 的作用是什麼？為何 `-!!(e)` 可能變成 `-1`？為何 `int : -1` 會導致編譯時期的錯誤？
    * 為何 `int : 0` 是合法的？
    * 對應到 C11 以上的規格，有哪些替代方案？
* C11 規格指出，同一個結構體中的二個 bit-field 若位於同一記憶體位置，並行更新不安全。考慮 `struct flags { unsigned a : 1; unsigned b : 1; };`，假設 CPU~0~ 修改 `a` 且 CPU~1~ 修改 `b`，回答以下：
    * 為何這兩個操作可能發生 race condition？
    * bit-field 修改通常需要什麼指令序列？以 C11 (含之後) 規格書內文來解讀

## 練習題
> 逐一分析[第二週教材](https://wiki.csie.ncku.edu.tw/linux/schedule)列出的[題目-1](https://hackmd.io/@sysprog/linux2025-quiz2)、[題目-2](https://hackmd.io/@sysprog/linux2024-quiz2)、[題目-3](https://hackmd.io/@sysprog/linux2023-quiz2)、[題目-4](https://hackmd.io/@sysprog/linux2022-quiz2)，和[題目-5](https://hackmd.io/@sysprog/linux2021-quiz2)，確認理解題目且充分作答，並指出參考題解的錯誤和待改進之處

* `ldexpf` 的實作中，可用 `-!!(new_exp >> 8)` 產生全為 `1` 或全為 `0` 的 bitmask 來判斷 overflow，且不用條件分支，回答以下：
    * 說明 `!!x` 與 `-!!x` 在位元層級上的運作方式，為何可產生 `0x00000000` 或 `0xffffffff`？
    * 說明為何 Linux 核心中使用 branchless bit operations，而非 `if` 條件判斷，以 git log 舉例探討
    * 在 CPU pipeline 與 branch prediction 的角度，分析 branchless bitmask 技術可能帶來的效能優勢
* 利用 SWAR (SIMD Within A Register) 技巧可同時處理多個 byte，例如用於 `memchr` 的加速。回答以下：
    * SWAR 的原理是什麼？為何可在單一暫存器中同時處理多個位元組？
    * 利用 SWAR 來加速 Linux 核心原始程式碼的字串處理函式 (之後可貢獻回 Linux 核心)，務必詳盡測試並確認效益
* CRC 計算本質上是 mod 2 polynomial division，並可用 XOR 取代加減運算。回答以下：
    * 為何 CRC 的多項式運算可以用 XOR 取代加減？
    * 說明 CRC polynomial 的 bit representation 與 GF(2) 之間的數學關係
    * LSB-first CRC 計算需使用 reversed polynomial。說明其原因
    * Linux 核心中 CRC 的實作常見於 `lib/crc32.c` 和 `lib/crc-ccitt.c`，說明二者實作策略的差異
    * 若要設計 bit-field friendly CRC pipeline，如何利用 `crc = (crc >> 1) ^ (-int(crc & 1) & POLY);` 技巧降低運算成本？
* Linux CPU 排程器的 PELT 使用 EWMA 並透過位元操作實作衰減計算，其設計目標是 `y^32 = 0.5`，回答以下：
    * Linux 核心如何避免使用浮點數？
    * PELT 為何將 $y^n$ 轉換為 $(1/2)^{n/32}$ 的表示方式？
    * Linux 透過 `mul_u64_u32_shr()` 完成定點數乘法，說明其設計原理並從 C 語言規格書觀點解說
    * 說明 `val = mul_u64_u32_shr(val, runnable_avg_yN_inv[n], 32);` 的數學意義
    * 為何 CPU 排程器的 EWMA 必須保持 deterministic fixed-point arithmetic？搭配 Linux 核心原始程式碼和數學模型來解說

## 回顧期初測驗
針對「Linux 核心設計」[第 3 週測驗題](https://hackmd.io/@sysprog/linux2026-quiz3)，挑出至少 3 個題目群組，應當涵蓋 CPU 排程、資訊安全，還有電腦網路議題。除了給定的題目 (及延伸問題)，你該依據自身的理解，提出問題並充分討論。

## :penguin: 作業要求
* 研讀[第二週教材](https://wiki.csie.ncku.edu.tw/linux/schedule)的「所有」內容，紀錄你的發現和提問，並且針對上方的要點和對應到教材的提問，完整回覆，要以教材和 C 語言規格書、Linux 核心原始程式碼其及 git log、分科課程的教科書為主要參照，左以你的觀察、實驗、推測
    * 參照〈[提問的智慧](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way)〉，清楚描述你的疑惑，必須明確標注脈絡 (context) 和你做了哪些分析和實驗，附上相關的公開素材
    * 針對個別教材，在筆記建立 [Heading level 2](https://www.markdownguide.org/basic-syntax/) (即 `##`) 並羅列教材標題，隨後闡述問題和你的回覆，避免過多的縮排層級 (level)，使用 **`- [ ]`** 標注問題 $\to$ [示範用的筆記](https://hackmd.io/@sysprog/sample-linux-notte)
    * 針對 [2026-03-03/10 問答簡記](https://hackmd.io/p87SQ6WpT-ehlVhXglXk9w) 的討論，提出自己的認知並更新於該筆記
    * 過程中，你可能會遇到問題，請善用[課程討論區](https://www.facebook.com/groups/system.software2026)
* [HackMD](https://hackmd.io/) 筆記作為開發紀錄，必須嚴格依循上方的「筆記書寫規範」，且符合如下:
	* 標題格式固定為 ==2026q1 Homework2 (stdc)==，其中 "stdc" 是小寫，**2026q1** 表示「2026 年第 1 季」
	* 共筆內容的第二行則為 **contributed by < `你的GitHub帳號名稱` >**，務必確保你的 GitHub 帳號是有效的
	* 共筆內容的第三行僅留換行符號，第四行是 ==`{%hackmd NrmQUGbRQWemgwPfhzXj6g %}`== 並確保「作業書寫規範」正確顯示
* 課程助教預計在 3 月 13 日，針對每位選課的學員，從 ==[Homework1 作業區](https://hackmd.io/@sysprog/linux2026-homework1)== 挑出 5 位學員，逐一發信通知，若你在 3 月 14 日中午尚未收到如此的信件，請聯繫授課教師，當然若你願意額外評論其他同學，也歡迎。針對其他學員的開發紀錄，請編輯內文，加上 `Reviewed by 你的GitHub帳號名稱` 的段落，參見: [示範的 Review-1](https://hackmd.io/@r36EKfH2TwalEWG_fUuSyg/linux2024-homework1) 和 [示範的 Review-2](https://hackmd.io/@jason50123/linux2024-homework1)，你的總結意見要寫在共筆的最上方，僅次於 "contributed by"。要從以下方面探討:
    - 回覆給定題目的完整程度、是否參照權威材料去解讀和推理、是否設計實驗去驗證、論述和後續討論，落實上述 "Code Review" 提出的原則
	- 實驗設計的不足處、涵蓋程度是否全面，以及後續的改進空間
	- 共筆行文是否流暢且具體，結構規劃是否清晰，且以第一手材料為主要依循，並細緻驗證 $\to$ 台大電機系李宏毅教授對於 ChatGPT 的看法是，要善用人工智慧的成果，一旦人們得以善用，人類的書寫不該比 GPT 一類的大語言模型差。
	- 斟酌在選定的 GitHub repository 留下 code review 意見。
	- 嘗試回覆學員提出的問題。
	    > :information_source: 及早提交對學員的意見並藉由 HackMD 平台互動
	    > :warning: 不必擔心得罪人而刻意用委婉或模糊的詞彙，如此非但不利於有效溝通，還可能導致真正的訊息丟失。關鍵是不要過分拘謹於形式，若因你沒有直接說出問題，導致他人錯失學習機會，那才是真正的失禮 —— **真誠地分享你的專業知識，讓溝通能夠達到共鳴，才是真正展現禮貌的方式**。
* 應適時回應授課教師和其他同學在你羅列於 [Homework1 作業區](https://hackmd.io/@sysprog/linux2026-homework1) 的共筆中所做的評語意見、建議，和提問。你可趁這個機會，在其他學員的共筆提交相關疑惑
* 填寫 [Google 表單](https://forms.gle/yJEE2EsXCkms6vVJ6)，填入個人資訊和你建立的 HackMD 筆記的超連結，並回答指定問題。一旦系統確認你的提交內容，你的作業預期會出現「[作業區](https://hackmd.io/@sysprog/linux2026-homework2)」
    > :warning: 不用等到作業完成才填寫表單，當你開始進行作業時，即可填寫表單，系統會進行必要的檢查工作。某些問題的回答較費時，務必及早開始
* 本課程鼓勵學員相互觀摩，從而進行良性互動及批評，但要注意以下:
    * 當你參照其他學員作業的材料時，應該指明出處並加上對應的超連結
    * 善用 HackMD 的留言功能，在其他學員的筆記內文，留下你的想法、指出錯誤，和提及你對此的改進等等
