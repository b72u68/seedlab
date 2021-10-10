#!/bin/bash

openssl enc -aes-128-ecb -e -in plaintext.txt -out ecb.bin \
    -K 00010203040506070809aabbccddeeff
openssl enc -aes-128-cbc -e -in plaintext.txt -out cbc.bin \
    -K 00010203040506070809aabbccddeeff \
    -iv 0a0b0c0d0e0f00010203040506070809
openssl enc -aes-128-cfb -e -in plaintext.txt -out cfb.bin \
    -K 00010203040506070809aabbccddeeff \
    -iv 0a0b0c0d0e0f00010203040506070809
openssl enc -aes-128-ofb -e -in plaintext.txt -out ofb.bin \
    -K 00010203040506070809aabbccddeeff \
    -iv 0a0b0c0d0e0f00010203040506070809

python3 corrupt.py ecb.bin
python3 corrupt.py cbc.bin
python3 corrupt.py cfb.bin
python3 corrupt.py ofb.bin

openssl enc -aes-128-ecb -d -in corrupted_ecb.bin -out p_ecb.bin \
    -K 00010203040506070809aabbccddeeff
openssl enc -aes-128-cbc -d -in corrupted_cbc.bin -out p_cbc.bin \
    -K 00010203040506070809aabbccddeeff \
    -iv 0a0b0c0d0e0f00010203040506070809
openssl enc -aes-128-cfb -d -in corrupted_cfb.bin -out p_cfb.bin \
    -K 00010203040506070809aabbccddeeff \
    -iv 0a0b0c0d0e0f00010203040506070809
openssl enc -aes-128-ofb -d -in corrupted_ofb.bin -out p_ofb.bin \
    -K 00010203040506070809aabbccddeeff \
    -iv 0a0b0c0d0e0f00010203040506070809
