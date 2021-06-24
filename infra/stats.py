"""N-gram stats and other stats."""

import math
from dataclasses import dataclass
from typing import Dict, Iterable

from infra.nla import bigram_frq_en, letter_frq_en, trigram_frq_en

NGramFrequencies = Dict[str, float]


@dataclass
class Stats:
    """Text statistics."""

    letter_count: int
    monogram: NGramFrequencies
    monogram_error: float
    bigrams: NGramFrequencies
    bigram_error: float
    trigrams: NGramFrequencies
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


def count_ngram_frq(ngrams: Iterable[str]) -> NGramFrequencies:
    """
    Count the frequency of a series of n-grams.

    :param ngrams: The n-grams.
    :return: The frequencies, the values summing up to 1.

    >>> count_ngram_frq("AAABBC")
    {'A': 0.5, 'B': 0.3333333333333333, 'C': 0.16666666666666666}
    >>> count_ngram_frq(("AA", "AB", "AA", "BC"))
    {'AA': 0.5, 'AB': 0.25, 'BC': 0.25}
    """
    frequencies = dict()
    total = 0
    for ngram in ngrams:
        frequencies[ngram] = frequencies.get(ngram, 0.0) + 1.0
        total += 1
    return {ngram: frq / total for ngram, frq in frequencies.items()}


def _total_ngram_error(single_letter_error: float, bigram_error: float, trigram_error: float) -> float:
    return sum(a * b for a, b in zip((single_letter_error, bigram_error, trigram_error), (1.0, 1.0, 2.0)))


def _ngram_error(sample: NGramFrequencies, reference: NGramFrequencies) -> float:
    return sum((reference.get(ngram, 0.0) - v) ** 2 for ngram, v in sample.items())


def _coincidence_index(single_letter_frq: NGramFrequencies, letter_count: int) -> float:
    return sum(freq * (letter_count * freq - 1) / (letter_count - 1) for freq in single_letter_frq.values())


def _entropy(single_letter_frq: NGramFrequencies) -> float:
    return -sum(freq * math.log(freq) for freq in single_letter_frq.values() if freq > 0)


def calc_stats(text: str) -> Stats:
    """
    Calculate several stats about a given text.

    :param text: The text to calculate the stats on.
    :return: The stats.
    """
    single_letters = count_ngram_frq(text)
    monogram_error = _ngram_error(single_letters, letter_frq_en)

    bigrams = count_ngram_frq(map("".join, zip(text, text[1:])))
    bigram_error = _ngram_error(bigrams, bigram_frq_en)

    trigrams = count_ngram_frq(map("".join, zip(text, text[1:], text[2:])))
    trigram_error = _ngram_error(trigrams, trigram_frq_en)

    return Stats(
        letter_count=len(text),
        monogram=single_letters,
        monogram_error=monogram_error,
        bigrams=bigrams,
        bigram_error=bigram_error,
        trigrams=trigrams,
        trigram_error=trigram_error,
        total_error=_total_ngram_error(monogram_error, bigram_error, trigram_error),
        ic=_coincidence_index(single_letters, len(text)),
        entropy=_entropy(single_letters),
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

    single_letters = {substitute(i): it for i, it in stats.monogram.items()}
    bigrams = {substitute(i): it for i, it in stats.bigrams.items()}
    trigrams = {substitute(i): it for i, it in stats.trigrams.items()}

    single_letter_error = _ngram_error(single_letters, letter_frq_en)
    bigram_error = _ngram_error(bigrams, bigram_frq_en)
    trigram_error = _ngram_error(trigrams, trigram_frq_en)
    return Stats(
        letter_count=stats.letter_count,
        monogram=single_letters,
        monogram_error=single_letter_error,
        bigrams=bigrams,
        bigram_error=bigram_error,
        trigrams=trigrams,
        trigram_error=trigram_error,
        total_error=_total_ngram_error(single_letter_error, bigram_error, trigram_error),
        ic=stats.ic,
        entropy=stats.entropy,
    )
