from infra.utils import binary_decode_multi

sign_07_skin10 = (
    "01110000 01110101",
    "01101110 01100001",
    "01101001 01101110",
    "01100101 01101110",
    "00100000 01110100",
    "01110101 01110010",
    "01110011 01101011",
    "01100001",
)

if __name__ == "__main__":
    for entry in sign_07_skin10:
        print(binary_decode_multi(entry))
