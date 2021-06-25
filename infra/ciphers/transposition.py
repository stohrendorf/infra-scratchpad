"""Transposition cipher function."""
from enum import Enum, auto, unique
from typing import Callable, Iterable, List, Sequence, Tuple, TypeVar, Union

from infra.nla import dict_std_en
from infra.stats import Stats, calc_stats
from infra.string import all_string_indices, split_every
from infra.utils import reverse_sequence


def get_encoding_mapping(key: str) -> Tuple[int, ...]:
    """
    Compute the encoding mapping for columnar transposition ciphers.

    :param key: The encoding key.
    :return: The column indices resulting from the encoding key.

    >>> get_encoding_mapping("ALBERT")
    (0, 2, 3, 1, 4, 5)
    """
    key_chars = sorted(set(key))
    return tuple(src_idx for key_char in key_chars for src_idx in all_string_indices(key, key_char))


def get_decoding_mapping(key: str) -> Tuple[int, ...]:
    """
    Compute the decoding mapping for columnar transposition ciphers.

    :param key: The decoding key.
    :return: The column indices resulting from the encoding key.

    >>> get_decoding_mapping("ALBERT")
    (0, 3, 1, 2, 4, 5)
    """
    return tuple(dst for dst, _ in sorted(enumerate(get_encoding_mapping(key)), key=lambda dst_src: dst_src[1]))


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
    return [data[src_idx] for src_idx in get_decoding_mapping(key)]


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


class GridPathOrigin(Enum):
    """Where to start a path walk."""

    TopLeft = auto()
    TopRight = auto()
    BottomRight = auto()
    BottomLeft = auto()


class GridPath(Enum):
    """The possible paths when walking a grid."""

    Rows = auto()
    """Row by row."""

    SnakeRows = auto()
    """Every second row is walked in reverse."""

    Columns = auto()
    """Column by column."""
    SnakeColumns = auto()
    """Every second column is walked in reverse."""

    SpiralCwIn = auto()
    """Walk a spiral, inwards, clockwise."""
    SpiralCcwIn = auto()
    """Walk a spiral, inwards, counter-clockwise."""

    SpiralCwOut = auto()
    """Walk a spiral, outwards, clockwise."""
    SpiralCcwOut = auto()
    """Walk a spiral, outwards, counter-clockwise."""


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


@unique
class _WalkDirection(Enum):
    dir_up = 0
    dir_right = 1
    dir_down = 2
    dir_left = 3


def _spiral_path(
    rows: int,
    cols: int,
    y0: int,
    x0: int,
    direction: _WalkDirection,
    rotate: Callable[[_WalkDirection], _WalkDirection],
) -> Iterable[Tuple[int, int]]:
    """
    Get the coordinates when walking a spiral.

    :param rows: Grid rows.
    :param cols: Grid columns.
    :param y0: Starting row.
    :param x0: Starting column.
    :param direction: Starting direction.
    :param rotate: Called when the direction needs to be changed.
    :return: An iterable of (y,x) coordinates.
    """

    def dir_to_dy(d: _WalkDirection) -> int:
        if d == _WalkDirection.dir_up:
            return -1
        elif d == _WalkDirection.dir_down:
            return 1
        else:
            return 0

    def dir_to_dx(d: _WalkDirection) -> int:
        if d == _WalkDirection.dir_left:
            return -1
        elif d == _WalkDirection.dir_right:
            return 1
        else:
            return 0

    visited = create_grid(rows, cols, False)
    y, x = y0, x0

    for _ in range(1, rows * cols):
        assert not visited[y][x]
        visited[y][x] = True
        yield y, x

        nx = x + dir_to_dx(direction)
        ny = y + dir_to_dy(direction)
        if not (0 <= ny < rows) or not (0 <= nx < cols) or visited[ny][nx]:
            direction = rotate(direction)
        y += dir_to_dy(direction)
        x += dir_to_dx(direction)
    yield y, x


