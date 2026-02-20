# notes/ — 個人學習筆記

此目錄存放學習過程中的討論心得、技術分析與閱讀筆記。

## 特性

- **gitignored** — 個人筆記不進版本控制，不會汙染專案
- **Claude 可讀寫** — 討論完畢後可立即請 Claude 記錄重點
- **自由格式** — Markdown 為主，檔名建議用日期或主題命名

## 建議的檔案命名

```
notes/
├── README.md                          ← 本檔（git tracked 作為範例）
├── 2026-02-20-list-sort-analysis.md   ← 日期 + 主題
├── timsort-tradeoffs.md               ← 純主題
└── kxo-fixed-point-notes.md           ← 作業相關筆記
```

## 工作流程

1. 與 Claude 討論技術問題
2. 討論告一段落後，請 Claude 將重點寫入 `notes/`
3. 需要撰寫正式報告（HackMD）時，從 notes 整理精華
4. Claude 在後續 session 中可讀取 notes 作為上下文

> 詳見 [`docs/ARC42.md`](../docs/ARC42.md) §5 及 ADR-004。
