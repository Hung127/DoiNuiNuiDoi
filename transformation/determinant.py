from model.matrix import Matrix

from .echelon import to_echelon_form


def determinant(A: Matrix) -> float:
    """
    Tính định thức của ma trận vuông bằng phương pháp khử Gauss
    với partial pivoting.

    Phương pháp:
        - Thực hiện khử Gauss để đưa ma trận A về dạng tam giác trên U.
        - Khi đó:
              det(A) = (-1)^{k} * ∏ U[i,i]
          trong đó:
              - k là số lần hoán vị hàng (swap_count)
              - U[i,i] là các phần tử trên đường chéo chính của U

    Ảnh hưởng của các phép biến đổi hàng:
        - Hoán vị hai hàng (SWAP): đổi dấu định thức
        - Cộng bội số của một hàng vào hàng khác (ADD): không đổi định thức
        - Không sử dụng phép nhân hàng (SCALE), nên không cần hiệu chỉnh thêm

    Ổn định số học:
        - Sử dụng partial pivoting để giảm sai số làm tròn.
        - Nếu xuất hiện pivot rất nhỏ, kết quả có thể bị ảnh hưởng
          do hệ số khuếch đại sai số (ill-conditioned).

    Args:
        A (Matrix): Ma trận vuông kích thước n x n.

    Returns:
        float: Giá trị định thức của ma trận A.
            - det = 0: ma trận suy biến (singular)
            - det ≠ 0: ma trận khả nghịch (invertible)

    Raises:
        ValueError: Nếu A không phải ma trận vuông.

    Độ phức tạp:
        O(n^3) do sử dụng Gaussian elimination.

    Ghi chú:
        - Hàm không làm thay đổi ma trận A ban đầu (do to_echelon_form sử dụng bản sao).
        - Định thức được tính gián tiếp thông qua dạng tam giác trên,
          không sử dụng khai triển Laplace (vốn có độ phức tạp cao).
    """
    if not A.is_square():
        raise ValueError("Determinant is only defined for square matrices")

    # Đưa A về dạng tam giác trên bằng Gaussian elimination (partial pivoting)
    U, swap_count = to_echelon_form(A)

    # Định thức của ma trận tam giác trên = tích các phần tử đường chéo
    det = 1.0
    n = U.get_number_of_rows_matrix()

    for i in range(n):
        det *= U.matrix_access(i, i)

    # Mỗi lần hoán vị hàng làm đổi dấu định thức
    return det * ((-1) ** swap_count)
