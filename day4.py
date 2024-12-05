from typing import Union, Tuple


def count_xmas_occurrences(grid: list[list[str]]) -> int:
    xmas_count: int = 0

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            xmas_count += count_xmas_from_cell(grid, row, col)

    return xmas_count


def count_xmas_from_cell(grid, row, col) -> int:
    if grid[row][col] != 'X':
        return 0

    # search in every direction for M, A, S
    xmas_count: int = 0
    xmas_count += 1 \
        if search_in_direction(grid, row, col, 'top_left', ['M', 'A', 'S']) else 0
    xmas_count += 1 \
        if search_in_direction(grid, row, col, 'top', ['M', 'A', 'S']) else 0
    xmas_count += 1 \
        if search_in_direction(grid, row, col, 'top_right', ['M', 'A', 'S']) else 0
    xmas_count += 1 \
        if search_in_direction(grid, row, col, 'right', ['M', 'A', 'S']) else 0
    xmas_count += 1 \
        if search_in_direction(grid, row, col, 'bottom_right', ['M', 'A', 'S']) else 0
    xmas_count += 1 \
        if search_in_direction(grid, row, col, 'bottom', ['M', 'A', 'S']) else 0
    xmas_count += 1 \
        if search_in_direction(grid, row, col, 'bottom_left', ['M', 'A', 'S']) else 0
    xmas_count += 1 \
        if search_in_direction(grid, row, col, 'left', ['M', 'A', 'S']) else 0

    # if xmas_count > 0:
    #     print(f"found {xmas_count} XMAS from [{row}, {col}]\n")

    return xmas_count


def search_in_direction(grid, row, col, direction, target) -> bool:
    if not target:
        # print(f"found XMAS by searching to the: {direction}")
        return True

    top_left, \
        top, \
        top_right, \
        right, \
        bottom_right, \
        bottom, \
        bottom_left, \
        left = get_surrounding_letters(grid, row, col)

    if direction == 'top_left' and top_left == target[0]:
        return search_in_direction(grid, row - 1, col - 1, direction, target[1:])
    elif direction == 'top' and top == target[0]:
        return search_in_direction(grid, row - 1, col, direction, target[1:])
    elif direction == 'top_right' and top_right == target[0]:
        return search_in_direction(grid, row - 1, col + 1, direction, target[1:])
    elif direction == 'right' and right == target[0]:
        return search_in_direction(grid, row, col + 1, direction, target[1:])
    elif direction == 'bottom_right' and bottom_right == target[0]:
        return search_in_direction(grid, row + 1, col + 1, direction, target[1:])
    elif direction == 'bottom' and bottom == target[0]:
        return search_in_direction(grid, row + 1, col, direction, target[1:])
    elif direction == 'bottom_left' and bottom_left == target[0]:
        return search_in_direction(grid, row + 1, col - 1, direction, target[1:])
    elif direction == 'left' and left == target[0]:
        return search_in_direction(grid, row, col - 1, direction, target[1:])
    else:
        return False


def get_surrounding_letters(grid: list[list[str]], row: int, col: int) -> Tuple[Union[str, None], Union[str, None], Union[str, None], Union[str, None], Union[str, None], Union[str, None], Union[str, None], Union[str, None]]:
    top_left = grid[row - 1][col - 1] \
        if row != 0 and col != 0 else None

    top = grid[row - 1][col] if row != 0 else None

    top_right = grid[row - 1][col + 1] \
        if row != 0 and col != len(grid[0]) - 1 else None

    right = grid[row][col + 1] \
        if col != len(grid[0]) - 1 else None

    bottom_right = grid[row + 1][col + 1] \
        if row != len(grid) - 1 and col != len(grid[0]) - 1 else None

    bottom = grid[row + 1][col] \
        if row != len(grid) - 1 else None

    bottom_left = grid[row + 1][col - 1] \
        if row != len(grid) - 1 and col != 0 else None

    left = grid[row][col - 1] if col != 0 else None

    return top_left, top, top_right, right, bottom_right, bottom, bottom_left, left


def count_mas_in_x_shape(grid: list[list[str]]) -> int:
    mas_in_x_shape_count: int = 0

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            mas_in_x_shape_count += 1 \
                if is_mas_in_x_shape_from_cell(grid, row, col) else 0

    return mas_in_x_shape_count


def is_mas_in_x_shape_from_cell(grid, row, col) -> bool:
    if grid[row][col] != 'A':
        return False

    mas_in_bottom_left_to_top_right_diagonal = \
        (search_in_direction(grid, row, col, 'bottom_left', ['M']) and
         search_in_direction(grid, row, col, 'top_right', ['S'])) or \
        (search_in_direction(grid, row, col, 'bottom_left', ['S']) and
         search_in_direction(grid, row, col, 'top_right', ['M']))

    mas_in_top_left_to_bottom_right_diagonal = \
        (search_in_direction(grid, row, col, 'top_left', ['M']) and
         search_in_direction(grid, row, col, 'bottom_right', ['S'])) or \
        (search_in_direction(grid, row, col, 'top_left', ['S']) and
         search_in_direction(grid, row, col, 'bottom_right', ['M']))

    if mas_in_bottom_left_to_top_right_diagonal and mas_in_top_left_to_bottom_right_diagonal:
        return True

    return False


def main():

    input_str: str = ''
    with open('day4-input.txt') as f:
        input_str = f.read()

    grid = [list(row) for row in input_str.split('\n') if row]

    xmas_count: int = count_xmas_occurrences(grid)
    print(f"Answer to part 1\nXMAS count: {xmas_count}")

    mas_in_x_shape_count: int = count_mas_in_x_shape(grid)
    print(f"Answer to part 2\nMAS in X shape count: {mas_in_x_shape_count}")


if __name__ == '__main__':
    main()
