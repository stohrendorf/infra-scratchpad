"""The morse code found in central_projector_morse.wav."""

from infra.morse import decode_morse

central_projector_morse = (
    "-.-- --- ..- # -.-. .- -. # -. --- - # ..-. .. -. -.. # .-. .. --. .... - # .- -. ... .-- . .-. --- .-. # - .... ."
    " # --.- ..- . ... - .. --- -. -... ..- - # .. ..-. # -.-- --- ..- # -.-. .- -. # ..-. .. -. -.."
    " # .... .. -- -.-- --- ..- # -.-. .- -. # .- ... -.-"
    " ### -- .- -.-- -... . # .... . # --. .. ...- . ... # -.-- --- ..-"
    " ### - .... .. ... # .--. .-.. .- -.-. . # .. ... -.-- --- ..- # -.-. .- -. # ... . . # .- ...."
)


if __name__ == "__main__":
    for sentence in decode_morse(central_projector_morse):
        print(sentence)
