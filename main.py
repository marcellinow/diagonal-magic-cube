from tensor import *

tensor = Tensor(5,5,5)

# print(f"magic constant: {tensor.magic_constant()}")
# print(f"straight lines: {tensor.straight_line()}")
# print()
tensor.initial_state_tensor()
tensor.print_tensor()

# row_result = tensor.check_row_sum()
# column_result = tensor.check_column_sum()
# diagonal_result = tensor.check_diagonal_sum()
# print(f"Row Result: {row_result}")
# print(f"Column Result: {column_result}")
# print(f"Diagonal Result: {diagonal_result}")
