import math

from model.consts import ABS_TOL
from model.identity import identity_matrix
from model.matrix import Matrix

from .determinant import determinant
from .gauss_jordan import gauss_jordan_elimination


def inverse(A: Matrix) -> Matrix:
    """
    Tính ma trận nghịch đảo của A sử dụng phương pháp Gauss-Jordan.

    Hàm tìm ma trận A^(-1) sao cho A * A^(-1) = A^(-1) * A = I,
    trong đó I là ma trận đơn vị cùng kích thước.

    Phương pháp:
        1. Kiểm tra A là ma trận vuông
        2. Tính định thức det(A). Nếu det(A) = 0, ma trận suy biến, không có nghịch đảo
        3. Tạo ma trận ghép [A | I] (A với phần mở rộng là ma trận đơn vị)
        4. Áp dụng Gauss-Jordan elimination trên [A | I]
        5. Kết quả là [I | A^(-1)], trích xuất phần bên phải để được A^(-1)

    Công thức:
        Nếu [A | I] →(Gauss-Jordan) [I | A^(-1)]
        thì A^(-1) là phần mở rộng của ma trận kết quả

    Args:
        A (Matrix): Ma trận đầu vào (kích thước n x n).
                   Phải là ma trận vuông (is_square() == True).
                   Phải khả nghịch (det(A) ≠ 0).

    Returns:
        Matrix: Ma trận nghịch đảo A^(-1) có kích thước n x n.
               Thỏa mãn: A * A^(-1) = I và A^(-1) * A = I

    Raises:
        ValueError:
            - Nếu ma trận không phải vuông
            - Nếu ma trận suy biến (det(A) = 0)

    Ví dụ:
        >>> # Ma trận 2x2 khả nghịch
        >>> A = Matrix([[4, 7], [2, 6]])
        >>> A_inv = inverse(A)
        >>> # A_inv ≈ [[0.6, -0.7], [-0.2, 0.4]]

        >>> # Ma trận 3x3
        >>> A = Matrix([[1, 2, 3], [0, 1, 4], [5, 6, 0]])
        >>> A_inv = inverse(A)
        >>> # A * A_inv ≈ I (ma trận đơn vị)

        >>> # Ma trận suy biến (Không khả nghịch)
        >>> A = Matrix([[1, 2], [2, 4]])
        >>> A_inv = inverse(A)  # Raise ValueError

        >>> # Ma trận không vuông
        >>> A = Matrix([[1, 2, 3], [4, 5, 6]])
        >>> A_inv = inverse(A)  # Raise ValueError

    Ghi chú:
        - Độ phức tạp thời gian: O(n³) do Gauss-Jordan elimination
        - Hàm kiểm tra tính khả nghịch bằng định thức trước khi tính toán
        - Sử dụng hằng số ABS_TOL (từ model.consts) để so sánh floating-point
        - Không sửa đổi ma trận đầu vào gốc
        - Sử dụng phương pháp Gauss-Jordan (hiệu quả hơn công thức Cramer cho ma trận lớn)
        - Kết quả có độ chính xác phụ thuộc vào độ ổn định số của máy tính

    Thuật toán chi tiết:
        1. Lấy số hàng n = A.rows
        2. Kiểm tra A là ma trận vuông
        3. Tính det(A), nếu ≈ 0 thì bất khả nghịch
        4. Tạo ma trận đơn vị I (n x n)
        5. Tạo ma trận ghép [A | I] (n x 2n)
        6. Áp dụng Gauss-Jordan elimination trên [A | I]
           - Kết quả là [I | A^(-1)]
        7. Trích xuất phần mở rộng (cột n đến 2n-1) để được A^(-1)
        8. Trả về A^(-1)
    """
    n = A.get_number_of_rows_matrix()

    # Kiểm tra ma trận vuông
    if not A.is_square():
        raise ValueError("Ma tran phai la ma tran vuong moi co nghich dao!")

    # Tính định thức của A
    # Nếu det(A) = 0, ma trận suy biến, không khả nghịch
    det = determinant(A)
    if math.isclose(det, 0, abs_tol=ABS_TOL):
        raise ValueError("Ma tran suy bien (det = 0), khong the tim ma tran nghich dao!")

    # Tạo ma trận đơn vị I (n x n)
    # I sẽ là phần mở rộng của ma trận ghép
    i_obj = identity_matrix(n)

    # Tạo ma trận ghép [A | I]
    augmented_matrix = Matrix(A.get_matrix_part(), i_obj.get_matrix_part())

    # Áp dụng Gauss-Jordan elimination trên [A | I]
    # Kết quả sẽ là [I | A^(-1)]
    res_augmented = gauss_jordan_elimination(augmented_matrix)

    # Trích xuất phần mở rộng (A^(-1)) từ ma trận kết quả
    # Phần mở rộng nằm từ cột n đến cột 2n-1
    inv_data = []
    for i in range(n):
        row_inv = []
        for j in range(n):
            # Truy cập phần tử mở rộng tại vị trí (i, j)
            # augmented_access(i, j) tương đương với matrix_access(i, n + j)
            val = res_augmented.augmented_access(i, j)
            row_inv.append(val)
        inv_data.append(row_inv)

    # Trả về ma trận nghịch đảo
    return Matrix(inv_data)
