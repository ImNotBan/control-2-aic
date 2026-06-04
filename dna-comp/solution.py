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

    raise NotImplementedError("Implement me!")


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
