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
    skills = instance.skills

    def skill_value(skill: Skill) -> float:
        return sum(
            instance.scoring.get(attribute, 0.0) * value
            for attribute, value in skill.attributes.items()
        )

    def synergy_value(synergy: Synergy) -> float:
        return sum(
            instance.scoring.get(attribute, 0.0) * value
            for attribute, value in synergy.bonus.items()
        )

    # posem els prerequisits abans de les habilitats que els necessiten.
    ordered_skills: List[str] = []
    visited: Set[str] = set()

    def visit(skill_name: str):
        if skill_name in visited:
            return
        visited.add(skill_name)
        for required in skills[skill_name].requires:
            visit(required)
        ordered_skills.append(skill_name)

    for name in skills:
        visit(name)

    base_values = {name: skill_value(skill) for name, skill in skills.items()}
    positive_suffix = [0.0] * (len(ordered_skills) + 1)
    for i in range(len(ordered_skills) - 1, -1, -1):
        positive_suffix[i] = positive_suffix[i + 1] + max(0.0, base_values[ordered_skills[i]])

    positive_synergy_total = sum(max(0.0, synergy_value(s)) for s in instance.synergies)

    def score_selection(selected: Set[str]) -> float:
        score = 0.0
        for name in selected:
            score += base_values[name]
        for synergy in instance.synergies:
            if set(synergy.skills).issubset(selected):
                score += synergy_value(synergy)
        return score

    def cost_selection(selected: Set[str]) -> int:
        return sum(skills[name].cost for name in selected)

    def required_closure(skill_name: str) -> Set[str]:
        needed = set()

        def add(name: str):
            if name in needed:
                return
            needed.add(name)
            for required in skills[name].requires:
                add(required)

        add(skill_name)
        return needed

    def greedy_solution() -> Set[str]:
        selected: Set[str] = set()

        while True:
            best_group = None
            best_ratio = 0.0
            current_score = score_selection(selected)
            current_cost = cost_selection(selected)

            for name in ordered_skills:
                if name in selected:
                    continue

                group = required_closure(name) - selected
                group_cost = sum(skills[x].cost for x in group)
                if current_cost + group_cost > instance.budget:
                    continue

                new_selected = selected | group
                gain = score_selection(new_selected) - current_score
                if gain <= 0:
                    continue

                ratio = gain / max(1, group_cost)
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_group = group

            if best_group is None:
                break
            selected |= best_group

        changed = True
        while changed:
            changed = False
            current_score = score_selection(selected)
            current_cost = cost_selection(selected)
            for name in ordered_skills:
                if name in selected:
                    continue
                group = required_closure(name) - selected
                group_cost = sum(skills[x].cost for x in group)
                if current_cost + group_cost <= instance.budget:
                    new_selected = selected | group
                    if score_selection(new_selected) > current_score:
                        selected = new_selected
                        changed = True
                        break

        return selected

    if len(ordered_skills) > 25:
        return greedy_solution()

    best_score = 0.0
    best_selection: Set[str] = set()

    def total_score(selected: Set[str], base_score: float) -> float:
        score = base_score
        for synergy in instance.synergies:
            if set(synergy.skills).issubset(selected):
                score += synergy_value(synergy)
        return score

    def search(index: int, selected: Set[str], cost: int, base_score: float):
        nonlocal best_score, best_selection

        if index == len(ordered_skills):
            score = total_score(selected, base_score)
            if score > best_score:
                best_score = score
                best_selection = set(selected)
            return

        if base_score + positive_suffix[index] + positive_synergy_total < best_score:
            return

        name = ordered_skills[index]
        skill = skills[name]

        search(index + 1, selected, cost, base_score)

        if cost + skill.cost <= instance.budget and set(skill.requires).issubset(selected):
            selected.add(name)
            search(index + 1, selected, cost + skill.cost, base_score + base_values[name])
            selected.remove(name)

    search(0, set(), 0, 0.0)
    return best_selection


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
