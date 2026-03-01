# CLAUDE.md — 專案指引

本文件供 Claude CLI 讀取，作為與使用者協同工作時的上下文基礎。

## 專案概述

本專案是一個以 AI 驅動的 Linux Kernel 學習環境，目的是讓學習者與 Claude 協同學習 Linux Kernel 2026 課程。Claude 在本專案中身兼 **助手** 與 **老師**，協助閱讀原始碼、解釋概念，並從中提供洞見以加速學習。

## 架構文件

本專案採用 **ARC42** 作為架構文件模板，位於：

- [`docs/ARC42.md`](docs/ARC42.md) — 完整架構文件

在回答架構相關問題時，請優先參考 ARC42 文件。

## 參考文件

`docs/references/` 目錄存放課程相關的參考資料（論文、規格書、教材摘要等），目的是讓 Claude 能快速取用，減少重複說明的溝通成本。

回答問題時，若 `docs/references/` 中有相關資料，請優先引用。

### 漸進式揭露原則

參考文件採用 **漸進式揭露（Progressive Disclosure）** 策略，根據來源品質決定本地存放深度：

| 來源狀況 | 本地存放 | Claude 行為 |
|----------|---------|------------|
| **課程教材**（`hackmd.io/@sysprog/` 開頭） | **完整 raw markdown** | 用 `curl` 抓 `/download` 端點，直接讀取本地檔案（見下方說明） |
| **其他結構良好的來源** | 摘要 + metadata | 需要細節時從原始出處 `WebFetch` 抓取 |
| **結構不佳**（PDF、無分段長頁面等） | 本地存完整整理版 | 直接讀取本地檔案 |

每個參考檔案的 header 包含以下 metadata：

```markdown
> **原始出處：** URL（Claude 按需取用的來源）
> **擷取日期：** YYYY-MM-DD
> **用途：** 說明
> **涵蓋度：** 完整 / 摘要（約 N%）
> **省略內容：** 被省略的主要段落（僅摘要版填寫）
```

#### 參考文件索引

| 檔案 | 用途 |
|------|------|
| `n1256-c99.md` | ISO/IEC 9899:TC3 (C99) 規格書完整 markdown 轉換 |
| `it-vocabulary.md` | 資訊科技詞彙翻譯 |
| `warmup.md` | 第一週作業 (warmup) 完整要求 |
| `ai-guidelines.md` | 本課程 AI 工具使用規範 |
| `linux-course-schedule.md` | Linux 核心設計 (Spring 2026) 課程進度表 |
| `quiz1.md` | 2026q1 第 1 週測驗題 |
| `c-pointer.md` | 你所不知道的 C 語言：指標篇 |
| `c-linked-list.md` | linked list 和非連續記憶體 |
| `binary-representation.md` | 解讀計算機編碼（二補數、群論、資安） |
| `gnu-linux-dev.md` | 課程開發工具參考 |
| `linux-concepts.md` | Linux 作業系統術語及概念 |
| `from-entropy-to-os.md` | 從熱力學第二定律到系統軟體 |
| `git-with-github.md` | 課程 Git 工作流程參考 |
| `git-commit-message.md` | commit message 規範參考 |
| `floating-point.md` | 留意浮點數運算的陷阱 |
| `floating-point-intro.md` | 初步解讀浮點數 |
| `linux-interrupt.md` | 中斷處理機制 |
| `linux-kernel-module.md` | Linux kernel module 深入機制分析 |
| `linux-perf.md` | 運用 Perf 分析程式效能並改善 |
| `lkmpg.md` | Linux Kernel Module Programming Guide |

**維護要求：** 新增、刪除或重新命名 `docs/references/` 中的檔案時，必須同步更新上方索引表。索引不同步會導致 Claude 找不到已有的參考資料或引用已刪除的檔案。

#### 課程教材抓取方式

老師的教材（`hackmd.io/@sysprog/` 開頭的 URL）**必須用 `curl` 抓 raw markdown**，不可用 `WebFetch`：

```bash
curl -sL "https://hackmd.io/@sysprog/{note-id}/download" -o docs/references/{filename}.md
```

**原因：** `WebFetch` 內部使用較小的模型處理內容，最終只會產出摘要，無法保留教材的完整細節（程式碼、數學式、延伸問題等）。抓取 raw markdown 後由 Claude 主模型直接分析，才能達到足夠的理解深度。

Claude 處理參考文件時的行為：
1. 先讀本地檔案，判斷是否足以回答問題
2. 若不足，檢查「涵蓋度」和「省略內容」確認缺少的部分
3. 若為課程教材，用 `curl` 抓取 raw markdown；其他來源才用 `WebFetch`

