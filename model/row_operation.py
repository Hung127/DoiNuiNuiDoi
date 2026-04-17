from enum import Enum, auto


class RowOperationType(Enum):
    SWAP = (auto(),)  # hoan vi 2 dong i, j
    SCALE = (auto(),)  # a_i = k * a_i
    ADD = (auto(),)  # a_i = a_i + k a_j


class RowOperation:
    def __init__(
        self,
        type: RowOperationType,
        target_row: int, # dong bi gan lai
        source_row: int | None = None, # dong dung de cong, hoac hoan vi
        multiplier: float = 1, # he so nhan
    ):
        self.type = type
        self.target_row = target_row
        self.source_row = source_row
        self.multiplier = multiplier

        if (
            type == RowOperationType.ADD or type == RowOperationType.SWAP
        ) and source_row is None:
            raise ValueError("ADD and SWAP operations require a 'source_row'.")

        if target_row < 0 or (source_row is not None and source_row < 0):
            raise ValueError("Row indices (target_row, source_row) cannot be negative.")

        if multiplier == 0 and (self.type == RowOperationType.SCALE):
            raise ValueError(
                "SCALE operation is not valid with a multiplier of 0. This is not a reversible elementary operation."
            )

    def determinant_effect(self) -> float:
        if self.type == RowOperationType.SWAP:
            return -1
        elif self.type == RowOperationType.SCALE:
            return self.multiplier
        else:  # add
            return 1
