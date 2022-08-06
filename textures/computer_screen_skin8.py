"""Solution of https://stalburg.net/Office_monitor_code."""

from infra.encodings.binary import binary_decode
from infra.output import section
from infra.utils import rotate_right

# codes start with the first complete code, the last one is usually wrapped
computer_screen_skin8 = (
    ("01110100 01100101 01111000 01100100 00101110", 2),
    ("00101110 01110010 01100101 01101110 01110100", 2),
    ("01101001 01100100 01100101 01100011 01100011", 2),
    ("01101111 00101110 01100001 01110100 01110010", 2),
    ("00101110 01101101 01100101 01101001 01101110", 2),
    ("01101000 01101001 01101110 01100100 01100010 01100101", 2),
    ("01100101 01111001 00101110 01101100", 1),
    ("01100001 01101100 00101110 01110110", 2),
    ("01110010 01101101 01100101", 2),
    ("01100001 01101101 01101000", 1),
    ("01110011 00101110 01101001 01110010 01100100", 3),
    ("01100010 01110010 01110101 01100101 00101110", 4),
    ("00101110 01110100 01110011 01100101", 2),
    ("01101100 00101110 01100110 01100001", 3),
    ("01100101 01110011 01100011 01101111 01100100", 3),
    ("01111001 00101110 01101110 01100001 01110010", 3),
    ("01110100 00101110 01100010 01101001", 0),
)

if __name__ == "__main__":
    result = "".join(
        rotate_right(
            [rotate_right(binary_decode(binary), rotation) for binary, rotation in computer_screen_skin8[::-1]],
            5,
        ),
    )
    with section("computer_screen_skin8 solution") as s:
        s.print(result)
