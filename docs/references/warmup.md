> **原始出處：** https://hackmd.io/@sysprog/linux2026-warmup
> **擷取日期：** 2026-02-26
> **用途：** 2026q1 第 1 週作業 (warm-up)
> **涵蓋度：** 完整
> **省略內容：** 無

---
title: 2026 年 Linux 核心設計課程作業 —— warmup
image: https://i.imgur.com/robmeiQ.png
description: 做好探索 Linux 核心的準備
tags: linux2026
---

# warm-up

> 主講人: [jserv](https://wiki.csie.ncku.edu.tw/User/jserv) / 課程討論區: [2026 年系統軟體課程](https://www.facebook.com/groups/system.software2026/)
:mega: 返回「[Linux 核心設計](https://wiki.csie.ncku.edu.tw/linux/schedule)」課程進度表

:::info
* 請在 2 月 28 日 13:00 重新整理本頁面，會有提交作業的相關描述
* 繳交期限: 3 月 11 日
:::

## :memo: 預期目標
* 理解實數到離散數值系統的權衡，以及 Linux 核心作為資訊科技的縮影，如何引入工程手法來解決問題
* 充分檢視第一週教材
* 誠實面對自己：缺什麼就補什麼

## :rocket: 檢查清單
* 確認購買指定的教科書《[Computer Systems: A Programmer's Perspective](https://hackmd.io/@sysprog/CSAPP)》，紙本或電子書、英文和簡體中文版都可，==不得使用盜版==，一旦發現，授課教師將委託律師處理 $\to$ 你今天若不尊重他人的智慧財產，來日你憑什麼要求他人尊重你的成果並支付合理薪酬？
* 做好前 6 週每週投入 16 小時的準備並落實
* 認清「[寫作業才是主體](https://docs.google.com/presentation/d/1LIP64FQRa9J34ks9rKPmXmNQ-ZhL91qfB9KkF2nr30g/edit?usp=sharing)」的教學方式
* 充分閱讀教材、紀錄認知和提問，並回覆給定的延伸問題

## 筆記書寫規範
* 共筆書寫請考慮到日後協作，避免過多的個人色彩，用詞儘量中性
* 不要在筆記內加入 `[TOC]` : 筆記左上方已有 Table of Contents (TOC) 功能，不需要畫蛇添足
* 不要變更預設的 CSS 也不要加入任何佈景主題: 這是「開發紀錄」，主要作為是評分和接受同儕的檢閱，不是彰顯「個人風格」的地方
* 當[在筆記中貼入程式碼](https://hackmd.io/c/tutorials-tw/%2Fs%2Fhow-to-use-code-blocks-tw)時，避免非必要的行號，也就是該手動將 `c=` 或 `cpp=` 變更為 `c` 或 `cpp`。行號只在後續討論明確需要行號時，才要出現，否則維持精簡的展現。可留意「[你所不知道的 C 語言: linked list 和非連續記憶體](https://hackmd.io/@sysprog/c-linked-list)」裡頭程式碼展現的方式
* HackMD 不是讓你張貼完整程式碼的地方，GitHub 才是！因此你在開發紀錄只該列出關鍵程式碼 (善用 `diff` 標示)，可附上對應 GitHub commit 的超連結，列出程式碼是為了「檢討」和「便於他人參與討論」，不是用來「假裝自己有付出」
    * 單頁 HackMD 筆記會有內容長度的限制，這也是為何作業規範強調要記錄你的洞見和關鍵程式碼，完整的程式碼該在 GitHub 儲存庫或 [gist](https://gist.github.com/) 出現。
* 留意科技詞彙的使用，請參見「[資訊科技詞彙翻譯](https://hackmd.io/@sysprog/it-vocabulary)」及「[詞彙對照表](https://hackmd.io/@l10n-tw/glossaries)」
* 避免過多的中英文混用，已有明確翻譯詞彙者，例如「鏈結串列」(linked list) 和「佇列」(queue)，就使用該中文詞彙，英文則留給變數名稱、人名，或者缺乏通用翻譯詞彙的場景。
* 不要濫用 `:::info`, `:::success`, `:::warning` 等標示，儘量用清晰的文字書寫。`:::danger` 則僅限授課教師作為批注使用
* 在中文敘述中，使用全形標點符號，例如該用「，」，而非 ","。注意書名號的使用，即 `〈` 和 `〉`，非「小於」和「大於」符號。
* 避免使用不必要的 [emoji 字元](https://en.wikipedia.org/wiki/List_of_emojis)
* 撰寫的過程中，可善用 ChatGPT 一類的工具，但需要明確標示並指出裡頭謬誤和不精確之處。搭配 [ChatGPT cheatsheet](https://quickref.me/chatgpt)
    * 台大電機系李宏毅教授對於 ChatGPT 的看法是，要善用人工智慧的成果，一旦人們得以善用，人類的書寫不該比 GPT 一類的大語言模型差。
* 可使用 ChatGPT 一類的人工智慧工具，但不得由 ChatGPT 產生整篇報告並直接張貼在 HackMD，相反地，你應該依據子主題書寫，並斟酌運用 ChatGPT 一類的人工智慧工具潤飾你的書寫內容，這些都該在 HackMD 的變更紀錄中可見 $\to$ 本課程不接受沒有完整編修紀錄的筆記，學員應當漸進更新並回應授課教師和學員的指教


## 探討〈[資訊科技詞彙翻譯](https://hackmd.io/@sysprog/it-vocabulary)〉
* "render" 在電腦圖學語境中為何應強調「如實呈現」？「渲染」一詞喪失什麼關鍵意涵？在 Linux 核心原始程式碼中，"render" 出現在哪些場景、語境又有哪些？
* 說明 constant 與 immutable 的差異，並探討程式設計中的關鍵考量
* 比較 concurrent 與 parallel 的語意差異，並說明為何「並行」較貼近 concurrent 的本意
* 當我們撰寫 Linux 核心文件，應如何區分 process, thread, task, job 等術語，才能避免跨領域誤解又省去過多的中英並陳？

## 細讀〈[GNU/Linux 開發工具](https://hackmd.io/@sysprog/gnu-linux-dev/)〉
* 確保 Linux 系統已正確安裝，且每天使用 (對比: 在游泳課買泳裝並下水)
* 學習 HackMD 的操作，並可正確使用 LaTeX。能夠在 HackMD 筆記中用 LaTeX 語法展現波函數和密度矩陣
* 學習 git 的操作，依據給定的教學錄影實際練習，並知曉 `git rebase` 一類命令的操作

## 探討〈[解讀計算機編碼](https://hackmd.io/@sysprog/binary-representation)〉
* 為何計算機的加法在固定 $k$ 位元下，本質等價於 $\mathbb{Z}/2^k\mathbb{Z}$ 上的加法？
* 為何「允許溢位」反而保證封閉性？若不允許溢位，會破壞哪些群的性質？
* 為何 $2^k$ 不為質數時，乘法不形成群？這和文件中質數模數的乘法表有何關聯？找出 Linux 核心相關的程式碼
* 為何 $x % 2^n \equiv x & (2^n - 1)$ 僅對 unsigned 或非負整數安全？從 CVE/CWE 找到相關資訊安全的議題
* 為何 sign extension 僅在「跨圓環」搬移時才有意義？從數學觀點解釋，要一般化相關證明
* 為何 Linux 核心中 unsigned overflow 是 defined behavior，但 signed overflow 是 undefined behavior？
* 為何 Linux 核心大量使用 unsigned long 作為時間計數器？
* 若模數改為質數 $p$，是否可構成有限域？這和 AES 中 $GF(2^8)$ 有何關聯？
* 二補數構成環但非域，這對除法有何限制？找出 Linux 核心原始程式碼對應的案例
* 二補數的設計是否本質上是種 algebraic encoding？
* 若將系統時間設計於 $\mathbb{Z}/2^{64}$ 上，其安全極限為何？
* 證明 $(\mathbb{Z}/2^k\mathbb{Z}, +)$ 為阿貝爾群，但 $(\mathbb{Z}/2^k\mathbb{Z}, \times)$ 非群

## 探討〈[你所不知道的C語言：指標篇](https://hackmd.io/@sysprog/c-pointer)〉
* 根據 C99 對 object 的定義，請分析以下程式是否具有未定義行為，並說明理由 `int *foo(void) { int x = 10; return &x; }`
    1. 若改成 `static int x = 10;` 結果是否改變？
    2. 請用「storage duration」與「lifetime」兩個術語解釋差異。
    3. 為何規格明確指出：
        > The value of a pointer becomes indeterminate when the object it points to reaches the end of its lifetime. 
* 以下程式的輸出為何？ `int a[3] = {1,2,3}; int *p = a; printf("%zu %zu\n", sizeof(a), sizeof(p));`
    1. 為何 array 在 expression 中會 decay 成 pointer，但在 sizeof 中不會？
    2. 為何 `&a` 與 `a` 的值相同但型態不同？
    3. 用 Graphviz 繪製記憶體示意圖說明以上
* 分析： `double x[3]; int *p = (int *)&x[0]; printf("%d\n", *(p+1));`
    1. 為何 pointer arithmetic 的單位取決於 type？
    2. 這是否涉及 strict aliasing 問題？
    3. 在 ARMv5 或 RISC-V 上可能出現什麼錯誤？
* 解釋為何以下程式不會改變 main 中的 ptrA： `void func(int *p) { p = &B; }` 並分析 `void func(int **p) { *p = &B; }`
    1. 用 call-by-value 解釋
    2. 用 Graphviz 繪製 stack frame 示意圖
    3. 為何「雙指標」這個說法在語意上不精確？
* 解釋為何以下程式合法： `int main() { return (********puts)("Hello"); }`
    1. 依據 C99 6.3.2.1 說明 function designator 的轉換規則。
    2. 為何 `*` 的數量不影響結果？
    3. 若對 function pointer 使用 `&` 會發生什麼？
* 從「儲存-執行模型」角度解釋 `int a = 10; char *p = (char *)&a;`
    1. CPU 實際做哪些事？
    2. 為何 C 語言可以被視為 assembly 的語法抽象？
* 考慮以下程式碼:
    ```c
    struct opaque;
    struct opaque *create(void);
    void destroy(struct opaque *);
    ```
    1. 為何可以只 forward declaration？
    2. 這如何達成 binary compatibility？
    3. 為何 incomplete type 只能搭配 pointer？
* 舉出一個程式碼案例，使得以下得以滿足，並用 C99 對 lifetime 的定義精確解釋
    * object lifetime 結束
    * storage 尚未被重用
    * pointer 仍保留原數值
    * 但 dereference 屬於 UB
* 以下程式在 -O2 下可能輸出什麼？
    ```c
    float f = 1.0f;
    int *p = (int *)&f;
    *p = 0;
    printf("%f\n", f);
    ```
    分析：
    1. 是否違反 strict aliasing？
    2. 若使用 `memcpy` 是否等價？
    3. 為何 C 規格允許 `unsigned char *` 例外？
    4. 在不同架構下是否行為不同？
* 為何以下二者 ABI 不同？
    ```c
    void f(int a[10]);
    void f(int *a);
    ```
    比較：
    ```c
    void g(int (*a)[10]);
    ```
    回答：
    1. 為何 `sizeof` 結果不同？
    2. 為何 `&a` 與 `a` 型別差異重大？
    3. 若跨編譯單元宣告不一致會發生什麼？

## 探討〈[linked list 和非連續記憶體](https://hackmd.io/@sysprog/c-linked-list)〉
* 從〈[資訊科技詞彙翻譯](https://hackmd.io/@sysprog/it-vocabulary)〉的角度，探討何以 linked list 翻譯為「鏈結串列」，而非「鏈表」或「連結串列」，而「串列」的詞源又在哪？翻閱詞典和二十世紀出版物來解說
* 教材中使用 `struct ListNode **indir = &head;`，描述以下:
    1. `indir` 的型別語意
    2. `*indir` 的語意
    3. `&(*indir)->next` 的語意
    並說明為何這不是「雙指標」，而是「指標的指標」 
* 考慮 `prev->next = (*indir)->next; free(*indir);`，分析：
    1. `*indir` 在哪一行失去 lifetime？
    2. 若先 `free` 再改鏈結會發生什麼？
    3. 為何 AddressSanitizer 能偵測？
    4. 若在 `-O3` 下編譯器是否可能出現指令的 reorder？
* 為何針對鏈結串列的節點走訪 (linked list traversal) 難以被 hardware prefetcher 預測？若使用 `__builtin_prefetch(node->next);` 是否一定改善效能？請記憶體存取圖形角度解釋，並從 git log 探討 Linux 核心的 List API 一度採用 prefetcher 又棄置的考量。
* 針對 Linux 的 merge sort 設計，回答
    1. 為何 list_sort 是 stable？
    2. 為何不使用 quicksort？
    3. 為何 merge sort 適合 linked list？
* Linux 核心的 `list_sort` 建構方式不同於 fully-eager bottom-up mergesort，回答
    * 推導 worst-case comparison 次數
    * 說明為何延遲合併可降低比較次數
    * 建立數學上界
* 鏈結串列的新增節點的時間複雜度是 O(1)，而陣列 (array) 則是 O(n)，但在實際硬體上，陣列可能更快，解釋為何如此並充分量化分析

## 細讀〈[Linux: 作業系統術語及概念](https://hackmd.io/@sysprog/linux-concepts)〉
* 若若一個惡意應用程式成功觸發多次系統呼叫並頻繁進入核心態，是否等同於繞過 user/kernel 隔離？分析：
    * CPU privilege level
    * page table 權限位元
    * 系統呼叫機制的作用和考量
* fork 作為並行流程的分岔點。假釋一個程式流程包含 $n$ 個 fork 點與 $m$ 個 join 點<推導在最理想無同步成本下，可產生的最大並行行程數上界。
* 若 fork-join 模型可抽象為 [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph)，請說明：
    * critical path 長度如何決定 theoretical speedup
    * 與 [Amdahl's law](https://en.wikipedia.org/wiki/Amdahl%27s_law) 的關係
* Mach microkernel 將 thread 與 task 分離為獨立物件。比較在 NPTL 之前的 Linux 核心 與 Mach 的設計，在 scheduling abstraction 上的本質差異，而引入 NPTL 之後又如何讓 Linux 具備現代作業系統的關鍵特徵？
* 若將 Linux 的 VFS 或 network stack 遷移至 userspace (類似 microkernel multi-server 模型，這在 hybrid kernel 不少見)，分析：
    * context switch 數量變化
    * cache locality
    * fault isolation
    * worst-case latency
* 若 page fault handler 的平均成本為 $T_{pf}$，page fault 發生機率為 $p$，建立整體存取延遲的期望值模型
* scalability 常來自 cache coherence 與 lock 競爭。給定全域計數器使用 spinlock 保護，
* 在 $N$ 核系統中，若每核每秒更新 $f$ 次，估算：
    * coherence traffic
    * lock contention 成長趨勢
* CPU 排程器是「一堆處理器」與「一堆行程」的多對多映射，在 time-sharing 下，$f : (P, t) \rightarrow C$ 是否應視為時間函數，翻閱經典論文來探討排程考量
* 教材以「卡比吸入能力」比喻 Linux 演化。從以下角度分析：
    1. abstraction preservation
    2. backward compatibility
    3. scalability pressure
    4. real-time requirement
    討論：
    * 為何 Linux 在 monolithic 架構下仍能持續擴展？
    * 哪些 abstraction 是演化關鍵？

## 探討〈[從熱力學第二定律到系統軟體：機率、資訊熵與現代作業系統的大融通](https://hackmd.io/@sysprog/from-entropy-to-os)〉
> 本文致敬《[Consilience: The Unity of Knowledge](https://en.wikipedia.org/wiki/Consilience_(book))》(繁體中文版《知識大融通》)

* 將文中提出三項宏觀穩定條件 (尾部可重現、吞吐時間序列分段平穩、排程誤差無長期漂移) 改寫為可被拒絕的統計假說
   * 明確寫出 $H_0, H_1$
   * 指出檢定方法（例如 ADF test、KPSS、two-sample KS）
* 指出文中 i.i.d. 假設在 CPU 排程的追蹤，何時不成立
    * 提供數學定義
    * 給出 CI 與顯著水準
    * 討論 Type I / Type II error
* 文件引用 M/G/1 的 P-K 公式 
    1. 嚴格推導 $E[W_q]$ 對 $E[S^2]$ 的敏感度
    2. 證明當 $\rho \to 1$ 時的發散階數
    3. 構造一個 lognormal 與 Pareto 分佈: 固定 $E[S]$、改變 $E[S^2]$，隨後比較 tail latency
* 針對 EEVDF 的 lag 有界性證明，即 $Lagi(t) = S_i(t) - s_i(t)$
    1. 在流體模型下證明 $\sum_i Lagi(t) = 0$
    2. 在離散 slice 條件下推導誤差界限
    3. 推導當 request length 改變時界限如何縮放
    4. 驗證 lag 分佈是否穩態
* 熵率優於單次熵 
    1. 對 `sched_wakeup` 和 `sched_switch` 事件序列，建立 n-gram 模型並計算 entropy rate
    2. 設計一個負載 regime change，並比較前後熵率
* 改進數學嚴格性和書寫
    1. 補充所有公式的前提條件
    2. 區分「方法論類比」與「數學等價」
    3. 明確說明適用範圍與失效條件

## 誠實面對[期初考題](https://hackmd.io/@sysprog/linux2026-quiz1)
> 進行所有延伸問題