from typing import Tuple, Union

from other.bunker_computer import bunker_computer_code_2_solution

PlateValue = Union[str, int]
Plate = Tuple[PlateValue, PlateValue]
Column = Tuple[Plate, Plate, Plate, Plate, Plate]
control_panel_puzzle_ultimate_alternative: Tuple[Column, Column, Column, Column] = (
    (("B", "O"), ("U", "T"), ("H", "N"), ("E", "K"), ("R", "E")),
    (("W", "C"), ("O", "O"), ("M", "R"), ("L", "P"), ("U", "D")),
    ((1, "M"), (6, "I"), ("D", "R"), (14, "D"), ("L", "D")),
    (("I", "Q"), (12, "U"), (14, "E"), ("S", "I"), (9, "T")),
)

# this is only one of the solutions, the other one is found by using the values not used in this solution
control_panel_puzzle_ultimate_column_selection: Tuple[
    Tuple[int, int, int, int, int], ...
] = (
    (0, 0, 1, 1, 1),
    (1, 0, 0, 1, 0),
    (1, 1, 0, 1, 0),
    (1, 1, 1, 0, 1),
)


def decrypt_control_panel_puzzle_ultimate_column_selection(
    alternative: bool,
) -> Tuple[str, ...]:
    def decrypt_value(value: PlateValue) -> str:
        return (
            value
            if isinstance(value, str)
            else bunker_computer_code_2_solution[value - 1]
        )

    return tuple(
        "".join(
            decrypt_value(value)
            for value in (
                plate[value_selection]
                if not alternative
                else plate[1 - value_selection]
                for plate, value_selection in zip(column, column_selection)
            )
        )
        for column, column_selection in zip(
            control_panel_puzzle_ultimate_alternative,
            control_panel_puzzle_ultimate_column_selection,
        )
    )


control_panel_puzzle_ultimate_alternative_solution_1 = (
    decrypt_control_panel_puzzle_ultimate_column_selection(False)
)
control_panel_puzzle_ultimate_alternative_solution_2 = (
    decrypt_control_panel_puzzle_ultimate_column_selection(True)
)

if __name__ == "__main__":
    for column in control_panel_puzzle_ultimate_alternative_solution_1:
        print(column)
    print()
    for column in control_panel_puzzle_ultimate_alternative_solution_2:
        print(column)
