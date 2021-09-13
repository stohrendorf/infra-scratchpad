"""A collection of stuff related to https://stalburg.net/Body_message#Pegs."""

from typing import Tuple

Pegs = Tuple[Tuple[str, str], ...]

metro_control_panel_001_pegboard: Pegs = (
    # panel 1
    ("MPMEEMPMPMEEEMPMPMPEEEMP", "PMPMPPEPEEEEEEEEMPMPMPMP"),
    # panel 2
    ("MPMPMPEEEEMPMPEEEEMPMPMP", "PMPMPMPMEEEMEMPEPMPMPMPM"),
    # panel 4
    ("MPMPMPMPEEEEEEEEEEEEEEEE", "PMPMPMEEEEEEEEEEEEEEEEEE"),
)


def _print_pegs(pegs: Pegs):
    for i in range(2):
        print(" ".join(panel[i] for panel in pegs))


def _remove_empty(pegs: Pegs) -> Pegs:
    # noinspection PyTypeChecker
    return tuple(tuple(s.replace("E", "") for s in panel) for panel in pegs)


def _swap_pegs(pegs: Pegs, a: str, b: str) -> Pegs:
    assert len(a) == 1 and len(b) == 1

    placeholder = "_"
    # noinspection PyTypeChecker
    return tuple(
        tuple(s.replace(a, placeholder).replace(b, a).replace(placeholder, b) for s in panel) for panel in pegs
    )
