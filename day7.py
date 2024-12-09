from typing import Union


class Equation:
    def __init__(self, sum: int, values: list[int]):
        self.sum = sum
        self.values = values

    def is_valid(self) -> bool:
        operators: list[str] = ['+'] * (len(self.values) - 1)
        if self.sum == self.calc_sum_with_operators(operators):
            return True
        for i in range(0, 2 ** len(operators)):
            binary = format(i, f'0{len(operators)}b')
            for j in range(0, len(operators)):
                operators[j] = '*' if binary[j] == '1' else '+'
            if self.sum == self.calc_sum_with_operators(operators):
                return True
        return False

    def calc_sum_with_operators(self, operators: list[str]) -> int:
        sum = self.values[0]
        for i in range(1, len(self.values)):
            if operators[i - 1] == '+':
                sum += self.values[i]
            elif operators[i - 1] == '*':
                sum *= self.values[i]
        return sum

    @staticmethod
    def from_string(string: str) -> Union['Equation', None]:
        if not string:
            return None
        sum = int(string.split(':')[0])
        values = list(map(int, string.split(':')[1].split(' ')[1:]))
        return Equation(sum, values)

    def __repr__(self) -> str:
        return f"{self.sum} = {self.values.join(' ? ')}"


class Day7:

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.equations: list[Equation] = self.read_equations_file()

    def part1_answer(self) -> int:
        answer: int = 0
        for equation in self.equations:
            if equation.is_valid():
                answer += equation.sum
        return answer

    def read_equations_file(self) -> list[Equation]:
        equations = []
        with open(self.input_file_path) as file:
            for line in file:
                equations.append(Equation.from_string(line.strip()))
        return equations


if __name__ == '__main__':
    day7 = Day7('day7-input.txt')
    print(f"Part 1 answer: {day7.part1_answer()}")