def walk_path(
    path: GridPath,
    origin: GridPathOrigin,
    rows: int,
    cols: int,
) -> Iterable[Tuple[int, int]]:
    """
    Execute actions while walking over a grid.

    :param path: The path to follow.
    :param origin: Where to start walking.
    :param rows: Rows in the grid.
    :param cols: Columns in the grid.
    :return: The coordinates on the requested path.

    >>> tuple(walk_path(GridPath.Rows, GridPathOrigin.TopLeft, 3, 3))
    ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2))
    >>> tuple(walk_path(GridPath.Rows, GridPathOrigin.TopRight, 3, 3))
    ((0, 2), (0, 1), (0, 0), (1, 2), (1, 1), (1, 0), (2, 2), (2, 1), (2, 0))
    >>> tuple(walk_path(GridPath.Rows, GridPathOrigin.BottomLeft, 3, 3))
    ((2, 0), (2, 1), (2, 2), (1, 0), (1, 1), (1, 2), (0, 0), (0, 1), (0, 2))
    >>> tuple(walk_path(GridPath.Rows, GridPathOrigin.BottomRight, 3, 3))
    ((2, 2), (2, 1), (2, 0), (1, 2), (1, 1), (1, 0), (0, 2), (0, 1), (0, 0))

    >>> tuple(walk_path(GridPath.SnakeRows, GridPathOrigin.TopLeft, 3, 3))
    ((0, 0), (0, 1), (0, 2), (1, 2), (1, 1), (1, 0), (2, 0), (2, 1), (2, 2))
    >>> tuple(walk_path(GridPath.SnakeRows, GridPathOrigin.TopRight, 3, 3))
    ((0, 2), (0, 1), (0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (2, 1), (2, 0))
    >>> tuple(walk_path(GridPath.SnakeRows, GridPathOrigin.BottomLeft, 3, 3))
    ((2, 0), (2, 1), (2, 2), (1, 2), (1, 1), (1, 0), (0, 0), (0, 1), (0, 2))
    >>> tuple(walk_path(GridPath.SnakeRows, GridPathOrigin.BottomRight, 3, 3))
    ((2, 2), (2, 1), (2, 0), (1, 0), (1, 1), (1, 2), (0, 2), (0, 1), (0, 0))

    >>> tuple(walk_path(GridPath.Columns, GridPathOrigin.TopLeft, 3, 3))
    ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2))
    >>> tuple(walk_path(GridPath.Columns, GridPathOrigin.TopRight, 3, 3))
    ((0, 2), (1, 2), (2, 2), (0, 1), (1, 1), (2, 1), (0, 0), (1, 0), (2, 0))
    >>> tuple(walk_path(GridPath.Columns, GridPathOrigin.BottomLeft, 3, 3))
    ((2, 0), (1, 0), (0, 0), (2, 1), (1, 1), (0, 1), (2, 2), (1, 2), (0, 2))
    >>> tuple(walk_path(GridPath.Columns, GridPathOrigin.BottomRight, 3, 3))
    ((2, 2), (1, 2), (0, 2), (2, 1), (1, 1), (0, 1), (2, 0), (1, 0), (0, 0))
    >>> tuple(walk_path(GridPath.SnakeColumns, GridPathOrigin.TopLeft, 3, 3))
    ((0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2))
    >>> tuple(walk_path(GridPath.SnakeColumns, GridPathOrigin.TopRight, 3, 3))
    ((0, 2), (1, 2), (2, 2), (2, 1), (1, 1), (0, 1), (0, 0), (1, 0), (2, 0))
    >>> tuple(walk_path(GridPath.SnakeColumns, GridPathOrigin.BottomLeft, 3, 3))
    ((2, 0), (1, 0), (0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (1, 2), (0, 2))
    >>> tuple(walk_path(GridPath.SnakeColumns, GridPathOrigin.BottomRight, 3, 3))
    ((2, 2), (1, 2), (0, 2), (0, 1), (1, 1), (2, 1), (2, 0), (1, 0), (0, 0))

    >>> tuple(walk_path(GridPath.SpiralCwIn, GridPathOrigin.TopLeft, 3, 3))
    ((0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0), (1, 1))
    >>> tuple(walk_path(GridPath.SpiralCwIn, GridPathOrigin.TopRight, 3, 3))
    ((0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0), (0, 1), (1, 1))
    >>> tuple(walk_path(GridPath.SpiralCwIn, GridPathOrigin.BottomLeft, 3, 3))
    ((2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (1, 1))
    >>> tuple(walk_path(GridPath.SpiralCwIn, GridPathOrigin.BottomRight, 3, 3))
    ((2, 2), (2, 1), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (1, 2), (1, 1))
    >>> tuple(walk_path(GridPath.SpiralCcwIn, GridPathOrigin.TopLeft, 3, 3))
    ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (1, 1))
    >>> tuple(walk_path(GridPath.SpiralCcwIn, GridPathOrigin.TopRight, 3, 3))
    ((0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (1, 1))
    >>> tuple(walk_path(GridPath.SpiralCcwIn, GridPathOrigin.BottomLeft, 3, 3))
    ((2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (0, 0), (1, 0), (1, 1))
    >>> tuple(walk_path(GridPath.SpiralCcwIn, GridPathOrigin.BottomRight, 3, 3))
    ((2, 2), (1, 2), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (2, 1), (1, 1))

    >>> tuple(walk_path(GridPath.SpiralCwOut, GridPathOrigin.TopLeft, 3, 3))
    ((1, 1), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (0, 0))
    >>> tuple(walk_path(GridPath.SpiralCwOut, GridPathOrigin.TopRight, 3, 3))
    ((1, 1), (0, 1), (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2))
    >>> tuple(walk_path(GridPath.SpiralCwOut, GridPathOrigin.BottomLeft, 3, 3))
    ((1, 1), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0))
    >>> tuple(walk_path(GridPath.SpiralCwOut, GridPathOrigin.BottomRight, 3, 3))
    ((1, 1), (1, 2), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (2, 1), (2, 2))
    >>> tuple(walk_path(GridPath.SpiralCcwOut, GridPathOrigin.TopLeft, 3, 3))
    ((1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0))
    >>> tuple(walk_path(GridPath.SpiralCcwOut, GridPathOrigin.TopRight, 3, 3))
    ((1, 1), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2))
    >>> tuple(walk_path(GridPath.SpiralCcwOut, GridPathOrigin.BottomLeft, 3, 3))
    ((1, 1), (1, 0), (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0))
    >>> tuple(walk_path(GridPath.SpiralCcwOut, GridPathOrigin.BottomRight, 3, 3))
    ((1, 1), (2, 1), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (1, 2), (2, 2))
    """

    def rotate_cw(d: _WalkDirection) -> _WalkDirection:
        return _WalkDirection((d.value + 1) % 4)

    def rotate_ccw(d: _WalkDirection) -> _WalkDirection:
        return _WalkDirection((d.value + 3) % 4)

    def origin_range(n: int, *origins: GridPathOrigin) -> Iterable[int]:
        return range(n) if origin in origins else reverse_sequence(n)

    if path == GridPath.Rows:
        for r in origin_range(rows, GridPathOrigin.TopLeft, GridPathOrigin.TopRight):
            for c in origin_range(cols, GridPathOrigin.TopLeft, GridPathOrigin.BottomLeft):
                yield r, c
    elif path == GridPath.SnakeRows:
        forward = origin in (GridPathOrigin.TopLeft, GridPathOrigin.BottomLeft)
        for r in origin_range(rows, GridPathOrigin.TopLeft, GridPathOrigin.TopRight):
            for c in range(cols) if forward else reverse_sequence(cols):
                yield r, c
            forward = not forward
    elif path == GridPath.Columns:
        for c in origin_range(cols, GridPathOrigin.TopLeft, GridPathOrigin.BottomLeft):
            for r in origin_range(rows, GridPathOrigin.TopLeft, GridPathOrigin.TopRight):
                yield r, c
    elif path == GridPath.SnakeColumns:
        forward = origin in (GridPathOrigin.TopLeft, GridPathOrigin.TopRight)
        for c in origin_range(cols, GridPathOrigin.TopLeft, GridPathOrigin.BottomLeft):
            for r in range(rows) if forward else reverse_sequence(rows):
                yield r, c
            forward = not forward
    elif path in (GridPath.SpiralCwIn, GridPath.SpiralCwOut):

        def reverse_if_out(coords: Iterable[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
            return coords if path != GridPath.SpiralCwOut else reversed(tuple(coords))

        yield from reverse_if_out(
            _spiral_path(
                rows,
                cols,
                0 if origin in (GridPathOrigin.TopLeft, GridPathOrigin.TopRight) else rows - 1,
                0 if origin in (GridPathOrigin.TopLeft, GridPathOrigin.BottomLeft) else cols - 1,
                {
                    GridPathOrigin.TopLeft: _WalkDirection.dir_right,
                    GridPathOrigin.TopRight: _WalkDirection.dir_down,
                    GridPathOrigin.BottomRight: _WalkDirection.dir_left,
                    GridPathOrigin.BottomLeft: _WalkDirection.dir_up,
                }[origin],
                rotate_cw,
            ),
        )
    elif path in (GridPath.SpiralCcwIn, GridPath.SpiralCcwOut):

        def reverse_if_out(coords: Iterable[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
            return coords if path != GridPath.SpiralCcwOut else reversed(tuple(coords))

        yield from reverse_if_out(
            _spiral_path(
                rows,
                cols,
                0 if origin in (GridPathOrigin.TopLeft, GridPathOrigin.TopRight) else rows - 1,
                0 if origin in (GridPathOrigin.TopLeft, GridPathOrigin.BottomLeft) else cols - 1,
                {
                    GridPathOrigin.TopLeft: _WalkDirection.dir_down,
                    GridPathOrigin.TopRight: _WalkDirection.dir_left,
                    GridPathOrigin.BottomRight: _WalkDirection.dir_up,
                    GridPathOrigin.BottomLeft: _WalkDirection.dir_right,
                }[origin],
                rotate_ccw,
            ),
        )
    else:
        raise ValueError


def text_to_grid(rows: int, cols: int, text: str, path: GridPath, origin: GridPathOrigin) -> List[List[str]]:
    """
    Write text into a grid.

    :param rows: The grid rows.
    :param cols: The grid columns.
    :param text: The text to write into the grid.
    :param path: The path to follow when writing the characters.
    :param origin: Where to start walking.
    :return: The grid.

    >>> text_to_grid(3, 3, "ABCDEFGHI", GridPath.SpiralCwIn, GridPathOrigin.BottomRight)
    [['E', 'F', 'G'], ['D', 'I', 'H'], ['C', 'B', 'A']]
    """
    grid = create_grid(rows, cols, " ")
    text_iter = iter(text)

    for y, x in walk_path(path, origin, rows, cols):
        grid[y][x] = next(text_iter)

    return grid


def grid_to_text(grid: List[List[str]], path: GridPath, origin: GridPathOrigin) -> str:
    """
    Convert a grid to text.

    :param grid: The grid to convert.
    :param path: The path to use when reading the characters from the grid.
    :param origin: Where to start walking.
    :return: The text.

    >>> grid_to_text(
    ...     [['E', 'F', 'G'], ['D', 'I', 'H'], ['C', 'B', 'A']], GridPath.SpiralCwIn, GridPathOrigin.BottomRight)
    'ABCDEFGHI'
    """
    return "".join(grid[y][x] for y, x in walk_path(path, origin, len(grid), len(grid[0])))


def transform_text_with_grid(
    rows: int,
    cols: int,
    text: str,
    output_path: GridPath,
    output_origin: GridPathOrigin,
    input_path: GridPath,
    input_origin: GridPathOrigin,
    null_char: str = "_",
) -> str:
    """
    Transform a text by passing it through a grid, using different paths for writing and reading.

    :param rows: Grid rows.
    :param cols: Grid columns.
    :param text: Text to transform.
    :param output_path: How to write the initial text into the grid.
    :param output_origin: Where to start walking when writing text into the grid.
    :param input_path: How to read the text back from the grid.
    :param input_origin: Where to start walking when reading text from the grid.
    :param null_char: A characters inserted if there's too less text to fill the grid.
    :return: The transformed text.
    """
    grid_size = cols * rows
    result = ""
    for pos in range(0, len(text), grid_size):
        partial = text[pos : pos + grid_size].ljust(grid_size, null_char)
        grid = text_to_grid(rows, cols, partial, output_path, output_origin)
        result += grid_to_text(grid, input_path, input_origin)
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
) -> Tuple[float, str, GridPath, GridPathOrigin, GridPath, GridPathOrigin]:
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
    best_input_origin = None
    best_output_path = None
    best_output_origin = None

    for output_path in GridPath:
        for output_origin in GridPathOrigin:
            for input_path in GridPath:
                for input_origin in GridPathOrigin:
                    transformed = transform_text_with_grid(
                        rows,
                        cols,
                        text,
                        output_path,
                        output_origin,
                        input_path,
                        input_origin,
                    )
                    current_fitness = fitness_fn(transformed)
                    if current_fitness > best_fitness:
                        best_fitness = current_fitness
                        best_text = transformed
                        best_input_path = input_path
                        best_input_origin = input_origin
                        best_output_path = output_path
                        best_output_origin = output_origin

    assert best_text is not None
    return best_fitness, best_text, best_input_path, best_input_origin, best_output_path, best_output_origin
