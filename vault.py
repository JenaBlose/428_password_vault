import json
from cryptography.fernet import Fernet

KEY_FILE = "vault.key"
DATA_FILE = "vault.json"


def load_key():

    try:
        return open(KEY_FILE,"rb").read()

    except:
        key = Fernet.generate_key()
        open(KEY_FILE,"wb").write(key)
        return key


key = load_key()
cipher = Fernet(key)


def save_entry(site, username, password):

    try:
        data = json.load(open(DATA_FILE))
    except:
        data = []

    encrypted = cipher.encrypt(password.encode()).decode()

    data.append({
    "type": "password",
    "site": site,
    "username": username,
    "password": encrypted
    })

    json.dump(data, open(DATA_FILE,"w"), indent=2)


def get_entries():

    try:
        data = json.load(open(DATA_FILE))
    except:
        return []

    entries = []

    for entry in data:

        # only process password entries
        if entry.get("type") == "password":

            entry["password"] = cipher.decrypt(
                entry["password"].encode()
            ).decode()

            entries.append(entry)

    return entries

def save_card(name, number, exp, cvc, card_type):

    try:
        data = json.load(open(DATA_FILE))
    except:
        data = []

    enc_number = cipher.encrypt(number.encode()).decode()
    enc_cvc = cipher.encrypt(cvc.encode()).decode()

    data.append({
        "type": "card",
        "name": name,
        "brand": card_type,
        "number": enc_number,
        "exp": exp,
        "cvc": enc_cvc
    })

    json.dump(data, open(DATA_FILE, "w"), indent=2)


def get_cards():

    try:
        data = json.load(open(DATA_FILE))
    except:
        return []

    cards = []

    for entry in data:
        if entry.get("type") == "card":

            entry["number"] = cipher.decrypt(entry["number"].encode()).decode()
            entry["cvc"] = cipher.decrypt(entry["cvc"].encode()).decode()

            cards.append(entry)

    return cards