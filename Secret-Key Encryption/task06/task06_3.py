from binascii import unhexlify

# guess that the original plaintext is "Yes"
p1 = "Yes"
iv = "31323334353637383930313233343536"
iv_next = "31323334353637383930313233343537"

# convert string to hexadecimal and split them into block of 1 byte
p1 = list(p1.encode('utf-8'))
iv = list(unhexlify(iv))
iv_next = list(unhexlify(iv_next))

# check if plaintext can be split into 128bit-block. If not, add padding to
# the plaintext before encryption
padding = 16 - len(p1) % 16
p1 += [padding] * padding

# calculate p2
p2 = bytes([p1[x] ^ iv[x] ^ iv_next[x] for x in range(len(p1))]).decode("utf-8")
print(p2)
