import math

from model.consts import ABS_TOL, PIVOT_WARN_TOL
from model.matrix import Matrix
from model.row_operation import RowOperation, RowOperationType


def to_echelon_form(A: Matrix) -> tuple[Matrix, int]:
    """
    Thực hiện khử Gauss với partial pivoting để đưa ma trận về dạng bậc thang (row echelon form).

    Thuật toán:
        - Duyệt từng cột và chọn pivot là phần tử có trị tuyệt đối lớn nhất
          trong cột đó (từ hàng hiện tại trở xuống).
        - Thực hiện hoán vị hàng nếu cần (partial pivoting) để đưa pivot lên vị trí đầu.
        - Dùng phép biến đổi sơ cấp để khử các phần tử bên dưới pivot.
        - Bỏ qua cột nếu toàn bộ phần tử trong cột gần bằng 0 (theo ABS_TOL).

    Ổn định số học:
        - Nếu giá trị pivot nhỏ hơn PIVOT_WARN_TOL, hàm sẽ in cảnh báo vì
          hệ phương trình có thể không ổn định số học (ill-conditioned).
        - Việc sử dụng partial pivoting giúp giảm sai số làm tròn nhưng
          không loại bỏ hoàn toàn vấn đề này.

    Args:
        A (Matrix): Ma trận đầu vào (có thể là ma trận mở rộng [A|b]).

    Returns:
        tuple[Matrix, int]:
            - Matrix: Ma trận dạng bậc thang trên (echelon form).
            - int: Số lần thực hiện hoán vị hàng trong quá trình khử.

    Raises:
        ValueError: Nếu ma trận rỗng hoặc không hợp lệ.
    """
    if A.get_number_of_rows_matrix() == 0 or A.get_number_of_cols_matrix() == 0:
        raise ValueError("Matrix must not be empty")

    U = A.copy()
    n_rows = U.get_number_of_rows_matrix()
    n_cols = U.get_number_of_cols_matrix()
    swap_count = 0
    pivot_row = 0

    for col in range(n_cols):
        if pivot_row >= n_rows:
            break
        # Partial pivoting
        max_row = pivot_row
        max_val = abs(U.matrix_access(pivot_row, col))
        for r in range(pivot_row + 1, n_rows):
            val = abs(U.matrix_access(r, col))
            if val > max_val:
                max_val = val
                max_row = r
        # Nếu cả cột = 0 thì bỏ qua
        if math.isclose(max_val, 0, abs_tol=ABS_TOL):
            continue
        # Kiểm tra pivot gần bằng 0, hệ có thể không ổn định số học (ill-conditioned).
        if max_val < PIVOT_WARN_TOL:
            print(f"Warning: Pivot at column {col} is very small ({max_val}) -> possible ill-conditioned system")
        # Swap nếu cần
        if max_row != pivot_row:
            op = RowOperation(RowOperationType.SWAP, pivot_row, max_row)
            U.apply_row_operation(op)
            swap_count += 1
        pivot = U.matrix_access(pivot_row, col)

        # Khử các dòng bên dưới
        for r in range(pivot_row + 1, n_rows):
            val = U.matrix_access(r, col)
            if math.isclose(val, 0, abs_tol=ABS_TOL):
                continue
            factor = -val / pivot
            op = RowOperation(RowOperationType.ADD, target_row=r, source_row=pivot_row, multiplier=factor)
            U.apply_row_operation(op)
        pivot_row += 1

    return U, swap_count
