# Introduction to Linux Kernel Driver Programming（中文摘譯）

> **原始出處：** <https://events19.linuxfoundation.org/wp-content/uploads/2017/12/Introduction-to-Linux-Kernel-Driver-Programming-Michael-Opdenacker-Bootlin-.pdf>
> **作者：** Michael Opdenacker (Bootlin)
> **授權：** Creative Commons Attribution – Share Alike 4.0
> **擷取日期：** 2026-02-20
> **用途：** Linux kernel device driver 開發入門（device model + Device Tree）
> **涵蓋度：** 完整（中文摘譯）

---

## 概述

本演講介紹 Linux kernel 的 **device model** 架構與 **device driver** 開發方式。核心問題：同一個裝置驅動程式如何在不同 CPU 架構（x86, ARM…）、不同硬體控制器上運作？答案是透過 device model 將驅動程式與硬體描述分離。

---

## 1. 為什麼需要 Device Model

- 同一裝置驅動需在多種 CPU 架構上運作，即使硬體控制器不同
- 單一驅動需支援多個同類裝置
- 需要清晰的程式碼組織：驅動程式、控制器驅動、硬體描述各自分離

---

## 2. Driver 的角色：介於 Bus Infrastructure 與 Framework 之間

在 Linux 中，一個 driver 同時對接：

- **Framework** — 以通用方式暴露硬體功能（如 network、IIO、input 等 subsystem）
- **Bus infrastructure** — 屬於 device model 的一部分，負責偵測與通訊硬體

---

## 3. Device Model 三大資料結構

| 結構 | 說明 |
|------|------|
| `struct bus_type` | 代表一種匯流排（USB, PCI, I2C 等） |
| `struct device_driver` | 代表一個能處理特定匯流排上特定裝置的驅動程式 |
| `struct device` | 代表一個連接在匯流排上的裝置 |

Kernel 使用**繼承**（inheritance）為每個匯流排子系統建立更特化的版本。

---

## 4. Bus Driver（以 USB 為例）

以 USB 為例（`drivers/usb/core/`）：

1. 建立並註冊 `bus_type` 結構
2. 提供 API 給 **adapter driver**（USB 控制器）— 偵測已連接的裝置並通訊
3. 提供 API 給 **device driver**（USB 裝置驅動）
4. 將 device driver 與 adapter driver 偵測到的裝置進行**配對（matching）**
5. 定義特化結構：`struct usb_driver`、`struct usb_interface`

**關鍵：** 同一個驅動可支援連接在不同控制器上的相容裝置。

---

## 5. Device Driver 開發三步驟

### 步驟一：宣告支援的裝置

```c
static struct usb_device_id rtl8150_table[] = {
    { USB_DEVICE(VENDOR_ID_REALTEK, PRODUCT_ID_RTL8150) },
    { USB_DEVICE(VENDOR_ID_MELCO, PRODUCT_ID_LUAKTX) },
    /* ... */
    {}
};
MODULE_DEVICE_TABLE(usb, rtl8150_table);
```

### 步驟二：註冊管理 hook

```c
static struct usb_driver rtl8150_driver = {
    .name       = "rtl8150",
    .probe      = rtl8150_probe,
    .disconnect = rtl8150_disconnect,
    .id_table   = rtl8150_table,
    .suspend    = rtl8150_suspend,
    .resume     = rtl8150_resume
};
```

### 步驟三：向 bus core 註冊

```c
static int __init usb_rtl8150_init(void)
{
    return usb_register(&rtl8150_driver);
}
module_init(usb_rtl8150_init);
```

> **注意：** 現代寫法已用 `module_usb_driver()` 巨集取代上述樣板程式碼。

---

## 6. `probe()` 函式的工作

`probe()` 在每個新配對的裝置上被呼叫：

1. **初始化裝置**
2. **準備驅動運作：** 配置 framework 結構、記憶體、映射 I/O、註冊中斷
3. **一切就緒後，** 向 framework 註冊新裝置

### 載入時序

1. USB adapter driver 向 USB core 註冊
2. rtl8150 device driver 向 USB core 註冊
3. USB core 得知 vendor/product ID 與 `struct usb_driver` 的對應關係

### 裝置偵測時序

1. 裝置連接 → adapter driver 偵測到
2. USB core 比對 device table → 找到對應的 driver
3. 呼叫 driver 的 `probe()` 函式

**模型是遞迴的：** adapter driver 本身也是 device driver！

---

## 7. Platform Devices 與 Platform Drivers

### 問題

許多裝置不在能自動偵測的匯流排上（嵌入式系統中極為常見）：UART、flash、LED、GPIO、MMC/SD、Ethernet…

### 解決方案

1. 提供裝置描述（Device Tree）
2. 透過一個假的匯流排管理：**platform bus**
3. 以 platform driver 驅動 platform device

---

## 8. Device Tree（裝置樹）

### 結構

- **`.dts`**（Device Tree Source）— 每個板子一份，描述板級裝置配置
- **`.dtsi`**（Device Tree Source Include）— 描述 SoC 層級的共用裝置
- 優勢：新板子不需寫 kernel code（如果所有裝置都已有驅動）

