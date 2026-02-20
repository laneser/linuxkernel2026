# GNU/Linux 開發工具共筆

> **原始出處：** <https://hackmd.io/@sysprog/gnu-linux-dev/>
> **擷取日期：** 2026-02-19
> **用途：** 課程開發工具參考（常設文件，非年份性）
> **涵蓋度：** 摘要（約 15%）
> **省略內容：** 各子頁面完整內容（雙系統安裝、HackMD 使用、Markdown 語法、VS Code 設定、terminal/Vim 操作、Perf 效能分析、gnuplot 繪圖）

---

## 子頁面索引

| 主題 | 原始連結 |
|------|---------|
| 為什麼該接觸 GNU/Linux 開發工具 | [hackmd](https://hackmd.io/@sysprog/r1Psrf0KW) |
| Windows / Ubuntu 雙系統安裝 | [hackmd](https://hackmd.io/@sysprog/Bks3DypY-) |
| 從無到有學習 HackMD | [hackmd](https://hackmd.io/s/Bk0nFk6FZ) |
| HackMD LaTeX 語法與示範 | [hackmd](https://hackmd.io/s/B1RwlM85Z) |
| Markdown 文件標記語言簡介 | [hackmd](https://hackmd.io/@ntouind/markdown-basics/) |
| 熟悉 Git 和 GitHub 操作 | [hackmd](https://hackmd.io/@sysprog/git-with-github)（另見 `git-with-github.md`） |
| 編輯器：Visual Studio Code | [hackmd](https://hackmd.io/s/rJPKpohsx) |
| 終端機和 Vim 設定 | [hackmd](https://hackmd.io/s/HJv9naEwl) |
| Makefile 語法和示範 | [hackmd](https://hackmd.io/s/SySTMXPvl) |
| 運用 Perf 定位出效能議題 | [hackmd](https://hackmd.io/@sysprog/linux-perf) |
| Linux 製圖工具: gnuplot | [hackmd](https://hackmd.io/s/Skwp-alOg) |

---

## 為什麼該接觸 GNU/Linux 開發工具

- **學習與研究：** 高品質的編譯器、除錯器、效能分析器、系統模擬器，揭示內部原理
- **專業網絡：** 透過 GitHub 和 Linux Kernel Mailing List 與全球專家連結
- **就業優勢：** 系統層級的 Linux 專家稀缺；大學期間開始學習可累積 ~4 年競爭優勢
- **實作導向：** GNU/Linux 提供從硬體到軟體的完整範例，從基礎到進階逐步提升工程能力

延伸閱讀：[為什麼計算機的學生要學習 Linux 開源技術](https://tinylab.org/why-computer-students-learn-linux-open-source-technologies/)

---

## Visual Studio Code

### 安裝

```shell
# Snap
sudo snap install --classic code

# 或 DEB 套件
sudo dpkg -i <file>.deb

# 或 APT
sudo apt-get update && sudo apt-get install code
```

### 主要功能

- **File Explorer** — 瀏覽專案檔案
- **Search** — 跨檔案搜尋，支援 regex
- **Git Control** — pull, push, commit
- **Debugging** — 設定中斷點，搭配 GDB（需安裝 Native Debug 擴充套件）
- **Extensions** — 安裝與管理外掛

### 設定

- 設定格式：JSON（File → Preferences → Settings）
- Color Theme：File → Preferences → Color Theme
- Keyboard Shortcuts：File → Preferences → Keyboard Shortcuts

### Git 整合

VS Code 自動偵測 `.git`。基本流程：stage（`+` 圖示）→ commit（Ctrl+Enter）→ push。

安裝 "Git History" 擴充套件可視覺化 commit 時間軸。

### 除錯

1. 安裝 "Native Debug" 擴充套件
2. F5 選擇 debugger 類型
3. 設定 `launch.json` 的 target 路徑
4. 點擊行號設定中斷點
5. 綠色播放鈕開始除錯

---

## 終端機和 Vim 設定

### 自訂終端機提示字元

編輯 `~/.bashrc` 中的 `PS1` 變數：

| 代碼 | 顯示 |
|------|------|
| `\u` | 使用者名稱 |
| `\h` | 主機名稱 |
| `\w` | 完整路徑 |
| `\W` | 目前目錄名 |
| `\t` | 時間 hh:mm:ss |

顏色控制：`\e[0;34m` 開始，`\e[0m` 結束。修改後 `source ~/.bashrc` 生效。

### Vim 設定

安裝：`sudo apt-get install vim`

`~/.vimrc` 關鍵設定：
```vim
set ai              " 自動縮排
syntax on           " 語法高亮
set background=dark
set cursorline      " 高亮目前行
set number          " 顯示行號
set expandtab       " Tab 轉空白
set tabstop=4       " Tab 寬度 4
```

外掛管理：Vundle 或 vim-plug。常用外掛：neocomplcache（自動補全）、NERDTree（檔案導覽）。

### Byobu 終端機管理

安裝：`sudo apt-get install byobu`

| 快捷鍵 | 功能 |
|--------|------|
| F2 | 新終端分頁 |
| F3 / F4 | 切換分頁 |
| Shift+F2 | 水平分割 |
| Ctrl+F2 | 垂直分割 |

---

## Makefile 語法和示範

### 基本結構

```makefile
target: dependency1 dependency2
	command    # 行首必須是 <tab>
```

### 變數

| 語法 | 行為 |
|------|------|
| `=` | 延後展開（使用時才求值） |
| `:=` | 立即展開 |
| `?=` | 若未定義則賦值 |
| `+=` | 追加 |

### 自動化變數

| 變數 | 意義 |
|------|------|
| `$@` | 目標檔名 |
| `$<` | 第一個依賴檔名 |
| `$^` | 所有依賴檔名（去重） |
| `$*` | 目標主檔名（不含副檔名） |

### Pattern Rule

```makefile
%.o: %.c
	$(CC) -c -o $@ $<
```

### .PHONY

避免同名檔案干擾，提升執行效率：

```makefile
.PHONY: clean
clean:
	@echo "Clean..."
	-rm *.o
```

### 自動產生依賴

```shell
gcc -MMD -MF program.o.d program.c
```

### 參考

- [GNU Make Manual](https://www.gnu.org/software/make/manual/)

---

## 運用 Perf 定位效能議題

### 什麼是 Perf

Linux v2.6.31 起內建的系統效能分析工具，透過 Performance Monitoring Unit (PMU) 和 kernel tracepoints 收集效能數據。

### 安裝

```shell
sudo apt-get install linux-tools-generic linux-tools-$(uname -r)
```

### 權限設定

```shell
cat /proc/sys/kernel/perf_event_paranoid     # 查看目前權限
sudo sysctl kernel.perf_event_paranoid=-1    # -1: 不限制
```

### 事件類型

- **Hardware events** — CPU cycles, instructions, cache misses, branch misses
- **Software events** — page faults, context switches
- **Tracepoint events** — kernel 追蹤機制

### 核心命令

| 命令 | 用途 |
|------|------|
| `perf list` | 列出支援的事件 |
| `perf stat [-e events] [cmd]` | 執行後顯示統計 |
| `perf record [-e events] [-g] [cmd]` | 取樣記錄（含 call stack） |
| `perf report [-g graph,0.5,caller]` | 從記錄產生報告 |

### 取樣原理

- PMU 硬體計數器追蹤事件（cycles, instructions 等）
- Kernel 設定 period，計數器歸零時觸發中斷，記錄執行上下文
- 取樣準確度取決於**樣本代表性**和**樣本數量**
- **Skid 效應：** 深管線與亂序執行可能導致事件歸因到鄰近的指令

### 實例：矩陣乘法最佳化

1024×1024 矩陣乘法，轉置矩陣 B 後的改善：

| 指標 | v1 | v2 | 改善 |
|------|----|----|------|
| Instructions/Cycle | 4.58 | 24.43 | +433% |
| L1 Cache Misses | 5.2B | 254M | -95% |
| 執行時間 (sec) | 10.40 | 1.67 | -84% |

### 編譯建議

效能分析時使用：
```shell
gcc -g -fno-omit-frame-pointer -O2 program.c
```

`-g` 提供除錯資訊，`-fno-omit-frame-pointer` 確保 call graph 正確。

### Call Graph

兩種解讀模式：
- **Caller-based**（top-down）— 顯示呼叫者及其累積執行時間
- **Callee-based**（bottom-up）— 顯示被呼叫函式及其時間來源

### 關鍵要點

1. 用 perf 量測實際執行行為
2. 用 call graph 找出熱點程式碼路徑
3. 理解硬體與軟體的交互作用（快取、記憶體、CPU 架構）
4. 迭代式地改善並重新量測
