"""Natural language analysis functions."""
import csv
from pathlib import Path
from typing import Dict, Iterable, Set, Tuple

from infra.utils import get_pairs, split_every

alphabet_fi = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"


def _load_frq_csv(path: Path) -> Dict[str, float]:
    return {key: float(count) for key, count in csv.reader(path.read_text().splitlines())}


def _load_cblw_score_csv(path: Path) -> Dict[str, float]:
    def idx_to_letter(idx: int) -> str:
        return chr(ord("A") + idx)

    return {
        f"{idx_to_letter(x)}{idx_to_letter(y)}": float(score)
        for x, scores in enumerate(csv.reader(path.read_text().splitlines()))
        for y, score in enumerate(scores)
    }


def get_quantile(data: Dict[str, float], quantile: float) -> Set[str]:
    """
    Get the top quantile of a data set.

    :param data: The data set.
    :param quantile: The quantile.
    :return: The keys of the dataset.
    """
    total = sum(data.values())
    current_sum = 0
    result = set()
    sorted_data = sorted(data.items(), key=lambda kv: kv[1], reverse=True)
    for key, value in sorted_data:
        if current_sum >= quantile:
            break

        result.add(key)
        current_sum += value / total

    return result


letter_frq_en = _load_frq_csv(Path(__file__).parent / "letter_frq_en.csv")
total_letter_frq_en = sum(letter_frq_en.values())
top_letters_en = get_quantile(letter_frq_en, 0.75)
cblw_scores_en = _load_cblw_score_csv(Path(__file__).parent / "cblw_scores_en.csv")

bigram_frq_en = _load_frq_csv(Path(__file__).parent / "bigram_frq_en.csv")
total_bigram_frq_en = sum(bigram_frq_en.values())
top_bigrams_en = get_quantile(bigram_frq_en, 0.75)


def get_mfl_score_en(string: str) -> float:
    """
    https://www.staff.uni-mainz.de/pommeren/Cryptology/Classic/3_Coincid/MFL.html.

    :return: The MFL score.

    >>> get_mfl_score_en("hello world")
    0.8181818181818182
    >>> get_mfl_score_en("uibyl jhboli")
    0.5
    """
    return sum(1 for c in string if c.upper() in top_letters_en) / len(string)


def get_mfl_bigram_score_en(string: str) -> float:
    """
    https://www.staff.uni-mainz.de/pommeren/Cryptology/Classic/3_Coincid/MFL.html.

    :return: The MFL score.

    >>> get_mfl_bigram_score_en("hello world")
    0.2
    >>> get_mfl_bigram_score_en("uibyl jhboli")
    0.0
    """
    if len(string) <= 1:
        return 0.0

    return sum(1 for c1, c2 in zip(string, string[1:]) if f"{c1}{c2}".upper() in top_bigrams_en) / (len(string) - 1)


def get_cblw_score(s1: str, s2: str) -> float:
    """
    Get the conditional bigram log-weight score of two strings.

    https://www.staff.uni-mainz.de/pommeren/Cryptology/Classic/8_Transpos/Approach.html

    :param s1: First string.
    :param s2: Second string.
    :return: The score.

    >>> get_cblw_score("HELLO", "WORLD")
    1.3599999999999999
    >>> get_cblw_score("HLOOL", "ELWRD")
    2.1000000000000005
    """
    score = 0.0
    for c1, c2 in zip(s1, s2):
        score += cblw_scores_en.get(f"{c1}{c2}".upper(), 0.0)
    return score / min(len(s1), len(s2))


def find_best_shifted_cblw_score(a: str, b: str, max_shift: int = 20) -> Tuple[int, float]:
    """
    Find the combination of two strings with the best cblw score when shifting the strings.

    :param a: The first string.
    :param b: The second string.
    :param max_shift: The max amount of shifting when combining the strings.
    :return: A tuple of the best shift (negative if the first string is shifted) and the best score.

    >>> find_best_shifted_cblw_score("HLOOL", "ELWRD")
    (0, 2.1000000000000005)
    >>> find_best_shifted_cblw_score("HLOOL", "xxELWRD")
    (-2, 1.5000000000000002)
    >>> find_best_shifted_cblw_score("xxHLOOL", "ELWRD")
    (2, 1.5000000000000002)
    """
    max_shift = min(max_shift, max(len(a), len(b)))
    best_shift = None
    best_score = -1.0

    for shift in range(max_shift + 1):
        score = get_cblw_score(a, " " * shift + b)
        if score > best_score:
            best_shift = shift
            best_score = score
        score = get_cblw_score(" " * shift + a, b)
        if score > best_score:
            best_shift = -shift
            best_score = score

    assert best_shift is not None
    return best_shift, best_score


def calc_cblw_scores(
    plaintext: str,
    min_split_size: int = 5,
    max_shift: int = 20,
) -> Iterable[Tuple[Tuple[int, int], float, int, int]]:
    """
    Find all best cblw scores of shifted string combinations.

    :param plaintext: The plaintext to split and combine.
    :param min_split_size: The minimum line split size.
    :param max_shift: The maximum shift when combining split lines.
    :return: Tuples of the best split indices, the best score for these indices, the best shift for these indices,
             and the split size.

    >>> test = "HLOOLELWRD"
    >>> scores = tuple(calc_cblw_scores(test))
    >>> for best_pair, best_score, best_shift, best_split_size in scores:
    ...     print(f"{best_pair=} {best_score=} {best_shift=} {best_split_size=}")
    ...     for line in split_every(test, best_split_size):
    ...         print(line)
    best_pair=(0, 1) best_score=2.1000000000000005 best_shift=0 best_split_size=5
    HLOOL
    ELWRD
    best_pair=(0, 1) best_score=1.56 best_shift=1 best_split_size=6
    HLOOLE
    LWRD
    best_pair=(1, 0) best_score=1.9000000000000001 best_shift=0 best_split_size=7
    HLOOLEL
    WRD
    best_pair=(0, 1) best_score=1.5 best_shift=0 best_split_size=8
    HLOOLELW
    RD
    """
    for split_size in range(min_split_size, len(plaintext) // 2 + 4):
        splits = split_every(plaintext, split_size)

        best_shift = -1
        best_score = -1.0
        best_pair = (-1, -1)
        for p1, p2 in get_pairs(len(splits)):
            shift, score = find_best_shifted_cblw_score(splits[p1], splits[p2], max_shift)
            if score > best_score:
                best_shift = shift
                best_score = score
                best_pair = (p1, p2)

        yield best_pair, best_score, best_shift, split_size
