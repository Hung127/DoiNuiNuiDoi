# Hill Cipher - Mã Hóa Tuyến Tính

## 📋 Giới Thiệu

**Hill Cipher** là một hệ thống mã hóa đa bảng dựa trên đại số tuyến tính (ma trận). Nó được phát minh năm 1929 bởi Lester S. Hill.

### Nguyên Tắc Hoạt Động

- **Mã hóa**: `C ≡ K × P (mod 26)` - Nhân ma trận khóa với vector bản rõ
- **Giải mã**: `P ≡ K⁻¹ × C (mod 26)` - Nhân ma trận khóa nghịch đảo với vector bản mã
- **Khối**: Văn bản được chia thành các block có kích thước `block_size`

### Ưu & Nhược Điểm

✅ **Ưu điểm**:
- Khó phân tích tần suất ký tự so với Caesar cipher
- An toàn hơn với block size lớn

❌ **Nhược điểm**:
- Dễ bị tấn công nếu biết cặp (bản rõ, bản mã)
- Ma trận khóa phải khả nghịch (det(K) ≠ 0 mod 26)

---

## 🚀 Cách Sử Dụng

### Cài Đặt
```bash
# Không cần cài đặt thêm thư viện, chỉ cần Python 3.9+
python test.py
```

### Ví Dụ Cơ Bản

```python
from hill_cipher import HillCipher

# Tạo cipher với block_size = 2
cipher = HillCipher(block_size=2)

# Mã hóa
plaintext = "HELLO"
ciphertext = cipher.encrypt(plaintext)
print(f"Bản rõ: {plaintext}")
print(f"Bản mã: {ciphertext}")

# Giải mã
decrypted = cipher.decrypt(ciphertext)
print(f"Bản giải mã: {decrypted}")
```

### Ghi Chú
- ✅ Tự động chuyển chữ thường → chữ hoa
- ✅ Giữ nguyên khoảng trống, dấu câu, số
- ✅ Padding tự động nếu độ dài không chia hết cho `block_size`

---

## 📁 Cấu Trúc Dự Án

```
.
├── hill_cipher.py           # Main: Lớp HillCipher
├── model/
│   ├── matrix.py            # Lớp Matrix (ma trận)
│   ├── matrix_transformation.py  # Phép toán: nhân, chuyển vị
│   ├── row_operation.py     # Phép biến đổi hàng sơ cấp
│   ├── identity.py          # Tạo ma trận đơn vị
│   └── consts.py            # Hằng số toán học
├── transformation/
│   ├── determinant.py       # Tính định thức (Gaussian elimination)
│   ├── inverse.py           # Tính ma trận nghịch đảo (Gauss-Jordan)
│   ├── echelon.py           # Đưa ma trận về dạng bậc thang
│   └── gauss_jordan.py      # Gaussian-Jordan elimination
├── test.py                  # Test script
└── README.md                # Tài liệu này
```

---

## 🔧 Các Hàm Chính

### `HillCipher` Class

| Hàm | Mô Tả |
|-----|-------|
| `__init__(block_size)` | Khởi tạo cipher với kích thước khối |
| `encrypt(text)` | Mã hóa văn bản |
| `decrypt(text)` | Giải mã văn bản |

### Ví Dụ Chi Tiết

```python
from hill_cipher import HillCipher

# Block size = 3 (ma trận khóa 3x3)
cipher = HillCipher(block_size=3)

# Test với văn bản chứa khoảng trống
text = "Hello, World!"
encrypted = cipher.encrypt(text)
decrypted = cipher.decrypt(encrypted)

print(f"Original:  {text}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
# Output: Decrypted sẽ giống Original
```

---

## 📊 Toán Học Cơ Bản

### Chuyển Ký Tự → Số
```
A=0, B=1, C=2, ..., Z=25
```

### Ma Trận Khóa
Ma trận khóa `K` là ma trận vuông `block_size × block_size` với:
- Các phần tử ngẫu nhiên trong [0, 26)
- `gcd(det(K), 26) = 1` (để có ma trận nghịch đảo)

### Mã Hóa Một Block
```
plaintext_vector = [P₀, P₁, ..., Pₙ₋₁]ᵀ
ciphertext_vector = (K × plaintext_vector) mod 26
```

---

## ⚠️ Lưu Ý

1. **Block Size**:
   - `block_size=2`: Nhanh nhưng kém an toàn
   - `block_size=3-5`: Cân bằng giữa tốc độ và bảo mật
   - `block_size>5`: Chậm, nhưng an toàn hơn

2. **Ma Trận Khóa**: Được tạo ngẫu nhiên mỗi lần khởi tạo
   - Mỗi instance `HillCipher` có ma trận khóa riêng
   - Nếu cần chia sẻ khóa, cần lưu ma trận khóa riêng

3. **Ký Tự Đặc Biệt**: Giữ nguyên vị trí trong output

---

## 🧪 Test & Chạy Thử

```bash
python test.py
# Nhập: "Hello World"
# Output: Hiển thị bản rõ, bản mã, bản giải mã
```

---

## 📚 Tài Liệu Thêm

### Các Thuật Toán Dùng
- **Gaussian Elimination** (khử Gauss): Tính định thức, bậc thang
- **Gauss-Jordan Elimination**: Tính ma trận nghịch đảo
- **Modular Arithmetic** (số học mô-đun): Làm việc trong Z₂₆

### Độ Phức Tạp
- Mã hóa: O(block_size³) cho mỗi block
- Giải mã: O(block_size³) cho mỗi block
- Khởi tạo: O(block_size³) để tính ma trận nghịch đảo

---

## 📝 Ví Dụ Chạy

```
$ python test.py
Enter something: CRYPTOGRAPHY
Plaintext: CRYPTOGRAPHY
Encrypted: YXMXWEOMIWVL
Decrypted: CRYPTOGRAPHY
```

---

**Tác Giả**: Hill Cipher Implementation  
**Năm**: 2026  
**Ngôn Ngữ**: Python 3.9+
