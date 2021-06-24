"""The morse code found in Open Sewer radio_broken_001.wav."""

from infra.encodings.morse import decode_morse

radio_broken_001 = (
    # start 0:20, end ...
    "-.-. ---  -.. . ---... # .-. .- ...- . -. .-.-.-"
    # start 0:34, end 0:48
    " ### ... - .- - ..- ... ---... # ..-. .- .. .-.. ..- .-. . .-.-.-"
    # start 0:54, end 1:13
    " ### -- . ... ... .- --. . ---... # . ...- .- -.-. ..- .- - . # - .... . # .- .-. . .-"
    # start 1:26, end 1:35
    " ### .. -- -- . -.. .. .- - . .-.. -.-- .-.-.-"
    # start 1:38, end 1:45
    " ### .- .-. . .- # .. ... # -.-. ---"
)


if __name__ == "__main__":
    for sentence in decode_morse(radio_broken_001):
        print(sentence)
