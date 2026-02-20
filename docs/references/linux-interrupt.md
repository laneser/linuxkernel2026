# Linux 核心設計：中斷處理和現代架構考量

> **原始出處：** <https://hackmd.io/@sysprog/linux-interrupt>
> **作者：** Jim Huang (jserv)
> **擷取日期：** 2026-02-20
> **用途：** 課程教材——中斷處理機制（Week 10 主題）
> **涵蓋度：** 摘要（約 30%）
> **省略內容：** PIC/APIC 硬體架構詳細圖解、Intel/ARM 中斷控制器比較、多核心中斷分配機制、虛擬化中斷處理、即時系統中斷延遲分析

---

## 概述

中斷處理涉及硬體特性、多種周邊 I/O、中斷控制器（是否支援 nested）、排程和任務調度、延遲和即時處理等。本文涵蓋 Intel 和 ARM 架構，包括多核處理器、虛擬化技術、及隔離執行（資訊安全）等面向。

---

## 一、硬體中斷基礎

### PIC（Programmable Interrupt Controller）

- 將 IRQ 轉譯為 vector（translates IRQ to vector）
- 向 CPU 發出中斷訊號（raises interrupt to CPU）
- Vector 存於暫存器中，等待 CPU 確認（ACK）
- 中斷可具有不同優先級
- 可在 PIC 或 CPU 層級 mask（禁用）中斷

### 時鐘信號觸發模式

| 模式 | 說明 |
|------|------|
| Level-triggered | 電平觸發——訊號維持某電位時觸發 |
| Positive edge-triggered | 正邊沿觸發——上升沿觸發 |
| Negative edge-triggered | 負邊沿觸發——下降沿觸發 |

---

## 二、中斷處理的上半部與下半部

### 為何需要分離

降低 interrupt latency，將工作分為：

**上半部（Top Half）：**
- 需要盡快執行
- 在禁用部分或全部中斷級別下執行
- 通常處理時間關鍵的硬體事件
- 不在 process context 中運行，不可阻塞（block）

**下半部（Bottom Half）：**
- 處理耗時任務
- 由 softirq、tasklet 或 workqueue 實作

---

## 三、Softirq（軟中斷）

### 結構定義

```c
/* <include/linux/interrupt.h> */
struct softirq_action {
    void (*action)(struct softirq_action *);
};
```

### ksoftirqd 核心執行緒

每個 CPU 一個專用執行緒處理延遲軟中斷：

```c
/* kernel/softirq.c */
static void run_ksoftirqd(unsigned int cpu) {
    local_irq_disable();
    if (local_softirq_pending()) {
        __do_softirq();
        rcu_note_context_switch(cpu);
        local_irq_enable();
        cond_resched();
        return;
    }
    local_irq_enable();
}
```

---

## 四、Tasklet

- 建構於 softirq 之上，可動態配置
- 同一 tasklet 不會在不同 CPU 上同時執行
- 不同 tasklet 可在不同 CPU 上並行

### API

| 函式 | 用途 |
|------|------|
| `DECLARE_TASKLET(name, func, data)` | 靜態建立 tasklet |
| `tasklet_schedule(t)` | 排程執行 |
| `tasklet_hi_schedule(t)` | 高優先排程 |
| `tasklet_disable()` | 禁用 |
| `tasklet_kill()` | 終止 |
| `tasklet_enable()` | 啟用 |

---

## 五、Workqueue（工作佇列）

在 kernel thread（worker thread）中執行，**可休眠、可被搶佔**。

### API

| 函式 | 用途 |
|------|------|
| `create_workqueue(name)` | 建立工作佇列 |
| `DECLARE_WORK(name, func, data)` | 靜態建立 work |
| `INIT_WORK(work, func, data)` | 動態初始化 work |
| `schedule_work(work)` | 排程執行 |
| `flush_scheduled_work()` | 等待所有 work 完成 |

### 與 Tasklet 的差異

| 特性 | Tasklet | Workqueue |
|------|---------|-----------|
| 執行 context | Softirq（atomic） | Process context |
| 可否休眠 | 不可 | 可 |
| 排程方式 | `tasklet_schedule()` | `schedule_work()` |

---

## 六、Threaded Interrupts（執行緒化中斷）

### 特性

- 允許在 sleeping spinlock 中使用（一般 interrupt context 不行）
- PREEMPT_RT 中，所有中斷處理器改為執行緒化
- 主線核心驅動逐漸轉換為 threaded interrupt API（Linux 2.6.30 合併）
- 降低中斷延遲，提升即時性

---

## 七、虛擬化與中斷：GIC-400

### GIC-400（Generic Interrupt Controller v2）

- ARM 中斷控制器架構
- 相容 TrustZone 和虛擬化架構
- 最多支援 8 個 ARM cores

### 四大組件

| 組件 | 暫存器前綴 | 功能 |
|------|-----------|------|
| Distributor | `GICD_*` | 中斷分配與優先級管理 |
| CPU interface | `GICC_*` | CPU 接收中斷 |
| Virtual control interface | `GICH_*` | Hypervisor 虛擬中斷控制 |
| Virtual CPU interface | `GICV_*` | Guest OS 看到的虛擬 CPU 中斷介面 |

後兩個組件專為虛擬化設計（`GICH_*` 和 `GICV_*`）。

---

## 八、實驗資源

- [I/O access and Interrupts](https://linux-kernel-labs.github.io/) — Linux Kernel Labs
- [Examples of Linux Drivers](https://github.com/) — Kernel 4.10 範例
- Linux Kernel Module Programming Guide — Ch.16 Interrupt Handlers
- O'Reilly *Understanding the Linux Kernel* 中斷處理篇

### 注意事項

Linux v4.15 起：`#include <asm/uaccess.h>` 改為 `#include <linux/uaccess.h>`（供 `copy_to_user()` 使用）。

---

## 九、參考文獻

- COMS W4118: Operating Systems（哥倫比亞大學）
- CSE 438/598 Embedded Systems Programming（Arizona State University）
- Linux 核心的中斷子系統（wowotech.net）
- I/O in Linux Hypervisors and Virtual Machines（GitHub）
- ARM Interrupt Virtualization（Linux Foundation 會議）
- Interrupts and Interrupt Handling（Linux Insides）
- GIC-400 簡介（Justin Chu Notes）
