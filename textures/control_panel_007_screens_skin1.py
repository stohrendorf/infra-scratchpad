"""The solution for the code found in control_panel_007_screens_skin1.vtf."""

from infra.encodings.binary import binary_decode
from infra.output import section

control_panel_007_screens_skin1 = (
    "01101000 01100101 01101100 01110000 00100000 01101101",
    "01100101 00100001 00100000 01001001 00100111 01101101",
    "00100000 01110011 01110100 01110101 01100011 01101011",
    "00100000 01101001 01101110 00100000 01110100 01101000",
    "01100101 00100000 01110011 01101111 01110101 01110100",
    "01101000 00100000 01110100 01110101 01101110 01101110",
    "01100101 01101100 00100000 01000010 00110010 00101110",
)

if __name__ == "__main__":
    with section("control_panel_007_screens_skin1 solution") as s:
        for entry in control_panel_007_screens_skin1:
            s.print(binary_decode(entry))
