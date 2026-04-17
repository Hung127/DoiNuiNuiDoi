import random
from math import gcd

from model.matrix import Matrix
from model.matrix_transformation import multiply
from transformation.determinant import determinant
from transformation.inverse import inverse


def multiply_by_number(A: Matrix, number: int) -> Matrix:
    """
    Nhân tất cả phần tử của ma trận với một số.
    
    Args:
        A: Ma trận cần nhân
        number: Số nhân (khác 0)
    
    Returns:
        Ma trận mới sau khi nhân
    
    Raises:
        ValueError: Nếu number == 0
    """
    if number == 0:
        raise ValueError("Can not multiply by 0")
    new_mat = A.copy()
    n_rows = new_mat.get_number_of_rows_matrix()
    n_cols = new_mat.get_number_of_cols_matrix()
    for i in range(n_rows):
        for j in range(n_cols):
            new_mat.set_matrix_value(i, j, round(new_mat.matrix_access(i, j) * number))
    return new_mat

def to_modulo_matrix(A: Matrix, mod: int) -> Matrix:
    """
    Chuyển tất cả phần tử ma trận về modulo (dư số trong phép chia).
    
    Args:
        A: Ma trận gốc
        mod: Modulo (thường là 26 cho Hill Cipher với bảng chữ cái)
    
    Returns:
        Ma trận mới với tất cả phần tử trong range [0, mod)
    """
    new_mat = A.copy()
    n_rows = new_mat.get_number_of_rows_matrix()
    n_cols = new_mat.get_number_of_cols_matrix()
    for i in range(n_rows):
        for j in range(n_cols):
            new_mat.set_matrix_value(i, j, new_mat.matrix_access(i, j) % mod)
    return new_mat


def getAdj(A: Matrix) -> Matrix:
    """
    Tính ma trận liên hợp (Adjugate Matrix).
    
    Toán học: Adj(A) = det(A) × A^(-1)
    
    Lý do: Công thức cơ bản để tính ma trận nghịch đảo là:
        A^(-1) = Adj(A) / det(A)
    Nên Adj(A) = det(A) × A^(-1)
    
    Args:
        A: Ma trận vuông khả nghịch
    
    Returns:
        Ma trận liên hợp của A
    """
    det = round(determinant(A))
    adj_A = multiply_by_number(inverse(A), det)
    return adj_A

def mod_inverse(a: int, m: int) -> int:
    """
    Tìm số nghịch đảo modulo (modular multiplicative inverse).
    
    Toán học: Tìm x sao cho (a × x) ≡ 1 (mod m)
    
    Ý nghĩa trong Hill Cipher:
    - Khi mã hóa: nhân ma trận khóa với vector bản rõ
    - Khi giải mã: cần nhân với ma trận khóa nghịch đảo
    - Để tính được, ta cần det(K)^(-1) mod 26
    
    Args:
        a: Số cần tìm nghịch đảo
        m: Modulo
    
    Returns:
        Số x trong range [1, m) sao cho (a × x) % m == 1
    
    Raises:
        ValueError: Nếu không tồn tại nghịch đảo (khi gcd(a, m) ≠ 1)
    
    Ví dụ: mod_inverse(3, 26) = 9 vì (3 × 9) % 26 = 1
    """
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"{a} has no inverse mod {m}")

def get_inverse_mod(A: Matrix, mod: int) -> Matrix:
    """
    Tính ma trận nghịch đảo modulo (Modular Matrix Inverse).
    
    Toán học: A^(-1) ≡ det(A)^(-1) × Adj(A) (mod m)
    
    Quy trình:
    1. Tính ma trận liên hợp: Adj(A)
    2. Lấy modulo tất cả phần tử
    3. Tính det(A) mod m
    4. Tìm [det(A)]^(-1) mod m (số nghịch đảo)
    5. Nhân Adj(A) với [det(A)]^(-1)
    6. Lấy modulo kết quả cuối cùng
    
    Lý do cần modulo:
    - Hill Cipher làm việc trong trường số nguyên modulo m (Z_m)
    - Ma trận khóa giải mã phải tính toán trong cùng trường này
    
    Args:
        A: Ma trận khóa (phải khả nghịch mod m)
        mod: Modulo (26 cho Hill Cipher tiêu chuẩn)
    
    Returns:
        Ma trận nghịch đảo của A trong Z_mod
    
    Raises:
        ValueError: Nếu det(A) không có nghịch đảo mod m
    """
    adj_A = getAdj(A)
    adj_A_mod = to_modulo_matrix(adj_A, mod)
    det_A_mod = round(determinant(A)) % mod
    inverse_det_A_mod = mod_inverse(det_A_mod, mod)
    res = multiply_by_number(adj_A_mod, inverse_det_A_mod)
    res = to_modulo_matrix(res, mod)
    return res

