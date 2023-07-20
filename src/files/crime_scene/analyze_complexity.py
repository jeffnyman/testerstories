"""Generic complexity analyzer."""

import argparse

import descriptive_stats
import negative_space_complexity


def as_stats(
    revision: str,
    complexity_by_line: list,
) -> descriptive_stats.DescriptiveStats:
    """Provide data as stats data structure."""

    return descriptive_stats.DescriptiveStats(revision, complexity_by_line)


def as_csv(stats: descriptive_stats.DescriptiveStats) -> None:
    """Provide data as csv delimited."""

    print("n,total,mean,sd,max")

    fields_of_interest = [
        stats.n_revs,
        stats.total,
        round(stats.mean(), 2),
        round(stats.sd(), 2),
        stats.max_value(),
    ]

    printable = [str(field) for field in fields_of_interest]

    print(",".join(printable))


def generate(args: list) -> None:
    """Generate complexity statistics."""

    with open(args.file, "r") as file_to_calc:
        complexity_by_line = negative_space_complexity.calculate_complexity(
            file_to_calc.read(),
        )

        stats = descriptive_stats.DescriptiveStats(args.file, complexity_by_line)

        as_csv(stats)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculates whitespace complexity of the given file.",
    )

    parser.add_argument("file", type=str, help="file to calculate complexity on")

    args = parser.parse_args()

    generate(args)
