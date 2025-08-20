from dataclasses import dataclass


@dataclass
class Homicidal:
    plugin_type = "themedadj"
    id = "homicidal"
    name = "Homicidal"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.15)
