# Linux 核心模組運作原理

> **原始出處：** <https://hackmd.io/@sysprog/linux-kernel-module>
> **擷取日期：** 2026-02-20
> **用途：** Linux kernel module 深入機制分析（與 LKMPG 互補）
> **涵蓋度：** 摘要（約 30%）
> **省略內容：** Hello World 完整建構步驟、fibdrv 完整程式碼、insmod/finit_module 系統呼叫追蹤細節、ELF .modinfo 段分析、sysfs 實作細節、lkm-hidden 自我隱藏模組完整分析

---

## 概述

本文件深入分析 Linux kernel module 的內部運作機制，從基礎的 Hello World 到 module 載入的 syscall 流程、ELF 結構，以及可自我隱藏的模組技術。與 LKMPG 互補——LKMPG 側重入門教學，本文側重底層機制。

---

## 1. 前期準備

**Kernel 版本：** 5.4.0 以上

**安全設定：** Ubuntu EFI Secure Boot（kernel 4.4 起強制）需關閉才能載入自訂 kernel module，須在 UEFI 設定中停用。

**必要套件：**
```bash
sudo apt install linux-headers-`uname -r`
```

**驗證安裝：**
```bash
dpkg -L linux-headers-`uname -r` | grep "/lib/modules/.*/build"
```

---

## 2. Hello World Module

**基本結構（`hello.c`）：**
- `#include <linux/init.h>` 和 `#include <linux/module.h>`
- `MODULE_LICENSE("Dual BSD/GPL")`
- `static int hello_init(void)` — 初始化函式
- `static void hello_exit(void)` — 清理函式
- `module_init()` / `module_exit()` 巨集

**Makefile：**
```makefile
obj-m := hello.o
clean:
	rm -rf *.o *.ko *.mod.* *.symvers *.order *.mod.cmd *.mod
```

**編譯與操作：**
```bash
make -C /lib/modules/`uname -r`/build M=`pwd` modules
sudo insmod hello.ko    # 載入
dmesg                   # 查看 kernel 訊息
sudo rmmod hello        # 卸載
```

---

## 3. fibdrv — Fibonacci 數列 Kernel Module

實作字元裝置的實際範例，展示：
- Character device 實作
- Module parameter 處理
- Device file 建立（`/dev/fibonacci`）

```bash
git clone https://github.com/sysprog21/fibdrv
cd fibdrv && make check
modinfo fibdrv.ko       # 顯示模組 metadata
```

---

## 4. Module Metadata 系統（MODULE_* 巨集）

**巨集展開流程：**
1. `MODULE_AUTHOR()` → `MODULE_INFO()` → `__MODULE_INFO()`
2. 建立 `static const char` 陣列，帶有 section attribute
3. 資料放入 `.modinfo` ELF section

**編譯器 attributes：**
- `section(".modinfo")` — 指定 ELF section
- `unused` — 避免編譯器警告
- `aligned(1)` — 最小對齊

使用 `__stringify()` 將 preprocessor token 轉為字串。

---

## 5. Module 載入機制

**System call 流程：**
1. `insmod` 開啟 `.ko` 檔案
2. 呼叫 `finit_module()` system call（傳入 file descriptor）
3. Kernel 執行 `load_module()`
4. `layout_and_allocate()` 進行記憶體配置
5. `do_init_module()` → `do_one_initcall()`
6. 執行使用者定義的初始化函式

**函式別名：** `module_init()` 巨集建立 alias，將使用者的 init 函式映射為 `init_module()`，讓 kernel 能定位並執行。

---

## 6. Sysfs 整合

**Module 註冊：**
Kernel 在 `/sys/module/<module-name>/` 建立目錄，包含：
- 版本資訊
- Reference counting 資料
- Module-specific attributes

使用 `sysfs_create_file()` 動態建立 attribute 檔案。

---

## 7. ELF 檔案結構分析

`.ko` 檔案是 relocatable ELF object（非直接可執行），設計用於 kernel space 整合。

**關鍵組成：**
- **ELF Header** — 檔案 metadata 與 section 資訊
- **Sections** — `.text`, `.data`, `.modinfo`, `.rodata`
- **Section Headers** — 各 section 的 metadata

**檢視工具：**
```bash
readelf -h fibdrv.ko    # Header 資訊
readelf -S fibdrv.ko    # Section headers
objdump -s fibdrv.ko    # Section 內容
```

---

## 8. 可自我隱藏的 Kernel Module

**隱藏技術：**
- 從 `/proc/modules` 列表中移除
- 從 `/sys/modules` sysfs 中刪除
- 從 `vmallocinfo` 中取消註冊
- 解除 module 依賴關係

**使用的關鍵函式：**
- `kallsyms_lookup_name()` — 動態定位 kernel symbols
- `list_del()` — 從 kernel linked list 移除
- `rb_erase()` — 從 red-black tree 移除
- `kobject_del()` — 刪除 sysfs 表示

**參考 Repository：** <https://github.com/sysprog21/lkm-hidden>

---

## 注意事項

- 避免以 root 帳號操作，使用 `sudo` 執行特權操作
- 確保開發用編譯器版本與 kernel build tools 一致，否則 module 載入會失敗

## 延伸閱讀

- [The Linux Kernel Module Programming Guide](https://sysprog21.github.io/lkmpg/)
- Linux Device Drivers (3rd Edition)
- [fibdrv 作業說明](https://hackmd.io/@sysprog/linux2022-fibdrv)
