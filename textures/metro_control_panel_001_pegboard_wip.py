"""A collection of stuff related to https://stalburg.net/Body_message#Pegs."""
from typing import Callable, Sequence

from termcolor import colored

from infra.utils import chunked
from textures.metro_control_panel_001_pegboard import (
    bools_to_int_be,
    bools_to_nor_mask,
    invert_bools,
    matching_elements,
    metro_control_panel_001_pegboard,
    PegGroup,
)

ColorFunc = Callable[[str], str]


def bools_to_ascii_str(bits: Sequence[bool], post_op: ColorFunc = lambda x: x) -> str:
    """
    Convert a sequence of bits (booleans) to one ascii character for each byte.
    Non printing characters are represented like "x1f".
    Each character or hex code will have a padded width of 3 characters, and
    a space will be inserted between consecutive characters.

    :param bits: Sequence of booleans as bits to be decoded.
    :return: String containing the decoded bits.
    :param post_op: Optional function to be applied to.

    >>> bools_to_ascii_str([False, True, True, False, False, True, False, True])
    'e  '
    >>> bools_to_ascii_str([False, False, False, False, True, False, True, False])
    'x0a'
    """

    ints = (bools_to_int_be(byte) for byte in chunked(bits, 8))

    return " ".join(f"{x:#04x}"[1:] if not chr(x).isalnum() else f"{post_op(chr(x))}  " for x in ints)


if __name__ == "__main__":

    # Following are some tests applying a nor mask to various combinations of pegs.

    peg_group_names = (("pegs[1,1]", "pegs[1,2]"), ("pegs[3,1]", "pegs[3,2]"), ("pegs[4,1]", "pegs[4,2]"))

    # Flatten the peg groupings for easier handling.
    # pegs[1,1]                 pegs[3,1]    pegs[4,1]
    # pegs[1,2]                 pegs[3,2]    pegs[4,2]

    peg_groups = [
        PegGroup(
            name=peg_group_names[i][j],
            pegs=invert_bools(matching_elements(peg_str, "E")),
            markers=matching_elements(peg_str, "M"),
        )
        for i, panels in enumerate(metro_control_panel_001_pegboard)
        for j, peg_str in enumerate(panels)
    ]

    zeros = [False] * 24

    def red_text(text: str):
        return colored(text, "red")

    # Some labeling to help identify interesting results.
    print()
    print(" " * 27 + (" " * 8).join(f"col {x: <2d}" for x in range(1, 9)))

    # Iterate through all combinations of the peg groupings.
    # Bits are represented by peg locations.
    # A nor mask is made from the marker locations from one of the peg groupings.
    for i, pegs1 in enumerate(peg_groups):
        mask_1 = bools_to_nor_mask(pegs1.markers)
        inverted_1 = invert_bools(pegs1.pegs)

        for j, pegs2 in enumerate(peg_groups):
            mask_2 = bools_to_nor_mask(pegs2.markers)
            inverted_2 = invert_bools(pegs2.pegs)

            print(f"{pegs1.name} x {pegs2.name}", end=" =  ")

            print(bools_to_ascii_str(mask_1(pegs1.pegs, pegs2.pegs), red_text), end="   ")  # col 1
            print(bools_to_ascii_str(mask_2(pegs1.pegs, pegs2.pegs), red_text), end="   ")  # col 2

            print(bools_to_ascii_str(mask_1(pegs1.pegs, inverted_2), red_text), end="   ")  # col 3
            print(bools_to_ascii_str(mask_2(pegs1.pegs, inverted_2), red_text), end="   ")  # col 4

            print(bools_to_ascii_str(mask_1(inverted_1, pegs2.pegs), red_text), end="   ")  # col 5
            print(bools_to_ascii_str(mask_2(inverted_1, pegs2.pegs), red_text), end="   ")  # col 6

            print(bools_to_ascii_str(mask_1(inverted_1, inverted_2), red_text), end="   ")  # col 7
            print(bools_to_ascii_str(mask_2(inverted_1, inverted_2), red_text), end="   ")  # col 8
            print()
        print()

    # Reverse each peg group
    for i, peg_group in enumerate(peg_groups):
        peg_groups[i] = PegGroup(
            name=peg_group.name, pegs=tuple(reversed(peg_group.pegs)), markers=tuple(reversed(peg_group.markers))
        )

    for i, pegs1 in enumerate(peg_groups):
        mask_1 = bools_to_nor_mask(pegs1.markers)
        inverted_1 = invert_bools(pegs1.pegs)

        for j, pegs2 in enumerate(peg_groups):
            mask_2 = bools_to_nor_mask(pegs2.markers)
            inverted_2 = invert_bools(pegs2.pegs)

            print(f"{pegs1.name} x {pegs2.name}", end=" =  ")

            print(bools_to_ascii_str(mask_1(pegs1.pegs, pegs2.pegs), red_text), end="   ")  # col 1
            print(bools_to_ascii_str(mask_2(pegs1.pegs, pegs2.pegs), red_text), end="   ")  # col 2

            print(bools_to_ascii_str(mask_1(pegs1.pegs, inverted_2), red_text), end="   ")  # col 3
            print(bools_to_ascii_str(mask_2(pegs1.pegs, inverted_2), red_text), end="   ")  # col 4

            print(bools_to_ascii_str(mask_1(inverted_1, pegs2.pegs), red_text), end="   ")  # col 5
            print(bools_to_ascii_str(mask_2(inverted_1, pegs2.pegs), red_text), end="   ")  # col 6

            print(bools_to_ascii_str(mask_1(inverted_1, inverted_2), red_text), end="   ")  # col 7
            print(bools_to_ascii_str(mask_2(inverted_1, inverted_2), red_text), end="   ")  # col 8
            print()
        print()
