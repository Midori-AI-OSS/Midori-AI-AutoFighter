from dataclasses import dataclass


@dataclass
class Malicious:
    plugin_type = "themedadj"
    id = "malicious"
    name = "Malicious"

    def apply(self, target) -> None:
        target.atk = int(target.atk * 1.07)
