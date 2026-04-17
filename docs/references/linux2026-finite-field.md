> **原始出處：** https://hackmd.io/@sysprog/BJ7DvyPtWg
> **擷取日期：** 2026-04-17
> **用途：** basics 作業指定閱讀教材 (有限體算術與 2^k 索引)
> **涵蓋度：** 完整
> **省略內容：** 無

# 有限體算術與 $2^k$ 索引：Linux 核心對數學封閉性與硬體成本的權衡

## 摘要
在 Linux 核心中，模運算並非單一技術問題，而是隨子系統目標而改變的工程選擇。以密碼學為例，X25519 的運算域是由 RFC 7748 固定為質數域 $GF(2^{255}-19)$。核心的責任是在通用處理器上實作符合規範且具備恆定時間特性 (constant-time) 的有限體算術基本操作，使演算法既能維持數學正確性，也能避免側信道洩漏。一般資料結構中的雜湊索引並不要求可逆性，也不需要維持群或體的代數結構；其任務是以盡可能低的整數運算成本，將鍵值快速映射到固定大小的 bucket 空間，並儘量降低碰撞與記憶體層級成本。Linux 核心因此普遍採用 $2^k$ 大小的索引空間，搭配乘法混合後取高位元的策略來完成映射。從數學角度看，這類索引實際上運作於整數環 $\mathbb{Z}/2^k\mathbb{Z}$ 中，而非質數域。

這二種實作表面上都涉及模的概念，但真正關心的失敗模式完全不同。X25519 的風險在於數學結果錯誤，或私鑰資訊經由執行時間、分支路徑與記憶體存取模式洩漏。RFC 7748 明確提醒，實作者應避免洩漏資訊的分支、記憶體存取與一般除法。雜湊索引則可能因分佈不均而產生大量碰撞，使搜尋鏈結變長，進而增加額外的快取失誤與記憶體存取成本。前者必須維持質數域上的封閉性與反元素存在性，後者則直接依附處理器字寬所提供的自然溢位與位元截斷，以最低成本完成索引運算。

