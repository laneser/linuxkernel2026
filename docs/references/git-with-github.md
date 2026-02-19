# Git 教學和 GitHub 設定指引

> **原始出處：** <https://hackmd.io/@sysprog/git-with-github>
> **擷取日期：** 2026-02-19
> **用途：** 課程 Git 工作流程參考

---

## 影片教學系列（共 11 集）

本指引搭配完整的中文影片教學，涵蓋安裝、commit、分支、rebase、遠端 repository、stashing、patching 與除錯工具。

## GitHub 帳號設定

GitHub 是 Git repository 的託管服務，讓開發者能在全球分享專案。

### SSH Key 設定

1. 使用 `ssh-keygen` 產生 SSH key
2. 將 key 加入 ssh-agent
3. 上傳 public key 至 GitHub
4. 注意：authentication key 與 signing key 用途不同

## 常用 Git 操作

### 同步
- `git remote add origin <url>` — 連結本地與遠端 repository
- `git push` — 推送 commit 至遠端

### 複製
- 可透過 SSH、Git protocol 或 HTTPS clone
- 有防火牆限制時優先使用 HTTPS

### Pull/Push
- `git pull` = `git fetch` + `git merge`
- `git push` — 推送本地 commit

## Commit 簽署驗證

GitHub 的 "Require signed commits" ruleset 要求區分：
- **Authentication key** — repository 存取權限
- **Signing key** — 驗證 commit 作者身份

## 學習資源

- [LearnGitBranching](https://learngitbranching.js.org/) — 互動式 Git 分支視覺化學習
- [Visualizing Git Concepts with D3](https://onlywei.github.io/explain-git-with-d3/) — 以 D3 視覺化 Git 概念
