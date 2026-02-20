# homework/ — 課程作業工作區

此目錄存放 fork 下來的課程作業 repository。

## 特性

- **gitignored** — 作業 repo 各自有獨立的 git 歷史，不進本專案版控
- **一作業一目錄** — 每份作業以其 repository 名稱作為子目錄
- **Claude 可存取** — Claude 可讀取作業程式碼，協助理解與討論

## 建議的目錄結構

```
homework/
├── README.md          ← 本檔（git tracked 作為說明）
├── lab0-c/            ← git clone from fork
├── kxo/               ← git clone from fork
└── fibdrv/            ← git clone from fork
```

## 工作流程

```bash
# 1. 在 GitHub 上 fork 課程 repo（使用 gh CLI）
gh repo fork sysprog21/lab0-c --clone=false

# 2. Clone 自己的 fork 到 homework/
cd homework/
gh repo clone <username>/lab0-c

# 3. 開發、commit、push
cd lab0-c/
# ... 編輯程式碼 ...
git add -A && git commit -m "Implement queue operations"
git push origin master

# 4. 需要在實體機測試時，rsync 至遠端
rsync -avz --exclude='.git' homework/lab0-c/ lab0:~/lab0-c/
ssh lab0 'cd ~/lab0-c && make clean && make && make test'
```

## 注意事項

- 每份作業是獨立的 git repository，有自己的 `.git/`
- 本專案的 `.gitignore` 會忽略 `homework/` 下的所有內容（除本 README）
- 作業 repo 的 commit 不會混入本學習專案的歷史
- 使用 AI 輔助時，請遵循 [`docs/references/ai-guidelines.md`](../docs/references/ai-guidelines.md) 的規範

> 詳見 [`docs/ARC42.md`](../docs/ARC42.md) §5 及 ADR-005。
