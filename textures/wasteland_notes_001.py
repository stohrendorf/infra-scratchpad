from collections import defaultdict
from typing import Dict, Tuple

from other.bunker_computer import bunker_computer_code_2_solution
from textures.hartman_woodbox import hartman_woodbox_002_solution

wasteland_notes_001_key = {
    "A": "OTHERSIDE",
    "R": f"{hartman_woodbox_002_solution}HARTMAN",
    "Q": bunker_computer_code_2_solution,
    "T": "IFYOUKNOWITJUSTSAYITTHENYOUGETI?REDRAVEN",
}

wasteland_notes_001 = (
    "A.1 Q.4 A.3 A.9 A.5 A.6 A.7 A.8 A.9 Q.7 Q.6 Q.16 A.1 Q.4 A.3 A.9 A.5 Q.1 Q.6 A.5 Q.14 A.8",
    "YOU CAN R.7 R.4 R.8 R.9 R.6 R.7 R.4 R.11 R.3 R.5 R.4 R.8 R.6 R.7 A.7 R.13 T.28 WHERE THEY DIED",
    "R.5 R.12 T.38 R.4 R.13 T.2 A.1 T.13 T.24 A.8 A.7 A.2",
    "Q.1 Q.17 T.3 Q.12 Q.6 R.11 R.12 R.13 T.18 Q.5 Q.13 Q.8 Q.16 T.2 T.31 T.7 A.8 Q.3 Q.1 Q.3 T.25 Q.6 T.13 Q.11 Q.4 Q.6 Q.11 Q.2 Q.9 SURFACE",
    "EVERYONE Q.2 Q.9 A.5 A.4 A.7 Q.7 A.6 A.2 Q.3 Q.14 R.3 T.27 R.5 T.28 T.28 T.23 T.30 R.7 A.4 A.5 A.4",
    "T.19 T.15 T.9 T.17 R.13 T.20 T.14 T.20 T.4 T.6 T.29 T.23 T.50 T.18 T.26 T.5 T.13 T.24 A.8 T.23 T.36 T.28 R.5 T.8 T.5 T.7 A.8",
    "T.28 T.22 T.4 T.14 T.11 Q.1 Q.6 A.5 Q.14 A.8 Q.5 Q.6 Q.7 Q.8 Q.9 Q.10 Q.11 Q.20 T.35 A.2 A.1 A.2 A.3 A.4 WRONG WORLD",
    "Q.1 Q.17 Q.20 Q.7 T.25 Q.6 T.13 A.8 A.7 A.9 YOU CAN'T GET OUT",
    "EVERY WORLD HAS OWN LAWS THEY JUST HAVE TO BE CORRECT ONES",
    "T.9 T.22 T.19 T.11 T.29 R.11 T.17 T.16 T.6 T.14 T.20 T.22 T.23 T.18 T.6 T.24 T.8 T.9 Q.4 A.3 A.7 A.6 PLACE",
    "GOD OF UNDERGROUND KEEPS EVERYONE HERE",
    "T.28 A.1 A.8 SUFFERS A.7 A.6 A.7 A.2 A.8 A.4 Q.3 A.8",
    "WHAT HAPPENED IN A.1 A.2 A.3 A.9 A.5 A.6 A.7 A.8 A.9 WAS IT ALWAYS LIKE THIS",
    "THEY ARE Q.13 Q.14 Q.15 Q.14 Q.6 Q.12 Q.11 STUCK IN THAT R.3 R.2 R.12 Q.5 T.6 Q.1 Q.6 A.5 A.8",
    "A.8 A.7 A.8 R.6 R.7 R.1 R.10 R.3 A.1 R.11 R.3 A.8 R.4 A.6 R.10 R.5 A.1 T.18 EVERYTHING",
    "THE PLACE OUTSIDE THE WORLDS",
    "THE BORDER OF THE CHAOS IT IS THIS WORLD",
    "A.3 A.1 Q.1 R.11 T.17 R.13 T.25 T.11 T.10 R.11 R.4 T.14 T.25 A.1 T.5 R.7 R.12 T.36 R.4 A.6 A.9 A.9 Q.7 A.2 A.3 A.7 A.6 R.3 R.2 R.12 Q.5 T.6 Q.1 Q.6 A.5 Q.14 A.8",
    "WITHOUT THE CORRECT LAWS NOTHING STAYS TOGETHER",
    "THE MACHINE Q.5 Q.3 T.27 Q.12 Q.9 Q.19 A.7 A.2 A.2 A.3 A.9 T.3 A.8 A.1 Q.7 A.2 T.6 Q.7 Q.6 Q.1 A.7 A.2",
    "A.7 A.6 A.2 T.22 A.7 A.6 Q.3 Q.14 Q.15 T.12 T.5 Q.12 Q.11 Q.3 Q.14 A.7 A.4",
    "R.5 R.8 T.38 R.4 T.40 Q.1 Q.13 Q.19 Q.17 Q.9 A.5 T.29 THEY TRIED TO HELP",
    "A.8 A.7 T.38 A.7 T.7 T.28 A.6 T.27 A.7 A.2 PROTECTION",
    "T.28 T.26 T.35 T.4 T.2 R.11 T.1 R.13 R.4 R.5 T.14 T.14 R.6 R.12 R.6 T.13 T.39 T.14 T.31 R.13 R.11 T.10 R.13 R.4 T.14",
    "WHEN EVERYTHING IS CORRECT THE NEW WORLD IS BORN",
    "A.2 T.22 A.4 T.18 T.6 Q.7 A.1 T.9 A.3 A.1 Q.1 A.2 A.1 T.28 A.4 A.2 A.3 A.4 A.5 A.9",
    "Q.1 Q.2 Q.3 Q.4 A.7 Q.19 Q.4 Q.2 T.34 A.2 T.33 T.27 A.2 A.3",
    "WHERE EVERYTHING IS BORN THERE ARE NO LAWS",
    "T.21 R.7 R.4 T.18 R.11 T.37 T.35 R.4 A.1 Q.7 T.23 R.11 A.7 T.16 R.6 R.8 T.6 R.4",
    "T.5 R.13 T.35 R.4 R.9 T.28 R.5 T.4 T.27 R.13 T.35 Q.5 T.19 R.6 T.3 TRYING TO GET THEM OUT",
    "YOU CAN GET THERE IF YOU KNOW HOW",
)


def decode_wasteland_message(
    key: Dict[str, str], message: str, with_code: bool = False
) -> str:
    def decode_word(word: str) -> str:
        if "." not in word:
            return word

        prefix, index = word.split(".")
        try:
            decoded = key[prefix][int(index) - 1]
            return f"{decoded}={word}" if with_code else decoded
        except IndexError:
            return word

    return " ".join(map(decode_word, message.split()))


def clean_unreferenced_key_chars(
    key: Dict[str, str], messages: Tuple[str, ...]
) -> Dict[str, str]:
    used = defaultdict(set)
    for message in messages:
        for word in message.split():
            if "." not in word:
                continue

            prefix, index = word.split(".")
            used[prefix].add(int(index) - 1)

    key = key.copy()
    for used_key, used_indices in used.items():
        real_key = key[used_key]
        for i in range(len(real_key)):
            if i not in used_indices:
                real_key = real_key[:i] + "_" + real_key[i + 1 :]
        key[used_key] = real_key

    return key


if __name__ == "__main__":
    for note in wasteland_notes_001:
        print(decode_wasteland_message(wasteland_notes_001_key, note))
    print(clean_unreferenced_key_chars(wasteland_notes_001_key, wasteland_notes_001))
