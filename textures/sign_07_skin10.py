"""The solution of sign_07_skin10.vtf."""

from infra.encodings.binary import binary_decode
from infra.output import section

sign_07_skin10 = (
    "01110000 01110101",
    "01101110 01100001",
    "01101001 01101110",
    "01100101 01101110",
    "00100000 01110100",
    "01110101 01110010",
    "01110011 01101011",
    "01100001",
)

if __name__ == "__main__":
    with section("sign_07_skin10 solution") as s:
        for entry in sign_07_skin10:
            s.print(binary_decode(entry))
