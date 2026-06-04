#!/usr/bin/env python3

import json
import sys
from dataclasses import dataclass
from typing import List, Dict, Any

# Data structures
# ----------------------------------------------------------------------------


@dataclass
class ProblemInstance:
    sequence: str
    literal_cost: int
    copy_cost: int
    length_cost: int
    min_match_length: int


# Input parsing
# ----------------------------------------------------------------------------


def load_instance(path: str) -> ProblemInstance:

    with open(path, "r") as f:
        data = json.load(f)

    return ProblemInstance(
        sequence=data["sequence"],
        literal_cost=data["literal_cost"],
        copy_cost=data["copy_cost"],
        length_cost=data["length_cost"],
        min_match_length=data["min_match_length"],
    )


# YOUR CODE HERE!
# ----------------------------------------------------------------------------


def my_algorithm(instance: ProblemInstance) -> List[Dict[str, Any]]:
    """
    Implement your compression algorithm here.

    Return value:
        A list of encoding operations.

    Example:

    [
        {
            "type": "literal",
            "char": "A"
        },
        {
            "type": "literal",
            "char": "A"
        },
        {
            "type": "copy",
            "offset": 2,
            "length": 2
        }
    ]
    """
    sequence = instance.sequence
    n = len(sequence)

    dp = [float("inf")] * (n + 1)
    previous = [None] * (n + 1)
    dp[0] = 0

    # dp[i] guarda el millor cost per comprimir fins a la posicio i.
    for i in range(n):
        literal_cost = dp[i] + instance.literal_cost
        if literal_cost < dp[i + 1]:
            dp[i + 1] = literal_cost
            previous[i + 1] = (i, {"type": "literal", "char": sequence[i]})

        for start in range(i):
            max_length = min(i - start, n - i)
            length = 0
            while length < max_length and sequence[start + length] == sequence[i + length]:
                length += 1

            for copy_length in range(instance.min_match_length, length + 1):
                cost = dp[i] + instance.copy_cost + instance.length_cost * copy_length
                end = i + copy_length
                if cost < dp[end]:
                    dp[end] = cost
                    previous[end] = (
                        i,
                        {
                            "type": "copy",
                            "offset": i - start,
                            "length": copy_length,
                        },
                    )

    operations = []
    pos = n
    while pos > 0:
        prev_pos, operation = previous[pos]
        operations.append(operation)
        pos = prev_pos

    operations.reverse()
    return operations


# Output
# ----------------------------------------------------------------------------


def output_solution(operations):

    result = {"operations": operations}

    print(json.dumps(result, indent=4))


# Main
# ----------------------------------------------------------------------------


def main():

    if len(sys.argv) != 2:
        print("Usage: python solution.py instance.json")
        sys.exit(1)

    instance_path = sys.argv[1]

    instance = load_instance(instance_path)

    operations = my_algorithm(instance)

    output_solution(operations)


if __name__ == "__main__":
    main()
