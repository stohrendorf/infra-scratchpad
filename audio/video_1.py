"""The morse code found in video/video_1.wav."""

from infra.encodings.morse import decode_morse
from infra.output import section

central_projector_morse = (
    "-.-- --- ..- # -.-. .- -. # -. --- - # ..-. .. -. -.. # .-. .. --. .... - # .- -. ... .-- . .-. --- .-. # - .... ."
    " # --.- ..- . ... - .. --- -. -... ..- - # .. ..-. # -.-- --- ..- # -.-. .- -. # ..-. .. -. -.."
    " # .... .. -- -.-- --- ..- # -.-. .- -. # .- ... -.-"
    " ### -- .- -.-- -... . # .... . # --. .. ...- . ... # -.-- --- ..-"
    " ### - .... .. ... # .--. .-.. .- -.-. . # .. ... -.-- --- ..- # -.-. .- -. # ... . . # .- ...."
)


if __name__ == "__main__":
    with section("central_projector_morse solution") as s:
        for sentence in decode_morse(central_projector_morse):
            s.print(sentence)
