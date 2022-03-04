"""The morse code found in random/wasteland_radio_001.wav."""

from infra.encodings.morse import decode_morse

wasteland_radio_morse = (
    ".-. .- ...- . -. .-.-.- # --- - .... . .-."
    " ### ... .. -.. . .-.-.- # .-. . ... . .- .-."
    " ### ... - --- .--. .--. . -.."
)


if __name__ == "__main__":
    for sentence in decode_morse(wasteland_radio_morse):
        print(sentence)