### 課程文件更新

目前 references 中的課程文件為 **2025 版**，目標是 2026 課程。課程教材 URL 遵循固定模式：
- HackMD：`hackmd.io/@sysprog/linux{YEAR}-{topic}`（如 `linux2026-lab0`、`linux2026-review`）
- 非年份性文件（如 `git-with-github`、`it-vocabulary`）通常不隨年度變動

當 2026 版本發布時，以新 URL 重新抓取並覆蓋對應檔案，更新檔案頂部的「原始出處」與「擷取日期」。

## 開發環境

本專案採用雙機架構（詳見 [`docs/ARC42.md`](docs/ARC42.md) §7 部署視角）：

- **Dev Container (VM)** — VS Code + Claude CLI + uv/Python 3.12，負責編輯、AI 討論、git 操作
- **實體 Linux 機器** — 透過 SSH 連接，負責編譯與原生效能測試（valgrind, perf）
  - SSH 設定：host `lab0`（定義於 `~/.ssh/config`）
  - 同步程式碼：`rsync -avz --exclude='.git' <src> lab0:~/lab0-c/`
  - 遠端測試：`ssh lab0 'cd ~/lab0-c && make && make test'`
  - **狀態：尚未設定，待取得硬體**

需要撰寫腳本或資料處理時，優先使用 `uv run` 執行 Python。

## 學習進度追蹤

本專案使用 Markdown checkbox 追蹤學習進度（詳見 [`docs/ARC42.md`](docs/ARC42.md) §5）：

- **通用模板：** [`docs/learning-checklist.md`](docs/learning-checklist.md)（git tracked）— 定義所有學習項目
- **個人進度：** `.learning-progress.md`（gitignored）— 使用者的完成狀態與筆記

Claude 可讀取個人進度，根據學習狀態建議下一步方向。模板更新時，協助將新項目 merge 進個人進度。

### 學習筆記

- **個人筆記：** `notes/`（gitignored，僅 `README.md` 進 git）— 與 Claude 討論後的心得紀錄

討論技術問題後，可請 Claude 將分析重點寫入 `notes/`。Claude 在後續 session 中可讀取這些筆記作為上下文。詳見 [`docs/ARC42.md`](docs/ARC42.md) ADR-004。

#### Notes 撰寫規範：記錄人機互動過程

Notes 的核心價值不僅是技術結論，更是**學習者如何與 AI 協作解決問題的過程紀錄**。這讓其他學習者能理解思路並從中學習。

撰寫 notes 時，Claude 應記錄以下互動脈絡：

1. **學習者提問/指令** — 使用者問了什麼、提出什麼方向
2. **Claude 回報** — Claude 做了什麼研究、發現什麼、提供哪些選項
3. **學習者決策** — 使用者在選項中做了什麼選擇、為什麼
4. **迭代修正** — 過程中遇到什麼問題、如何調整方向

範例格式：

```markdown
### 步驟 N：主題

**我的提問：** 「原始問題或指令」
**Claude 回報：** 分析結果、發現的問題、提供的選項
**我的決定：** 選擇了什麼方案，理由
**結果：** 實際產出、遇到的問題、後續調整
```

這種格式能展現 **substantial personal contribution**（課程 AI 使用規範要求），證明學習者主導了方向決策，而非被動接受 AI 輸出。

#### HackMD 報告撰寫規範

HackMD 報告是公開發表的學習成果，具備教育意義，應讓其他學習者能從中學到東西。

**書寫規範（強制）：** 所有發布至 HackMD 的內容，**必須嚴格遵守**課程書寫規範（見 `.claude/skills/hackmd/references/writing-conventions.md`）。撰寫前必須讀取該規範並逐條檢查。

**個人寫作風格：禁用** — 書寫規範明確要求「避免過多的個人色彩，用詞儘量中性」。因此撰寫 HackMD 內容時，**不得參考 `notes/writing_style.md`**，不得模仿個人書寫語氣。用詞應中性、客觀、專業。

**角色分工：**
- **學習者** — 思路核心、方向決策者、最終審核者
- **Claude** — 主筆，但服務於學習者的思路，且嚴格遵守書寫規範

