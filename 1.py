# https://adventofcode.com/2024/day/1

def main():
    total_distance: int = 0
    input_str: str = ""
    left_ids = []
    right_ids = []

    with open('1-input.txt', 'r') as f:
        input_str = f.read()

    for line in input_str.strip().split('\n'):
        left_id, right_id = map(int, line.strip().split())
        left_ids.append(left_id)
        right_ids.append(right_id)
    left_ids = sorted(left_ids)
    right_ids = sorted(right_ids)

    for left_id, right_id in zip(left_ids, right_ids):
        total_distance += abs(right_id - left_id)

    print(f"Answer to part 1\nTotal distance: {total_distance}")

    similarity_score: int = 0
    freq_map = {}
    for id in right_ids:
        if id not in freq_map:
            freq_map[id] = 1
        else:
            freq_map[id] += 1

    for id in left_ids:
        if id in freq_map:
            similarity_score += id * freq_map[id]

    print(f"Answer to part 2\nSimilarity score: {similarity_score}")


if __name__ == '__main__':
    main()
