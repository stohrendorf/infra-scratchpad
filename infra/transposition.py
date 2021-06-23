"""Transposition cipher function."""
from enum import Enum, auto
from typing import Callable, List, Sequence, Tuple, TypeVar, Union

from infra.nla import dict_std_en
from infra.stats import Stats, calc_stats
from infra.string import all_string_indices, split_every
from infra.utils import reverse_sequence


def get_encoding_mapping(key: str) -> Tuple[int]:
    """
    Compute the encoding mapping for columnar transposition ciphers.

    :param key: The encoding key.
    :return: The column indices resulting from the encoding key.

    >>> get_encoding_mapping("ALBERT")
    (0, 2, 3, 1, 4, 5)
    """
    key_chars = sorted(set(key))
    return tuple(src_idx for key_char in key_chars for src_idx in all_string_indices(key, key_char))


T = TypeVar("T")
IndexableT = Union[List[T], Union[T], str]


def columnar_encode_shuffle(data: IndexableT, key: str) -> IndexableT:
    """
    Shuffle data with a columnar transposition cipher.

    :param data: The data to be shuffled.
    :param key: The encoding key.
    :return: The shuffled data.

    >>> "".join(columnar_encode_shuffle("HELLOWORLD", "ALBERTHART"))
    'HRLLOEOLWD'
    """
    assert len(data) == len(key)
    return [data[src_idx] for src_idx in get_encoding_mapping(key)]


def columnar_encode(plaintext: str, key: str, null_char: str = "") -> str:
    """
    Apply a columnar transposition cipher.

    :param plaintext: The text to be encoded.
    :param key: The encoding key.
    :param null_char: The null char for irregular texts.
    :return: The encoded string.

    >>> columnar_encode("this is a test", "somekey")
    'stis ei hat st'
    """
    assert len(null_char) in (0, 1)

    def prepare_row(row: str) -> str:
        adjusted_row = row if not null_char else row.ljust(len(key), null_char)
        return columnar_encode_shuffle(adjusted_row, key[: len(adjusted_row)])

    rows = [prepare_row(row) for row in split_every(plaintext, len(key))]
    return "".join(row[i] for i in range(len(key)) for row in rows if i < len(row))


def columnar_decode_shuffle(data: IndexableT, key: str) -> IndexableT:
    """
    Shuffle data with a columnar transposition cipher.

    :param data: The encoded data to be shuffled.
    :param key: The encoding key.
    :return: The shuffled data.

    >>> "".join(columnar_decode_shuffle("HRLLOEOLWD", "ALBERTHART"))
    'HELLOWORLD'
    """
    assert len(data) == len(key)
    decoding_mapping = tuple(
        dst for dst, _ in sorted(enumerate(get_encoding_mapping(key)), key=lambda dst_src: dst_src[1])
    )
    return [data[src_idx] for src_idx in decoding_mapping]


