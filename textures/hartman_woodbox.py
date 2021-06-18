from typing import Union, Tuple

hartman_woodbox_001 = (1, "M", 22, 2, "Y")
hartman_woodbox_002 = (12, 2, "B", 1, 13, 17)

hartman_woodbox_key = {
    1: "E",
    2: "L",
    12: "A",
    13: "R",
    17: "T",
    22: "I",
}


def decrypt_hartman_woodbox(code: Tuple[Union[str, int], ...]) -> str:
    return "".join(
        value if isinstance(value, str) else hartman_woodbox_key[value]
        for value in code
    )


hartman_woodbox_001_solution = decrypt_hartman_woodbox(hartman_woodbox_001)
hartman_woodbox_002_solution = decrypt_hartman_woodbox(hartman_woodbox_002)

if __name__ == "__main__":
    print(hartman_woodbox_001_solution)
    print(hartman_woodbox_002_solution)
