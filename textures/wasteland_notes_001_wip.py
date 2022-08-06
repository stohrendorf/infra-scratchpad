from typing import Dict

from infra.output import section
from textures.wasteland_notes_001 import (
    Notes,
    solve_wasteland_notes_001,
    wasteland_notes_001,
    wasteland_notes_001_key,
)


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

    with section("wasteland_notes_001 solution") as s:
        for row_index, row in enumerate(decoded):
            for column_index, note in enumerate(row):
                with section(f"column {column_index+1}, row {row_index+1}") as s2:
                    s2.print("\n".join(note))

    with section("wasteland_notes_001 unreferenced key chars") as s2:
        s2.print(_clean_unreferenced_key_chars(wasteland_notes_001_key, wasteland_notes_001).__str__())