**撰寫原則：**
1. **每句話都要有憑據** — 不得「想當然爾」。每個技術主張都必須附上出處（原始碼檔案與行號、規格書章節、實驗輸出等）。無法提供憑據的內容不得寫入報告。撰寫前應先透過 Grep/Read 或實驗驗證，確認事實正確後才落筆。
2. **以學習者的思路為核心** — 報告的主線是「我怎麼想、我怎麼做、我學到什麼」，而非 Claude 的分析報告
3. **用詞中性客觀** — 遵守書寫規範，不帶入個人色彩或語氣風格
4. **展現探索過程** — 不只寫最終結果，也寫走過的彎路、嘗試過的失敗方案、為什麼改變方向
5. **教育價值優先** — 讀者應能從報告中學到：技術知識 + 問題解決思路 + AI 協作方法
6. **只列關鍵程式碼** — 完整程式碼放 GitHub，HackMD 只放關鍵片段和 diff

**工作流程：**
1. Claude 從 `notes/` 中的互動紀錄整理出報告草稿
2. 草稿以學習者第一人稱撰寫，用詞中性客觀
3. **逐題審核（強制）** — 每寫完一題，Claude 必須重新讀取原始題目，逐句比對回答是否**針對題目要求回答**。具體檢查：題目問 A，回答是否在答 A 而非答 B？引用的 CWE/CVE/原始碼是否真的與題目描述的機制吻合，而非僅「相關」？若發現答非所問，必須在上傳前修正。
4. **發布前檢查** — 逐條對照書寫規範，確認無違規內容
5. 學習者審核草稿，可直接在 HackMD 上修改或要求 Claude 修正
6. 最終版本由學習者確認後發布

**上傳紀律（強制）：**
- **上傳 HackMD 時，必須直接使用 `notes/` 中學習者已審核的原文**，不得在上傳過程中自行改寫、刪減或重新整理內容。
- 若 Claude 認為內容有問題（書寫規範、事實錯誤等），應**在上傳前告知學習者**，討論修改後再上傳，而非擅自改寫後上傳。
- 學習者的審核是最終決定，Claude 不得在上傳環節繞過。

## 作業工作流程

課程作業的 fork → 開發 → 報告完整流程：

1. **Fork & Clone** — 使用 `gh` CLI fork 課程 repo，clone 至 `homework/` 目錄
2. **開發** — 在 `homework/<repo>/` 內編輯、commit、push
3. **測試** — 透過 SSH 同步至實體機進行編譯與效能測試（待設定）
4. **撰寫報告** — 在 `notes/` 撰寫草稿，完成後透過 HackMD skill 發布

```bash
# Fork + clone
gh repo fork sysprog21/lab0-c --clone=false
gh repo clone <username>/lab0-c homework/lab0-c

# 發布報告至 HackMD
uv run .claude/skills/hackmd/scripts/hackmd.py notes create \
  --title "lab0-c 開發紀錄" --content "$(cat notes/lab0-report-draft.md)"
```

- **`homework/`** — 作業 repo 的工作區（gitignored，僅 `README.md` 進 git）
- **`gh` CLI** — DevContainer 已預裝，用於 GitHub 操作（fork, clone, PR）
- **HackMD skill** — 透過 API 管理 HackMD 筆記，詳見 `.claude/skills/hackmd/SKILL.md`

## 慣例

- 文件語言以**繁體中文**為主
- 程式碼註解與 commit message 使用英文
- 協助課程作業時，須留意 [`docs/references/ai-guidelines.md`](docs/references/ai-guidelines.md) 中的 AI 使用規範：AI 僅作為輔助，學習者須展現 **substantial personal contribution**；必要時提醒使用者注意引用揭露與開發過程文件化

### 術語規範

撰寫中文技術文件時，使用以下術語（詳見 [`docs/references/it-vocabulary.md`](docs/references/it-vocabulary.md)）：

| English | 中文 | 避免 |
|---------|------|------|
| cache | 快取 | ~~緩存~~ |
| buffer | 緩衝區 | 勿與 cache 混淆 |
| render | 算繪 | ~~渲染~~ |
| traverse | 走訪 | ~~遍歷~~ |
| linked list | 鏈結串列 | ~~鏈表~~ |
| concurrent | 並行 | |
| process | 行程 | ~~進程~~ |
| iterate | 迭代 | |
| real-time | 即時 | 區別 in time（及時） |
| directory | 目錄 | ~~檔案夾~~ |
| socket | socket | ~~插座~~ |
| function | 函式 | 數學語境用「函數」 |
| implement | 實作 | |
| immutable | 不可變 | 區別 constant（常數） |
| atomic | 不可再分的 | ~~原子操作~~ |
| operator / operand | 運算子 / 運算元 | |
| optimize | 視語境：改善、充分利用 | 勿濫用「最佳化」 |
| kernel | 核心 | 僅用於 Linux kernel；其他語境避免使用「核心」以免混淆 |
