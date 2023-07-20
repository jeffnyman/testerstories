"""Abstraction for statistics calculations."""


class DescriptiveStats:
    """Abstraction for statistics calculations."""

    def __init__(self, name: str, all_values: list) -> None:
        self.name = name
        self._all_values = all_values
        self.total = sum(all_values)
        self.n_revs = len(all_values)

    def mean(self) -> float:
        """Report mean value from list."""

        return self.total / float(self._protected_n())

    def max_value(self) -> int:
        """Report max value from list."""

        return max(self._all_values)

    def min_value(self) -> int:
        """Report min value from list."""

        return min(self._all_values)

    def sd(self) -> float:
        """Report standard deviation."""

        from math import sqrt

        std = 0
        mean = self.mean()

        for value in self._all_values:
            std = std + (value - mean) ** 2

        return sqrt(std / float(self._protected_n()))

    def _protected_n(self) -> int:
        revisions = self.n_revs

        return max(revisions, 1)
