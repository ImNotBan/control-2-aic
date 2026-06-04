#!/usr/bin/env python3

import json
import sys
from collections import defaultdict

# ============================================================
# LOAD INSTANCE
# ============================================================


def load_instance(path):

    with open(path, "r") as f:
        return json.load(f)


# ============================================================
# TREE CONSTRUCTION
# ============================================================


def build_tree(skills):

    children = defaultdict(list)

    roots = []

    for skill_name, data in skills.items():

        requires = data["requires"]

        if not requires:
            roots.append(skill_name)

        for parent in requires:
            children[parent].append(skill_name)

    return roots, children


# ============================================================
# FORMATTING HELPERS
# ============================================================


def format_attributes(attributes):

    parts = []

    for attr, value in attributes.items():

        if value >= 0:
            parts.append(f"+{value} {attr}")
        else:
            parts.append(f"{value} {attr}")

    return ", ".join(parts)


# ============================================================
# TREE PRINTING
# ============================================================


def print_tree(
    node,
    skills,
    children,
    prefix="",
    is_last=True,
):

    skill = skills[node]

    connector = "└── " if is_last else "├── "

    line = (
        prefix
        + connector
        + f"{node} "
        + f"[cost={skill['cost']}] "
        + f"({format_attributes(skill['attributes'])})"
    )

    print(line)

    new_prefix = prefix + ("    " if is_last else "│   ")

    node_children = sorted(children[node])

    for i, child in enumerate(node_children):

        child_is_last = i == len(node_children) - 1

        print_tree(
            child,
            skills,
            children,
            new_prefix,
            child_is_last,
        )


# ============================================================
# SYNERGIES
# ============================================================


def print_synergies(synergies):

    print("\n=== SYNERGIES ===\n")

    if not synergies:
        print("(none)")
        return

    for synergy in synergies:

        skills = " + ".join(synergy["skills"])

        bonus = format_attributes(synergy["bonus"])

        print(f"* {skills}  =>  {bonus}")


# ============================================================
# SCORING FUNCTION
# ============================================================


def print_scoring(scoring):

    print("=== SCORING FUNCTION ===\n")

    for attr, weight in scoring.items():

        print(f"{attr:20s} x {weight}")


# ============================================================
# SUMMARY
# ============================================================


def print_summary(instance):

    print("=== INSTANCE SUMMARY ===\n")

    print(f"Budget: {instance['budget']}")
    print(f"Skills: {len(instance['skills'])}")
    print(f"Synergies: {len(instance['synergies'])}")

    all_attributes = set()

    for skill in instance["skills"].values():
        all_attributes.update(skill["attributes"].keys())

    print(f"Attributes: {len(all_attributes)}")


# ============================================================
# MAIN
# ============================================================


def main():

    if len(sys.argv) != 2:

        print("Usage: python visualize.py instance.json")

        sys.exit(1)

    instance = load_instance(sys.argv[1])

    skills = instance["skills"]

    roots, children = build_tree(skills)

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print_summary(instance)

    print()

    # --------------------------------------------------------
    # SCORING
    # --------------------------------------------------------

    print_scoring(instance["scoring"])

    print()

    # --------------------------------------------------------
    # SKILL TREE
    # --------------------------------------------------------

    print("=== SKILL TREE ===\n")

    roots = sorted(roots)

    for i, root in enumerate(roots):

        root_is_last = i == len(roots) - 1

        print_tree(
            root,
            skills,
            children,
            prefix="",
            is_last=root_is_last,
        )

    # --------------------------------------------------------
    # SYNERGIES
    # --------------------------------------------------------

    print_synergies(instance["synergies"])


if __name__ == "__main__":
    main()
