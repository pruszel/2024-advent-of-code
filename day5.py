class Day5:

    def __init__(self, rules: list[list[int, int]] = None, pages: list[list[int]] = None):
        self.rules = rules
        self.pages = pages

    def read_input(self, file_path: str) -> tuple[list[list[int, int]], list[list[int]]]:

        # [
        #   [47, 53], <-- rule_nums (first, second)
        #   [97, 13],
        #   ...
        # ]
        self.rules: list[list[int, int]] = []

        # [
        #   [75,47,61,53,29], <-- page_nums
        #   [97,61,53,29,13],
        #   ...
        # ]
        self.pages: list[list[int]] = []

        with open(file_path) as f:
            for line in f:
                if line == '\n':
                    break
                """
                Convert rule string '47|53' to list of ints [47, 53]
                """
                self.rules.append(list(map(int, line.strip().split('|'))))
            for line in f:
                """
                Convert page numbers string '75,47,61,53,29' to list of ints [75, 47, 61, 53, 29]
                """
                self.pages.append(list(map(int, line.strip().split(','))))

    def calc_valid_middle_page_sum(self) -> int:
        valid_middle_page_sum: int = 0

        for page_nums in self.pages:
            valid_middle_page_sum += self.get_middle_page(page_nums) \
                if self.is_valid_page_nums(page_nums) else 0

        return valid_middle_page_sum

    def calc_invalid_middle_page_sum(self) -> int:
        invalid_middle_page_sum: int = 0

        for page_nums in self.pages:
            if self.is_valid_page_nums(page_nums):
                continue
            page_nums: list[list[int]] = \
                self.reorder_page_nums(page_nums)
            invalid_middle_page_sum += self.get_middle_page(page_nums)

        return invalid_middle_page_sum

    def is_valid_page_nums(self, page_nums: list[int]) -> bool:
        """
        Iterate through rules and check if the first number is found after the second number.
        To be valid, the first number should be found **before** the second number.
        """
        for first, second in self.rules:
            try:
                first_index = page_nums.index(first)
                second_index = page_nums.index(second)
                if first_index > second_index:
                    return False
            except ValueError:
                continue

        return True

    def get_middle_page(self, page_nums: list[int]) -> int:
        return page_nums[len(page_nums) // 2]

    def reorder_page_nums(self, page_nums: list[int]) -> list[int]:
        """
        Re-orders the given page numbers so that they satisfy all related rules.
        """
        rule_violations: list[list[int]] = \
            self.find_rule_violations(page_nums)
        for rule in rule_violations:
            if page_nums.index(rule[0]) > page_nums.index(rule[1]):
                new_position: int = \
                    self.find_new_position_for_page(page_nums, rule[0])
                page_nums.insert(new_position,
                                 page_nums.pop(page_nums.index(rule[0])))

        return page_nums

    def find_new_position_for_page(self, page_nums: list[int], page: int) -> int:
        """
        Find the rules relevant to the given page, where the rule has the page number as the first number (should go before).
        Of those rules, return the smallest index (closest to 0) of the second number in given page numbers.
        The new position for the first number to be placed will be the farthest left position, just before the second number.
        """
        all_rules_for_page: list[list[int, int]] = [
            rule for rule in self.rules if rule[0] == page]

        smallest_index_of_second_number: int = len(page_nums)
        for rule in all_rules_for_page:
            _, second = rule
            try:
                smallest_index_of_second_number = \
                    min(smallest_index_of_second_number, page_nums.index(second))
            except ValueError:
                continue

        return smallest_index_of_second_number

    def find_rule_violations(self, page_nums: list[int]) -> list[list[int]]:
        """
        Returns a list of all instances where the first number in a rule is found after the second number in the given page numbers.
        """
        violations: list[list[int, int]] = []

        for rule in self.rules:
            first, second = rule
            try:
                first_index = page_nums.index(first)
                second_index = page_nums.index(second)
                if first_index > second_index:
                    violations.append(rule)
            except ValueError:
                continue

        return violations


def main():
    solution = Day5()
    solution.read_input('day5-input.txt')
    print(
        f"Answer to part 1\nSum of the middle page numbers of the valid page updates: {solution.calc_valid_middle_page_sum()}")
    print(
        f"Answer to part 2\nSum of the middle page numbers of the invalid page updates after re-ordering them correctly: {solution.calc_invalid_middle_page_sum()}")


if __name__ == '__main__':
    main()
