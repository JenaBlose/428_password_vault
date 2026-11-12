import re
from datetime import datetime

def normalize_number(number: str) -> str:
    return re.sub(r"\s+", "", number)

def detect_card_type(number: str) -> str:
    n = normalize_number(number)

    if n.startswith("4") and len(n) in (13, 16):
        return "Visa"

    if len(n) == 15 and n[:2] in ("34", "37"):
        return "American Express"

    if len(n) == 16 and (51 <= int(n[:2]) <= 55 or 2221 <= int(n[:4]) <= 2720):
        return "Mastercard"

    if len(n) == 16 and (n.startswith("6011") or n.startswith("65")):
        return "Discover"

    return "Unknown"

def luhn_check(number: str) -> bool:
    n = normalize_number(number)
    if not n.isdigit():
        return False

    digits = [int(d) for d in n]
    checksum = 0
    double = False

    for d in reversed(digits):
        if double:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
        double = not double

    return checksum % 10 == 0

def parse_expiration(exp: str):
    exp = exp.strip()

    if "/" not in exp:
        return None, None

    m, y = exp.split("/")
    month = int(m)

    if len(y) == 2:
        year = 2000 + int(y)
    else:
        year = int(y)

    return month, year

def validate_expiration(exp: str) -> bool:
    month, year = parse_expiration(exp)

    if not month or not year:
        return False

    if month < 1 or month > 12:
        return False

    now = datetime.now()

    if year < now.year:
        return False

    if year == now.year and month < now.month:
        return False

    return True

def validate_cvc(card_type: str, cvc: str) -> bool:
    if not cvc.isdigit():
        return False

    if card_type == "American Express":
        return len(cvc) == 4

    return len(cvc) == 3