
def report_is_safe(levels: list[int]) -> bool:
    is_increasing: bool = levels[1] > levels[0]

    for i in range(1, len(levels)):
        is_still_increasing_or_decreasing = (
            is_increasing and levels[i] > levels[i-1]) or (not is_increasing and levels[i] < levels[i-1])
        is_at_least_one_apart = levels[i] != levels[i-1]
        is_more_than_3_apart = (
            is_increasing and levels[i] > levels[i-1]+3) or (not is_increasing and levels[i] < levels[i-1]-3)
        is_safe = is_still_increasing_or_decreasing and is_at_least_one_apart and not is_more_than_3_apart
        if not is_safe:
            return False

    return True


def report_is_safe_with_problem_dampener(levels: list[int]) -> bool:
    if report_is_safe(levels):
        return True

    for i in range(len(levels)):
        temp_levels = levels[:i] + levels[i+1:]
        if report_is_safe(temp_levels):
            return True


def main():
    input_str: str = ""
    with open('day2-input.txt') as f:
        input_str = f.read()

    safe_reports: int = 0
    for report in input_str.strip().split('\n'):
        levels: list[int] = [int(num) for num in report.split()]
        if report_is_safe(levels):
            safe_reports += 1
    print(f"Answer to part 1\nSafe reports: {safe_reports}")

    safe_reports_with_problem_dampener: int = 0
    for report in input_str.strip().split('\n'):
        levels: list[int] = [int(num) for num in report.split()]
        if report_is_safe_with_problem_dampener(levels):
            safe_reports_with_problem_dampener += 1

    print(
        f"Answer to part 2\nSafe reports with problem dampener: {safe_reports_with_problem_dampener}")


if __name__ == '__main__':
    main()
