# 從熵到作業系統：統計物理觀點的效能分析

> **原始出處：** https://hackmd.io/@sysprog/from-entropy-to-os
> **擷取日期：** 2026-02-22
> **用途：** 課程教材 — 連結熱力學、資訊理論與 Linux 核心效能分析
> **涵蓋度：** 摘要（約 30%）
> **省略內容：** 各節的數學推導細節、完整公式、附錄工具對齊表、報告結構範例

## 核心主張

作業系統不只是軟體工程產物，更是一個可量測的動態系統，適用統計物理的分析框架。應以**分布**（而非平均值）為思考基礎，尤其關注尾端延遲（tail latency）。

## 文章結構

### 第一部分：量測基礎（§1–§5）

- **前言** — 主張 OS 設計是可量測的動態系統，拒絕平均值思維
- **宏觀穩定性定義** — 可重複的尾端分布形狀、穩態吞吐量序列、有界的排程誤差分布
- **標記法與量測定義** — 嚴謹定義尾端延遲（CCDF）、延遲取樣邊界（wakeup→enqueue、enqueue→oncpu）、on/off-CPU 分析、bootstrap 信賴區間
- **熱力學第二定律的定位** — 澄清熵語言描述的是「粗粒化可觀測量的方向性」，非直接的熱力學類比
- **從決定性路徑到統計大數法則** — 以 Glivenko-Cantelli 定理和 DKW 不等式，論證有限樣本分位數估計的理論基礎

### 第二部分：排隊理論與 Linux 長尾來源（§6–§7）

- **尾端放大與排隊理論** — Pollaczek-Khinchine 公式顯示服務時間變異數如何非線性放大佇列等待時間，解釋微服務雪崩現象
- **Linux 核心四大長尾來源**：
  1. 搶占/中斷禁用區段
  2. Runqueue 競爭
  3. 記憶體階層 / 快取一致性
  4. 背景核心執行緒與 writeback

### 第三部分：熱力學與資訊理論（§8–§11）

- **古典熱力學與 Landauer 原理** — 不可逆資訊刪除的能量耗散下界，將 OS 狀態損失重新定義為資訊理論事件
- **Boltzmann 統計力學** — 粗粒化與量測模型選擇如何引入資訊損失，類比 tracepoint 定義如何建立觀測模型
- **PSI (Pressure Stall Information)** — 透過任務停滯統計揭示系統約束（CPU、記憶體、I/O）
- **Shannon 資訊理論與熵率** — 熵率作為序列每步的平均不可預測性，以 n-gram 和 Lempel-Ziv 估計器擴展至時間動態

### 第四部分：實務案例與反例（§12–§14）

- **False sharing** — 從快取一致性到排程到應用延遲的量測鏈；強調用 CCDF 斜率變化（而非僅 P99 偏移）作為驗證
- **核心層級反例** — RCU grace period、lock contention、NUMA balancing、softirq 處理；事件邊界選擇從根本上影響結論
- **重尾與模型比較** — 警告簡化的尾端指數估計，主張以基準分布（Pareto、lognormal、Weibull）擬合並用 KS 或 Anderson-Darling 檢定驗證

### 第五部分：安全、亂數與方法論（§15–§18）

- **異常偵測** — 用資訊增益（IG）和 KL 散度偵測行為偏移，延伸至 audit/LSM hooks 和 eBPF 遙測
- **核心熵池與亂數產生** — min-entropy 約束、Landauer 原理對確定性 extractor 的影響、RDSEED/RDRAND 取捨、Linux 5.17+ per-CPU CRNG 改進
- **不確定性與方法論** — 信賴區間僅量化取樣不確定性，不涵蓋環境漂移或模型誤設；主張 bootstrap 校準與預測驗證
- **可重複研究流程** — 五步驟 benchmark 工作流：事件定義 → 取樣策略 → 分布分析（CCDF/bootstrap）→ 假設檢定 → 威脅模型

### 附錄

- **量測工具與事件定義對齊表** — Linux v6.12+ tracepoint 對應（wakeup→enqueue、false sharing 偵測、softirq、direct reclaim、CFS bandwidth throttling）
- **標準效能量測報告結構** — 實驗設定、樣本量與暖機、CCDF 圖表含 P50/P95/P99、bootstrap 95% CI、機制討論

## 關鍵概念索引

| 概念 | 說明 |
|------|------|
| CCDF (互補累積分布函式) | 尾端延遲的標準視覺化方式 |
| Bootstrap 信賴區間 | 對 percentile 的穩健估計方法 |
| Pollaczek-Khinchine 公式 | 服務時間變異數與佇列延遲的非線性關係 |
| Landauer 原理 | 不可逆位元刪除的最低能量耗散 |
| 熵率 | 序列中每步平均不可預測性 |
| PSI | Linux 核心的壓力停滯資訊指標 |
| 粗粒化 (coarse-graining) | 量測模型選擇引入的資訊損失 |
| min-entropy | 亂數產生器輸出品質的下界約束 |
| KL 散度 | 偵測分布偏移的資訊理論工具 |
