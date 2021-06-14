from typing import Dict

from body_message import body_code

bunker_computer_code_1 = (
    ("Underground", "Trees", "Lead", "Message"),
    ("Knowledge", "Research", "Body", "Question"),
    ("UGU", "Us", "Diving", "People"),
    ("Raven", "Tunnel", "Open", "Machine"),
    ("Inventor", "Homeless", "Omitted", "Mask"),
    ("Suit", "Institute", "Right", "Man"),
    ("God", "Show", "Truth", "Mines"),
    ("Organization", "AH", "Guard", "City"),
    ("Death", "Legend", "Meaning", "Sewer"),
    ("Green", "Blue", "Water", "World"),
)

bunker_computer_code_2 = (
    "C3.1",
    "F1.2",
    "F4.1",
    "B2.1",
    "A3.2",
    "E4.2",
    "F4.2",
    "G2.6",
    "G3.2",
    "A3.2",
    "G1.5",
    "F1.1",
    "F4.1",
    "G3.3",
    "G3.4",
    "B2.1",
    "G1.4",
    "B2.3",
    "G2.4",
    "H4.5",
)

bunker_computer_code_3 = (
    "1.3",
    "1.1",
    "4.10",
    "1.7",
    "4.7",
    "1.5",
    "2.8",
    "2.5",
    "4.3",
    "4.4",
    "4.5",
    "4.6",
    "2.4",
    "3.8",
    "1.2",
    "3.2",
    "4.1",
    "4.2",
    "2.7",
    "3.7",
    "1.4",
    "2.2",
    "2.6",
    "3.1",
    "1.8",
    "1.10",
    "1.9",
    "2.10",
    "3.6",
    "3.9",
    "3.10",
    "2.1",
    "3.3",
    "1.6",
    "2.9",
    "4.8",
    "2.4",
    "4.9",
    "2.3",
    "3.5",
)


def decrypt_bunker_computer_code_2() -> str:
    def decode_single(code: str) -> str:
        body_code_key, letter = code.split(".")
        try:
            return body_code[body_code_key][int(letter) - 1]
        except KeyError:
            return f"[{code}]"

    return "".join(decode_single(code) for code in bunker_computer_code_2)


def get_code_3_usage() -> Dict[str, int]:
    result = {f"{x + 1}.{y + 1}": 0 for x in range(4) for y in range(10)}
    for code in bunker_computer_code_3:
        result[code] += 1

    return result


def print_non_unique_code_usage_part_3():
    for code, usage_count in get_code_3_usage().items():
        if usage_count != 1:
            column, row = code.split(".")
            print(
                code, bunker_computer_code_1[int(row) - 1][int(column) - 1], usage_count
            )


if __name__ == "__main__":
    print(decrypt_bunker_computer_code_2())
    print_non_unique_code_usage_part_3()