def generate_invertible_key_matrix(n: int, mod: int) -> Matrix:
    """
    Tạo ma trận khóa ngẫu nhiên khả nghịch modulo.
    
    Toán học: Ma trận khả nghịch mod m ⟺ gcd(det(A), m) = 1
    (det(A) và m phải nguyên tố cùng nhau)
    
    Ý nghĩa: Ma trận khóa phải khả nghịch để tính được ma trận giải mã.
    Nếu det(A) không nguyên tố cùng nhau với 26, không thể giải mã.
    
    Args:
        n: Kích thước ma trận (n×n)
        mod: Modulo (26 cho Hill Cipher)
    
    Returns:
        Ma trận n×n với các phần tử ngẫu nhiên trong [0, mod),
        có tính chất gcd(det, mod) = 1
    """
    while True:
        matrix_list = [[random.randint(0, mod - 1) for _ in range(n)] for _ in range(n)]
        matrix = Matrix(matrix_list)
        det = round(determinant(matrix))
        if gcd(det % mod, mod) == 1:
            return matrix

class HillCipher:
    """
    Mã hóa Hill Cipher - một hệ thống mã hóa đa bảng dựa trên đại số tuyến tính.
    
    Nguyên tắc:
    - Mã hóa: C ≡ K × P (mod 26), K là ma trận khóa, P là vector bản rõ
    - Giải mã: P ≡ K^(-1) × C (mod 26)
    - Chia bản rõ thành các block có kích thước block_size
    
    Ưu điểm: Khó phân tích tần suất chữ cái so với Caesar cipher
    Nhược điểm: Dễ bị tấn công nếu biết một số cặp (bản rõ, bản mã)
    
    Attributes:
        mod: Modulo cố định = 26 (số chữ cái)
        block_size: Kích thước khối (quyết định kích thước ma trận khóa n×n)
        key_matrix: Ma trận khóa mã hóa K
        inversed_key: Ma trận khóa giải mã K^(-1)
    """
    
    def __init__(self, block_size: int):
        """
        Khởi tạo Hill Cipher với kích thước khối.
        
        Args:
            block_size: Số ký tự trong mỗi khối (ma trận khóa sẽ là block_size × block_size)
                       Thường là 2 hoặc 3 (lớn hơn khó tính toán, nhỏ hơn dễ bị tấn công)
        """
        self.mod = 26
        self.block_size = block_size
        self.key_matrix = generate_invertible_key_matrix(self.block_size, self.mod)
        self.inversed_key = get_inverse_mod(self.key_matrix, self.mod)

    def _normalize(self, text: str) -> tuple[str, dict]:
        """
        Chuẩn hóa text: lọc ký tự chữ cái và lưu vị trí ký tự đặc biệt.
        
        Lý do: Hill Cipher chỉ làm việc với A-Z (26 ký tự).
        Nhưng cần giữ nguyên vị trí khoảng trống, dấu câu để output dễ đọc.
        
        Args:
            text: Văn bản gốc (có thể chứa khoảng trống, dấu câu)
        
        Returns:
            (alpha_text, special_characters_dict)
            - alpha_text: Chỉ chứa chữ cái in hoa
            - special_characters_dict: {vị_trí_gốc: ký_tự_đặc_biệt}
        
        Ví dụ: "Hello, World!" → ("HELLOWORLD", {5: ',', 11: '!'})
        """
        alpha_text = ""
        special_characters = {}
        
        for i, ch in enumerate(text):
            if ch.isalpha():
                alpha_text += ch.upper()
            elif ch != '\0':
                special_characters[i] = ch
        
        return alpha_text, special_characters

    def _padding(self, text: str) -> str:
        """
        Thêm padding (null character) để độ dài chia hết cho block_size.
        
        Lý do: Hill Cipher xử lý từng block có kích thước block_size.
        Nếu bản rõ không chia hết, cần padding để tạo block cuối đủ.
        
        Args:
            text: Văn bản cần padding
        
        Returns:
            Văn bản sau khi thêm null character ('\0')
        
        Ví dụ: block_size=2, text="ABC" → "ABC\0" (thêm 1 ký tự)
        """
        if len(text) % self.block_size != 0:
            text += "\0" * (self.block_size - len(text) % self.block_size)
        return text

    def encrypt(self, text: str) -> str:
        """
        Mã hóa văn bản bằng Hill Cipher.
        
        Quy trình:
        1. Chuẩn hóa text (tách ký tự đặc biệt)
        2. Thêm padding nếu cần
        3. Với mỗi block: chuyển thành vector → nhân với ma trận khóa → lấy modulo
        4. Ghép kết quả, giữ nguyên vị trí ký tự đặc biệt
        
        Args:
            text: Bản rõ cần mã hóa
        
        Returns:
            Bản mã hóa (cùng độ dài và format như input)
        """
        origin_len = len(text)
        text, special_characters = self._normalize(text)
        padding_len = len(self._padding(text)) - len(text)
        text = self._padding(text)

        result = ""
        for i in range(0, len(text), self.block_size):
            block = text[i:i + self.block_size]
            block_mat = self.text_to_matrix(block)
            result_mat = multiply(self.key_matrix, block_mat)
            for k in range(result_mat.get_number_of_rows_matrix()):
                val = result_mat.matrix_access(k, 0) % self.mod
                result_mat.set_matrix_value(k, 0, val)
            result += self.matrix_to_text(result_mat)

        real_res = list('\0' * (origin_len + padding_len))
        for i in special_characters:
            real_res[i] = special_characters[i]
        
        result_idx = 0
        for i in range(len(real_res)):
            if real_res[i] == "\0":
                if result_idx < len(result):
                    real_res[i] = result[result_idx]
                    result_idx += 1

        return ''.join(real_res)

    def decrypt(self, encrypted_text: str) -> str:
        """
        Giải mã văn bản đã mã hóa bằng Hill Cipher.
        
        Quy trình: Tương tự encrypt nhưng dùng ma trận khóa nghịch đảo (inversed_key).
        
        Args:
            encrypted_text: Bản mã hóa
        
        Returns:
            Bản rõ gốc (cùng định dạng)
        
        Raises:
            ValueError: Nếu độ dài ký tự chữ cái không chia hết cho block_size
        """
        origin_len = len(encrypted_text)
        encrypted_text, special_characters = self._normalize(encrypted_text)
        if (len(encrypted_text) % self.block_size != 0):
            raise ValueError
        padding_len = len(self._padding(encrypted_text)) - len(encrypted_text)
        encrypted_text = self._padding(encrypted_text)
        result = ""
        for i in range(0, len(encrypted_text), self.block_size):
            block = encrypted_text[i:i + self.block_size]
            block_mat = self.text_to_matrix(block)
            result_mat = multiply(self.inversed_key, block_mat)
            for k in range(result_mat.get_number_of_rows_matrix()):
                val = result_mat.matrix_access(k, 0) % self.mod
                result_mat.set_matrix_value(k, 0, val)
            result += self.matrix_to_text(result_mat)

        real_res = list('\0' * (origin_len + padding_len))
        for i in special_characters:
            real_res[i] = special_characters[i]
        
        result_idx = 0
        for i in range(len(real_res)):
            if real_res[i] == "\0":
                if result_idx < len(result):
                    real_res[i] = result[result_idx]
                    result_idx += 1

        return ''.join(real_res)

    def text_to_matrix(self, text: str) -> Matrix:
        """
        Chuyển string thành ma trận cột (vector).
        
        Phép chuyển: Mỗi ký tự → số (A=0, B=1, ..., Z=25)
        Kết quả: Ma trận cột có kích thước block_size × 1
        
        Args:
            text: Chuỗi ký tự chữ cái (độ dài = block_size)
        
        Returns:
            Ma trận cột chứa giá trị ASCII - ord('A')
        """
        s_matrix = Matrix([[ord(c) - ord('A')] for c in text])
        return s_matrix

    def matrix_to_text(self, matrix: Matrix):
        """
        Chuyển ma trận cột ngược lại thành string.
        
        Phép chuyển ngược: Số → ký tự (0=A, 1=B, ..., 25=Z)
        Với modulo 26 để đảm bảo kết quả trong A-Z
        
        Args:
            matrix: Ma trận cột kết quả từ phép nhân
        
        Returns:
            Chuỗi ký tự chữ cái tương ứng
        """
        return ''.join(chr((int(matrix.matrix_access(i, 0)) % self.mod + ord('A')))
            for i in range(matrix.get_number_of_rows_matrix()))