## 核心背景：連結抽象代數、微架構與原始程式碼
理解 Linux 核心在這二種模運算上的不同策略，需要同時觀察抽象代數、微架構與實際原始程式碼。在 [include/linux/hash.h](https://github.com/torvalds/linux/blob/master/include/linux/hash.h) 中，Linux 核心對整數與指標鍵值的雜湊方式相當直接：輸入先乘上大的奇數常數，再取乘積的高位元作為索引。其概念可簡化為
```c
index = (val * C) >> (BITS - k);
```

其中 `C` 是常數，`BITS` 是整數寬度，而 `k` 是 bucket 空間的位元數。Linux 核心目前的定義與註解可概括為下列形式：
```c
#define GOLDEN_RATIO_32 0x61C88647
#define GOLDEN_RATIO_64 0x61C8864680B583EBull

static inline u32 hash_32(u32 val, unsigned int bits)
{
    return (val * GOLDEN_RATIO_32) >> (32 - bits);
}

static inline u64 hash_64(u64 val, unsigned int bits)
{
    return (val * GOLDEN_RATIO_64) >> (64 - bits);
}
```

核心註解直接指出 "high bits are more random, so use them"。其理由可從微架構理解。乘法不是單純把低位元留在低位元、高位元留在高位元；輸入位元的差異會透過硬體乘法器內部的 carry chain 向高位端傳播，形成位元傳播效果。從這個角度看，乘積的高位元實際上攜帶了整個輸入字更完整的混合資訊，因此較適合作為索引。若輸入本身具有結構性，例如指標因對齊而使低位元長期為零，直接取低位元做 bucket 選擇就會導致碰撞高度集中；乘法混合後取高位元，則可有效打散這種偏斜。

第二個背景是 X25519 的演算法路徑。RFC 7748 給出的 X25519 並非在仿射座標中直接操作，而是使用 Montgomery ladder 搭配 XZ 投影座標。演算法迴圈中維持二組投影狀態，並以固定形式的加法、減法、平方與乘法更新。最後一步才將投影座標還原為仿射座標，方式是計算有限體中的反元素，也就是以 $x_2 \cdot z_2^{p-2}$ 得到輸出。這裡的關鍵不只是避免中途除法，更重要的是整個 ladder 的執行形狀固定，私鑰位元不應影響控制流結構。RFC 7748 甚至明確要求 `cswap` 以 constant-time 的方式實作，避免秘密資訊反映在跳躍或記憶體存取行為上。

第三個背景是 Fiat-Crypto 在 Linux 核心中的作用。[lib/crypto/curve25519-fiat32.c](https://github.com/torvalds/linux/blob/master/lib/crypto/curve25519-fiat32.c) 開頭的註解就說這是機器產生、經由[形式化驗證](https://hackmd.io/@sysprog/formal-verification)的實作，來源是 Fiat-Crypto，之後再為核心環境做調整。該實作將一個 field element 表示為 10 個 `u32` limb，交錯使用 26 位元與 25 位元邊界。這種切分並非隨意安排，而是精準對應到 32 位元處理器上的乘加路徑：2 個 26 位元 limb 相乘，最大不超過 52 位元，因此可以安全放入 `u64` 中，並在累積多個部分乘積後再統一傳遞進位。也就是說，這種 25/26 位元交錯的表示法讓延遲進位成為可能，使大數算術能展開為一連串固定的整數運算，而不是頻繁依賴即時約簡或資料相依分支。這種安排同時兼顧了正確性、可驗證性以及微架構上的實作效率。

## 針對不同考量的模運算
在 Linux 核心中，密碼學與雜湊表都會出現模運算，但二者要避免的失敗模式並不相同。對 X25519 而言，首要問題是正確性與側信道安全。若結果算錯，協定即失效；若執行時間、分支路徑或記憶體存取模式受私鑰影響，則可能形成計時攻擊。RFC 7748 特別提醒，實作者要避免與秘密資料相依的跳躍、記憶體存取，甚至是可能具有輸入相依時間特性的除法。這表示密碼學實作的失敗不只是算錯，還包括算對但洩漏資訊。

Linux 核心中的 `fe_cswap` 恰好把這種設計思維表現得非常清楚。簡化的程式碼如下：
```c
static void fe_cswap(fe f, fe g, unsigned int b)
{
    b = 0 - b;
    for (i = 0; i < 10; i++) {
        u32 x = b & (f[i] ^ g[i]);
        f[i] ^= x;
        g[i] ^= x;
    }
}
```

這裡 `b = 0 - b` 的精妙之處，在於它利用二補數特性將布林值展開為遮罩。當 `b` 為 1 時，`0 - b` 會變成全 1 遮罩；當 `b` 為 0 時，結果維持全 0。後續交換動作便可完全藉由 XOR 與 AND 完成，而不需要任何條件分支。對處理器而言，這代表相同的指令序列、相同的控制流形狀，以及更穩定的分支預測與指令快取行為。從微架構角度看，這不只是 branchless 技巧，更是有意將私鑰位元隔離在資料路徑中，避免其污染控制路徑。

雜湊索引面對的則是另一種失敗模式。它不要求可逆性，也不嘗試從 bucket index 還原原始鍵值。真正重要的是，當輸入位元模式具有結構性時，是否仍能維持足夠均勻的分佈。這在核心中特別常見，因為許多鍵值其實是指標，而指標常因 8 或 16 位元組對齊而使低位元長期固定為零。若直接以 `% m` 取模，或只看低位元，便可能把這種規律原封不動帶入 bucket 選擇，形成明顯碰撞。Linux 因此採用乘法混合後取高位元的方式，先將低位元中的差異傳播到高位，再以高位元決定 bucket。這麼做的目的不是追求密碼學上的抗碰撞，而是避免結構化輸入使搜尋鏈結過長，連帶拖累快取與記憶體存取表現。

## 模數結構的代數意義與實作影響
X25519 所使用的模數為 $p = 2^{255}-19$。這是個質數，因此底層數域是 $GF(p)$。在有限體中，每個非零元素都存在乘法反元素，這正是 Montgomery ladder 能在投影座標中穩定運作、並在最後一步將 $x/z$ 還原為仿射座標的數學基礎。RFC 7748 的參考程序直接以 $z^{p-2}$ 取得反元素，這等價於利用費馬小定理完成 inversion。這一點不是數學上的裝飾，而是整個演算法路徑得以避開一般除法、又維持封閉性的核心依據。

雜湊索引的情況則完全不同。當 bucket 數量為 $2^k$ 時，整數運算可視為在環 $\mathbb{Z}/2^k\mathbb{Z}$ 中進行。這個環不是有限體，其中確實存在大量零因子；但 Linux 核心在選擇乘法常數時，刻意使用奇數。這個細節在代數上非常重要，因為在 $\mathbb{Z}/2^k\mathbb{Z}$ 中，任何奇數都與 $2^k$ 互質，依據貝祖定理，必定存在乘法反元素。換句話說，乘上奇數本身是一個雙射，不會平白丟失資訊熵。真正的資訊截斷發生在最後取高 $k$ 位元的那一步，而不是乘法本身。這也說明為何 Linux 核心可將乘法當作混合步驟：先用可逆的整數置換將資料打散，再以高位元截取完成不可逆的壓縮。如此的分工不僅工程上高效，在代數上也相當簡潔。

## 4. Curve25519 的微架構實作
X25519 的模數 $2^{255}-19$ 屬於 pseudo-Mersenne 形式，其關鍵性質是
$$
2^{255} \equiv 19 \pmod p
$$

這使得高於 bit 255 的部分不必經過一般除法才能約簡，而可直接折返成乘以 19 再加回低位的形式。RFC 7748 選擇這個質數的一個重要理由，就是它在軟體與硬體實作上都相對友善。對 Linux 核心而言，這意味著模約簡可以展開為固定型態的乘法、加法與位移，而不需要通用除法這種延遲高、且可能具有輸入相依行為的操作。

`curve25519-fiat32.c` 的 10-limb 25/26 位元表示法正是為這種折返約簡服務。由於 limb 乘積最多約為 52 位元，部分結果可以安全保存在 `u64` 中，並延後處理 carry。這種 delayed carry 的策略使乘法與加法能以更直通的資料路徑完成，而非每一步都穿插完整約簡。從編譯器與微架構的角度看，Fiat-Crypto 所產生的程式碼等於把大數有限體算術壓平為一串沒有資料相依分支的整數操作，讓編譯器更容易映射到底層的 add-with-carry 類型機制。

Montgomery ladder 的另一個關鍵優勢，在於其迭代形狀完全固定。從最高位到最低位，X25519 會執行固定次數的迴圈，每一輪皆遵循同一組指令模式。這不僅避免了資料相依的控制流，也使指令快取與分支預測器所觀察到的行為保持穩定。對密碼學而言，這種固定性很重要，因為計時側信道並不只來自顯式 `if` 分支，也可能來自微架構內部對控制流與記憶體模式的放大效應。Montgomery ladder 的價值，正是在演算法層與微架構層同時封住這些洩漏路徑。

## Linux 核心雜湊實作
在 [include/linux/hash.h](https://github.com/torvalds/linux/blob/master/include/linux/hash.h) 中，Linux 核心對雜湊常數的演進本身就是一段很有代表性的工程史。早期核心曾使用一個 bit-sparse 的 64 位元常數 `0x9e37fffffffc0001UL`，其名稱中帶有 `GOLDEN_RATIO_PRIME`，並刻意選成可藉由位移與加減來近似乘法的形式。這種設計思路在當時看似合理，因為它能減少某些平台上乘法的成本；但後來實務發現，這類稀疏常數的位元混合效果並不好，甚至被核心註解直接形容為 actively bad for hashing。
> The "GOLDEN_RATIO_PRIME" is used in fs/btrfs/brtfs_inode.h and fs/inode.c.  It's not actually prime any more (the previous primes were actively bad for hashing), but the name remains

現行核心已改用 `0x61C8864680B583EBull` 作為 `GOLDEN_RATIO_64`，並在註解中明白說明，現在不再要求它是質數，名稱只是[歷史遺留](https://android.googlesource.com/kernel/common/+/refs/tags/ASB-2021-05-05_3.18-o-mr1/include/linux/hash.h)。這段演進說明：對雜湊而言，能否把輸入位元均勻打散，遠比常數在數論上是否是質數來得重要。
>  Knuth recommends primes in approximately golden ratio to the maximum integer representable by a machine word for multiplicative hashing.
>  Chuck Lever verified the effectiveness of this technique: http://www.citi.umich.edu/techreports/reports/citi-tr-00-1.pdf
>  These primes are chosen to be bit-sparse, that is operations on them can use shifts and additions instead of multiplications for machines where multiplications are slow.

目前 Linux 核心的相關定義可寫成
```c
#define GOLDEN_RATIO_64 0x61C8864680B583EBull

static inline u64 hash_64(u64 val, unsigned int bits)
{
    return (val * GOLDEN_RATIO_64) >> (64 - bits);
}
```

這個常數非常接近黃金比例相關值，屬於 Fibonacci hashing 一脈的選擇。它的價值不在於質數性，而在於能將連續輸入或具規律的鍵值較均勻地散布到整個空間。Linux 核心在註解中也直接提到 Knuth 與 golden ratio 的背景。結合前述的整數環觀點，整個雜湊流程其實相當清楚：先以奇數乘法在 $\mathbb{Z}/2^k\mathbb{Z}$ 中做一個可逆置換，再取高位元作為最終索引。從硬體觀點看，這只用到乘法與位移；從代數觀點看，則是將資訊流失延後到最後一步的位元截取。

## 結論
Linux 核心中的 X25519 與一般雜湊索引，展示二種截然不同的工程策略。對 X25519 而言，模數由規格固定，核心無權更改；因此設計焦點不在於挑選較方便的數域，而在於如何於既定質數域上，以固定控制流實作正確、可驗證且具 constant-time 性質的有限體算術。Montgomery ladder、pseudo-Mersenne 約簡、遮罩式交換，及 Fiat-Crypto 產生的 limb 算術，都是這個目標下的自然結果。

對雜湊索引而言，核心則徹底站在另一側。它不追求有限體所帶來的可逆性與封閉性，也不在乎零因子是否存在，因為 bucket index 本來就不是用來還原原始鍵值的。真正重要的是，以最低的整數運算成本做出足夠好的位元打散。$2^k$ bucket 空間、奇數乘法、取高位元，以及放棄歷史上混合效果不佳的 bit-sparse prime，正好體現這種務實取向。

當需要抵禦攻擊時，核心會不計成本地以微架構技巧維持數學封閉性與執行路徑穩定性；當只需打散資料時，它則毫不猶豫地擁抱自然溢位、位元截斷與最便宜的整數基本操作。這種衡量在數學結構與硬體成本之間的取捨，正是 Linux 核心經典的工程判斷。