import base64
from base64 import b64decode


def dec():
    with open("b64.txt") as f:
        data = f.read()
        for x in range(50):
            base64_bytes = data.encode("ascii") #
            string_bytes = base64.b64decode(base64_bytes)
            string = string_bytes.decode("ascii")
            data = string # Update data for next iteration

    print(string)

if __name__ == "__main__":
    dec()