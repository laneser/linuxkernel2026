# ARC42 — 架構文件

> 本文件採用 [ARC42](https://arc42.org/) 模板，作為本專案的架構文件。

## 1. 簡介與目標

### 1.1 需求概述

建構一個 AI 輔助的 Linux Kernel 學習環境，讓學習者能透過 Claude 助手加速理解 kernel 原始碼與核心概念。

### 1.2 品質目標

| 優先序 | 品質目標 | 說明 |
|--------|---------|------|
| 1 | 可重現性 | 透過 Dev Container 確保環境一致 |
| 2 | 學習效率 | 透過 Claude Skills 與參考文件降低溝通成本 |
| 3 | 可擴充性 | 能隨課程進度持續擴充內容與工具 |

### 1.3 利害關係人

| 角色 | 期望 |
|------|------|
| 學習者 | 快速建立環境、高效學習 kernel |
| Claude 助手 | 有充足上下文以提供精準回答 |

## 2. 約束條件

- 開發環境：VS Code + Dev Container
- AI 工具：Claude CLI + Claude Skills
- 課程範圍：Linux Kernel 2026

## 3. 上下文與範圍

```
┌──────────────┐          ┌─────────────────────────────┐
│   學習者     │◄────────►│  Dev Container (VM)         │
│              │  VS Code │  - Claude CLI + Skills       │
└──────────────┘          │  - uv + Python 3.12         │
                          │  - 編輯、AI 討論、git 操作   │
                          └──────────┬──────────────────┘
                                     │ SSH (rsync + 遠端命令)
                                     ▼
                          ┌─────────────────────────────┐
                          │  實體 Linux 機器 (lab0)      │
                          │  - gcc, make, valgrind, perf │
                          │  - 原生效能測試與分析        │
                          │  - 無 GUI，僅 sshd           │
                          └─────────────────────────────┘
```

**Dev Container** 負責編輯、AI 輔助、版本控制；**實體機**負責編譯與原生效能測試。分離的原因是課程要求效能量測必須在原生 Linux 上進行，虛擬機的 overhead 會干擾結果。

## 4. 解決方案策略

| 策略 | 說明 |
|------|------|
| AI 輔助學習 | 透過 Claude CLI + Skills 提供即時的原始碼解釋與概念教學 |
| 參考文件預載 | 課程教材存於 `docs/references/`，降低重複查找的溝通成本 |
| 雙機分離 | VM 負責開發，實體機負責原生測試，透過 SSH 連接 |
| 漸進式深入 | 從 lab0 的 queue 實作開始，逐步展開至 kernel 子系統 |

## 5. 建構區塊視角

<!-- TODO: 描述主要元件與其關係 -->

## 6. 執行期視角

<!-- TODO: 描述關鍵執行場景 -->

## 7. 部署視角

### 雙機部署架構

#### Dev Container（VM 端）

- **用途：** 程式碼編輯、Claude AI 對話、git 操作、文件撰寫
- **基礎映像：** `mcr.microsoft.com/devcontainers/base:noble`
- **工具：** VS Code, Claude CLI, uv + Python 3.12
- **SSH 連線：** 透過 bind mount host 的 `~/.ssh` 存取 SSH key

devcontainer.json 設定：
```jsonc
{
    "mounts": [
        "source=${localEnv:HOME}/.ssh,target=/home/vscode/.ssh,type=bind,readonly"
    ]
}
```

#### 實體 Linux 機器（測試端）

- **用途：** 編譯、執行、效能測試（valgrind, perf, massif）
- **最低需求：** 任何 x86_64 Linux 機器（不需 GUI）
- **必要套件：**
  ```shell
  sudo apt install build-essential git valgrind cppcheck clang-format \
                   wamerican aspell colordiff linux-tools-common
  ```
- **服務：** sshd

#### SSH 設定

Host 端 `~/.ssh/config`：
```
Host lab0
    HostName <實體機 IP>
    User <username>
    IdentityFile ~/.ssh/id_ed25519
```

#### 遠端測試工作流程

```shell
# 從 Dev Container 內操作：
# 1. 同步程式碼至實體機
rsync -avz --exclude='.git' /path/to/lab0-c/ lab0:~/lab0-c/

# 2. 遠端編譯與測試
ssh lab0 'cd ~/lab0-c && make clean && make && make test'

# 3. 遠端 valgrind 分析
ssh lab0 'cd ~/lab0-c && make valgrind'

# 4. 遠端效能分析
ssh lab0 'cd ~/lab0-c && perf stat ./qtest -f traces/trace-14-perf.cmd'
```

> **狀態：** 實體機尚未設定，待取得硬體後補完。

## 8. 橫切關注點

<!-- TODO: 描述跨元件的共通議題 -->

## 9. 架構決策

<!-- TODO: 記錄重要的架構決策 (ADR) -->

## 10. 品質需求

<!-- TODO: 細化品質場景 -->

## 11. 風險與技術債

<!-- TODO: 記錄已知風險與技術債 -->

## 12. 詞彙表

| 術語 | 說明 |
|------|------|
| Dev Container | VS Code 的容器化開發環境 |
| Claude CLI | Anthropic 的命令列 AI 助手 |
| Claude Skills | Claude CLI 中可自訂的指令快捷方式 |
| ARC42 | 軟體架構文件模板 |
| lab0-c | 課程第一份作業的 repository（`sysprog21/lab0-c`） |
| 實體機 | 用於原生效能測試的 Linux 實體機器，透過 SSH 連接 |
