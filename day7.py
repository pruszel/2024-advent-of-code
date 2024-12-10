from typing import Union


class Equation:
    def __init__(self, sum: int, operands: list[int]):
        self.sum = sum
        self.operands = operands

    def is_valid_with_operators(self, operators: list[str]) -> bool:
        """Returns True if some possible combination of the given operators with the equation's operands equals the sum."""

        def evaluate(operands: list[int], operators: list[str]) -> int:
            """Calculates the sum of the operands with the given operators."""
            sum = operands[0]
            for i, operator in enumerate(operators[:len(operands) - 1]):
                next_operand = operands[i + 1]
                if operator == '+':
                    sum += next_operand
                elif operator == '*':
                    sum *= next_operand
                elif operator == '||':
                    sum = int(str(sum) + str(next_operand))
            return sum

        def generate_operator_permutations(operators: list[str], current_operators: list[str] = []) -> list[list[str]]:
            """
            Generates all possible permutations of the given operators using recursion.

            Example:
            ['+'],
            ['+', '+'],
            ['+', '*'],
            ['*'],
            ['*', '+'],
            ['*', '*']
            """
            if len(current_operators) == len(self.operands) - 1:
                # got them all
                return [current_operators]
            permutations = []
            for operator in operators:
                permutations.extend(generate_operator_permutations(
                    operators, current_operators + [operator]))
            return permutations

        permutations = generate_operator_permutations(operators)
        for permutation in permutations:
            if evaluate(self.operands, permutation) == self.sum:
                return True

        return False

    @staticmethod
    def from_string(string: str) -> Union['Equation', None]:
        if not string:
            return None
        sum = int(string.split(':')[0])
        operands = list(map(int, string.split(':')[1].split(' ')[1:]))
        return Equation(sum, operands)

    def __repr__(self) -> str:
        return f"{self.sum} = {self.operands.join(' ? ')}"


class Day7:

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.equations: list[Equation] = self.read_equations_file()

    def part1_answer(self) -> int:
        answer: int = 0
        for equation in self.equations:
            answer += equation.sum \
                if equation.is_valid_with_operators(['+', '*']) else 0
        return answer

    def part2_answer(self) -> int:
        answer: int = 0
        for equation in self.equations:
            answer += equation.sum if \
                equation.is_valid_with_operators(['+', '*', '||']) else 0
        return answer

    def read_equations_file(self) -> list[Equation]:
        equations = []
        with open(self.input_file_path) as file:
            for line in file:
                if line.strip():
                    equations.append(Equation.from_string(line.strip()))
        return equations


if __name__ == '__main__':
    day7 = Day7('day7-input.txt')
    print(f"Part 1 answer: {day7.part1_answer()}")
    print(f"Part 2 answer: {day7.part2_answer()}")
