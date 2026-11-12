import secrets
import string
import random

AMBIGUOUS = {"0","O","o","1","l","I"}


def build_charsets(use_upper, use_lower, use_digits, use_symbols, avoid_ambiguous):

    charsets = []

    if use_upper:
        upper = string.ascii_uppercase
        if avoid_ambiguous:
            upper = "".join(c for c in upper if c not in AMBIGUOUS)
        charsets.append(upper)

    if use_lower:
        lower = string.ascii_lowercase
        if avoid_ambiguous:
            lower = "".join(c for c in lower if c not in AMBIGUOUS)
        charsets.append(lower)

    if use_digits:
        digits = string.digits
        if avoid_ambiguous:
            digits = "".join(c for c in digits if c not in AMBIGUOUS)
        charsets.append(digits)

    if use_symbols:
        symbols = "!@#$%^&*()-_=+[]{};:,.<>?"
        charsets.append(symbols)

    return charsets


def generate_password(length, use_upper, use_lower, use_digits, use_symbols, avoid_ambiguous):

    charsets = build_charsets(
        use_upper,
        use_lower,
        use_digits,
        use_symbols,
        avoid_ambiguous
    )

    if not charsets:
        raise ValueError("Select at least one character type")

    # guarantee one character from each selected set
    password_chars = [secrets.choice(cs) for cs in charsets]

    # build combined charset
    all_chars = "".join(charsets)

    remaining = length - len(password_chars)

    if remaining > 0:
        password_chars += [secrets.choice(all_chars) for _ in range(remaining)]

    random.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)


# -------------------------------------------------
# PASSPHRASE GENERATOR
# -------------------------------------------------

WORDS = []

def load_words(path="dictionary2.txt"):

    words = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:
                    words.append(word)

    except FileNotFoundError:
        pass

    return words


WORDS = load_words()


def apply_digit_substitution(word):

    replacements = {
        "a":"4",
        "e":"3",
        "i":"1",
        "o":"0",
        "s":"5"
    }

    for k, v in replacements.items():
        word = word.replace(k, v)

    return word


def generate_passphrase(word_count, separator, caps, digits):

    words = [secrets.choice(WORDS) for _ in range(word_count)]

    if caps:
        words = [w.capitalize() for w in words]

    if digits:
        words = [apply_digit_substitution(w) for w in words]

    phrase = separator.join(words)

    return phrase