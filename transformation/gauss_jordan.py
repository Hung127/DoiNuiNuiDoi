import math

from model.consts import ABS_TOL
from model.matrix import Matrix
from model.row_operation import RowOperation, RowOperationType

from .echelon import to_echelon_form


def gauss_jordan_elimination(A: Matrix) -> Matrix:
    """
    Bien doi ma tran ve dang bac thang rut gon (RREF) bang cach tan dung Gaussian Elimination.
    Gia su matrix da la ma tran ghep [A | I] hoac [A | B].
    """
    # buoc 1: khu xuoi - tan dung ham Gaussian Elimination da co 
    U, _ = to_echelon_form(A)

    n_rows = U.get_number_of_rows_matrix()
    n_cols = U.get_number_of_cols_matrix()

    # buoc 2: khu nguoc (back-substitution) tu dong cuoi len dong dau
    # tim pivot cua tung dong de khu cac phan tu phia tren no 
    for r in range(n_rows - 1, -1, -1):
        # 1. Tim vi tri pivot (phan tu khac 0 dau tien cua dong r)
        pivot_col = -1
        for c in range(n_cols):
            if not math.isclose(U.matrix_access(r, c), 0, abs_tol=ABS_TOL):
                pivot_col = c
                break

        # neu dong toan so 0 thi bo qua
        if pivot_col == -1:
            continue

        # 2. Chuan hoa dong r de pivot tai (r, pivot_col) bang 1
        pivot_val = U.matrix_access(r, pivot_col)
        if not math.isclose(pivot_val, 1.0, abs_tol=ABS_TOL):
            scale_op = RowOperation(RowOperationType.SCALE, target_row = r, multiplier = 1.0/pivot_val)
            U.apply_row_operation(scale_op)

        # 3. Khu tat ca cac phan tu phia tren pivot thanh so 0
        for i in range(r - 1, -1, -1):
            val_above = U.matrix_access(i, pivot_col)
            if not math.isclose(val_above, 0, abs_tol=ABS_TOL):
                # R_i = R_i - val_above * R_r
                add_op = RowOperation(
                    RowOperationType.ADD,
                    target_row = i,
                    source_row = r,
                    multiplier = -val_above
                )
                U.apply_row_operation(add_op)

    return U
