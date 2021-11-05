#!/bin/sh


generate_md5() {
    echo -n $(python3 generate_string.py $1) > prefix.txt
    echo "+ prefix.txt content: $(cat prefix.txt)"
    echo "+ Size of prefix.txt: $(wc -c < prefix.txt) bytes"

    echo "\n+ Running md5collgen"
    md5collgen -p prefix.txt -o out1.bin out2.bin --quiet

    echo
    echo "+ Size of out1.bin: $(wc -c < out1.bin) bytes"
    echo "+ Size of out2.bin: $(wc -c < out2.bin) bytes"

    echo "\n+ Check diff out1.bin out2.bin"
    diff out1.bin out2.bin -q

    echo "\n+ View md5sum out1.bin and out2.bin"
    md5sum out1.bin
    md5sum out2.bin

    echo "\n+ Compare out1.bin and out2.bin hex"
    echo "out1.bin"
    hexdump out1.bin
    echo "\nout2.bin"
    hexdump out2.bin
}

question_1() {
    echo "\nQuestion 1"
    generate_md5 69
}

question_2() {
    echo "\nQuestion 2"
    generate_md5 64
}

question_3() {
    echo "\nQuestion 3"
    tail -c 128 out1.bin > data1
    tail -c 128 out2.bin > data2
    diff data1 data2 -q
}

question_1

question_2

question_3
