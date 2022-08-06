"""The morse code found in random/wasteland_radio_001.wav."""

from infra.encodings.morse import decode_morse
from infra.output import section

wasteland_radio_morse = (
    ".-. .- ...- . -. .-.-.- # --- - .... . .-."
    " ### ... .. -.. . .-.-.- # .-. . ... . .- .-."
    " ### ... - --- .--. .--. . -.."
)


if __name__ == "__main__":
    with section("wasteland_radio_morse solution") as s:
        for sentence in decode_morse(wasteland_radio_morse):
            s.print(sentence)
