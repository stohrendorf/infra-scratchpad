"""A collection of stuff related to https://stalburg.net/Body_message#Pegs."""
from typing import Sequence

from infra.utils import chunks
from textures.metro_control_panel_001_pegboard import (
    bools_to_int,
    bools_to_nor_mask,
    invert_bools,
    markers_to_bools,
    metro_control_panel_001_pegboard,
    PegGroup,
    pegs_to_bools,
)

non_print_vals = {*range(33), *range(127, 160), 160, 173}


def is_alpha_num(char: str) -> bool:
    return any(("0" <= char <= "9", "A" <= char <= "Z", "a" <= char <= "z"))


alpha_num_ = {*range(48, 58), *range(65, 90), *range(97, 123)}

if __name__ == "__main__":

    # Test applying nor mask to various combinations of pegs

    def color_red(chars: str) -> str:
        """Colorize alphanumeric characters"""
        return "".join(f"\x1b[11;31m{char}\x1b[0m" if is_alpha_num(char) else char for char in chars)

    def bools_to_ascii_str(bits: Sequence[bool]) -> str:
        # assert len(bits) % 8 == 0

        ints = (bools_to_int(byte) for byte in chunks(bits, 8))

        return " ".join(f"{x:#04x}"[1:] if x in non_print_vals else f"  {color_red(chr(x))}" for x in ints)

    # Flatten the peg groupings for easier handling
    # pegs[1,1]                 pegs[3,1]    pegs[4,1]
    # pegs[1,2]                 pegs[3,2]    pegs[4,2]
    peg_groups = []
    for i, panels in enumerate(metro_control_panel_001_pegboard):
        for j, peg_str in enumerate(panels):
            peg_group = PegGroup(
                # Correcting for the blank panel
                name=f"pegs[{i + (1 if not i else 2)},{j + 1}]",
                pegs=pegs_to_bools(peg_str),
                markers=markers_to_bools(peg_str),
            )
            peg_groups.append(peg_group)

    zeros = [False] * 24

    # Some labeling to help identify interesting results
    print()
    print(" " * 27 + (" " * 8).join(f"col {x: <2d}" for x in range(1, 9)))

    # Iterate through all combinations of the peg groupings
    # Bits are represented by peg locations
    # A nor mask is made from the marker locations from one of the peg groupings
    for i, pegs1 in enumerate(peg_groups):
        mask_1 = bools_to_nor_mask(pegs1.markers)
        inverses_1 = invert_bools(pegs1.pegs)

        for j, pegs2 in enumerate(peg_groups):

            mask_2 = bools_to_nor_mask(pegs2.markers)
            inverses_2 = invert_bools(pegs2.pegs)

            print(f"{pegs1.name} x {pegs2.name}", end=" =  ")

            print(bools_to_ascii_str(mask_1(pegs1.pegs, pegs2.pegs)), end="   ")  # col 1
            print(bools_to_ascii_str(mask_2(pegs1.pegs, pegs2.pegs)), end="   ")  # col 2

            print(bools_to_ascii_str(mask_1(pegs1.pegs, inverses_2)), end="   ")  # col 3
            print(bools_to_ascii_str(mask_2(pegs1.pegs, inverses_2)), end="   ")  # col 4

            print(bools_to_ascii_str(mask_1(inverses_1, pegs2.pegs)), end="   ")  # col 5
            print(bools_to_ascii_str(mask_2(inverses_1, pegs2.pegs)), end="   ")  # col 6

            print(bools_to_ascii_str(mask_1(inverses_1, inverses_2)), end="   ")  # col 7
            print(bools_to_ascii_str(mask_2(inverses_1, inverses_2)), end="   ")  # col 8
            print()
        print()
