import subprocess
import sys
import re


def _as_rev_range(start, end):
    return start + ".." + end


def _run_git_cmd(git_arguments: list) -> str:
    encoding = "UTF-8"

    if sys.stdout.encoding is not None:
        encoding = sys.stdout.encoding

    stdout_bytes = subprocess.Popen(
        git_arguments, stdout=subprocess.PIPE
    ).communicate()[0]

    stdout = stdout_bytes.decode(encoding)

    return stdout


def _read_revisions_matching(git_arguments: list) -> list:
    git_log = _run_git_cmd(git_arguments)
    revs = []
    rev_expr = re.compile(r"([^\s]+)")

    for line in git_log.split("\n"):
        m = rev_expr.search(line)

        if m:
            revs.append(m.group(1))

    return revs[::-1]


def _git_cmd_for(rev_start: str, rev_end: str) -> list:
    rev_range = rev_start + ".." + rev_end

    return ["git", "log", rev_range, "--oneline"]


def read_revs(rev_start: str, rev_end: str) -> list:
    """Returns a list of all commits in the given range."""

    return _read_revisions_matching(git_arguments=_git_cmd_for(rev_start, rev_end))


def read_revs_for(file_name: str, rev_start: str, rev_end: str) -> list:
    return _read_revisions_matching(
        git_arguments=_git_cmd_for(rev_start, rev_end) + [file_name]
    )


def read_diff_for(rev1: str, rev2: str) -> list:
    """Return the difference between two different revisions."""

    return _run_git_cmd(["git", "diff", rev1, rev2])


def read_file_diff_for(file_name: str, rev1: str, rev2: str) -> list:
    return _run_git_cmd(["git", "diff", rev1, rev2, file_name])


def read_version_matching(file_name: str, rev: str) -> list:
    return _run_git_cmd(["git", "show", rev + ":" + file_name])
