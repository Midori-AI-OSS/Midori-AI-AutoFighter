"""Template for creating a healing-over-time (HoT) plugin.

Add logic to steadily restore health to targets.
"""


class HotPlugin:
    """Example HoT plugin skeleton."""

    plugin_type = "hot"
    id = "example_hot"
    name = "Example Healing Over Time"

    def tick(self, target, dt: float) -> None:
        """Heal ``target`` over ``dt`` seconds.

        This sample logic restores a small amount of HP each tick. Replace the
        calculation with whatever makes sense for your custom HoT.
        """
        heal = int(5 * dt)
        target.HP = min(target.MHP, target.HP + heal)