def columnar_decode(encoded: str, key: str) -> str:
    """
    Apply a columnar transposition cipher for deciphering.

    :param encoded: The text to be decoded.
    :param key: The encoding key.
    :return: The decoded string.

    >>> columnar_decode("stis ei hat st", "somekey")
    'this is a test'
    """
    split_data = split_every(encoded, (len(encoded) + len(key) - 1) // len(key))
    columns = columnar_decode_shuffle(split_data, key[: min(len(key), len(split_data))])
    rows = max(len(column) for column in columns)
    return "".join(column[i] for i in range(rows) for column in columns if i < len(column))


def transpose(strings: Sequence[str]) -> Tuple[str, ...]:
    """
    Transpose a list of strings.

    :param strings: The strings to transpose.
    :return: The transposed strings.

    >>> transpose(("HELLO", "WORLD"))
    ('HW', 'EO', 'LR', 'LL', 'OD')
    """
    if not strings:
        return ()

    first_length = len(strings[0])
    assert all(first_length == len(s) for s in strings)

    return tuple("".join(column[x] for column in strings) for x in range(first_length))


class GridPath(Enum):
    """The possible paths when walking a grid."""

    HORIZONTALS_STRAIGHT_TL = auto()
    HORIZONTALS_STRAIGHT_BL = auto()
    HORIZONTALS_REVERSE_TR = auto()
    HORIZONTALS_REVERSE_BR = auto()
    HORIZONTALS_ALTERNATE_TL = auto()
    HORIZONTALS_ALTERNATE_TR = auto()
    HORIZONTALS_ALTERNATE_BR = auto()
    HORIZONTALS_ALTERNATE_BL = auto()

    VERTICALS_DESCENDING_TL = auto()
    VERTICALS_DESCENDING_TR = auto()
    VERTICALS_ASCENDING_BL = auto()
    VERTICALS_ASCENDING_BR = auto()
    VERTICALS_ALTERNATE_TL = auto()
    VERTICALS_ALTERNATE_TR = auto()
    VERTICALS_ALTERNATE_BR = auto()
    VERTICALS_ALTERNATE_BL = auto()

    SPIRAL_CLOCKWISE_IN_TL = auto()
    SPIRAL_CLOCKWISE_IN_TR = auto()
    SPIRAL_CLOCKWISE_IN_BR = auto()
    SPIRAL_CLOCKWISE_IN_BL = auto()

    SPIRAL_ANTICLOCKWISE_IN_TL = auto()
    SPIRAL_ANTICLOCKWISE_IN_TR = auto()
    SPIRAL_ANTICLOCKWISE_IN_BR = auto()
    SPIRAL_ANTICLOCKWISE_IN_BL = auto()

    SPIRAL_CLOCKWISE_OUT_TL = auto()
    SPIRAL_CLOCKWISE_OUT_TR = auto()
    SPIRAL_CLOCKWISE_OUT_BR = auto()
    SPIRAL_CLOCKWISE_OUT_BL = auto()

    SPIRAL_ANTICLOCKWISE_OUT_TL = auto()
    SPIRAL_ANTICLOCKWISE_OUT_TR = auto()
    SPIRAL_ANTICLOCKWISE_OUT_BR = auto()
    SPIRAL_ANTICLOCKWISE_OUT_BL = auto()


def create_grid(rows: int, cols: int, default: T) -> List[List[T]]:
    """
    Create a new rectangular grid of given dimensions.

    :param rows: Number of rows.
    :param cols: Number of columns.
    :param default: Default value to fill the grid with.
    :return: The grid of dimensions [rows][cols].

    >>> create_grid(3, 2, 0)
    [[0, 0], [0, 0], [0, 0]]
    """
    return [[default] * cols for _ in range(rows)]


def walk_path(
    path: GridPath,
    rows: int,
    cols: int,
    action: Callable[[int, int], None],
    action_reverse: Callable[[int, int], None],
):
    """
    Execute actions while walking over a grid.

    :param path: The path to follow.
    :param rows: Rows in the grid.
    :param cols: Columns in the grid.
    :param action: What to do when visiting a cell; "inwards" if on a spiral path.
    :param action_reverse: What to do when visiting a cell; "outwards" if on a spiral path,
           and only relevant for spiral paths.
    """
    dir_up = 0
    dir_right = 1
    dir_down = 2
    dir_left = 3

    def rotate_cw(d: int) -> int:
        return (d + 1) % 4

    def rotate_ccw(d: int) -> int:
        return (d + 3) % 4

    def dir_to_dy(d: int) -> int:
        if d == dir_up:
            return -1
        elif d == dir_down:
            return 1
        else:
            return 0

    def dir_to_dx(d: int) -> int:
        if d == dir_left:
            return -1
        elif d == dir_right:
            return 1
        else:
            return 0

    marker_grid = create_grid(rows, cols, False)

    def walk_spiral(
        y: int,
        x: int,
        direction: int,
        rotate: Callable[[int], int],
        action: Callable[[int, int], None],
    ):
        for _ in range(1, rows * cols):
            assert not marker_grid[y][x]
            action(y, x)
            marker_grid[y][x] = True

            nx = x + dir_to_dx(direction)
            ny = y + dir_to_dy(direction)
            if not (0 <= ny < rows) or not (0 <= nx < cols) or marker_grid[ny][nx]:
                direction = rotate(direction)
            y += dir_to_dy(direction)
            x += dir_to_dx(direction)
        action(y, x)

    if path == GridPath.HORIZONTALS_STRAIGHT_TL:
        for r in range(rows):
            for c in range(cols):
                action(r, c)
    elif path == GridPath.HORIZONTALS_STRAIGHT_BL:
        for r in reverse_sequence(rows):
            for c in range(cols):
                action(r, c)
    elif path == GridPath.HORIZONTALS_REVERSE_TR:
        for r in range(rows):
            for c in reverse_sequence(cols):
                action(r, c)
    elif path == GridPath.HORIZONTALS_REVERSE_BR:
        for r in reverse_sequence(rows):
            for c in reverse_sequence(cols):
                action(r, c)
    elif path == GridPath.HORIZONTALS_ALTERNATE_TL:
        for r in range(rows):
            if ((r + 1) % 2) != 0:
                for c in range(cols):
                    action(r, c)
            else:
                for c in reverse_sequence(cols):
                    action(r, c)
    elif path == GridPath.HORIZONTALS_ALTERNATE_TR:
        for r in range(rows):
            if (r % 2) != 0:
                for c in range(cols):
                    action(r, c)
            else:
                for c in reverse_sequence(cols):
                    action(r, c)
    elif path == GridPath.HORIZONTALS_ALTERNATE_BL:
        for r in reverse_sequence(rows):
            if ((rows - r) % 2) != 0:
                for c in range(cols):
                    action(r, c)
            else:
                for c in reverse_sequence(cols):
                    action(r, c)
    elif path == GridPath.HORIZONTALS_ALTERNATE_BR:
        for r in reverse_sequence(rows):
            if ((rows - r + 1) % 2) != 0:
                for c in range(cols):
                    action(r, c)
            else:
                for c in reverse_sequence(cols):
                    action(r, c)
    elif path == GridPath.VERTICALS_DESCENDING_TL:
        for c in range(cols):
            for r in range(rows):
                action(r, c)
    elif path == GridPath.VERTICALS_DESCENDING_TR:
        for c in reverse_sequence(cols):
            for r in range(rows):
                action(r, c)
    elif path == GridPath.VERTICALS_ASCENDING_BL:
        for c in range(cols):
            for r in reverse_sequence(rows):
                action(r, c)
    elif path == GridPath.VERTICALS_ASCENDING_BR:
        for c in reverse_sequence(cols):
            for r in reverse_sequence(rows):
                action(r, c)
    elif path == GridPath.VERTICALS_ALTERNATE_TL:
        for c in range(cols):
            if ((c + 1) % 2) != 0:
                for r in range(rows):
                    action(r, c)
            else:
                for r in reverse_sequence(rows):
                    action(r, c)
    elif path == GridPath.VERTICALS_ALTERNATE_BL:
        for c in range(cols):
            if (c % 2) != 0:
                for r in range(rows):
                    action(r, c)
            else:
                for r in reverse_sequence(rows):
                    action(r, c)
    elif path == GridPath.VERTICALS_ALTERNATE_TR:
        for c in reverse_sequence(cols):
            if ((cols - c) % 2) != 0:
                for r in range(rows):
                    action(r, c)
            else:
                for r in reverse_sequence(rows):
                    action(r, c)
    elif path == GridPath.VERTICALS_ALTERNATE_BR:
        for c in reverse_sequence(cols):
            if ((cols - c + 1) % 2) != 0:
                for r in range(rows):
                    action(r, c)
            else:
                for r in reverse_sequence(rows):
                    action(r, c)
    elif path == GridPath.SPIRAL_CLOCKWISE_IN_TL:
        walk_spiral(0, 0, dir_right, rotate_cw, action)
    elif path == GridPath.SPIRAL_CLOCKWISE_IN_TR:
        walk_spiral(0, cols - 1, dir_down, rotate_cw, action)
    elif path == GridPath.SPIRAL_CLOCKWISE_IN_BR:
        walk_spiral(rows - 1, cols - 1, dir_left, rotate_cw, action)
    elif path == GridPath.SPIRAL_CLOCKWISE_IN_BL:
        walk_spiral(rows - 1, 0, dir_up, rotate_cw, action)
    elif path == GridPath.SPIRAL_ANTICLOCKWISE_IN_TL:
        walk_spiral(0, 0, dir_down, rotate_ccw, action)
    elif path == GridPath.SPIRAL_ANTICLOCKWISE_IN_TR:
        walk_spiral(0, cols - 1, dir_left, rotate_ccw, action)
    elif path == GridPath.SPIRAL_ANTICLOCKWISE_IN_BR:
        walk_spiral(rows - 1, cols - 1, dir_up, rotate_ccw, action)
    elif path == GridPath.SPIRAL_ANTICLOCKWISE_IN_BL:
        walk_spiral(rows - 1, 0, dir_right, rotate_ccw, action)
    elif path == GridPath.SPIRAL_ANTICLOCKWISE_OUT_TL:
        walk_spiral(0, 0, dir_right, rotate_cw, action_reverse)
    elif path == GridPath.SPIRAL_ANTICLOCKWISE_OUT_TR:
        walk_spiral(0, cols - 1, dir_down, rotate_cw, action_reverse)
    elif path == GridPath.SPIRAL_ANTICLOCKWISE_OUT_BR:
        walk_spiral(rows - 1, cols - 1, dir_left, rotate_cw, action_reverse)
    elif path == GridPath.SPIRAL_ANTICLOCKWISE_OUT_BL:
        walk_spiral(rows - 1, 0, dir_up, rotate_cw, action_reverse)
    elif path == GridPath.SPIRAL_CLOCKWISE_OUT_TL:
        walk_spiral(0, 0, dir_down, rotate_ccw, action_reverse)
    elif path == GridPath.SPIRAL_CLOCKWISE_OUT_TR:
        walk_spiral(0, cols - 1, dir_left, rotate_ccw, action_reverse)
    elif path == GridPath.SPIRAL_CLOCKWISE_OUT_BR:
        walk_spiral(rows - 1, cols - 1, dir_up, rotate_ccw, action_reverse)
    elif path == GridPath.SPIRAL_CLOCKWISE_OUT_BL:
        walk_spiral(rows - 1, 0, dir_right, rotate_ccw, action_reverse)
    else:
        raise ValueError


def text_to_grid(rows: int, cols: int, text: str, path: GridPath) -> List[List[str]]:
    """
    Write text into a grid.

    :param rows: The grid rows.
    :param cols: The grid columns.
    :param text: The text to write into the grid.
    :param path: The path to follow when writing the characters.
    :return: The grid.
    """
    grid = create_grid(rows, cols, " ")
    text_iter = iter(text)
    rev_text_iter = iter(text[::-1])

    def action(y, x):
        grid[y][x] = next(text_iter)

    def rev_action(r, c):
        grid[r][c] = next(rev_text_iter)

    walk_path(path, rows, cols, action, rev_action)

    return grid


def grid_to_text(grid: List[List[str]], path: GridPath) -> str:
    """
    Convert a grid to text.

    :param grid: The grid to convert.
    :param path: The path to use when reading the characters from the grid.
    :return: The text.
    """
    text = [" "] * len(grid) * len(grid[0])
    pos = 0
    end_pos = len(text) - 1

    def action(r, c):
        nonlocal pos
        text[pos] = grid[r][c]
        pos += 1

    def rev_action(r, c):
        nonlocal end_pos
        text[end_pos] = grid[r][c]
        end_pos -= 1

    walk_path(path, len(grid), len(grid[0]), action, rev_action)

    return "".join(text)


def transform_text_with_grid(
    rows: int,
    cols: int,
    text: str,
    output_path: GridPath,
    input_path: GridPath,
    null_char: str = "_",
) -> str:
    """
    Transform a text by passing it through a grid, using different paths for writing and reading.

    :param rows: Grid rows.
    :param cols: Grid columns.
    :param text: Text to transform.
    :param output_path: How to write the initial text into the grid.
    :param input_path: How to read the text back from the grid.
    :param null_char: A characters inserted if there's too less text to fill the grid.
    :return: The transformed text.
    """
    grid_size = cols * rows
    result = ""
    for pos in range(0, len(text), grid_size):
        partial = text[pos : pos + grid_size].ljust(grid_size, null_char)
        grid = text_to_grid(rows, cols, partial, output_path)
        result += grid_to_text(grid, input_path)
    return result


def word_fitness_en(text: str, min_word_length: int = 3, max_word_length: int = 12) -> float:
    """
    Calculate a text fitness by searching for known dictionary words.

    :param text: The text to scan.
    :param min_word_length: The minimum word length to consider.
    :param max_word_length: The maximum word length to consider.
    :return: Text length divided by amount of matching words.
    """
    matching_chars = 0
    text_length = len(text)
    text = text.upper()
    for pos in range(text_length - min_word_length + 1):
        for word_size in range(min_word_length, max_word_length + 1):
            if pos + word_size >= text_length:
                break
            if text[pos : pos + word_size] in dict_std_en:
                matching_chars += word_size
                # Advance to next word
                pos += word_size - 1
    return max(1, matching_chars) / text_length


def find_best_path(
    text: str,
    rows: int,
    cols: int,
    fitness_fn: Callable[[str], float] = word_fitness_en,
) -> Tuple[float, str, GridPath, GridPath]:
    """
    Find the best path types for transforming a text through a grid.

    :param text: The text to transform.
    :param rows: The rows in the grid.
    :param cols: The columns in the grid.
    :param fitness_fn: A fitness scoring function.
    :return: A tuple of the fitness score, the transformed text, the input path type and the output path type.
    """
    text_stats: Stats
    best_fitness: float
    current_fitness: float

    # Calculate the stats
    text_stats = calc_stats(text)

    # Check for zero length text
    assert text_stats.letter_count != 0

    best_fitness = 0.0
    best_text = None
    best_input_path = None
    best_output_path = None

    for output_path in GridPath:
        for input_path in GridPath:
            transformed = transform_text_with_grid(rows, cols, text, output_path, input_path)
            current_fitness = fitness_fn(transformed)
            if current_fitness > best_fitness:
                best_fitness = current_fitness
                best_text = transformed
                best_input_path = input_path
                best_output_path = output_path

    assert best_text is not None
    return best_fitness, best_text, best_input_path, best_output_path
