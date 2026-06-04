import json
import sys
from dataclasses import dataclass
from typing import Dict, List, Set

# Data structures
# ----------------------------------------------------------------------------


@dataclass
class Skill:
    name: str
    cost: int
    attributes: Dict[str, int]
    requires: List[str]


@dataclass
class Synergy:
    skills: List[str]
    bonus: Dict[str, int]


@dataclass
class ProblemInstance:
    budget: int
    scoring: Dict[str, float]
    skills: Dict[str, Skill]
    synergies: List[Synergy]


# Input parsing
# ----------------------------------------------------------------------------


def load_instance(path: str) -> ProblemInstance:
    with open(path, "r") as f:
        data = json.load(f)

    skills = {}
    for skill_name, skill_data in data["skills"].items():
        skills[skill_name] = Skill(
            name=skill_name,
            cost=skill_data["cost"],
            attributes=skill_data["attributes"],
            requires=skill_data["requires"],
        )

    synergies = []
    for synergy_data in data["synergies"]:
        synergies.append(
            Synergy(skills=synergy_data["skills"], bonus=synergy_data["bonus"])
        )

    return ProblemInstance(
        budget=data["budget"],
        scoring=data["scoring"],
        skills=skills,
        synergies=synergies,
    )


# YOUR CODE HERE!
# ----------------------------------------------------------------------------


def my_algorithm(instance: ProblemInstance) -> Set[str]:
    """
    Implement your optimization algorithm here.

    Expected return value:
        A set containing the names of the selected skills.

    Example:
        {
            "Sword Mastery",
            "Critical Strike"
        }
    """
    raise NotImplementedError("Implement me!")


# main
# ----------------------------------------------------------------------------


def main():
    if len(sys.argv) != 2:
        print("Usage: python solution.py instance.json")
        sys.exit(1)

    instance_path = sys.argv[1]
    instance = load_instance(instance_path)
    selected_skills = my_algorithm(instance)
    output_solution(selected_skills)


def output_solution(selected_skills: Set[str]):
    result = {"selected_skills": sorted(selected_skills)}
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
