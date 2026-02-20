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
| **結構良好**（有清晰標題分段的 HackMD 等） | 摘要 + metadata | 需要細節時從原始出處 `WebFetch` 抓取 |
| **結構不佳**（PDF、無分段長頁面等） | 本地存完整整理版 | 直接讀取本地檔案 |

每個參考檔案的 header 包含以下 metadata：

```markdown
> **原始出處：** URL（Claude 按需取用的來源）
> **擷取日期：** YYYY-MM-DD
> **用途：** 說明
> **涵蓋度：** 完整 / 摘要（約 N%）
> **省略內容：** 被省略的主要段落（僅摘要版填寫）
```

Claude 處理參考文件時的行為：
1. 先讀本地摘要，判斷是否足以回答問題
2. 若不足，檢查「涵蓋度」和「省略內容」確認缺少的部分
3. 從「原始出處」URL 抓取所需段落（不需全抓）

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
