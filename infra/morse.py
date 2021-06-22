"""Morse code encoding and decoding."""

from typing import Tuple

WORD_DELIMITER = "#"
SENTENCE_DELIMITER = "###"

morse = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "-----": "0",
    ".-.-.-": ".",
    "---...": ":",
}

assert len(set(morse.values())) == len(morse), "Morse code mappings are not unique"


def decode_morse(encoded: str) -> Tuple[str]:
    """
    Decode a morse string.

    :param encoded: The morse code string.
    :return: The decoded morse code string.

    >>> decode_morse(".- -... ### -.-. # -..")
    ('AB', 'C D')
    """

    def decode_word(encoded_word: str) -> str:
        return "".join(morse[char] for char in encoded_word.split())

    def decode_sentence(encoded_sentence: str) -> str:
        return " ".join(decode_word(encoded_word) for encoded_word in encoded_sentence.split(WORD_DELIMITER))

    return tuple(decode_sentence(encoded_sentence.strip()) for encoded_sentence in encoded.split(SENTENCE_DELIMITER))
