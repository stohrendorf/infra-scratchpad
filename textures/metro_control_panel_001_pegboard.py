"""A collection of stuff related to https://stalburg.net/Body_message#Pegs."""
from functools import reduce
from typing import Callable, Iterable, NamedTuple, Sequence, Tuple, TypeVar, Collection

T = TypeVar("T")

NorMask = Callable[[Sequence[bool], Sequence[bool]], Tuple[bool]]
Pegs = Tuple[Tuple[str, str], ...]
PegGroup = NamedTuple("PegGroup", [("name", str), ("pegs", Sequence[bool]), ("markers", Sequence[bool])])

# █◉█oo█◉█◉█ooo█◉█◉█◉ooo█◉ | █◉█◉█◉oooo█◉█◉oooo█◉█◉█◉ | █◉█◉█◉█◉oooooooooooooooo
# ◉█◉█◉◉o◉oooooooo█◉█◉█◉█◉ | ◉█◉█◉█◉█ooo█o█◉o◉█◉█◉█◉█ | ◉█◉█◉█oooooooooooooooooo

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
    """Trade places of two symbols"""
    assert len(a) == 1 and len(b) == 1

    placeholder = "_"
    # noinspection PyTypeChecker
    return tuple(
        tuple(s.replace(a, placeholder).replace(b, a).replace(placeholder, b) for s in panel) for panel in pegs
    )


def markers_to_bools(peg_str: str) -> Tuple[bool]:
    """
    The positions of the markers represented as booleans

    :param peg_str: String of peg symbols
    :return: List of booleans, true where each marker (M) was

    >>> markers_to_bools("PME")
    [False, True, False]
    """
    return tuple(peg == "M" for peg in peg_str)


def pegs_to_bools(peg_str: str) -> Tuple[bool]:
    """
    The positions of the markers represented as booleans

    :param peg_str: String of peg symbols
    :return: List of booleans, true where each peg (P) was

    >>> markers_to_bools("PME")
    [True, False, False]
    """
    return tuple(peg == "E" for peg in peg_str)


def invert_bools(bits: Iterable[bool]) -> Tuple[bool]:
    return tuple(not bit for bit in bits)


def bools_to_nor_mask(masking_bools: Collection[bool]) -> NorMask:
    """
    Creates an elementwise function that can called with two lists of booleans
    of the same shape.
    How the returned nor mask function is meant to be used:
    (A, B, and C are lists; * is the nor mask function)
    A * B = C
    For C[n] the value A[n] is given where masking_bools[n] is False
    and A[n] NOR B[n] is given where masking_bools[n] is True

    :param masking_bools: Bools that determine if the function should NOR or not
    :return: Elementwise operator

    >>> a = [False, True, False, True]
    >>> b = [False, False, True, True]
    >>> nor_mask_false = bools_to_nor_mask([False, False, False, False])
    >>> nor_mask_false(a, b)
    [False, True, False, True]
    >>> nor_mask_true = bools_to_nor_mask([True, True, True, True])
    >>> nor_mask_true(a, b)
    [True, False, False, False]
    """

    def nor(a: bool, b: bool) -> bool:
        return not (a or b)

    # noinspection PyUnusedLocal
    def left(a: bool, b: bool) -> bool:
        return a

    def nor_mask_function(left_: Collection[bool], right_: Collection[bool]) -> Tuple[bool]:
        assert len(left_) == len(right_) == len(masking_bools)

        operators = [nor if bit else left for bit in masking_bools]
        return tuple(operator(l, r) for operator, l, r in zip(operators, left_, right_))

    return nor_mask_function


def bools_to_int(bits: Collection) -> int:
    """
    Integer from a sequence of boolean values.
    Assumes the sequence is stored big endian style

    :param bits: The sequence of booleans
    :return: The integer

    >>> bools_to_int([False, True, False, True])
    5

    """
    return reduce(lambda prev, current: prev << 1 | current, bits)
