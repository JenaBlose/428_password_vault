import json
from cryptography.fernet import Fernet

KEY_FILE = "vault.key"
DATA_FILE = "vault.json"


def load_key():
    try:
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key


key = load_key()
cipher = Fernet(key)


def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as data_file:
            return json.load(data_file)
    except FileNotFoundError:
        return []


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as data_file:
        json.dump(data, data_file, indent=2)


def save_entry(site, username, password):
    data = load_data()

    encrypted = cipher.encrypt(password.encode()).decode()
    
    data.append({
        "type": "password",
        "site": site,
        "username": username,
        "password": encrypted
    })
    
    save_data(data)


def get_entries():
    data = load_data()
    entries = []

    for entry in data:
        if entry.get("type") == "password":
            entry["password"] = cipher.decrypt(
                entry["password"].encode()
            ).decode()
        
            entries.append(entry)
    
    return entries


def save_card(name, number, exp, cvc, card_type):
    data = load_data()

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

    save_data(data)


def get_cards():
    data = load_data()
    cards = []

    for entry in data:
        if entry.get("type") == "card":
            entry["number"] = cipher.decrypt(
                entry["number"].encode()
            ).decode()
            
            entry["cvc"] = cipher.decrypt(
                entry["cvc"].encode()
            ).decode()
            
            cards.append(entry)

    return cards
