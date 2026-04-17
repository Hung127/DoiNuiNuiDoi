import copy
import math
from typing import TypeAlias, TypeGuard, overload

from .consts import ABS_TOL
from .row_operation import RowOperation, RowOperationType

# Matrix2DInput ho tro nhieu kieu du lieu, sau khi init xong se cast tat ca sang float
Matrix2DInput: TypeAlias = list[list[float]] | list[list[int]] | list[list[int | float]]
# Vector ho tro nhieu kieu du lieu, sau khi init xong se cast tat ca sang float
Vector1DInput: TypeAlias = list[float] | list[int] | list[int | float]

# kieu du lieu xu ly chinh sau khi thuc hien init xong
Matrix2D: TypeAlias = list[list[float]]
Vector1D: TypeAlias = list[float]


class Matrix:
    """
    Lớp đại diện cho ma trận, hỗ trợ ma trận mở rộng (augmented matrix).

    Lớp này quản lý ma trận dưới dạng danh sách 2 chiều (list of lists),
    với khả năng thêm phần mở rộng (ví dụ: cho hệ phương trình Ax = b).
    Ma trận được lưu trữ dưới dạng float để đảm bảo độ chính xác số học.

    Attributes:
        _matrix (list[list[float]]): Ma trận nội bộ, bao gồm phần chính và phần mở rộng.
        begin_augmented_col (int): Chỉ số cột bắt đầu phần mở rộng (-1 nếu không có).

    Args:
        matrix_a (Matrix2DInput): Ma trận chính (phần A trong Ax = b).
        matrix_b (Matrix2DInput | Vector1DInput | None, optional): 
            Phần mở rộng (phần B), có thể là ma trận hoặc vector. Mặc định None.

    Raises:
        ValueError: Nếu matrix_a không hợp lệ hoặc kích thước không khớp với matrix_b.

    Ví dụ:
        >>> # Ma trận 2x2 đơn giản
        >>> m = Matrix([[1, 2], [3, 4]])
        >>> # Ma trận mở rộng [A | b]
        >>> m_aug = Matrix([[1, 2], [3, 4]], [5, 6])
    """

    @overload
    def __init__(
        # tao ma tran mo rong tu hai ma tran a va b
        self,
        matrix_a: Matrix2DInput,
        matrix_b: Matrix2DInput,
    ): ...

    @overload
    def __init__(
        # tao ma tran mo rong tu hai ma tran a va vector b
        self,
        matrix_a: Matrix2DInput,
        matrix_b: Vector1DInput | None = None,
    ): ...

    def __init__(
        self,
        matrix_a: Matrix2DInput,
        matrix_b: Matrix2DInput | Vector1DInput | None = None,
    ):
        # Khởi tạo ma trận chính từ matrix_a, ép kiểu sang float
        self._matrix: list[list[float]] = [
            [float(x) for x in row] for row in matrix_a
        ]
        if not self._is_valid_matrix_list(self._matrix):
            raise ValueError(
                "Input 'matrix_a' is not a valid matrix. All rows must be non-empty and have the same length."
            )
        matrix_augmented: list[list[float]] | None = None

        if matrix_b is not None:
            if not matrix_b:
                raise ValueError(
                    "Input 'matrix_b' for augmentation cannot be an empty list."
                )

            if self._is_2d_list(matrix_b):
                if not self._is_valid_matrix_list(matrix_b):
                    raise ValueError(
                        "Augmentation 'matrix_b' is not a valid matrix. All rows must have the same length."
                    )
                # Convert to float
                matrix_augmented = [
                    [float(x) for x in row] for row in matrix_b
                ]
            elif self._is_1d_list(matrix_b):
                # Convert to float
                matrix_augmented = [[float(x)] for x in matrix_b]

        if (matrix_augmented is not None and len(matrix_augmented) != len(self._matrix)):
            raise ValueError(
                f"Number of rows in matrix A ({len(self._matrix)}) does not match the number of rows in augmentation B ({len(matrix_augmented) if matrix_augmented else 0})."
            )

        self.begin_augmented_col = -1
        if (matrix_augmented is not None):
            self.begin_augmented_col = len(self._matrix[0])
            for i in range(len(self._matrix)):
                self._matrix[i] += matrix_augmented[i]

    def _is_2d_list(
        self, x: Vector1DInput | Matrix2DInput
    ) -> TypeGuard[list[list[float]]]:
        return len(x) > 0 and all(isinstance(element, list) for element in x)

    def _is_1d_list(self, x: Matrix2DInput | Vector1DInput) -> TypeGuard[list[float]]:
        return (len(x) > 0 and isinstance(x, list) and all(isinstance(element, (int, float)) for element in x))

    def _is_valid_matrix_list(self, matrix: Matrix2DInput) -> bool:
        if not matrix:
            return False
        first_row_len = len(matrix[0])
        if first_row_len == 0:
            return False
        # kiem tra tat ca cac dong deu co so cot bang nhau
        return all(len(row) == first_row_len for row in matrix)

    def _is_valid_vector(self, vector: Vector1DInput | None) -> bool:
        if vector is None:
            return False
        return len(vector) > 0

    def get_number_of_rows_matrix(self) -> int:
        """Trả về số hàng của ma trận (bao gồm phần mở rộng)."""
        return len(self._matrix)

    def get_number_of_rows_augmented(self) -> int:
        # augmented rows = matrix rows
        return self.get_number_of_rows_matrix()

    def get_number_of_cols_matrix(self) -> int:
        """Trả về số cột của phần ma trận chính (không bao gồm phần mở rộng)."""
        return self.begin_augmented_col if self.has_augmentation() else len(self._matrix[0])

    def get_number_of_cols_augmented(self) -> int:
        """Trả về số cột của phần mở rộng."""
        return 0 if not self.has_augmentation() else (len(self._matrix[0]) - self.begin_augmented_col)

    def _find_pivot_on_row(self, row: Vector1D, max_cols: int) -> int:
        for i in range(max_cols + 1):
            if not math.isclose(row[i], 0, abs_tol=ABS_TOL):
                return i
        return -1

    def _check_echelon_rules(self, pivot_cols: list[int]) -> bool:
        prev_pivot = -1
        found_zero_row = False
        for pivot in pivot_cols:
            if found_zero_row and pivot != -1:
                return False  # Non-zero after zero row
            if pivot != -1 and pivot <= prev_pivot:
                return False  # Pivot not strictly right
            if pivot != -1:
                prev_pivot = pivot
            found_zero_row = found_zero_row or (pivot == -1)
        return True

    def is_echelon(self) -> bool:
        """Kiểm tra ma trận có ở dạng bậc thang (echelon form) không."""
        max_cols = self.get_number_of_cols_matrix() - 1
        pivot_cols = [self._find_pivot_on_row(self._matrix[i], max_cols) 
                        for i in range(self.get_number_of_rows_matrix())]
        return self._check_echelon_rules(pivot_cols=pivot_cols)

    def has_augmentation(self) -> bool:
        """Kiểm tra ma trận có phần mở rộng không."""
        return self.begin_augmented_col != -1

    def is_square(self) -> bool:
        """Kiểm tra ma trận có phải vuông không (số hàng = số cột phần chính)."""
        cols = self.begin_augmented_col if self.has_augmentation() else len(self._matrix[0])
        return len(self._matrix) == cols

    def _is_valid_augmentation_access(
        self, i: int, j: int
    ) -> bool:
        return (
            self.has_augmentation()
            and (i >= 0)
            and (j >= 0)
            and (i < len(self._matrix))
            and ((j + self.begin_augmented_col) < len(self._matrix[0]))
        )

    def _is_valid_matrix_access(self, i: int, j: int) -> bool:
        cols = self.get_number_of_cols_matrix()
        rows = self.get_number_of_rows_matrix()
        return (i >= 0) and (j >= 0) and (i < rows) and (j < cols)

    def augmented_access(self, i: int, j: int = 0) -> float:
        """
        Truy cập phần tử trong phần mở rộng.

        Args:
            i (int): Chỉ số hàng.
            j (int): Chỉ số cột trong phần mở rộng (mặc định 0).

        Returns:
            float: Giá trị phần tử.

        Raises:
            IndexError: Nếu không có phần mở rộng hoặc chỉ số ngoài phạm vi.
        """
        # kiem tra xem ma tran co phan mo rong de truy cap hay khong
        if (self.has_augmentation()):
            return self._matrix[i][j + self.begin_augmented_col]
        raise IndexError(
            f"Augmented matrix access out of bounds at row {i}, column {j}."
        )

    def matrix_access(self, i: int, j: int) -> float:
        """
        Truy cập phần tử trong phần ma trận chính.

        Args:
            i (int): Chỉ số hàng.
            j (int): Chỉ số cột.

        Returns:
            float: Giá trị phần tử.

        Raises:
            IndexError: Nếu chỉ số ngoài phạm vi phần ma trận chính.
        """
        if self._is_valid_matrix_access(i, j):
            return self._matrix[i][j]
        raise IndexError(f"Matrix access out of bounds at row {i}, column {j}.")

    def set_matrix_value(self, i: int, j: int, value: float):
        """
        Đặt giá trị phần tử trong phần ma trận chính.

        Args:
            i (int): Chỉ số hàng.
            j (int): Chỉ số cột.
            value (float): Giá trị mới.

        Raises:
            IndexError: Nếu chỉ số ngoài phạm vi phần ma trận chính.
        """
        if (self._is_valid_matrix_access(i, j)):
            self._matrix[i][j] = value
        else:
            raise IndexError(f"Matrix access out of bounds at row {i}, column {j}.")

    def copy(self):
        """Tạo bản sao sâu của ma trận."""
        return copy.deepcopy(self)

    def _validate_target_row(self, row: int) -> None:
        """Validate that the target row index is within bounds."""
        n_rows = self.get_number_of_rows_matrix()
        if not (0 <= row < n_rows):
            raise IndexError(
                f"Target row {row} is out of bounds for a matrix with {n_rows} rows."
            )

    def _validate_source_row(self, row: int | None) -> None:
        """Validate that the source row index is within bounds (if provided)."""
        n_rows = self.get_number_of_rows_matrix()
        if row is not None and not (0 <= row < n_rows):
            raise IndexError(
                f"Source row {row} is out of bounds for a matrix with {n_rows} rows."
            )

    def _swap_rows(self, source_row: int, target_row: int) -> None:
        """Swap two rows in the matrix."""
        self._matrix[target_row], self._matrix[source_row] = self._matrix[source_row], self._matrix[target_row]

    def _add_rows(self, source_row: int, target_row: int, multiplier: float) -> None:
        """Add a multiple of the source row to the target row."""
        self._matrix[target_row] = [
            a + multiplier * b for a, b in zip(self._matrix[target_row], self._matrix[source_row])
        ]

    def _scale_row(self, row_idx: int, multiplier: float) -> None:
        """Scale a row by a multiplier."""
        self._matrix[row_idx] = [a * multiplier for a in self._matrix[row_idx]]

    def apply_row_operation(self, operation: RowOperation) -> float:
        """
        Áp dụng phép biến đổi hàng (row operation) lên ma trận.

        Args:
            operation (RowOperation): Phép biến đổi cần thực hiện.

        Returns:
            float: Hệ số ảnh hưởng đến định thức.

        Raises:
            IndexError: Nếu chỉ số hàng ngoài phạm vi.
            ValueError: Nếu phép biến đổi không hợp lệ.
        """
        # Validate target row
        self._validate_target_row(operation.target_row)

        # Handle operations based on type
        if operation.type == RowOperationType.SWAP:
            self._validate_source_row(operation.source_row)
            if operation.source_row is None:
                raise ValueError("SWAP operation requires a 'source_row'.")
            self._swap_rows(operation.source_row, operation.target_row)
        elif operation.type == RowOperationType.ADD:
            self._validate_source_row(operation.source_row)
            if operation.source_row is None:
                raise ValueError("ADD operation requires a 'source_row'.")
            self._add_rows(operation.source_row, operation.target_row, operation.multiplier)
        elif operation.type == RowOperationType.SCALE:
            self._scale_row(operation.target_row, operation.multiplier)

        return operation.determinant_effect()

    def get_matrix(self) -> Matrix2D:
        """Trả về bản sao sâu của ma trận đầy đủ (bao gồm phần mở rộng nếu có)."""
        return copy.deepcopy(self._matrix)

    def get_matrix_part(self) -> Matrix2D:
        """Trả về bản sao của phần ma trận chính (không bao gồm phần mở rộng)."""
        rows = self.get_number_of_rows_matrix()
        cols = self.get_number_of_cols_matrix()
        return copy.deepcopy([row[:cols] for row in self._matrix[:rows]])

    def get_augmented_part(self) -> Matrix2D | None:
        """
        Trả về bản sao của phần mở rộng dưới dạng ma trận cột, hoặc None nếu không có.

        Returns:
            Matrix2D | None: Ma trận cột chứa phần mở rộng, hoặc None.
        """
        if not self.has_augmentation():
            return None
        rows = self.get_number_of_rows_matrix()
        start_col = self.begin_augmented_col
        return copy.deepcopy([row[start_col:] for row in self._matrix[:rows]])
