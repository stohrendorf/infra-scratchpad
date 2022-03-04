"""The morse code found in video/video_1.wav."""

from infra.encodings.morse import decode_morse

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
