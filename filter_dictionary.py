import os

def load_dictionary_words(path: str = "dictionary.txt") -> list:
    """Load lowercase words from a dictionary file, one word per line."""
    if not os.path.exists(path):
        return list()

    words = list()
    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            word = line.strip().lower()
            if word:
                words.append(word + "\n")
    return words
def write_dictionary_words(d:list, path: str = "dictionary.txt"):
    """Load lowercase words from a dictionary file, one word per line."""
    if not os.path.exists(path):
        return

    with open(path, "w", encoding="utf-8", errors="ignore") as handle:
        handle.flush()
        handle.writelines(d)
        handle.close()

d = load_dictionary_words()
for word in d:
    if len(word) < 5:
        d.remove(word)
write_dictionary_words(d)
