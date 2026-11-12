import os

INPUT_FILE = "dictionary.txt"
OUTPUT_FILE = "dictionary2.txt"

MIN_LEN = 6
MAX_LEN = 10

def build_dictionary():

    words = set()

    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:

            word = line.strip().lower()

            if word.isalpha() and MIN_LEN <= len(word) <= MAX_LEN:
                words.add(word)

    words = sorted(words)

    with open(OUTPUT_FILE, "w") as out:
        for w in words:
            out.write(w + "\n")

    print("Generated dictionary2.txt")
    print("Word count:", len(words))


if __name__ == "__main__":
    build_dictionary()