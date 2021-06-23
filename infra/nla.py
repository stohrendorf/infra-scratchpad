"""Natural language analysis functions."""
import csv
from pathlib import Path
from typing import Dict, Set

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
    >>> get_cblw_score("HLLOWRD", "ELLOOL")
    1.9333333333333336
    """
    score = 0.0
    for c1, c2 in zip(s1, s2):
        score += cblw_scores_en.get(f"{c1}{c2}".upper(), 0.0)
    return score / min(len(s1), len(s2))
