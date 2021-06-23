"""N-gram stats and other stats."""

import math
from dataclasses import dataclass
from typing import Dict, Tuple

from infra.nla import bigram_frq_en, letter_frq_en, trigram_frq_en


@dataclass
class Stats:
    """Text statistics."""

    letter_count: int
    single_letters: Dict[str, float]
    single_letter_error: float
    bigrams: Dict[str, float]
    bigram_error: float
    trigrams: Dict[str, float]
    trigram_error: float
    total_error: float
    ic: float
    entropy: float

    @property
    def efficiency(self) -> float:  # noqa D102
        return self.entropy / math.log(26.0)

    @property
    def redundancy(self) -> float:  # noqa D102
        return 1.0 - self.efficiency


def _make_frq_table(text: str) -> Tuple[Dict[str, float], Dict[str, float], Dict[str, float]]:
    single_letters = dict()
    for letter in text:
        single_letters[letter] = single_letters.get(letter, 0.0) + 1.0
    single_letters = {k: v / sum(single_letters.values()) for k, v in single_letters.items()}

    bigrams = dict()
    for bigram in map("".join, zip(text, text[1:])):
        bigrams[bigram] = bigrams.get(bigram, 0.0) + 1.0
    bigrams = {k: v / sum(bigrams.values()) for k, v in bigrams.items()}

    trigrams = dict()
    for trigram in map("".join, zip(text, text[1:], text[2:])):
        trigrams[trigram] = trigrams.get(trigram, 0.0) + 1.0
    trigrams = {k: v / sum(trigrams.values()) for k, v in trigrams.items()}

    return single_letters, bigrams, trigrams


def _total_error(single_letter_error: float, bigram_error: float, trigram_error: float) -> float:
    return sum(a * b for a, b in zip((single_letter_error, bigram_error, trigram_error), (1.0, 1.0, 2.0)))


def _calc_error(sample: Dict[str, float], base: Dict[str, float]) -> float:
    return sum((base.get(k, 0.0) - v) ** 2 for k, v in sample.items())


# Calculate index of coincidence
def _calc_coincidence_index(single_letter_frq: Dict[str, float], letter_count: int) -> float:
    return sum(freq * (letter_count * freq - 1) / (letter_count - 1) for freq in single_letter_frq.values())


def _calc_entropy(single_letter_frq: Dict[str, float]) -> float:
    return -sum(freq * math.log(freq) for freq in single_letter_frq.values() if freq > 0)


def calc_stats(text: str) -> Stats:
    """
    Calculate several stats about a given text.

    :param text: The text to calculate the stats on.
    :return: The stats.
    """
    single_letters, bigrams, trigrams = _make_frq_table(text)
    single_letter_error = _calc_error(single_letters, letter_frq_en)
    bigram_error = _calc_error(bigrams, bigram_frq_en)
    trigram_error = _calc_error(trigrams, trigram_frq_en)
    return Stats(
        letter_count=len(text),
        single_letters=single_letters,
        single_letter_error=single_letter_error,
        bigrams=bigrams,
        bigram_error=bigram_error,
        trigrams=trigrams,
        trigram_error=trigram_error,
        total_error=_total_error(single_letter_error, bigram_error, trigram_error),
        ic=_calc_coincidence_index(single_letters, len(text)),
        entropy=_calc_entropy(single_letters),
    )


def transform_stats_with_substitution_key(stats: Stats, key: Dict[str, str]) -> Stats:
    """
    Perform a substitution cipher on stats.

    :param stats: The stats.
    :param key: The substitution key.
    :return: The mutated stats.
    """

    def substitute(text: str) -> str:
        return "".join(key.get(c, c) for c in text)

    single_letters = {substitute(i): it for i, it in stats.single_letters.items()}
    bigrams = {substitute(i): it for i, it in stats.bigrams.items()}
    trigrams = {substitute(i): it for i, it in stats.trigrams.items()}

    single_letter_error = _calc_error(single_letters, letter_frq_en)
    bigram_error = _calc_error(bigrams, bigram_frq_en)
    trigram_error = _calc_error(trigrams, trigram_frq_en)
    return Stats(
        letter_count=stats.letter_count,
        single_letters=single_letters,
        single_letter_error=single_letter_error,
        bigrams=bigrams,
        bigram_error=bigram_error,
        trigrams=trigrams,
        trigram_error=trigram_error,
        total_error=_total_error(single_letter_error, bigram_error, trigram_error),
        ic=stats.ic,
        entropy=stats.entropy,
    )
