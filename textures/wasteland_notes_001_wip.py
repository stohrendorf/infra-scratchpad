from typing import Tuple, Dict

from textures.wasteland_notes_001 import (
    MESSAGE_LINE_SEPARATOR,
    solve_wasteland_notes_001,
    wasteland_notes_001_key,
    wasteland_notes_001,
    Notes,
)

_magic_square = (
    (6, 32, 3, 34, 35, 1),
    (7, 11, 27, 28, 8, 30),
    (19, 14, 16, 15, 23, 24),
    (18, 20, 22, 21, 17, 13),
    (25, 29, 10, 9, 26, 12),
    (36, 5, 33, 4, 2, 31),
)


def _find_square_co(n: int) -> Tuple[int, int]:
    for x in range(6):
        for y in range(6):
            if _magic_square[y][x] == n:
                return x, y
    raise KeyError


def _count_code_usage(notes: Notes) -> Dict[str, int]:
    usage = dict()
    for row in notes:
        for note in row:
            for line in note:
                for word in line.split():
                    if "." in word:
                        usage[word] = usage.get(word, 0) + 1
    return usage


def _clean_unreferenced_key_chars(key: Dict[str, str], notes: Notes) -> Dict[str, str]:
    usage = _count_code_usage(notes)

    key = key.copy()
    for prefix, value in key.items():
        for i in range(len(value)):
            code = f"{prefix}.{i+1}"
            if usage.get(code, 0) <= 0:
                value = value[:i] + "_" + value[i + 1 :]
        key[prefix] = value
    return key


if __name__ == "__main__":
    decoded = solve_wasteland_notes_001()

    modifiers = (
        lambda x: x,
        lambda x: 5 - x,
    )

    modifiers_xy = (
        lambda x, y: (x, y),
        lambda x, y: (y, x),
    )

    for mod_x in modifiers:
        for mod_y in modifiers:
            for mod_xy in modifiers_xy:
                print("---------------------------------------------------")
                for i in range(36):
                    x, y = mod_xy(*_find_square_co(i + 1))
                    print(decoded[mod_x(x)][mod_y(y)].replace(MESSAGE_LINE_SEPARATOR, " "))

    print("unreferenced key chars", _clean_unreferenced_key_chars(wasteland_notes_001_key, wasteland_notes_001))
