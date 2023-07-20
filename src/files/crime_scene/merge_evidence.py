"""Merge two evidence data files."""

import _csv
import csv
import os
import sys
from typing import Callable


class MergeError(Exception):
    """Raise for any issues with the merge process."""


class Evidence:
    """Abstraction for a merged set of evidence data."""

    def __init__(self) -> None:
        self._all_modules_with_complexity: dict = {}
        self._merged_evidence: dict = {}

    def add_data(self, module: str, complexity_measure: str) -> None:
        """Add module with associated complexity measure to dictionary."""

        self._all_modules_with_complexity[module] = complexity_measure

    def augment_data(self, module: str, change_frequency: str) -> None:
        """Add change frequency to complexity measure for each module."""

        if module in self._all_modules_with_complexity:
            complexity_measure = self._all_modules_with_complexity[module]
            self._merged_evidence[module] = change_frequency, complexity_measure

    def sorted_list(self) -> list:
        """Returns evidence data sorted in descending order."""

        return sorted(
            self._merged_evidence.items(),
            key=lambda item: int(item[1][0]),
            reverse=True,
        )


def read_header_data(reader: "_csv._reader") -> list:
    """Get header from evidence data."""

    data: list = next(reader)

    while data == []:
        data = next(reader)

    return data


def validate_header_content(header: list, expected: str) -> None:
    """Validate header data matches the expected data signature."""

    expected_list = expected.split(",")
    stripped_list = header[0 : len(expected_list)]

    if stripped_list != expected_list:
        raise MergeError(
            "Merge problem with header. Expected = "
            + ",".join(expected_list)
            + ", got = "
            + ",".join(stripped_list),
        )


def write_data(evidence: list) -> None:
    """Generate evidence data."""

    print("module,revisions,code")

    for item in evidence:
        module, (frequency, complexity) = item
        print((module + "," + frequency + "," + complexity))


def parse_data(
    merged: Evidence,
    data_file: str,
    action: Callable,
    expected_format: str,
) -> None:
    """Run parsing algorithm on evidence data."""

    with open(data_file, "r", encoding="utf-8") as data:
        reader = csv.reader(data, delimiter=",")
        header = read_header_data(reader)

        validate_header_content(header, expected_format)

        for row in reader:
            action(merged, row)


def parse_complexity(evidence: Evidence, evidence_line: list) -> None:
    """Parse delimited data related to complexity measure."""

    module = os.path.normpath(evidence_line[1][2:])
    complexity_measure = evidence_line[4]

    evidence.add_data(module, complexity_measure)


def parse_change_frequency(evidence: Evidence, evidence_line: list) -> None:
    """Parse delimited data related to change frequency measure."""

    module = os.path.normpath(evidence_line[0])
    change_frequency = evidence_line[1]

    evidence.augment_data(module, change_frequency)


def merge(change_data_file: str, complexity_data_file: str) -> None:
    """Write combined evidence data into one evidence data set."""

    evidence = Evidence()

    parse_data(
        evidence,
        complexity_data_file,
        parse_complexity,
        expected_format="language,filename,blank,comment,code",
    )

    parse_data(
        evidence,
        change_data_file,
        parse_change_frequency,
        expected_format="entity,n-revs",
    )

    write_data(evidence.sorted_list())


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise MergeError(
            "Requires two data files: change frequency data and complexity data.",
        )

    change_data = sys.argv[1]
    complexity_data = sys.argv[2]

    merge(change_data, complexity_data)
