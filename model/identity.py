from model.matrix import Matrix


def identity_matrix(n: int) -> Matrix:
    """
    Tạo ma trận đơn vị cấp n.
    Args:
        n (int): Kích thước của ma trận vuông (n x n).
    Returns:
        Matrix: Đối tượng Matrix là ma trận đơn vị.
    """
    if n <= 0:
        raise ValueError("Kích thước ma trận đơn vị phải lớn hơn 0.")

    # Tạo list 2D với các số 1 trên đường chéo chính và 0 ở các vị trí khác
    id_data = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    # Khởi tạo đối tượng Matrix từ dữ liệu trên
    return Matrix(id_data)

