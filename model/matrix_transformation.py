from .matrix import Matrix, Matrix2D


def transpose(matrix: Matrix) -> Matrix:
    """
    Chuyển vị ma trận

    Args:
        matrix (Matrix): Ma trận đầu vào.

    Returns:
        Matrix: Ma trận chuyển vị (đổi hàng thành cột).
    """
    n_rows = matrix.get_number_of_rows_matrix()
    n_cols = matrix.get_number_of_cols_matrix()
    # Tạo ma trận mới gồm n_cols hàng và n_rows cột
    new_matrix: Matrix2D = [[0.0] * n_rows for _ in range(n_cols)]

    for i in range(n_rows):
        for j in range(n_cols):
            new_matrix[j][i] = matrix.matrix_access(i, j)

    return Matrix(new_matrix)

def multiply(a: Matrix, b: Matrix) -> Matrix:
    """
    Nhân hai ma trận

    Args:
        a (Matrix): Ma trận thứ nhất kích thước (m x n).
        b (Matrix): Ma trận thứ hai kích thước (n x p).

    Returns:
        Matrix: Ma trận kết quả kích thước (m x p).

    Raises:
        ValueError: Nếu số cột của a khác số hàng của b.
    """

    n_rows1 = a.get_number_of_rows_matrix()
    n_cols1 = a.get_number_of_cols_matrix()
    n_rows2 = b.get_number_of_rows_matrix()
    n_cols2 = b.get_number_of_cols_matrix()

    if n_cols1 != n_rows2:
        raise ValueError(f"Cannot multiply {n_rows1}x{n_cols1} matrix by {n_rows2}x{n_cols2} matrix")

    result: Matrix2D = [[0.0] * n_cols2 for _ in range(n_rows1)]
    for r1 in range(n_rows1):
        for c2 in range(n_cols2):
            for k in range(n_cols1):
                result[r1][c2] += a.matrix_access(r1, k) * b.matrix_access(k, c2)

    return Matrix(result)
