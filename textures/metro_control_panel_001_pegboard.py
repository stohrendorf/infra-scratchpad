"""A collection of stuff related to https://stalburg.net/Body_message#Pegs."""

from typing import Tuple, Iterable, Callable
from infra.encodings.binary import binary_decode
from infra.string import insert_spaces

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


def _markers_to_bool_list(peg_str: str) -> Iterable[bool]:
    return map(lambda b: True if b == "M" else False, peg_str)


def _pegs_to_bool_list(peg_str: str) -> Iterable[bool]:
    return map(lambda b: False if b == "E" else True, peg_str)


def _invert_bool_list(bits: Iterable[bool]) -> Iterable[bool]:
    return map(lambda b: not b, bits)


def _bools_to_nor_mask(peg_str: str) -> Iterable[Callable]:
    def nor(a: bool, b: bool) -> bool:
        return not (a or b)

    def pass_thru(a: bool, b: bool) -> bool:
        return a

    return [nor if bit else pass_thru for bit in _markers_to_bool_list(peg_str)]


def _bools_to_binary_str(bits: Iterable[bool]) -> str:
    return insert_spaces("".join(str(int(b)) for b in bits), 8)
