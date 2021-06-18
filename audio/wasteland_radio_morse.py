from infra.morse import decode_morse

wasteland_radio_morse = (
    ".-. .- ...- . -. .-.-.- # --- - .... . .-."
    " ### ... .. -.. . .-.-.- # .-. . ... . .- .-."
    " ### ... - --- .--. .--. . -.."
)


if __name__ == "__main__":
    for sentence in decode_morse(wasteland_radio_morse):
        print(sentence)
