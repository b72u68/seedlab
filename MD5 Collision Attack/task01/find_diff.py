with open("data1", "rb") as f:
    hex1 = f.read()

with open("data2", "rb") as f:
    hex2 = f.read()

for i in range(len(hex1)):
    if hex1[i] != hex2[i]:
        print(f'Diff hex value at position {hex(i)} in data1 and data2: {hex(hex1[i])} {hex(hex2[i])}')
