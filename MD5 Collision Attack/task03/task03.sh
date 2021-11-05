#!/bin/sh

# get prefix and suffix file using the given sizes
get_prefix_and_suffix() {
    PREFIX_SIZE=$1
    SUFFIX_SIZE=$2

    echo "prefix size: ${PREFIX_SIZE}, suffix size: ${SUFFIX_SIZE}"
    head -c $PREFIX_SIZE a.out > prefix
    tail -c $SUFFIX_SIZE a.out > suffix
}

# compile and create executable file for the given C program
gcc array.c

# get prefix and suffix from the result size of prefix_suffix_size program
echo "+ Get prefix and suffix size"
get_prefix_and_suffix $(python3 prefix_suffix_size.py)

# generate P and Q with the same md5 hash
echo "\n+ Generating P and Q using prefix as prefixfile"
md5collgen -p prefix -o P Q

# create new executable files a1.out and a2.out using the new generated prefix
# P and Q
cat P suffix > a1.out
cat Q suffix > a2.out

echo "\n+ Check a1.out and a2.out md5 hash"
md5sum a1.out a2.out

echo "\n+ Compare a1.out and a2.out"
diff a1.out a2.out

echo "\n+ Execute a1.out"
./a1.out > array1
cat array1

echo "\n+ Execute a2.out"
./a2.out > array2
cat array2

echo "\n+ Compare the array in a1.out and a2.out"
diff -q array1 array2
