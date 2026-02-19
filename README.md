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
├── .devcontainer/       # Dev Container 設定
├── docs/
│   ├── ARC42.md         # 架構文件 (ARC42 模板)
│   └── references/      # 參考資料，供 Claude 快速取用
│       └── git-commit-message.md
├── CLAUDE.md            # Claude CLI 專案指引
└── README.md
```
