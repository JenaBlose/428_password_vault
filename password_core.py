import secrets
import string
import random
import math
from dataclasses import dataclass

AMBIGUOUS = {"0","O","o","1","l","I"}


# -------------------------------------------------
# PASSWORD GENERATOR
# -------------------------------------------------

def load_dictionary_words(path):

    words = set()

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    words.add(word)

    except FileNotFoundError:
        pass

    return words

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

    password_chars = [secrets.choice(cs) for cs in charsets]

    all_chars = "".join(charsets)

    remaining = length - len(password_chars)

    if remaining > 0:
        password_chars += [secrets.choice(all_chars) for _ in range(remaining)]

    random.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)


# -------------------------------------------------
# PASSPHRASE GENERATOR
# -------------------------------------------------

def load_words(path="dictionary2.txt"):

    words = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                w = line.strip()
                if w:
                    words.append(w)

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


# -------------------------------------------------
# RESULT STRUCTURE
# -------------------------------------------------

@dataclass
class PasswordResult:
    score: int
    label: str
    color: str
    entropy: float
    feedback: list


# -------------------------------------------------
# CHARSET DETECTION
# -------------------------------------------------

def detect_charset(password):

    charset = 0
    options_used = 0

    if any(c.islower() for c in password):
        charset += 26
        options_used += 1

    if any(c.isupper() for c in password):
        charset += 26
        options_used += 1

    if any(c.isdigit() for c in password):
        charset += 10
        options_used += 1

    if any(c in string.punctuation for c in password):
        charset += 32
        options_used += 1

    return charset, options_used


# -------------------------------------------------
# ENTROPY
# -------------------------------------------------

def calculate_entropy(password):

    charset, _ = detect_charset(password)

    if charset == 0:
        return 0

    return len(password) * math.log2(charset)


def calculate_passphrase_entropy(word_count, dictionary_size):

    if dictionary_size == 0:
        return 0

    return word_count * math.log2(dictionary_size)


# -------------------------------------------------
# PASSPHRASE DETECTION
# -------------------------------------------------

def is_passphrase(password):

    separators = ["-", "_", ".", ",", " "]

    return any(sep in password for sep in separators)


def split_passphrase(password):

    separators = ["-", "_", ".", ",", " "]

    for sep in separators:
        if sep in password:
            return password.split(sep)

    return [password]


# -------------------------------------------------
# PASSWORD RULES (NordPass style)
# -------------------------------------------------

def evaluate_password_rules(password):

    length = len(password)

    _, options_used = detect_charset(password)

    if 8 <= length <= 10:

        if options_used >= 2:
            return 5, "Moderate", "gold"

        return 3, "Weak", "orange"

    if 11 <= length <= 19:

        if options_used >= 2:
            return 8, "Strong", "green"

        return 5, "Moderate", "gold"

    if 20 <= length <= 64:
        return 8, "Strong", "green"

    return 1, "Very Weak", "red"


# -------------------------------------------------
# PASSPHRASE RULES
# -------------------------------------------------

def evaluate_passphrase_rules(password):

    words = split_passphrase(password)
    word_count = len(words)

    has_option = (
        any(c.isupper() for c in password)
        or any(c.isdigit() for c in password)
    )

    if word_count == 3:

        if has_option:
            return 8, "Strong", "green"

        return 5, "Moderate", "gold"

    if word_count > 3:
        return 8, "Strong", "green"

    return 3, "Weak", "orange"


# -------------------------------------------------
# FEEDBACK
# -------------------------------------------------

def generate_feedback(password, is_phrase):

    feedback = []

    if is_phrase:

        words = split_passphrase(password)

        if len(words) < 4:
            feedback.append("Use more words for stronger passphrases")

    else:

        if len(password) < 12:
            feedback.append("Longer passwords are more secure")

        if not any(c.isdigit() for c in password):
            feedback.append("Adding numbers improves strength")

        if not any(c in string.punctuation for c in password):
            feedback.append("Adding special characters improves strength")

    return feedback


# -------------------------------------------------
# MAIN EVALUATION
# -------------------------------------------------

def evaluate_password(password, dictionary_words, mode="characters"):

    if not password:
        return PasswordResult(0, "N/A", "gray", 0, [])

    phrase = (mode == "words")

    if phrase:

        words = split_passphrase(password)

        entropy = calculate_passphrase_entropy(
            len(words),
            max(len(dictionary_words), 1)
        )

        score, label, color = evaluate_passphrase_rules(password)

    else:

        entropy = calculate_entropy(password)

        score, label, color = evaluate_password_rules(password)

    feedback = generate_feedback(password, phrase)

    return PasswordResult(score, label, color, entropy, feedback)