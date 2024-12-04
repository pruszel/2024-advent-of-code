
def calculate_result_by_splitting_input(input_str: str) -> int:
    result: int = 0
    chunks = input_str.split("mul(")
    for i in range(len(chunks)):
        chunk = chunks[i]
        if ')' not in chunk or ',' not in chunk:
            continue

        left: str = chunk.split(",")[0]
        right: str = chunk.split(",")[1].split(")")[0]
        try:
            left_num: int = int(left)
            right_num: int = int(right)
        except ValueError:
            continue
        result += left_num * right_num


def calculate_result_using_regex(input_str: str) -> int:
    import re
    result: int = 0
    pattern = re.compile(r"mul\((\d+),(\d+)\)")
    matches = pattern.findall(input_str)
    for match in matches:
        left: int = int(match[0])
        right: int = int(match[1])
        result += left * right
    return result


def calculate_result_with_conditional_statements(input_str: str) -> int:
    import re
    result: int = 0
    multiplication_enabled = True
    pattern = re.compile(
        r"mul\((\d+),(\d+)\)|(do\(\))|(don\'t\(\))")

    matches = pattern.findall(input_str)
    for match in matches:
        if match[2] == 'do()':
            multiplication_enabled = True
            continue
        if match[3] == "don't()":
            multiplication_enabled = False
            continue
        if multiplication_enabled and match[0].isnumeric() and match[1].isnumeric():
            left: int = int(match[0])
            right: int = int(match[1])
            result += left * right
    return result


def main():
    input_str: str = ""
    with open('day3-input.txt') as f:
        input_str = f.read().strip()

    print(
        f"Answer to part 1\nMultiplication result: {calculate_result_using_regex(input_str)}")
    print(
        f"Answer to part 2\nMultiplication result with conditional statements: {calculate_result_with_conditional_statements(input_str)}")


if __name__ == '__main__':
    main()
