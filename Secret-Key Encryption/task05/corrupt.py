import sys

from subprocess import check_output


# corrupt one bit in given position of 55th byte of ciphertext
def corrupt(ciphertext: bytes, position: int) -> bytes:

    # split the ciphertext into list of decimal numbers converted from the bytes
    # of the ciphertext
    ciphertext_bytes = list(ciphertext)

    # get the 55th byte
    target_byte = ciphertext_bytes[54]

    # flip the bit at the given position
    new_byte = target_byte ^ (1 << position)

    # change the 55th byte in the ciphertext to the new byte
    ciphertext_bytes[54] = new_byte

    return bytes(ciphertext_bytes)


if __name__ == "__main__":

    if len(sys.argv) == 2:
        try:
            filename = sys.argv[1]

            # read bytes of ciphertext from given filename
            ciphertext = check_output(['cat', filename])

            # corrupt the first bit of 55th byte in the ciphertext
            corrupted_ciphertext_bytes = corrupt(ciphertext, 0)

            # write the result bytes into a file
            f_corrupt = open(f'corrupted_{filename}', 'wb')
            f_corrupt.write(corrupted_ciphertext_bytes)
            f_corrupt.close()

        except FileNotFoundError:
            print("Cannot open file.")
    else:
        print("Please provide a filename.")
