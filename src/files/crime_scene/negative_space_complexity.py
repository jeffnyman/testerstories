"""Complexity module related to negative space (indentations)."""

import re

leading_tabs_expr = re.compile(r"^(\t+)")
leading_spaces_expr = re.compile(r"^( +)")
empty_line_expr = re.compile(r"^\s*$")


def n_log_tabs(line: str) -> int:
    """Calculate the number of tabs logged."""

    pattern = re.compile(r" +")
    wo_spaces = re.sub(pattern, "", line)
    matching_data = leading_tabs_expr.search(wo_spaces)

    if matching_data:
        tabs = matching_data.group()
        return len(tabs)

    return 0


def n_log_spaces(line: str) -> int:
    """Calculate the number of spaces logged."""

    pattern = re.compile(r"\t+")
    wo_tabs = re.sub(pattern, "", line)
    matching_data = leading_spaces_expr.search(wo_tabs)

    if matching_data:
        spaces = matching_data.group()
        
        return len(spaces)

    return 0


def contains_code(line: str) -> re.Match:
    """Check for empty lines (pure whitespace)."""

    return not empty_line_expr.match(line)


def complexity_of(line: str) -> float:
    """Calculate complexity value for a given source line of code."""

    return n_log_tabs(line) + (n_log_spaces(line) / 4)


def calculate_complexity(source: str) -> list:
    """Perform calculation for all source lines that contain code."""

    return [complexity_of(line) for line in source.split("\n") if contains_code(line)]
