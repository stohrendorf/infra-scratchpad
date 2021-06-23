"""Functions for substitution ciphers."""

import math
import random
from typing import Dict, Tuple

from infra.stats import calc_stats, transform_stats_with_substitution_key


def substitution_hillclimb_attack(
    text: str,
    key: Dict[str, str],
    max_tries: float = 1000,
    max_search_depth: int = 3,
) -> Tuple[float, Dict[str, str]]:
    """
    Perform a hillclimb bruteforce substition cipher attack.

    This algorithm is non-deterministic and results may vary when called multiple times with the same input.

    :param text: The text to decrypt.
    :param key: The initial key to mutate from.
    :param max_tries: Number of mutations tried before increasing search depth.
    :param max_search_depth: Maximum search depth.
    :return: The best error score and corresponding mutated key.
    """
    text_stats = calc_stats(text)

    assert text_stats.letter_count != 0

    # Init best scores and key to current
    best_key = key.copy()
    best_error = transform_stats_with_substitution_key(text_stats, best_key).total_error

    search_depth = 1

    while True:
        try_max = math.ceil(max_tries * 26.0 ** (search_depth - 1))

        next_depth_loop = False
        for _ in range(try_max):
            mutated_key = best_key.copy()
            for _ in range(search_depth):
                swap_a = random.choice(tuple(mutated_key.keys()))
                swap_b = random.choice(tuple(mutated_key.keys()))
                mutated_key[swap_a], mutated_key[swap_b] = mutated_key[swap_b], mutated_key[swap_a]

            key = mutated_key
            current_error = transform_stats_with_substitution_key(text_stats, key).total_error
            if current_error < best_error:
                search_depth = 1
                best_error = current_error
                best_key = key.copy()
                next_depth_loop = True
                break

        if next_depth_loop:
            continue

        search_depth += 1
        if search_depth > max_search_depth:
            break

    return best_error, best_key


def substitute(text: str, key: Dict[str, str]) -> str:
    """
    Apply a substitution cipher on a text.

    :param text: The text to modify.
    :param key: The key.
    :return: The substituted text.

    >>> substitute("HELLO", {"H": "X", "L": "Y"})
    'XEYYO'
    """
    return "".join(key.get(c, c) for c in text)
