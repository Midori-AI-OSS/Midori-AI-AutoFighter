"""Pity tracking for gacha pulls."""

from __future__ import annotations


class Pity:
    """Track gacha pulls without the featured character.

    The pity counter increases with each pull that does not yield the
    featured character. Odds for the next pull start at 0.001%, reach
    approximately 5% by the 159th pull, and are guaranteed at the 180th
    pull. The counter resets when a featured character is pulled.
    """

    base_rate = 0.00001
    soft_cap = 158
    hard_cap = 179

    def __init__(self) -> None:
        self.pulls_without_featured = 0

    def record_pull(self, featured: bool) -> None:
        """Record a pull result.

        Args:
            featured: ``True`` if the pull yielded the featured character.
        """
        if featured:
            self.pulls_without_featured = 0
        else:
            self.pulls_without_featured += 1

    def chance(self) -> float:
        """Return the probability of pulling the featured character next."""
        pulls = self.pulls_without_featured
        if pulls >= self.hard_cap:
            return 1.0
        if pulls <= self.soft_cap:
            return self.base_rate + (0.05 - self.base_rate) * (pulls / self.soft_cap)
        return 0.05 + (1 - 0.05) * ((pulls - self.soft_cap) / (self.hard_cap - self.soft_cap))
