---
name: hackmd
description: "Interact with HackMD for reading and publishing notes. Use when the user wants to create, update, read, or list HackMD notes, publish homework reports, or manage their HackMD workspace. Triggers on: HackMD, 'publish report', 'create HackMD note', 'push to HackMD', 'list my notes'."
---

# HackMD Integration

Manage HackMD notes via the CLI at `.claude/skills/hackmd/scripts/hackmd.py`.

## MANDATORY: Writing Conventions

**所有發布至 HackMD 的內容，必須嚴格遵守書寫規範。** 在建立或更新筆記前，先讀取規範：

```
Read .claude/skills/hackmd/references/writing-conventions.md
```

### 關鍵規則（摘要）

1. **用詞中性** — 避免個人色彩，**禁止參考 `notes/writing_style.md` 模仿個人語氣**
2. **不加 `[TOC]`**
3. **不變更 CSS / 佈景主題**
4. **數學公式一律用 LaTeX** — `$...$` 行內、`$$...$$` 獨立；C 運算子須跳脫（`\%`、`\mathbin{\&}`）
5. **程式碼區塊不加行號** — 用 `c` 而非 `c=`
5. **只列關鍵程式碼** — 善用 `diff` 標示，完整程式碼放 GitHub
6. **不濫用 `:::info` / `:::success` / `:::warning`** — `:::danger` 僅限老師
7. **中文用全形標點** — 「，」而非 ","
8. **術語遵循〈資訊科技詞彙翻譯〉** — 避免過多中英混用
9. **不使用不必要的 emoji**
10. **AI 使用須明確標示** — 並指出 AI 產出中的謬誤

違反任何規則的內容不得發布。完整規範見 `references/writing-conventions.md`。

## Step 1: Check authentication

```bash
uv run .claude/skills/hackmd/scripts/hackmd.py auth status
```

**If not authenticated**, guide the user:

1. Open https://hackmd.io/settings#api
2. Create an API token
3. Run login:
   ```bash
   uv run .claude/skills/hackmd/scripts/hackmd.py auth login
   ```

Token is stored at `~/.config/hackmd/token` (mode 0600).

## Step 2: Perform the requested operation

### List notes

```bash
uv run .claude/skills/hackmd/scripts/hackmd.py notes list
```

### Read a note

```bash
uv run .claude/skills/hackmd/scripts/hackmd.py notes get <note-id>
```

### Create a note

From arguments:
```bash
uv run .claude/skills/hackmd/scripts/hackmd.py notes create --title "Title" --content "# Content"
```

From a local file:
```bash
uv run .claude/skills/hackmd/scripts/hackmd.py notes create --title "Title" --content "$(cat path/to/file.md)"
```

**Permalink:** The HackMD API does not reliably support setting permalinks programmatically. After creating a note, the user should set the permalink manually via the note's sharing settings on HackMD.

### Update a note

```bash
uv run .claude/skills/hackmd/scripts/hackmd.py notes update <note-id> --content "$(cat path/to/file.md)"
```

### Delete a note

```bash
uv run .claude/skills/hackmd/scripts/hackmd.py notes delete <note-id> --yes
```

## Recommended workflow: homework report

課程作業報告的建議流程：

1. **在 `notes/` 撰寫草稿** — 先在本地用 Markdown 撰寫，Claude 可協助修改
2. **發布至 HackMD** — 完成後用 `notes create` 發布
3. **後續更新** — 用 `notes update` 同步修改

```bash
# 從本地草稿發布
uv run .claude/skills/hackmd/scripts/hackmd.py notes create \
  --title "lab0-c 開發紀錄" \
  --content "$(cat notes/lab0-report-draft.md)"

# 更新已發布的筆記
uv run .claude/skills/hackmd/scripts/hackmd.py notes update <note-id> \
  --content "$(cat notes/lab0-report-draft.md)"
```

## Guidelines

- 發布前提醒使用者檢查 AI 使用揭露（見 `docs/references/ai-guidelines.md`）
- Note 預設權限為 owner-only（readPermission / writePermission）
- HackMD API 有 rate limit，避免頻繁呼叫
- 大量內容建議先存檔再用 `--content "$(cat ...)"` 發布，避免 shell 引號問題
