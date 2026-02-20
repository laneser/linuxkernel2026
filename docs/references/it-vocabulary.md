# 資訊科技詞彙翻譯

> **原始出處：** <https://hackmd.io/@sysprog/it-vocabulary>
> **擷取日期：** 2026-02-19
> **用途：** 撰寫中文技術文件時的術語對照與翻譯原則
> **涵蓋度：** 摘要（約 15%）
> **省略內容：** 各術語的完整詞源考據與歷史脈絡（如 cache、buffer、render、process 等詞彙的詳細論述）

---

## 翻譯原則

1. **追溯詞源** — 理解術語的來源語言與原始含義
2. **語境特定含義** — 同一術語在不同領域可能有不同意義
3. **文化與語言演進** — 考量用法隨時間的變化
4. **避免機械式逐字翻譯** — 區分字面翻譯與實用翻譯

## 術語對照表

| English | 建議中文 | 說明 |
|---------|---------|------|
| cache | 快取 | 強調快速取回；避免與 buffer（緩衝）混淆 |
| render | 算繪 | 用於電腦圖學；強調計算＋繪製，避免「渲染」（藝術意涵） |
| traverse / traversal | 走訪 | 逐一拜訪；避免「遍歷」（暗示一定會走完全部） |
| linked list | 鏈結串列 | 鏈結的序列；不用「鏈表」 |
| concurrent | 並行 | 同時推進；有古典中文根據 |
| process | 行程 / 進程 | 執行中的程式；區別於靜態的 program |
| iterate | 迭代 | 循環重複 |
| optimize | 視語境而定 | 可用「改善」（improve）或「充分利用」（fully utilize），勿濫用「最佳化」 |
| in time | 及時 | just-in-time，在可接受的容許範圍內 |
| real-time | 即時 | 滿足嚴格的 deadline |
| directory | 目錄 | 區別於「檔案夾」(folder) |
| socket | socket | 保留英文；避免「插座」（電氣用語） |
| function | 函式 | 程式設計中的 routine；數學語境用「函數」 |
| implement | 實作 / 實現 | 執行 / 落實 |
| immutable | 不可變 | 區別於 constant（常數） |
| silicon | 矽 | 語音借自日語珪素 |
| power of 2 | 2 的冪 / 2 的乘方 | 2 raised to a power |
| atomic | 不可再分的 | 避免「原子操作」（暗示核子物理意涵） |
| row / column | 橫列 / 縱列 | 注意方向性，或直接保留英文 |
| rational number | 有理數 | 基於 ratio 的數 |
| operator | 運算子 | 執行運算者 |
| operand | 運算元 | 運算的基本單位 |

## 常見問題

- 大陸技術翻譯常過度簡化，應注意區分
- 日語影響的術語借用需考量台灣用法
- 英文中混用的概念在中文中可能需要區分（如 in time vs real-time）
