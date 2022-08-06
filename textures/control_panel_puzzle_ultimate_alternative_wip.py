from typing import Any, List, Set

_DIM_X = 4
_DIM_Y = 5
_RIGHT = ">"
_LEFT = "<"
_UP = "^"
_DOWN = "v"


def make_lights() -> List[List[Any]]:
    return [[None] * _DIM_Y for _ in range(_DIM_X)]


def try_go_down(x: int, y: int, lights: List[List[Any]]):
    if y >= _DIM_Y - 1:
        return None, None

    y += 1
    if lights[x][y] is not None:
        return None, None
    return x, y


def try_go_up(x: int, y: int, lights: List[List[Any]]):
    if y <= 0:
        return None, None

    y -= 1
    if lights[x][y] is not None:
        return None, None
    return x, y


def try_go_right(x: int, y: int, lights: List[List[Any]]):
    if x >= _DIM_X - 1:
        return None, None

    x += 1
    if lights[x][y] is not None:
        return None, None
    return x, y


def try_go_left(x: int, y: int, lights: List[List[Any]]):
    if x <= 0:
        return None, None

    x -= 1
    if lights[x][y] is not None:
        return None, None
    return x, y


def dump_path(path: str, x: int, y: int):
    lights = make_lights()
    prev_d = None
    for next_d in reversed(path):
        if next_d == _RIGHT:
            lights[x][y] = {
                None: "* ",
                _RIGHT: "──",
                _UP: "┌─",
                _DOWN: "└─",
            }[prev_d]
            x += 1
        elif next_d == _LEFT:
            lights[x][y] = {
                None: "* ",
                _LEFT: "──",
                _UP: "┐ ",
                _DOWN: "┘ ",
            }[prev_d]
            x -= 1
        elif next_d == _UP:
            lights[x][y] = {
                None: "* ",
                _UP: "│ ",
                _LEFT: "└─",
                _RIGHT: "┘ ",
            }[prev_d]
            y -= 1
        elif next_d == _DOWN:
            lights[x][y] = {
                None: "* ",
                _DOWN: "│ ",
                _LEFT: "┌─",
                _RIGHT: "┐ ",
            }[prev_d]
            y += 1
        prev_d = next_d

    lights[x][y] = "* "
    return "\n".join("".join(lights[xxx][yyy] for xxx in range(_DIM_X)) for yyy in range(_DIM_Y))


def find_paths_rec(x: int, y: int, lights: List[List[Any]], path: str, solutions: Set[str]):
    if len(path) == _DIM_X * _DIM_Y - 1:
        solutions.add(dump_path(path, x, y))
        return

    def try_dir(fn, dir):
        xx, yy = fn(x, y, lights)
        if xx is not None:
            lights[x][y] = dir
            find_paths_rec(xx, yy, lights, path + dir, solutions)
            lights[x][y] = None

    try_dir(try_go_down, _UP)
    try_dir(try_go_up, _DOWN)
    try_dir(try_go_right, _LEFT)
    try_dir(try_go_left, _RIGHT)


def find_paths():
    solutions = set()
    for x0 in range(_DIM_X):
        for y0 in range(_DIM_Y):
            lights = make_lights()
            find_paths_rec(x0, y0, lights, "", solutions)

    print(len(solutions), "solutions of ", _DIM_X * _DIM_Y * (_DIM_X * _DIM_Y - 1), " total start/end points")
    for solution in solutions:
        print(solution)
        print()


if __name__ == "__main__":
    find_paths()