### `.dtsi` 範例（SoC 層級裝置宣告）

```dts
/* arch/arm/boot/dts/am33xx.dtsi */
i2c0: i2c@44e0b000 {
    compatible = "ti,omap4-i2c";    /* 對應的驅動 */
    reg = <0x44e0b000 0x1000>;      /* 暫存器起始位址與範圍 */
    interrupts = <70>;
    status = "disabled";            /* 預設不啟用 */
};
```

### `.dts` 範例（板級裝置實例化）

```dts
/* arch/arm/boot/dts/am335x-boneblue.dts */
&i2c0 {
    pinctrl-names = "default";
    pinctrl-0 = <&i2c0_pins>;
    status = "okay";                /* 啟用此裝置 */
    clock-frequency = <400000>;

    baseboard_eeprom: baseboard_eeprom@50 {
        compatible = "at,24c256";
        reg = <0x50>;
    };
};
```

### Pin Multiplexing

現代 SoC 的硬體模組數量多於封裝引腳數量，因此引腳必須**多工（multiplexing）**。引腳配置定義在 Device Tree 中，正確的 pin mux 是裝置運作的前提。

### Device Tree Bindings

- 在 `Documentation/devicetree/bindings/` 中提供規格
- 查找方式：`git grep "ti,omap4-i2c" Documentation/devicetree/bindings/`

---

## 9. 裝置與驅動的配對

Platform driver 透過 `compatible` 屬性與 platform device 配對：

```c
/* drivers/i2c/busses/i2c-omap.c */
static const struct of_device_id omap_i2c_of_match[] = {
    { .compatible = "ti,omap4-i2c", .data = &omap4_pdata },
    { /* sentinel */ }
};

static struct platform_driver omap_i2c_driver = {
    .probe  = omap_i2c_probe,
    .remove = omap_i2c_remove,
    .driver = {
        .name           = "omap_i2c",
        .of_match_table = of_match_ptr(omap_i2c_of_match),
    },
};
```

在 `probe()` 中，驅動透過 platform bus API 取得裝置資訊：

```c
irq = platform_get_irq(pdev, 0);
mem = platform_get_resource(pdev, IORESOURCE_MEM, 0);
omap->base = devm_ioremap_resource(&pdev->dev, mem);
of_property_read_u32(node, "clock-frequency", &freq);
```

---

## 10. I2C Driver 範例

### `probe()` 函式（`drivers/iio/accel/mma7660.c`）

```c
static int mma7660_probe(struct i2c_client *client,
                         const struct i2c_device_id *id)
{
    struct iio_dev *indio_dev;
    struct mma7660_data *data;

    /* 配置 framework 結構（含 per-device 資料） */
    indio_dev = devm_iio_device_alloc(&client->dev, sizeof(*data));
    data = iio_priv(indio_dev);
    data->client = client;

    /* bus 結構 ↔ framework 結構 互相引用 */
    i2c_set_clientdata(client, indio_dev);
    indio_dev->dev.parent = &client->dev;

    /* 設定 framework 屬性 */
    indio_dev->info = &mma7660_info;
    indio_dev->channels = mma7660_channels;

    /* 啟用裝置 → 註冊至 framework（user-space 可存取） */
    mma7660_set_mode(data, MMA7660_MODE_ACTIVE);
    return iio_device_register(indio_dev);
}
```

### `remove()` 函式

```c
static int mma7660_remove(struct i2c_client *client)
{
    struct iio_dev *indio_dev = i2c_get_clientdata(client);

    iio_device_unregister(indio_dev);   /* 先從 framework 移除 */
    return mma7660_set_mode(             /* 再停用裝置 */
        iio_priv(indio_dev), MMA7660_MODE_STANDBY);
}
```

### 註冊（三種配對方式）

```c
/* 1. I2C name matching（必要） */
static const struct i2c_device_id mma7660_i2c_id[] = {
    {"mma7660", 0}, {}
};

/* 2. Device Tree compatible matching */
static const struct of_device_id mma7660_of_match[] = {
    { .compatible = "fsl,mma7660" }, {}
};

/* 3. ACPI matching（x86 平台） */
static const struct acpi_device_id mma7660_acpi_id[] = {
    {"MMA7660", 0}, {}
};

static struct i2c_driver mma7660_driver = {
    .driver = {
        .name           = "mma7660",
        .of_match_table = mma7660_of_match,
        .acpi_match_table = ACPI_PTR(mma7660_acpi_id),
    },
    .probe    = mma7660_probe,
    .remove   = mma7660_remove,
    .id_table = mma7660_i2c_id,
};
module_i2c_driver(mma7660_driver);
```

---

## 11. Driver 開發建議

1. **找相似裝置的程式碼** 作為起點
2. **讀程式碼** — 可用 [Elixir](https://elixir.bootlin.com/) 線上瀏覽
3. **由下往上讀** — 先看大架構（`module_init`、driver 結構），再深入細節

---

## 延伸閱讀

- [Bootlin kernel/driver 訓練教材](https://bootlin.com/training/kernel/)（完整版）
- [Device Tree for Dummies](http://j.mp/1jQU6NR) — Thomas Petazzoni (2014)
