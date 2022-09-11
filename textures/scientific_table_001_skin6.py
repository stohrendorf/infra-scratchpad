from infra.output import section

scientific_table_001_skin6 = {
    "GD1": ("K345", "T213", "U657", "R234", "H721", "A425", "T296", "Ä001"),
    "GD2": ("Y565", "T213", "U327", "R246", "K345", "T213"),
    "GD3": ("H721", "A425", "T296", "T213", "U657"),
    "GD4": ("T213", "U657"),
    "GD5": ("K345", "T213", "T213", "U657"),
    "GD6": ("H721", "A425", "T296", "Ä001", "T213", "U657"),
    "GD7": ("K345", "T213"),
    "GD8": ("T213", "U657"),
    "GD9": ("K345", "T213", "T213", "U657", "H721", "A425", "T296"),
    "GD12": ("T213", "U657"),
}


def _dump_counts():
    counts = {}
    for column in scientific_table_001_skin6.values():
        for cell in column:
            counts[cell] = counts.get(cell, 0) + 1

    with section("column lengths") as s:
        for column, values in scientific_table_001_skin6.items():
            s.print(f"{column} {len(values)}")

    with section("cell value counts") as s:
        counts = sorted(f"{value} {count}" for value, count in counts.items())
        for count in counts:
            s.print(count)


if __name__ == "__main__":
    _dump_counts()
