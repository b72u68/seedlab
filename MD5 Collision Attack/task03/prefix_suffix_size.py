with open("a.out", "rb") as f:
    byte_stream = f.read()
f.close()


# find the start and end byte block of the xyz array that contains 200 A's
def find_A_range():
    start, end = 0, 0
    for i in range(len(byte_stream)):
        if byte_stream[i] == 0x41:
            start = i
            end = i

            while end < len(byte_stream) and byte_stream[end] == 0x41:
                end += 1

            end -= 1

            if end - start + 1 == 200:
                break

    return (start, end)


# get the size of prefix
def get_prefix_size(start: int) -> int:
    return start + (64 - start % 64)


# get the size of prefix
def get_suffix_size(prefix_size: int) -> int:
    return len(byte_stream) - prefix_size - 128


if __name__ == "__main__":
    start, _ = find_A_range()
    prefix_size = get_prefix_size(start)
    suffix_size = get_suffix_size(prefix_size)

    print(prefix_size, suffix_size)
