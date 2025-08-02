"""Example healing-over-time plugin."""


class Regeneration:
    """Heals targets gradually over time.

    Attributes
    ----------
    plugin_type: str
        Category consumed by the plugin loader.
    id: str
        Unique identifier used to select this plugin.
    name: str
        Display name shown to the user.
    """

    plugin_type = "hot"
    id = "regeneration"  # Unique identifier used by the game
    name = "Regeneration"  # Display name

    def tick(self, target, dt):
        """Heal ``target`` over ``dt`` seconds.

        Called each update while the effect is active.
        """
        # TODO: implement healing logic
        raise NotImplementedError
