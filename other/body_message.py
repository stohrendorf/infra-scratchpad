"""The solution of https://stalburg.net/Body_message."""

from typing import Dict, Tuple

from infra.output import section
from textures.scientific_table_001_skin3 import solve_g1_g2_g3

body_code = {
    "A1": "WHAT",
    "A2": "HAPPENED",
    "A3": "TO",
    "A4": "AH",
    "B1": "I",
    "B2": "THE",
    "B3": "IN",
    "B4": "TO",
    "C1": "IS",
    "C3": "WILL",
    "E1": "IS",
    "F2": "TRUTH",
    "F4": "ANSWER",
    **solve_g1_g2_g3(),
}

body_message = (
    "B1",
    "C3",
    "F1",
    "B2",
    "F2",
    "C4",
    "E4",
    "G3",
    "B2",
    "G1",
    "F4",
    "B4",
    "B2",
    "G1",
    "G2",
)


def _decode_body_message(key: Dict[str, str], message: Tuple[str, ...]) -> str:
    return " ".join(key.get(code, f"[{code}]") for code in message)


if __name__ == "__main__":
    with section("body code") as s:
        s.print(_decode_body_message(body_code, body_message))
