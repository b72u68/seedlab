from binascii import unhexlify

# initialize p1, c1, c2
p1 = "This is a known message!"
c1 = "a469b1c502c1cab966965e50425438e1bb1b5f9037a4c15913"
c2 = "bf73bcd3509299d566c35b5d450337e1bb175f903fafc15913"

# extract the given p1, c1, c2 to array of bytes
p1 = list(p1.encode('utf-8'))
c1 = list(unhexlify(c1))
c2 = list(unhexlify(c2))

# perform each byte of p1, c1, c2, decode the byte and join it to find p2
p2 = bytes([p1[i] ^ c1[i] ^ c2[i] for i in range(len(p1))]).decode('utf-8')

print(p2)
