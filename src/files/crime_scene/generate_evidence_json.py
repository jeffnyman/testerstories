"""Generate D3.js compatible JSON data for enclosure diagram visualization."""

import _csv
import argparse
import csv
import json

from typing import Callable


class MergeError(Exception):
    """Raise for any issues with the merge process."""


class StructuralElement:
    """Abstraction for a given element of structural evidence."""

    def __init__(self, module: str, complexity: str) -> None:
        self.module = module
        self.complexity = complexity

    def parts(self) -> list:
        """Provide list of all evidence parts."""

        return self.module.split("/")


def read_header_data(reader: "_csv._reader") -> list:
    """Get header from evidence data."""

    data: list = next(reader)

    while data == []:
        data = next(reader)

    return data


def validate_header_content(header: list, expected: str) -> None:
    """Validate header data matches the expected data signature."""

    if not expected:
        return

    expected_list = expected.split(",")
    stripped_list = header[0 : len(expected_list)]

    if stripped_list != expected_list:
        raise MergeError(
            "Merge problem with header. Expected = "
            + ",".join(expected_list)
            + ", got = "
            + ",".join(stripped_list),
        )


def parse_structural_element(evidence_row: list) -> StructuralElement:
    """Create item of structural evidence."""

    module = evidence_row[1][2:]
    complexity = evidence_row[4]

    return StructuralElement(module, complexity)


def parse_data(data_file: str, action: Callable, expected_format: str = None) -> list:
    """Provide evidence from data files."""

    with open(data_file, "r", encoding="utf-8") as data:
        reader = csv.reader(data, delimiter=",")
        header = read_header_data(reader)

        validate_header_content(header, expected_format)

        return [action(row) for row in reader]


def generate_evidence_weight_parser(weight_column: str) -> Callable:
    """Create list of data based on weighted evidence value."""

    def parse_evidence_weight(evidence_row: list) -> tuple:
        module = evidence_row[0]
        weight = float(evidence_row[weight_column])

        return module, weight

    return parse_evidence_weight


def module_weight_calculator(analysis_results: list) -> Callable:
    """Create a module weight calculator."""

    max_raw_weight = max(analysis_results, key=lambda e: e[1])
    max_value = max_raw_weight[1]

    normalized_weights = {
        module: ((1.0 / max_value) * value) for module, value in analysis_results
    }

    def normalized_weight(module_name: str) -> float:
        if module_name in normalized_weights:
            return normalized_weights[module_name]

        return 0.0

    return normalized_weight


def matching_part(hierarchy: list, part: str) -> dict:
    """Check if there is a match for a part in the hierarchy."""

    return next((x for x in hierarchy if x["name"] == part), None)


def ensure_branch_exists(hierarchy: list, branch: str) -> str:
    """Determine if branch exists before adding to it."""

    existing = matching_part(hierarchy, branch)

    if not existing:
        new_branch = {"name": branch, "children": []}
        hierarchy.append(new_branch)
        existing = new_branch

    return existing


def add_leaf(
    hierarchy: list,
    module: StructuralElement,
    weight_calculator: Callable,
    name: str,
) -> list:
    """Generate a end of node leaf for the hierarchy."""

    new_leaf = {
        "name": name,
        "children": [],
        "size": module.complexity,
        "weight": weight_calculator(module.module),
    }

    hierarchy.append(new_leaf)

    return hierarchy


def insert_parts(
    hierarchy: list,
    module: StructuralElement,
    weight_calculator: Callable,
    parts: list,
) -> tuple:
    """
    Insert parts into the hiearcy.

    The way this function works is it recursively traverses the hierarchy and
    inserts the individual parts of the module, one by one. The parts specify
    branches. If any branch is missing, it's created during the traversal. The
    final part specifies a module name (without its path). This is where the
    size and weight are added to the leaf.
    """

    if len(parts) == 1:
        return add_leaf(hierarchy, module, weight_calculator, name=parts[0])

    next_branch = parts[0]

    existing_branch = ensure_branch_exists(hierarchy, next_branch)

    return insert_parts(
        existing_branch["children"],
        module,
        weight_calculator,
        parts=parts[1:],
    )


def generate_structure(modules: list, weight_calculator: Callable) -> dict:
    """Generate the nested data structure representing a tree."""

    hierarchy = []

    for module in modules:
        parts = module.parts()
        insert_parts(hierarchy, module, weight_calculator, parts)

    return {"name": "root", "children": hierarchy}


def write_json(result: dict) -> None:
    """Generate final JSON evidence data."""

    print(json.dumps(result))


def generate(args: list) -> None:
    """Process all evidence data."""

    raw_weights = parse_data(
        args.weights,
        action=generate_evidence_weight_parser(args.weightcolumn),
    )

    weight_calculator = module_weight_calculator(raw_weights)

    structure_input = parse_data(
        args.structure,
        expected_format="language,filename,blank,comment,code",
        action=parse_structural_element,
    )

    weighted_system_structure = generate_structure(structure_input, weight_calculator)

    write_json(weighted_system_structure)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates a JSON document suitable for enclosure diagrams.",
    )

    parser.add_argument("--structure", required=True, help="csv file generated by cloc")

    parser.add_argument(
        "--weights",
        required=True,
        help="csv file with hotspot results from Code Maat",
    )

    parser.add_argument(
        "--weightcolumn",
        type=int,
        default=1,
        help="index specifying the columnt to use in the weight table",
    )

    args = parser.parse_args()

    generate(args)
