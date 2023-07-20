import argparse

import negative_space_complexity
import descriptive_stats
import git_interactions


def as_stats(
    revision: str, complexity_by_line: list
) -> descriptive_stats.DescriptiveStats:
    """Provide data as stats data structure."""

    return descriptive_stats.DescriptiveStats(revision, complexity_by_line)


def as_csv(result: list) -> None:
    """Provide data as csv delimited."""

    print("rev,n,total,mean,sd")

    for stats in result:
        fields_of_interest = [
            stats.name,
            stats.n_revs,
            stats.total,
            round(stats.mean(), 2),
            round(stats.sd(), 2),
        ]

        printable = [str(field) for field in fields_of_interest]

        print(",".join(printable))


def calculate_complexity_over_range(file_name: str, revision_range: tuple) -> list:
    start_rev, end_rev = revision_range
    revs = git_interactions.read_revs_for(file_name, start_rev, end_rev)
    complexity_by_rev = []

    for rev in revs:
        historic_version = git_interactions.read_version_matching(file_name, rev)
        complexity_by_line = negative_space_complexity.calculate_complexity(
            historic_version
        )
        complexity_by_rev.append(as_stats(rev, complexity_by_line))

    return complexity_by_rev


def generate(args: list) -> None:
    """Generate complexity statistics."""

    revision_range = args.start, args.end
    complexity_trend = calculate_complexity_over_range(args.file, revision_range)

    as_csv(complexity_trend)


if __name__ == "__main__":
    desc = "Calculates whitespace complexity trends over a range of revisions."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--start", required=True, help="first commit hash to include")

    parser.add_argument("--end", required=True, help="last commit hash to include")

    parser.add_argument(
        "--file", required=True, type=str, help="file to calculate complexity on"
    )

    args = parser.parse_args()

    generate(args)
