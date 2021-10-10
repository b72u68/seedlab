from subprocess import check_output

from binascii import unhexlify

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

# read english words from file and store them in an arraylist
f = open("english_word_list.txt")
english_words = f.readlines()
english_words = [x.strip("\n") for x in english_words]
f.close()

# add padding to words so their size is 128 bits
english_words_padding = []

for w in english_words:
    wb = w.encode('utf-8')
    if len(wb)*8 < 128:
        english_words_padding.append(w + "#"*(128//8 - len(wb)))

# to make sure it works right, loop through the list and test if the words are
# 128 bits
for w in english_words_padding:
    if len(w.encode('utf-8'))*8 != 128:
        raise Exception("Key size is too small (less than 128 bits)!!!")

# bruteforce: try every key to see if the result matches the given ciphertext
plaintext = "This is a secret tool"
iv = "010203040506070809000a0b0c0d0e0f"
ciphertext = "ece6753e938f8f903cabbbe12d395bf5f7eae38ad918a2d3e1c3a832476d5c7a"


# in this function, I used openssl to get the key for to compare with the result
# of encryption without using openssl
def enc_openssl(plaintext: str, key: str, iv: str) -> bytes:

    encrypted = check_output(['echo', '-n', plaintext, '|', 'openssl', 'enc',
                              '-aes-128-cbc', '-e', '-K', key, '-iv', iv])

    return encrypted


# encrypt message using aes-128-cbc with pycrypto and pycryptodome library
def enc(plaintext: str, key: str, iv: str) -> bytes:

    key = unhexlify(key)
    iv = unhexlify(iv)

    # initialize the cipher type and mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # encrypt the message using the cipher type and mode declared above.
    # also add padding to the plaintext in case the size of blocks of message
    # from plaintext is smaller than 128 bits.
    encrypted = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))

    return encrypted


# decrypt ciphertext using aes-128-cbc with pycrypto and pycryptodome library
def dec(ciphertext: str, key: str, iv: str) -> bytes:

    ciphertext = unhexlify(ciphertext)
    key = unhexlify(key)
    iv = unhexlify(iv)

    # initialize the cipher type and mode
    decipher = AES.new(key, AES.MODE_CBC, iv)

    # decrypt the ciphertext using the cipher type and mode declared above.
    decrypted = decipher.decrypt(ciphertext)

    # check if the decrypted message has padding. If yes, remove the padding and
    # return the unpadded plaintext. Else, return the decrypted message.
    try:
        decrypted = unpad(decrypted, AES.block_size)
    except Exception:
        pass

    return decrypted


if __name__ == "__main__":

    # bruteforce: go through every possible key and encrypt the plaintext.
    # compare the result with the given ciphertext.
    for k in english_words_padding:
        key = k.encode('utf-8').hex()
        encrypted = enc(plaintext, key, iv)

        if encrypted.hex() == ciphertext:
            print(k)
            print("(ENC) The encryption key is:", k.strip("#"))
            break

    # bruteforce: go through every possible key and decrypt the ciphertext.
    # compare the result with the given plaintext.
    for k in english_words_padding:
        key = k.encode('utf-8').hex()
        decrypted = dec(ciphertext, key, iv)

        if decrypted == plaintext.encode('utf-8'):
            print("(DEC) The encryption key is:", k.strip("#"))
            break
