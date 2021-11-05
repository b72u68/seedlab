from subprocess import run

with open("a.out", "rb") as f:
    BYTE_STREAM = f.read()
f.close()


# get the starting and ending position of X and Y in the byte stream
def get_X_Y_location(byte_stream):
    start_end = []
    for i in range(len(byte_stream)):
        if byte_stream[i] == 0x41:
            start = i
            end = i
            while end < len(byte_stream) and byte_stream[end] == 0x41:
                end += 1
            end -= 1
            if end - start + 1 == 200:
                start_end.append((start, end))
    return start_end


# get the offset of the array in the byte stream
def get_array_offset(start: int) -> int:
    return 64 - start % 64


# get the prefix size
def get_prefix_size(start: int, offset: int) -> int:
    return start + offset


# get the suffix size
def get_suffix_size(byte_stream_size: int, prefix_size: int) -> int:
    return byte_stream_size - 128 - prefix_size


# clean file in the current directory
def clean():
    run('rm -rf prefix* suffix* P Q', shell=True)


if __name__ == "__main__":

    start_end = get_X_Y_location(BYTE_STREAM)

    s1, e1 = start_end[0]
    s2, e2 = start_end[1]

    offset = get_array_offset(s1)
    prefix_size = get_prefix_size(s1, offset)
    suffix_size = get_suffix_size(len(BYTE_STREAM), prefix_size)

    # get the prefix and the suffix of the executable file
    run(f'head -c {prefix_size} a.out > prefix', shell=True)
    run(f'tail -c {suffix_size} a.out > suffix', shell=True)

    # generate two files with the same md5 using prefix as prefixfile
    print("\n+ Generate prefix_P and prefix_Q")
    run('md5collgen -p prefix -o prefix_P prefix_Q', shell=True)

    # get P and Q (the 128 bytes generate by md5collgen) from prefix_P and prefix_Q
    run('tail -c 128 prefix_P > P', shell=True)
    run('tail -c 128 prefix_Q > Q', shell=True)

    # get the starting position of Y with offset relative to starting position
    # of suffix
    # get the end position of 128 bytes from the starting position of Y with
    # offset
    s2_P = s2 - 128 - prefix_size + offset
    e2_P = s2_P + 128

    # insert P in the middle of array Y in the suffix
    run(f'head -c {s2_P} suffix > suffix_pre', shell=True)
    run(f'tail -c +{e2_P} suffix > suffix_post', shell=True)
    run('cat suffix_pre P suffix_post > suffix_P', shell=True)

    # concat prefix_p and prefix_Q with suffix_P to create two new executable
    # files a1.out and a2.out with the same md5 hash
    run('cat prefix_P suffix_P > a1.out', shell=True)
    run('cat prefix_Q suffix_P > a2.out', shell=True)

    # compare md5 hash of a1.out and a2.out
    print("\n+ Compare a1.out and a2.out md5 hash")
    run('md5sum a1.out a2.out', shell=True)

    # execute a1.out and a2.out
    print("\n+ Result of program a1.out")
    run('./a1.out')

    print("\n+ Result of program a2.out")
    run('./a2.out')

    clean()
