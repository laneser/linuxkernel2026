> **原始出處：** https://hackmd.io/@sysprog/from-entropy-to-os
> **擷取日期：** 2026-02-26
> **用途：** 課程教材 — 從熱力學第二定律到系統軟體
> **涵蓋度：** 完整
> **省略內容：** 無

# 從熱力學第二定律到系統軟體：機率、資訊熵與現代作業系統的大融通
> 資料整理: [jserv](https://wiki.csie.ncku.edu.tw/User/jserv)

## 前言
傳統的電腦科學文獻往往將作業系統視為一組系統呼叫與程式碼的集合，探討行程 (process)、執行緒 (thread) 與 CPU 排程器 (scheduler) 的定義。然而，在面對真實環境中的尾端延遲 (tail latency) 與系統抖動 (jitter) 時，純粹的程式碼分析往往力有未逮。

本文的關鍵主張在於：作業系統不僅是軟體，更是個具備嚴謹數學結構、可量測，且受統計物理法則約束的動態系統。在可觀測的效能與競爭現象上，許多宏觀量呈現可用統計物理語彙描述的收斂與長尾，而非宣稱作業系統可被簡化為封閉的熱力學平衡系統。

本文將跨越學科界線，進行以下三項抽象映射與工程實踐：
1. 建立基於經驗分佈的穩定性公理：揚棄平均值迷思，將狀態空間概念映射至系統效能分析，建立基於分位數與信賴區間的尾端延遲量測規範
2. 數學化排程公平性：以流體近似與排程誤差 (Lag) 模型，解析 Linux 現代 CPU 排程器 (EEVDF) 如何解耦吞吐量與延遲，並定義其數學有界性
3. 確立密碼學的物理極限：以資訊理論中的最小熵 (min-entropy) 原則剖析系統亂數池，並從威脅模型角度評估硬體亂數指令的資安決策邊界

## 宏觀穩定性的可檢核定義與關鍵來源

穩定並非主觀感覺。在固定工作負載與量測邊界下，必須同時滿足：
1. 延遲分佈尾部形狀可重現
2. 吞吐量時間序列可分段視為平穩
3. 排程誤差分佈無長期漂移

此準則的有效性以工作負載描述可複現、且觀測窗口內近似平穩為前提。這三者若任一不成立，本文即宣告該系統在該工作負載下不具宏觀穩定性。

在 Linux 核心語境中，宏觀的延遲分佈並非單純 CPU 排程器的函式，而是二大核心子系統交錯後的統計投影：

- [ ] timekeeping 與 Tick 架構

量測的延遲分佈深受 tick 模式、`CONFIG_NO_HZ_IDLE`（tickless idle/dyntick-idle）與 `CONFIG_NO_HZ_FULL`（adaptive ticks/full dynticks）、及高解析度計時器 (high-resolution timers) 的影響。本文將 jitter (抖動)嚴格限定為在觀測事件邊界上的時間抖動，而非泛指所有不穩定。

- [ ] 記憶體回收對尾端的放大

實務上，tail latency 極常被記憶體壓力下的直接回收 (direct reclaim)、kswapd、writeback 或 dirty throttling 的擾動所主導。這類擾動極易被平均值掩蓋，使「熱力學到作業系統」的映射成為精確的工程因果，而非單純比喻。

## 標記法與基礎量測定義
> Notation & Measurement Primitives

在進入理論推演前，確立本文使用之測量原語與術語定義：

- [ ] 尾端延遲 (tail latency)

本文以互補累積分佈函數 (CCDF) 的尾部形狀與高分位數 (如 P99 或 P99.9) 描述 tail latency，並強調 tail 應視為整段尾部形狀而非單點數值。

CCDF (Complementary Cumulative Distribution Function)
定義為 $1 - \text{CDF}(x)$，在對數尺度 (log-scale) 下能有效放大並視覺化分佈尾部的衰減特徵。

- [ ] 延遲採樣點與事件邊界

延遲本質為隨機變數。本文規範常見的排程與系統延遲定義，混用將導致歸因錯誤：
* wakeup $\to$ enqueue：任務被喚醒到進入排程佇列 (受限於鎖競爭與中斷處理延遲)。
* enqueue $\to$ oncpu：在佇列中等待到實際獲得 CPU(反映 CPU 排程器本體的等待時間)。
* runnable $\to$ running：區分準備就緒與實際執行的精細邊界，對應 `sched_switch` 語意。
* wakeup $\to$ oncpu：端到端的總喚醒延遲。

- [ ] 對照延遲

引入 fork / exec 路徑延遲或 page fault latency 作為對照，避免將所有尾端延遲誤歸因於 CPU 排程器。

- [ ] On-CPU / Off-CPU 分析

將時間分解為 On-CPU 片段與 Off-CPU 阻塞時間，此為 eBPF 生態系中銜接 rolling quantile 與平穩性檢驗的常見分析手段。

- [ ] 量測工具

善用 Linux 核心提供的工具，如 `perf sched`、ftrace tracefs 及 eBPF tracepoints，以提升量測框架的可信度與原生操作性。

- [ ] bootstrap

分位數的抽樣分佈通常非簡單的常態近似，bootstrap 是在不強假設分佈形狀下的可行做法，用於計算高分位數的信賴區間。若樣本具明顯時間相依性（如排程或 I/O trace），應優先使用 block bootstrap 或 subsampling，而非 i.i.d. bootstrap。

### 符號與概念對齊總覽
> mapping table & scope

- [ ] 微觀狀態 (micro-states) 在作業系統的對應

Runqueue 狀態、排程 key 的排序關係、每核快取行擁有者、TLB 狀態、等待鎖集合，以及 IRQ 的到達時序。

- [ ] 巨觀可觀測量 (macro-observables)

延遲分佈、吞吐量時間序列、排程延遲的分位數、系統呼叫序列的熵率估計值。

- [ ] 模型 (model)

模型並非系統本身，而是由觀測設計與統計估計器共同定義的數學視角。模型改變，熵值與解釋隨之改變。

## 邊界條件提醒：熱力學第二定律的定位

本文並非宣稱作業系統遵循熱力學的形式推導，也非將 $dS = \delta Q_\mathrm{rev}/T$ 這種路徑定義硬套至軟體。本文是在借用巨大狀態空間下，宏觀量呈現方向性的方法論框架，亦即統計力學中的典型性 (typicality) 與體積支配 (measure concentration)，去說明為何工程上必須改用如此的語言形式。

本文採用的不可逆性語意，是指粗粒化後的宏觀量呈現方向性，而非指每個微觀方程不可逆。

## 從決定性路徑到統計大數法則

在擁有數十個 CPU core 的對稱多處理 (SMP) 機器上，每秒發生數百萬次的記憶體存取與上下文切換 (context switch)。放棄追蹤單次微觀事件的因果，改用分佈語言，其背後具備堅實的數學支撐：可重複觀測下的經驗分佈收斂。

![image](https://hackmd.io/_uploads/ByLs4Pdubg.png)
![image](https://hackmd.io/_uploads/S1X3EvOuWl.png)

Glivenko–Cantelli 定理在獨立同分佈 (i.i.d.) 假設下保證經驗累積分佈函數 (empirical CDF) 會均勻收斂至真實的 CDF(在特定弱相依條件下亦有對應的推廣版本)；而 DKW 不等式 (Dvoretzky–Kiefer–Wolfowitz inequality) 則在 i.i.d. 假設下給出有限樣本的 CDF 偏差絕對界限。這正是為何工程上能探討可重現的分佈形狀，並以有限樣本估計分位數。

### 尾端放大與排隊理論的敏感度來源
在 SLO/SLA 尾端敏感的服務情境中，平均值常是危險的摘要。在排隊理論的 $M/G/1$ 佇列模型中，Pollaczek–Khinchine(P-K) 公式揭示一項關鍵現象：
$$
E[W_q] = \frac{\lambda \, E[S^2]}{2(1 - \rho)}, \quad \rho = \lambda \, E[S] < 1
$$

平均等待時間 $E[W_q]$ 與服務時間的二階動差 $E[S^2]$ 直接相關 (此處 $\rho$ 為系統利用率，公式成立的前提是 FCFS 服務紀律且系統處於穩態 $\rho < 1$)。這意味著，在同樣的平均服務時間下，變異數越大或尾端越重，$E[S^2]$ 就越大，等待時間會被非線性地劇烈放大。

P-K 公式揭示的尾端敏感度機制，為微服務雪崩效應提供了直覺背書：在具備超時重試機制、上游退避策略不足、或下游服務接近飽和區 ($\rho \to 1$) 的前提下，極少數的 P99 慢請求會造成排隊延遲顯著放大，進而觸發重試，急遽增加系統總負載，導致尾端進一步變胖，最終引發系統崩潰。需注意，實際的重試風暴是多佇列回饋網路現象，超越單一穩態 $M/G/1$ 佇列的適用範圍，P-K 公式在此提供的是風險放大的機制直覺而非嚴格的因果證明。

### Linux 核心的四大長尾來源類別

在擁有多時間尺度或資源競爭時，CCDF 常呈現長尾特徵。Linux 核心導向的白皮書必須將抽象的長尾來源綁定至四個可驗證的關鍵現象類別：
1. Preemption 與 interrupt disabled 區段：某些核心路徑關閉搶佔或處於硬中斷上下文，會製造可觀測的尾端延遲。這引出了搶佔模型 (voluntary preemption、full preemption、乃至 [PREEMPT_RT](https://realtime-linux.org/)) 的差異，在延遲敏感場景中，這是極常見的差異來源。
2. Runqueue 競爭與負載平衡：SMP 下的 enqueue 與 wakeup 常被 rq lock 競爭、CPU 排程器的負載平衡 (load balancing) 及空閒追蹤 (idle tracking) 所干擾。尾端絕非完全由排程排序 key 決定。
3. 記憶體階層與快取一致性：除了 False sharing，還包含 NUMA remote access、page fault 與 THP(transparent huge pages)。NUMA 架構下的 remote page fault 或 task migration 會直接拖長尾端，完美印證多時間尺度的理論。
4. 背景核心執行緒與 writeback：kswapd、kcompactd、jbd2 或 flush threads 在記憶體與 I/O 壓力下，會將系統帶入完全不同的狀態 (regime change)。這些機制是吞吐量穩定準則中需要嚴格監控的干擾源。

若在嚴格受控的單核、固定工作集、無 I/O 的微基準測試中，分佈則可能接近薄尾。

## 古典熱力學與 Landauer 原理

![image](https://hackmd.io/_uploads/S1wANDud-l.png)

探討系統底層的能量耗散與熵增時，必須嚴格區分定義式與不等式：
$$
dS = \frac{\delta Q_\mathrm{rev}}{T} \quad \text{(可逆路徑定義式)}
$$

$$
dS \ge \frac{\delta Q}{T} \quad \text{(不可逆過程 Clausius 不等式，此為微分簡化表述)}
$$

在作業系統中，物理學家暨電腦科學家 [Rolf Landauer](https://en.wikipedia.org/wiki/Rolf_Landauer) 提出根本的物理極限 (Landauer 原理)：每抹除一個位元的邏輯不可逆操作，必然對應到至少 $k_B T \ln 2$ 的能量耗散下界。

:::info
:information_source: 避免誤用的專業告誡與工程對照

Landauer 給出的是不可逆位元抹除的能量下界，而非計算必然很耗能。在現代伺服器尺度，功耗與效能波動的主因通常是排程與記憶體競爭，而非熱力學下界。因此，本文將其作為「邏輯不可逆 $\to$ 物理不可逆」的概念錨點。
:::

將不可逆操作的概念映射回 Linux 核心常見的資料結構與狀態轉移：例如 page allocator 的 free list 操作、slab 記憶體分配器的物件生命週期，以及 dentry cache 的回收。在分析層面，這些機制可視為資訊被丟棄的狀態摘要更新（此為方法論類比，非物理耗散量的直接對應）。此類比提醒工程師，「狀態丟失」在作業系統內是天天發生的高頻事件，儘管軟體層的耗散並非直接受 Landauer 下界約束，但狀態的不可逆重設在工程層級同樣伴隨著資訊損失與不確定性的增長。

從方法論的角度看，這正是後續章節轉向統計語言的動機之一：當系統內不可逆的狀態重設頻繁發生，追蹤每次個別事件的因果鏈不再可行，分佈與統計摘要成為必要的分析手段。

## Boltzmann 的統計力學革命

![image](https://hackmd.io/_uploads/SJukSvuuWg.png)

古典熱力學面臨 Loschmidt 悖論：微觀粒子遵循時間可逆的牛頓力學，但巨觀現象卻表現出不可逆性。Ludwig Boltzmann 將熱力學轉化為統計力學結構。在此定義：

熵不是混亂感，更精確地說，它是宏觀約束下可及相空間體積或微觀狀態計數的對數：
$$
S = k_B \log \Omega
$$

Boltzmann 的 H 定理依賴分子混沌假設 (Stosszahlansatz)。不可逆性建立在三層結構上：
1. 微觀方程本身仍然可逆。
2. 不可逆性來自粗粒化 (coarse-graining) 加上初始條件與近似。
3. 分子混沌假設是在碰撞統計上引入近似獨立性 (忽略微觀關聯)。

這本質上是模型層級的資訊丟失。

在作業系統量測中，分析人員也採用結構上高度類似的粗粒化妥協：放棄追逐每一個快取未命中的因果鏈，改將喚醒延遲 (wakeup latency) 拆成 wakeup $\to$ enqueue 與 enqueue $\to$ oncpu。以 tracepoint 定義狀態邊界就是一種 coarse-graining，藉由忽略微小硬體關聯，換取可操作的模型。

### 宏觀約束與 PSI
> PSI: Pressure Stall Information

本文將可及狀態體積類比到可及排程序列/競爭交錯。在缺乏明確限制的情境下，系統會趨向把可用資源占滿到瓶頸點。然而，在現代 Linux 系統中，Cgroup 實際上是在工程上施加宏觀約束，確保系統不會自然飄移到某些高機率但不可接受的區域 (如透過 `memory.max`、`cpu.max`、`io.max` 控制)。

在此背景下，Linux 的 PSI (Pressure Stall Information) 是種絕佳的巨觀可觀測量 (macro-observables)。PSI 本質上是將系統內所有 task 因 CPU、Memory、I/O 產生的 stall (停頓) 統計，粗粒化聚合成可觀測的宏觀指標。在分析系統穩定性時，PSI 可作為與 tail latency 並列的關鍵宏觀指標，尤其在記憶體壓力的情境下，它能有效反映資源受限時的系統壓力狀態 (PSI 量測的是生產力損失比例，而非直接對應物理相空間的受限程度)。

## Shannon 資訊理論與熵率估計

![image](https://hackmd.io/_uploads/ryemBvdd-l.png)

Claude Shannon 將統計力學概念引入通訊工程。本文強調：Shannon 熵是相對於觀察者模型的描述長度期望值。
$$
H(X) = - \sum p(x) \log_2 p(x)
$$

在分析系統時，單次熵容易失真。例如事件邊際分佈可能很均勻 ($H(X)$ 高)，但序列若具備強烈的固定交替 (強相關)，則系統實際上高度可預測。因此，工程上應轉向探討熵率 (entropy rate, $h$)，即序列平均每推進一步新增的不可預測性。
$$
h = \lim_{n \to \infty} \frac{1}{n} H(X_1, \dots, X_n) \quad \text{(假設序列為平穩過程)}
$$

### 估計器流程與 Linux 核心擴展
熵率不是一個絕對數字，而是估計流程。實務上常使用 n-gram 近似序列模型，或基於壓縮器 (如 Lempel-Ziv) 的估計。

:::info
:information_source: 估計偏誤提醒

- n-gram 受限於模型階數：階數太低會低估結構，太高會導致資料稀疏 (data sparsity)
- Lempel-Ziv 類估計器對資料長度極端敏感，在短序列上極不穩定
:::

判定準則：熵率的上升或下降都可能指示異常。系統呼叫序列在正常服務下有穩定的語法結構。當攻擊發生時，結構崩壞常使熵率上升；但若故障導致系統陷入高度範本化的重試迴圈，序列反而變得更可預測，熵率會下降。

熵率模型不應僅侷限於系統呼叫層。它可自然延伸至：
- CPU 排程器追蹤序列：對 `sched_wakeup`、`sched_switch` 事件序列計算熵率或分佈偏移，能有效量化工作負載型態 (workload pattern) 的根本變化。
- block layer 與 network stack 事件序列：如 block request issue/complete 交錯，或 TCP retransmit 事件序列。此框架適用於各種核心子系統的非線性行為分析。

上述熵率估計與分佈偏移的量化方法，將在稍候的系統異常偵測中作為具體的工程工具加以落實。

## 系統現實：false sharing 與核心層級反例

![image](https://hackmd.io/_uploads/BkgNrwO_Ze.png)

在 Linux 中，task 是排程實體 (scheduling entity)，行程與執行緒只是共享資源組合的不同觀點。`fork` 可視為特定旗標組合的 `clone` 介面。在同一 CPU 核上、工作集相近、且沒有頻繁遷移或 NUMA 變動時，位址空間共享在特定條件下（如 PCID/ASID 有效、資料存取重疊）可使 TLB 與 L1 cache 失效率較低，但實際效益取決於工作集大小與切換模式。但量級差異極大，取決於旗標與位址空間建立成本。

### False sharing 的量測鏈與可否證性
執行緒共享記憶體在多核 (core) 環境中常引發 false sharing。尾端延遲不是直接從 MESI 協定跳過來，它經過等待與搶佔的累積：
1. 機制層：多執行緒寫入同一個快取行內未對齊的變數，引發 invalidation。
2. 量測層：`perf c2c` 觀測到 cache misses 與匯流排 Coherence traffic 上升。
3. 排程層中介量：當停頓 (stall) 造成臨界區段 (critical section) 延長，或造成 runqueue 競爭與可執行任務堆積時，會映射到排程延遲，使 runnable-to-oncpu 的尾端拉長。
4. 指標層：最終導致應用程式的尾端延遲爆發。

:::info
:information_source: 可否證的工程斷言

若 false sharing 是導致尾端延遲的主因，則在對齊快取行 (如 `alignas(64)`) 後，(1) coherence traffic 指標應顯著下降，且 (2) 尾端 CCDF 的斜率或彎折點應改變，而不只是 P99 數字的常數平移。
:::

### 常見核心層級的反例與對照主題

許多尾端延遲並非由 false sharing 引起。設計對照實驗時，必須考量以下常見的反例與邊界條件：
- RCU 與 lock contention：許多尾端延遲源自 RCU grace period 等待，或是特定路徑的鎖競爭與優先權反轉 (Priority inversion)。
- CPU 排程器的任務遷移 (task migration) 與 NUMA 自動平衡 (NUMA balancing)：除了 CPU core 遷移，AutoNUMA 機制亦會引入高昂尾端。量測時必須透過 `numa_balancing` 參數、affinity 及 cpuset 進行控制。
- softirq 與接收網路封包 (Network Rx)：在伺服器環境，softirq 處理與 NAPI budget 耗盡是常見的尾端來源。這類延遲不會直接表現在 CPU 排程延遲上，卻會使應用層的尾端爆發，突顯事件邊界選擇的關鍵性。

期望值公式 $E[\text{Latency}] = T_{\text{base}} + P_{\text{miss}} \times T_{\text{penalty}}$ 只能提示平均趨勢，無法推導 P99。尾端屬於分佈形狀問題，必須直接觀測 CCDF。

## 排程器公平性與 EEVDF 模型

在權重模型下，本文定義理想服務時間 $S_i(t)$ 是按權重比例 $w_i / W$ 分配的理想累積服務 (流體近似)。在 Linux 語境中，此對應於 CFS 透過 nice weight、CFS bandwidth (quota/period) 及 Cgroup CPU controller 進行的資源干預。

排程誤差定義為：
$$
\text{Lag}_i(t) = S_i(t) - s_i(t)
$$

在工程實務上，lag 有界具備兩種語意：
1. 對所有任務的 $|\text{Lag}_i(t)|$ 存在一個觀測上的高分位數界限。
2. $\text{Lag}$ 的分佈在穩態下不發生長期漂移，且對參數變動呈現可解釋的形變。

在真實系統中，睡眠任務與離散時間片段 (tick) 使得 $\sum \text{Lag}_i = 0$ 的守恆性質僅剩下某種近似。因而工程上更常看 lag 的 drift 與高分位界，而不是硬追求總和為零 (但其仍可作為基礎的 sanity check)。

### EEVDF 的實作語意與驗證

EEVDF 源自 Stoica 與 Abdel-Wahab 在 1995 年提出的 Earliest Eligible Virtual Deadline First 概念，後於 [1996 年 RTSS 論文](https://dl.acm.org/doi/10.5555/890606) 中擴展為完整的 proportional share 演算法。其本質是將資源分配目標轉寫為虛擬截止時間 (virtual deadline) 最早者優先，並利用 eligible (合資格) 條件避免不合理的超前服務。需注意，EEVDF 中的 virtual deadline 語意與 CFS 的 vruntime 有著本質差異，前者更反映了任務完成的急迫性。

EEVDF 自 [Linux 6.6 起合併至主線](https://lwn.net/Articles/969062/) 並持續補全；合併初期部分子功能仍與 CFS 框架交織整合，整體遷移分階段推進。EEVDF 引入 request length(在 Linux 語境中接近 slice / service request 的控制參數) 與 Eligible/Deadline 機制。此外，近年核心提供 `latency_nice` 作為延遲導向的控制手段之一，使 CPU 排程器能進一步解耦吞吐量與延遲。在 CFS 對短工作量不友善的面向上，EEVDF 改善了某些延遲型態；但效能表現仍需由工作負載與參數決定。

若未控制關鍵變因，觀測到的尾端差異可能被頻率調節、IRQ 擾動、NUMA 遷移等因素主導，造成歸因錯誤。驗證 EEVDF 行為時，必須固定 CPU affinity、CPU governor、隔離 IRQ，並嚴格定義延遲 (如 wakeup $\to$ oncpu)，以 bootstrap 做分位數 CI，比較 CCDF 差異。

## 重尾與模型比較的降風險處理

在處理偏離常態的效能資料時，本文強調：長程依賴 (long-range dependence) 與重尾 (heavy-tailed) 不是同一件事。前者牽涉時間序列上的相關結構 (偏向觀察 autocorrelation 或 Hurst exponent)，後者牽涉分佈尾端的衰減速率 (偏向觀察尾指數估計)。

為了更貼近核心分析，模型比較的受試資料來源應擴展至：page fault latency、Block I/O completion latency 以及 runqueue wait time。這些分佈常呈現迥異形狀，充分說明「看到長尾不等於重尾」，並揭示了長程依賴在 I/O 子系統中更為普遍。

處理尾端必須執行標準的模型比較流程。此流程適用於有足夠樣本且能合理假設觀測窗口內近似同分佈的情境：
1. 尾端線性化檢查：繪製 log-log 尺度的 CCDF。例如 Pareto 分佈會呈現近似直線特徵。必須明講，這僅是視覺診斷而非證明，且工程上常用的尾指數估計器 (如 Hill estimator) 對 threshold 極度敏感，容易產生誤導。
2. baseline 比較：先比對 lognormal、Pareto 與 Weibull 分佈。適合度檢定可採用 KS test 或 Anderson-Darling 檢定 (AD 檢定對尾端通常更敏感)。
3. 預測檢驗：不要只做擬合，必須做預測檢驗 (如用前 80% 資料擬合，後 20% 驗證尾端預測)。

## 系統異常偵測與資訊安全分佈偏移

![image](https://hackmd.io/_uploads/S1KuSvuuZx.png)

資安偵測的關鍵在於量化分佈偏移。本文聚焦在行為分佈/序列統計的偵測觀點，不涵蓋符號執行、污點分析或語意層的攻擊鏈重建。我們探討的實務來源應超越純系統呼叫追蹤，延伸至 audit subsystem 或 LSM hooks 的事件流，這更貼近資安審計語境；同時需考量 eBPF based telemetry 的安全邊界 (如 eBPF verifier 限制與本身的觀測擾動)。

本文採用資訊增益 (IG) 與 KL 散度：
$$
IG(s) = H(C) - H(C \mid s)
$$

$$
D_{KL}(P \| Q) = \sum p(x) \log \frac{p(x)}{q(x)}
$$

其中 $P$ 是觀測分佈，$Q$ 是基準分佈。

邊界條件與代價

基準取得與漂移代價：基準分佈 $Q$ 的建立可依賴正常期的滑動窗口、白名單 profile 或多模態分佈。基準 $Q$ 必然會漂移，包含核心版本更新、容器編排變更及 Cgroup 配置調整，都可能造成 $Q$ 的 regime change。因此，更新基準的策略是防禦面的一部分，而非純統計問題。

先驗比例陷阱：若惡意樣本在真實世界中的先驗比例極低，即使 $IG$ 很大，也可能造成大量 false positive。必須搭配條件機率或 likelihood ratio 語言。

KL 發散與 JS divergence：KL 散度具備非對稱性，且若 $q(x)=0$ 但 $p(x)>0$ 會直接發散。工程上常需加平滑化，或改用 JS divergence。JS divergence 的好處不只是對稱，還有有界性，這讓告警閾值能在跨系統或跨時間窗下比較，不會因 KL 發散而失去可操作性。

## 核心熵池與亂數產生的物理極限
![image](https://hackmd.io/_uploads/SyocBDuObe.png)

探討系統亂數時，本文使用最小熵 (min-entropy, $H_\infty$) 明確表述：在確定性後處理 (無額外獨立隨機源) 的模型下，擷取器輸出的可保證不可預測性上界，受限於輸入的最小熵。
$$
H_\infty(\text{Output}) \le H_\infty(\text{Input}) \quad \text{(確定性擷取，無旁路資訊)}
$$

這意味著雜湊與確定性擷取器是濃縮與擴散，不是創造熵。CSPRNG 則是在計算安全假設下將短種子擴展為長偽隨機序列，其安全性建立在計算不可區分性而非資訊理論保證上。針對 Linux 核心 RNG 的熵估計與熵計量 (entropy estimator/accounting)，一般寫入資料到 `/dev/random` 不會提高系統的熵計數 (但特權使用者透過 `RNDADDENTROPY` ioctl 可宣告額外熵，此為例外)。

在 2012 年 [Mining Your Ps and Qs](https://factorable.net/) 大規模掃描研究中，研究者對網際網路上的 TLS 與 SSH 主機金鑰進行大規模掃描，發現約 0.50% 的 TLS 主機的 RSA 模數可透過成對 GCD 分解 (即共用質因數)，另有約 0.75% 的 TLS 憑證因啟動熵不足而重複使用相同金鑰。兩者皆與嵌入式設備開機時播種熵不足高度相關。

根據[維護者設計說明](https://www.zx2c4.com/projects/linux-rng-5.17-5.18/)，Linux 5.17 與 5.18 在效能架構上的關鍵改動是將熱路徑改為 per-CPU CRNG 金鑰與局部鎖定，大幅降低 multi-core 環境下 `getrandom` 的鎖競爭，呼應了前文所述減少競爭的效能設計。在 API 語意層面，新版核心弱化了 `/dev/random` 與 `/dev/urandom` 的歷史行為差異：兩者皆改採相同的 BLAKE2s 與 ChaCha20 架構，核心 CRNG 初始化完成後行為已趨一致，實務上以 `getrandom()` 取代直接存取裝置節點為佳。

根據 [Linux 手冊](https://man7.org/linux/man-pages/man2/getrandom.2.html)，`getrandom()` 在特定旗標語意下會阻塞直到核心 RNG 初始化完成。長期金鑰在啟動早期必須使用阻塞語意；非金鑰用途的隨機性可用非阻塞語意。

硬體指令的定位：RDSEED 面向播種用途，RDRAND 面向高吞吐的隨機輸出。

降級路徑與威脅模型決策：硬體指令可能因微架構缺陷或實作瑕疵失效 (如近期針對特定 CPU 的 RDSEED 漏洞通報)。當硬體指令不可用或不被信任時，系統的降級路徑是什麼？是無期限等待熵池、延後金鑰生成，還是引入外部硬體熵源 (如 TPM / HWRNG)？白皮書讀者在架構設計時必須繪製出完整的決策樹，而非盲目信任單一介面。

## 從公式到儀器：不確定性與方法論收束

### 不確定性的來源與量測干擾模型
![image](https://hackmd.io/_uploads/SJQ3rP_dZe.png)

統計的存在不是因為系統亂，而是因為觀測能力有限。觀測會改變系統，在作業系統量測中有具體表現。執行量測前必須界定觀測成本的常見選擇：
- tracepoint 全量記錄：提供精確的事件鏈，但成本極高且資料量龐大，容易引發 I/O 擁塞。
- perf sampling：硬體 PMU 取樣成本較低，但存在無法精確捕捉短暫事件的抽樣偏差 (sampling bias)
- eBPF：彈性極高，但受限於 verifier 安全限制，且 JIT 編譯與 BPF map 存取仍會帶來執行時期開銷
- timekeeping 的潛在陷阱：高頻讀取時間戳的硬體成本為何？需特別注意跨核時間戳的一致性 (cross-core TSC drift)、CPU 頻率調節 (frequency scaling)，及 CPU idle state (如 C-states 切換) 對 timestamp 準確度的潛在影響

### 分位數與信賴區間的最小原則
本文反覆要求使用 bootstrap 計算信賴區間。其目的不是讓數字更漂亮，而是讓可重現擁有可被比較的統計語言。但必須提醒：CI 只反映抽樣的不確定性，不涵蓋環境漂移與工作負載描述不足所造成的系統性誤差。

### 收束為可重複的研究流程
1. 事件定義：查閱附錄工具表，精確界定觀察邊界。
2. 採樣與觀測：考量干擾成本模型，進行大樣本觀測。
3. 分佈與分位數：使用 CCDF 與 bootstrap。
4. 假說與比較：執行 baseline 對照與預測檢驗。
5. 反例與威脅模型：考量決策成本與極限風險。

## 附錄一：量測工具與事件定義對齊表

要確保實作可重現，必須將抽象定義對齊至具體的 Linux 核心追蹤點。下表以 Linux v6.12 為基準，實作時仍須核心原始碼為準：

| 延遲定義 / 觀測目標 | 意義與對應瓶頸 | 推薦 tracepoint 綁定 |
|---|---|---|
| wakeup $\to$ enqueue | 任務被喚醒到進入 Runqueue (鎖競爭、中斷處理) | `sched:sched_waking` $\to$ `sched:sched_wakeup`；新建任務另見 `sched:sched_wakeup_new` |
| enqueue $\to$ oncpu | 佇列中等待到實際獲得 CPU (CPU 排程器效能) | `sched:sched_wakeup` $\to$ `sched:sched_switch` |
| wakeup $\to$ oncpu | 端到端的總喚醒延遲 | `sched:sched_waking` $\to$ `sched:sched_switch` |
| 任務 runtime 計量 | 每次排程片段的實際執行時間；v6.12 已擴展至 DL/RT 排程類別 | `sched:sched_stat_runtime` |
| false sharing 偵測 | cache line 競爭與 invalidation | `perf c2c record` (需 Intel PEBS 支援) |
| softirq 處理延遲 | 網路收包與 Block I/O 底半部延遲 | `irq:softirq_entry` $\to$ `irq:softirq_exit` |
| direct reclaim 延遲 | 記憶體壓力下的 regime change 指標 | `vmscan:mm_vmscan_direct_reclaim_begin` $\to$ `vmscan:mm_vmscan_direct_reclaim_end` |
| CFS bandwidth throttling | v6.12 無專屬 tracepoint；觀測控制面阻擋事件有兩種途徑 | 輪詢：cgroup v2 `cpu.stat` 欄位 `nr_throttled` / `throttled_usec`；事件驅動：eBPF `fentry:throttle_cfs_rq` / `fentry:unthrottle_cfs_rq`（需 `CONFIG_DEBUG_INFO_BTF` 且符號可見） |

> 使用 tracepoint 配對計算延遲時的前提說明：
> - 事件配對鍵：以 (PID/TID, CPU) 或 sequence number 匹配；task migration 會使同一任務的 enqueue 與 sched_switch 落在不同 CPU，配對邏輯須處理跨 CPU 情況。
> - 重複 wakeup：同一任務在 enqueue 前可能觸發多次 `sched_waking`，應依實驗設計選擇取最後一次或全部計入。
> - `fentry` 方案的前提：需核心開啟 BTF（`CONFIG_DEBUG_INFO_BTF`）且目標函式為可見符號，屬診斷選項而非通用方案。
> - 版本依賴：上表以 Linux v6.12 為基準，部分 tracepoint 的語意或覆蓋範圍可能隨核心版本變動；tracepoint 為近似代理，實作前仍須以當前核心原始碼為準。

## 標準效能量測報告結構範例

在產出效能量測報告時，應包含以下結構。樣本數需由目標分位數與可接受 CI 寬度決定；$N > 10^4$ 是常見的最低量級起點，但對更高分位數或更重尾分佈可能不足：
1. 實驗設定：詳細記錄 CPU 型號、核心版本、CPU governor、隔離設定 (`isolcpus`)，以及具體的負載參數。
2. 資料量與採樣：記載總樣本數、暖機時間與穩態取樣時間。
3. 圖表呈現：提供以 Y 軸 log 尺度繪製的 CCDF 分佈圖，並以表格明確列出 P50, P95, P99 數值。
4. 信賴區間 (CI)：附上使用 bootstrap 演算法計算的 P99 95% CI。
5. 討論與物理對應：基於資料，解釋尾端分佈的形狀特徵與硬體機制的對應關係。

## 參考文獻與延伸閱讀
1. Stoica, I., Abdel-Wahab, H., Jeffay, K., Baruah, S., Gehrke, J., & Plaxton, C. (1996). [A Proportional Share Resource Allocation Algorithm for Real-Time, Time-Shared Systems](https://dl.acm.org/doi/10.5555/890606). _Proceedings of the 17th IEEE Real-Time Systems Symposium_. (EEVDF 演算法源起)
2. LWN.net. [An EEVDF CPU scheduler for Linux](https://lwn.net/Articles/925371/). (EEVDF 提案與設計脈絡)
3. LWN.net. [The EEVDF scheduler merge](https://lwn.net/Articles/969062/). (EEVDF 合併至 Linux 6.6 主線)
4. Heninger, N., Durumeric, Z., Wustrow, E., & Halderman, J. A. (2012). [Mining Your Ps and Qs: Detection of Widespread Weak Keys in Network Devices](https://factorable.net/weakkeys12.conference.pdf). _USENIX Security Symposium_. (RSA 共享質因數與開機熵漏洞原始研究)
5. Linux Kernel Documentation: [sched/tracing](https://www.kernel.org/doc/html/latest/scheduler/), [random(4)](https://man7.org/linux/man-pages/man4/random.4.html), [getrandom(2)](https://man7.org/linux/man-pages/man2/getrandom.2.html). (事件對齊與 RNG 介面規範)
6. Donenfeld, J. A. [Random number generator enhancements for Linux 5.17 and 5.18](https://www.zx2c4.com/projects/linux-rng-5.17-5.18/). (RNG 現代化設計說明)
