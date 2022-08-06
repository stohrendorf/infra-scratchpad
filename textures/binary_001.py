"""Solution of the texture used only in infra_ee_binary."""

from infra.encodings.binary import binary_decode
from infra.output import section
from infra.utils import rotate_right

# these are the first 7 columns, as they repeat over the whole texture
binary_001 = (
    "01010010 00100000 01010011 01001001 01000100 01000101 01001111 01010100 01001000 01000101",
    "01010100 01001000 01000101 01010010 00100000 01010011 01001001 01000100 01000101 01001111",
    "01000101 01001111 01010100 01001000 01000101 01010010 00100000 01010011 01001001 01000100",
    "01010011 01001001 01000100 01000101 01001111 01010100 01001000 01000101 01010010 00100000",
    "01010010 00100000 01010011 01001001 01000100 01000101 01001111 01010100 01001000 01000101",
    "01001111 01010100 01001000 01000101 01010010 00100000 01010011 01001001 01000100 01000101",
    "01001000 01000101 01010010 00100000 01010011 01001001 01000100 01000101 01001111 01010100",
)

binary_001_input = "OTHER SIDE"

if __name__ == "__main__":
    all_decoded = tuple(map(binary_decode, binary_001))

    with section("raw decoded") as s:
        for column in all_decoded:
            s.print(column)

    with section("amount of right rotations from previous column") as s:
        s.print(all_decoded[0])
        for prev, current in zip(all_decoded, all_decoded[1:] + all_decoded[:1]):
            assert len(prev) == len(current)
            for i in range(len(prev) + 1):
                if rotate_right(prev, i) == current:
                    s.print(f"{current} {i}")
                    break
            else:
                raise RuntimeError
