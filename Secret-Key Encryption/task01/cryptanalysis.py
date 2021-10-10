import re


def process_text(text) -> str:
    return re.sub('[^A-Za-z0-9 ]+', '', text.replace("\n", " ")).strip()


def sort_frequency(d) -> list:
    return sorted(d, key=lambda x: -d[x])


def count_letters(text) -> dict:
    d = {}

    for c in text:
        if c.isalpha():
            d.setdefault(c, 0)
            d[c] += 1

    return d


def count_words(words, n) -> dict:
    d = {}
    for w in words:
        if len(w) == n:
            d.setdefault(w, 0)
            d[w] += 1
    return d


def count_initial(words) -> dict:
    d = {}

    for w in words:
        d.setdefault(w[0], 0)
        d[w[0]] += 1

    return d


def count_final(words) -> dict:
    d = {}

    for w in words:
        d.setdefault(w[-1], 0)
        d[w[-1]] += 1

    return d


def count_doubled(words) -> dict:
    d = {}

    for w in words:
        for i in range(len(w)-1):
            if w[i] == w[i+1]:
                d.setdefault(w[i], 0)
                d[w[i]] += 1

    return d


if __name__ == "__main__":
    f = open("./ciphertext.txt")

    text = process_text(f.read())
    words = text.split(" ")

    letter_freq = count_letters(text)
    doubled_freq = count_doubled(words)
    one_letter_words = count_words(words, 1)
    two_letter_words = count_words(words, 2)
    three_letter_words = count_words(words, 3)
    initial_freq = count_initial(words)
    final_freq = count_final(words)

    print(letter_freq)
    print(sort_frequency(letter_freq))
    print(sort_frequency(doubled_freq))
    print(sort_frequency(one_letter_words))
    print(sort_frequency(two_letter_words))
    print(sort_frequency(three_letter_words))
    print(sort_frequency(initial_freq))
    print(sort_frequency(final_freq))

    f.close()
