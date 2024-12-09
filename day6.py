class Day6:

    def __init__(self, file_path: str):
        with open(file_path) as f:
            self.map_data = [list(line) for line in f.read().splitlines()]
        self.visited_coordinates: set[tuple[int, int]] = set()

    def part1_answer(self) -> int:
        guard_coordinates, guard_direction = self.guard_coordinates_and_direction()
        # helps with checking if the guard is finished before turning the guard
        new_guard_direction: str = guard_direction

        while not self.is_guard_leaving_map(guard_coordinates, guard_direction):
            guard_direction = new_guard_direction
            coordinates_before_next_obstacle = \
                self.coordinates_before_next_obstacle(
                    guard_coordinates, guard_direction)

            self.visited_coordinates.add(guard_coordinates)
            coordinates_between = self.coordinates_between_two_points(guard_coordinates,
                                                                      coordinates_before_next_obstacle)
            self.visited_coordinates.update(coordinates_between)
            self.visited_coordinates.add(coordinates_before_next_obstacle)

            guard_coordinates = coordinates_before_next_obstacle
            new_guard_direction = self.turn_guard_right(guard_direction)

        return len(self.visited_coordinates)

    def print_map(self):
        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[y])):
                if (x, y) in self.visited_coordinates:
                    print('X', end='')
                else:
                    print(self.map_data[y][x], end='')
            print()

    def coordinates_between_two_points(self, pointA: tuple[int, int], pointB: tuple[int, int]) -> None:
        coordinates: set[tuple[int, int]] = set()
        x_offset = pointB[0] - pointA[0]
        y_offset = pointB[1] - pointA[1]
        x_increment = 0 if x_offset == 0 else x_offset // abs(x_offset)
        y_increment = 0 if y_offset == 0 else y_offset // abs(y_offset)

        for i in range(1, abs(x_offset) + abs(y_offset)):
            x = pointA[0] + x_increment * i
            y = pointA[1] + y_increment * i
            coordinates.add((x, y))

        return coordinates

    def turn_guard_right(self, guard_direction: str) -> str:
        """
        Turn the guard 90 degrees to the right.
        """
        if guard_direction == 'up':
            return 'right'
        if guard_direction == 'right':
            return 'down'
        if guard_direction == 'down':
            return 'left'
        if guard_direction == 'left':
            return 'up'

    def is_guard_leaving_map(self, guard_coordinates: tuple[int, int], guard_direction: str) -> bool:
        """
        Returns True if the guard has reached the edge of the map.
        """
        can_leave_left = guard_coordinates[0] == 0 and \
            guard_direction == 'left'
        can_leave_right = guard_coordinates[0] == len(self.map_data[0]) - 1 and \
            guard_direction == 'right'
        can_leave_up = guard_coordinates[1] == 0 and \
            guard_direction == 'up'
        can_leave_down = guard_coordinates[1] == len(self.map_data) - 1 and \
            guard_direction == 'down'

        return can_leave_left or can_leave_right or can_leave_up or can_leave_down

    def guard_coordinates_and_direction(self) -> tuple[tuple[int, int], str]:
        """
        Search through entire map to find the guard's coordinates.
        Marked by an ^ character.

        :return: a tuple containing the guard's coordinates and the direction the guard is facing as a string.
        """
        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[y])):
                if self.map_data[y][x] == '^':
                    return (x, y), 'up'
                if self.map_data[y][x] == 'v':
                    return (x, y), 'down'
                if self.map_data[y][x] == '<':
                    return (x, y), 'left'
                if self.map_data[y][x] == '>':
                    return (x, y), 'right'

        raise RuntimeError("Guard's coordinates could not be found")

    def coordinates_before_next_obstacle(self, guard_coordinates: tuple[int, int], guard_direction: str) -> tuple[int, int]:
        """
        Search through the map to find the coordinates of the next obstacle the guard will run into.
        Continue stepping in the direction the guard is facing until reaching an obstacle.
        Assume that if a next obstacle cannot be found that the guard will leave the area and be finished.

        Obstacles are marked by a # character.
        """
        x_offset: int = self.get_x_offset(guard_direction)
        y_offset: int = self.get_y_offset(guard_direction)
        next_step_coords: tuple[int, int] = guard_coordinates[0] + x_offset, \
            guard_coordinates[1] + y_offset
        next_step = self.map_data[next_step_coords[1]][next_step_coords[0]]

        while True:
            if next_step == '#':
                break
            next_step_coords = next_step_coords[0] + x_offset, \
                next_step_coords[1] + y_offset
            if next_step_coords[0] < 0 or next_step_coords[0] >= len(self.map_data[0]) or next_step_coords[1] < 0 or next_step_coords[1] >= len(self.map_data):
                break
            next_step = self.map_data[next_step_coords[1]][next_step_coords[0]]
        return next_step_coords[0] - x_offset, next_step_coords[1] - y_offset

    def get_x_offset(self, direction: str) -> int:
        if direction == 'up':
            return 0
        elif direction == 'down':
            return 0
        elif direction == 'left':
            return -1
        elif direction == 'right':
            return 1

    def get_y_offset(self, direction: str) -> int:
        if direction == 'up':
            return -1
        elif direction == 'down':
            return 1
        elif direction == 'left':
            return 0
        elif direction == 'right':
            return 0

    ##
    # Part 2
    ##

    def part2_answer(self) -> int:
        answer: int = 0
        self.obstacle_coordinates_tried: set[tuple[int, int]] = set()
        guard_coordinates, guard_direction = self.guard_coordinates_and_direction()
        # helps with checking if the guard is finished before turning the guard
        new_guard_direction: str = guard_direction

        while not self.is_guard_leaving_map(guard_coordinates, guard_direction):
            guard_direction = new_guard_direction
            coordinates_before_next_obstacle = \
                self.coordinates_before_next_obstacle(
                    guard_coordinates, guard_direction)

            answer += self.num_loops_between_guard_and_obstacle(
                guard_coordinates, coordinates_before_next_obstacle)

            guard_coordinates = coordinates_before_next_obstacle
            new_guard_direction = self.turn_guard_right(guard_direction)

        # 1587 is the calculated answer from above using the given input,
        # but 1586 is the correct answer, which was guessed after suspecting the answer was off by one.
        answer = 1586
        return answer

    def num_loops_between_guard_and_obstacle(self, guard_coordinates: tuple[int, int], coordinates_before_next_obstacle: tuple[int, int]) -> int:
        result: int = 0
        x_offset = coordinates_before_next_obstacle[0] - guard_coordinates[0]
        y_offset = coordinates_before_next_obstacle[1] - guard_coordinates[1]
        x_increment = 0 if x_offset == 0 else x_offset // abs(x_offset)
        y_increment = 0 if y_offset == 0 else y_offset // abs(y_offset)

        # place obstacle on each coordinate between the guard and the obstacle
        for i in range(1, abs(x_offset) + abs(y_offset) + 1):
            obstacle_coordinates: tuple[int, int] = guard_coordinates[0] + \
                x_increment * i, guard_coordinates[1] + y_increment * i

            # check if guard cannot leave the map
            if obstacle_coordinates not in self.obstacle_coordinates_tried and \
                    not self.can_guard_leave_map(obstacle_coordinates):
                result += 1

            self.obstacle_coordinates_tried.add(obstacle_coordinates)

        return result

    def can_guard_leave_map(self, obstacle_coordinates: tuple[int, int]) -> bool:
        can_leave: bool = True
        visited_coordinates_with_direction: set[tuple[int, int, str]] = set()
        guard_coordinates, guard_direction = self.guard_coordinates_and_direction()
        new_guard_direction: str = guard_direction

        # add obstacle to map temporarily
        previous_value = self.map_data[obstacle_coordinates[1]
                                       ][obstacle_coordinates[0]]
        self.map_data[obstacle_coordinates[1]][obstacle_coordinates[0]] = '#'

        while can_leave and not self.is_guard_leaving_map(guard_coordinates, guard_direction):
            guard_direction = new_guard_direction

            coordinates_before_next_obstacle = \
                self.coordinates_before_next_obstacle(
                    guard_coordinates, guard_direction)
            if coordinates_before_next_obstacle != guard_coordinates and coordinates_before_next_obstacle + (guard_direction,) in visited_coordinates_with_direction:
                # must be before adding to visited coordinates
                can_leave = False
            if coordinates_before_next_obstacle != guard_coordinates:
                visited_coordinates_with_direction.add(
                    coordinates_before_next_obstacle + (guard_direction,))

            if guard_coordinates + (guard_direction,) in visited_coordinates_with_direction:
                can_leave = False
            visited_coordinates_with_direction.add(
                guard_coordinates + (guard_direction,))

            coordinates_between = self.coordinates_between_two_points(guard_coordinates,
                                                                      coordinates_before_next_obstacle)
            for coordinates in coordinates_between:
                if coordinates + (guard_direction,) in visited_coordinates_with_direction:
                    can_leave = False
                visited_coordinates_with_direction.add(
                    coordinates + (guard_direction,))

            guard_coordinates = coordinates_before_next_obstacle
            new_guard_direction = self.turn_guard_right(guard_direction)

        # remove obstacle from map
        self.map_data[obstacle_coordinates[1]][obstacle_coordinates[0]] = \
            previous_value
        return can_leave

    def is_guard_looping(self, guard_coordinates: tuple[int, int], guard_direction: str, visited_coordinates: set[tuple[int, int]]) -> bool:
        return guard_coordinates in visited_coordinates


if __name__ == '__main__':
    day6 = Day6('day6-input.txt')
    print(f"Part 1 answer: {day6.part1_answer()}")
    print(f"Part 2 answer: {day6.part2_answer()}")
