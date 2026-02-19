# Linux Kernel 2026 學習環境

一個以 AI 驅動的 Linux Kernel 學習環境。透過 VS Code Dev Container 與 Claude CLI 建構可重現的開發環境，讓學習者能與 Claude 助手協同學習 Linux Kernel，加速理解核心概念與原始碼。

## 理念

學習 Linux Kernel 的門檻高、範圍廣。本專案的核心想法是：**讓 Claude 不只是工具，而是你的學習夥伴。**

- **作為助手** — 協助閱讀原始碼、解釋資料結構、追蹤執行流程
- **作為老師** — 提供深入洞見、補充背景知識、引導思考方向
- **作為環境** — 透過 Claude Skills 預先封裝常用的學習工作流，降低操作門檻

## 開發環境

| 元件 | 說明 |
|------|------|
| VS Code | 編輯器與 IDE |
| Dev Container | 基於 Ubuntu Noble 的可重現開發環境 |
| Claude CLI | AI 助手，內建於容器中 |
| Claude Skills | 預定義的學習指令，加速常見操作 |
| uv + Python 3.12 | 腳本與資料處理工具，容器建立時自動安裝 |

## 快速開始

1. 安裝 [VS Code](https://code.visualstudio.com/) 與 [Dev Containers 擴充套件](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Clone 本專案：
   ```bash
   git clone https://github.com/laneser/linuxkernel2026.git
   ```
3. 以 VS Code 開啟專案，選擇 **Reopen in Container**
4. 在容器內啟動 Claude CLI：
   ```bash
   claude
   ```

## 專案結構

```
.
├── .claude/
│   └── skills/              # Claude Skills
│       └── commit-log/      # Git commit message 撰寫指引
├── .devcontainer/           # Dev Container 設定
├── docs/
│   ├── ARC42.md             # 架構文件 (ARC42 模板)
│   └── references/          # 課程參考資料（詳見下方）
├── CLAUDE.md                # Claude CLI 專案指引
└── README.md
```

### `docs/references/` — 參考資料

存放課程相關的重要文件，讓 Claude 能快速存取，減少重複查找與說明的溝通成本。Claude 在回答問題時會優先引用這些資料。

| 檔案 | 內容 | 來源 |
|------|------|------|
| `linux-course-schedule.md` | 20 週完整課程表與每週主題 | [課程表](https://wiki.csie.ncku.edu.tw/linux/schedule) |
| `linux2025-lab0.md` | 作業一完整規格（Part A-F） | [lab0](https://hackmd.io/@sysprog/linux2025-lab0) |
| `linux2025-review.md` | 作業 review 規範與 checklist | [review](https://hackmd.io/@sysprog/linux2025-review) |
| `linux2023-lab0-review.md` | 2023 年作業檢討範例 | [2023 review](https://hackmd.io/@sysprog/linux2023-lab0-review) |
| `linux2025-homework1.md` | 作業提交區索引 | [homework1](https://hackmd.io/@sysprog/linux2025-homework1) |
| `git-commit-message.md` | Git commit message 七條規則 | [cbea.ms](https://cbea.ms/git-commit/) |
| `git-with-github.md` | Git 教學與 GitHub 設定指引 | [git-with-github](https://hackmd.io/@sysprog/git-with-github) |
| `it-vocabulary.md` | 資訊科技詞彙翻譯對照 | [it-vocabulary](https://hackmd.io/@sysprog/it-vocabulary) |
| `ai-guidelines.md` | 課程 AI 工具使用規範 | [AI guidelines](https://hackmd.io/@sysprog/arch2025-ai-guidelines) |

> **注意：** 目前課程文件為 2025 版，待 2026 版發布後更新。URL 模式為 `hackmd.io/@sysprog/linux{YEAR}-{topic}`。
