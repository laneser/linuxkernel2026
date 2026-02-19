# 2025 年 Linux 核心設計/實作課程作業 —— review

> **原始出處：** <https://hackmd.io/@sysprog/linux2025-review>
> **擷取日期：** 2026-02-19
> **用途：** 課程作業 review 規範參考（2025 版，待更新為 2026）

---

## 課程資訊

**授課教師：** [jserv](https://wiki.csie.ncku.edu.tw/User/jserv)

**討論區：** [2025 年系統軟體課程](https://www.facebook.com/groups/system.software2025/)

**返回：** [Linux 核心設計](https://wiki.csie.ncku.edu.tw/linux/schedule) 課程表

**參考資料：**
- [第一次作業檢討 (2023 年)](https://hackmd.io/@sysprog/linux2023-lab0-review)
- [解說錄影 (2021 年)](https://youtu.be/Gwb-PC1azR0)

## 預期學習成果

- 強化 [作業一](https://hackmd.io/@sysprog/linux2025-lab0) 並完成指定里程碑
- 準備 [code review](https://en.wikipedia.org/wiki/Code_review) 並練習 [software peer review](https://en.wikipedia.org/wiki/Software_peer_review)
- 透過批判性檢視與觀察反思工作品質
- 透過建設性批評發展技術溝通技巧
- 建立專業工程能力以打造有影響力的系統

## Code Review 資源

- **影片：** [Amazing Code Reviews: Creating a Superhero Collective](https://youtu.be/ly86Wq_E18o)
- **Google Technical Writing Courses：** [developers.google.com/tech-writing](https://developers.google.com/tech-writing)
  - 核心原則："Every engineer is also a writer."

## 作業要求

### 1. Review 與文件紀錄

研讀 Code Review 材料並更新你的開發紀錄於 [Homework1 作業區](https://hackmd.io/@sysprog/linux2025-homework1)。要點：

- 徹底閱讀 [作業一規格](https://hackmd.io/@sysprog/linux2025-lab0)
- 更新既有筆記而非建立新筆記
- 第一週的作業值得花超過一個月的時間
- 研讀 [2023 review 資料](https://hackmd.io/@sysprog/linux2023-lab0-review)
- 注意：HackMD 有內容長度限制；完整程式碼請存放於 GitHub 或 [gist](https://gist.github.com/)

### Checklist Item 1：Timsort 分析
- 分析 Linux kernel 的 `lib/list_sort.c`
- 評估效能；以 kernel style 為 linked list 開發 Timsort
- 設計對應的排序測試
- **警告：** 使用原生 Linux 安裝，不要用虛擬機，以確保效能評估準確

### Checklist Item 2：學術論文閱讀
- 閱讀 [Dude, is my code constant time?](https://eprint.iacr.org/2016/1123.pdf)
- 閱讀 `lib/list_sort.c` commit [b5c56e](https://github.com/torvalds/linux/commit/b5c56e0cdd62979dd538e5363b06be5bdf735a09) 引用的 3 篇論文
- 辨認與目前 kernel 程式碼的差異
- 包含效能分析實驗
- 參考 [CPython listsort 文件](https://github.com/python/cpython/blob/main/Objects/listsort.txt)
- 測試各種資料分布

### Checklist Item 3：Git 工作流程
- 研讀 [Git 教學與 GitHub 設定指引](https://hackmd.io/@sysprog/git-with-github)（含影片）
- 使用 `git fetch` 取得 [sysprog21/lab0-c](https://github.com/sysprog21/lab0-c) 的最新更新
- 在更新後使用 `git rebase` 將 commit 重新基底
- 解決可能發生的衝突
- 遵循 [commit message 指引](https://chris.beams.io/posts/git-commit/)
- 需要時使用 `git rebase -i` 修改 commit message
- 小心使用 `git push --force`
- **確保 rebase 包含 commit [4a2ff9f](https://github.com/sysprog21/lab0-c/commit/4a2ff9fcab10a87923c4da8573759b10c9223846)**
- 安裝必要字典：`sudo apt install wamerican`

### Checklist Item 4：寫作標準
- 遵循指定的寫作慣例
- 使用 [資訊科技詞彙翻譯](https://hackmd.io/@sysprog/it-vocabulary) 中的術語
- 撰寫清晰、精確、流暢的中文（或正式英文技術標準）
- 理解詞彙語境並使用精確術語作為工程實踐

### Checklist Item 5：程式碼改進
- 提出更可重用、高效能、安全的實作
- 包含實驗與分析
- 參閱 [C Language Specification](https://www.open-std.org/jtc1/sc22/wg14/) 和 [The Linux Programming Interface](https://man7.org/tlpi/)

### Checklist Item 6：信號處理與 I/O
- 研讀 [select(2)](https://man7.org/linux/man-pages/man2/select.2.html)
- 討論 [sysprog21/lab0-c](https://github.com/sysprog21/lab0-c) 中的 timeout 偵測
- 探索 web server 與 linenoise 的共存
- 閱讀 [signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html) 用法

### Checklist Item 7：效能分析工具
- 使用 valgrind、massif、gdb、perf 進行量化分析
- 分析記憶體開銷、指令計數、cache 效能與熱點
- 徹底記錄實驗並討論改進

### Checklist Item 8：課程教材回顧
- 記錄第 1-4 週教材中的發現與問題
- 在開發筆記中描述發現
- 教師與同儕將參與討論

### Checklist Item 9：Shannon Entropy 計算改進
- 重寫 [lab0-c](https://github.com/sysprog21/lab0-c) 中的 `shannon_entropy.c` 和 `log2_lshift16.h`
- 實作更高效的定點數運算與更高 [精確度](https://highscope.ch.ntu.edu.tw/wordpress/?p=24512)
- 包含數學與統計分析
- 參考 [Linux kernel fs/btrfs/compression.c](https://github.com/torvalds/linux/blob/master/fs/btrfs/compression.c) 中的 [Shannon Entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)) 計算

### Checklist Item 10：Pull Requests
- 向 [sysprog21/lab0-c](https://github.com/sysprog21/lab0-c) 提交 bug 修復與改進的 pull request
- 在 GitHub 上進行 code review

### Checklist Item 11：職涯發展閱讀
- 研讀 [Teach Yourself Programming in Ten Years](https://norvig.com/21-days.html)
- 描述你的理解並將課程概念與文章觀點聯繫

### 2. Peer Review 流程

助教會在指定日期從 [Homework1 作業區](https://hackmd.io/@sysprog/linux2025-homework1) 選出 5 名學生進行正式通知。

**Review 指引：**
- 編輯其他學生的文件
- 新增區段：`Reviewed by [你的 GitHub 帳號]`
- 總結意見置於頂部

**Review 重點：**
- Coding style 與 git commit message（檢查他們的 GitHub repository）
- 程式碼與筆記是否符合作業要求（Checklist Items 1-8）
- 實驗設計的缺漏、涵蓋完整度與改進潛力
- 寫作的清晰度、具體性與結構組織
- 對新方法/工具的建設性建議
- GitHub 上的 code review 評論
- 對學生提問的回應

**重要提醒：** 清晰比禮貌重要。直接的回饋促進學習；模糊的語言造成資訊損失。

### 3. 回應與互動

及時回應教師與同儕對你 [Homework1](https://hackmd.io/@sysprog/linux2025-homework1) 筆記的回饋。參與其他學生文件上的問題討論。

### 4. 截止日期：2025 年 4 月 6 日
