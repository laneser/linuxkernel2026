---
name: hackmd
description: "Interact with HackMD for reading notes and managing GitHub Sync workflow. Use when the user wants to read or list HackMD notes, or sync reports to HackMD via GitHub. Triggers on: HackMD, 'publish report', 'sync to HackMD', 'list my notes', 'push to HackMD'."
---

# HackMD Integration

Read-only HackMD API client + GitHub Sync workflow for publishing reports.

## Writing Conventions

所有發布至 HackMD 的內容，必須嚴格遵守書寫規範。完整規範見 `references/writing-conventions.md`。

### 關鍵規則（摘要）

1. **用詞中性** — 避免個人色彩
2. **不加 `[TOC]`**
3. **不變更 CSS / 佈景主題**
4. **數學公式一律用 LaTeX** — `$...$` 行內、`$$...$$` 獨立；C 運算子須跳脫（`\%`、`\mathbin{\&}`）
5. **程式碼區塊不加行號** — 用 `c` 而非 `c=`
6. **只列關鍵程式碼** — 善用 `diff` 標示，完整程式碼放 GitHub
7. **不濫用 `:::info` / `:::success` / `:::warning`** — `:::danger` 僅限老師
8. **中文用全形標點** — 「，」而非 ","
9. **術語遵循〈資訊科技詞彙翻譯〉及 L10N 詞彙對照表**
10. **不使用不必要的 emoji**
11. **AI 使用須明確標示** — 並指出 AI 產出中的謬誤

## API 操作（唯讀）

```bash
# 驗證登入狀態
uv run .claude/skills/hackmd/scripts/hackmd.py auth status

# 列出筆記
uv run .claude/skills/hackmd/scripts/hackmd.py notes list

# 讀取筆記內容
uv run .claude/skills/hackmd/scripts/hackmd.py notes get <note-id>
```

首次使用需登入：到 https://hackmd.io/settings#api 取得 API token，然後：
```bash
uv run .claude/skills/hackmd/scripts/hackmd.py auth login
```

## 發布報告：GitHub Sync 工作流程

HackMD API 有 **100KB payload 限制**，中文 markdown 超過約 42,000 字元就無法透過 API 上傳。改用 GitHub Sync：

1. **Claude 編輯** `homework/linux2026hackmd/linux2026-warmup.md`
2. **commit + push** 至 GitHub（`laneser/linux2026hackmd`）
3. **使用者在 HackMD** 上操作：Versions and GitHub Sync → Pull from GitHub

```bash
cd homework/linux2026hackmd
git add linux2026-warmup.md
git commit -m "Update report"
git push
```

此流程同時解決兩個問題：
- **無大小限制** — GitHub 不受 100KB 限制
- **編修紀錄** — 每次 commit 都是一筆可追溯的編輯紀錄，滿足課程要求

## HackMD Anchor（內部連結）格式

HackMD 自動為每個標題生成 anchor，規則如下：

1. **轉小寫**（英文部分）
2. **空格轉 `-`**
3. **中文、全形標點原樣保留**（包括 `：`、`（`、`）` 等）
4. **移除半形特殊字元**（`()`、`.`、`,` 等），但 `-` 保留
5. **數字前綴保留** — 標題 `#### 2. 為何不使用 quicksort` 的 anchor 是 `#2-為何不使用-quicksort`

範例：

| 標題 | Anchor |
|------|--------|
| `### 鏈結串列 O(1) vs 陣列 O(n)：量化分析` | `#鏈結串列-O1-vs-陣列-On：量化分析` |
| `#### 2. 為何不使用 quicksort` | `#2-為何不使用-quicksort` |
| `## Linux 核心原始碼中的搜尋結果` | `#Linux-核心原始碼中的搜尋結果` |

撰寫內部連結時，直接用 `[顯示文字](#anchor)` 格式。如果不確定 anchor，以上述規則推導，或在 HackMD 上用 TOC 複製。

## Guidelines

- 發布前提醒使用者檢查 AI 使用揭露（見 `docs/references/ai-guidelines.md`）
- HackMD API 有 rate limit，避免頻繁呼叫
- create/update/delete 命令已停用，執行時會提示使用 GitHub Sync
