# Password Generator and Secure Vault

## Overview

This project implements a secure password generation and storage system inspired by modern password managers such as NordPass. The system allows users to generate strong passwords or passphrases, evaluate password strength, securely store credentials, and manage credit card information. The application is built using a Python backend with Flask and a web-based interface written in HTML, CSS, and JavaScript.

The tool supports both traditional character-based passwords and passphrase-based passwords composed of multiple dictionary words. Passwords can be stored in an encrypted vault and retrieved through the interface for autofill demonstrations.

---

## Features

### Password Generation

* Configurable password length (8–64 characters)
* Options for:

  * Uppercase letters
  * Lowercase letters
  * Numbers
  * Symbols
  * Avoid ambiguous characters (e.g., 0, O, l, 1)

### Passphrase Generation

* Generate passwords from multiple dictionary words
* Adjustable number of words
* Custom separator options:

  * hyphen
  * underscore
  * comma
  * period
  * space
* Optional capitalization
* Optional digit substitution

### Password Strength Evaluation

* Entropy-based evaluation
* Rule-based scoring similar to NordPass
* Strength categories:

  * Weak
  * Moderate
  * Strong

### Secure Password Vault

* Stores credentials in encrypted form
* Uses **Fernet symmetric encryption**
* Supports:

  * saving passwords
  * retrieving stored credentials
  * autofill demonstration
  * copying stored passwords

### Credit Card Storage

* Validates card numbers using the **Luhn algorithm**
* Detects card type (Visa, Mastercard, AmEx, Discover)
* Validates:

  * card number
  * expiration date
  * CVC format
* Stores card data encrypted
* Displays masked card numbers

---

## Project Structure

```
project/
│
├── api_server.py
├── password_generator.py
├── password_core.py
├── vault.py
├── card_utils.py
├── generator.html
├── password_gui.py
│
├── dictionary.txt
├── dictionary2.txt
│
├── build_passphrase_dictionary.py
├── filter_dictionary.py
│
├── vault.json
└── vault.key
```

---

## Installation

Install required Python dependencies:

```
pip install flask flask-cors cryptography
```

---

## Running the Server

Start the Flask backend:

```
python api_server.py
```

The server runs on:

```
http://127.0.0.1:5000
```

---

## Running the Interface

Open the file:

```
generator.html
```

in a web browser.

The interface communicates with the Flask backend through API calls.

---

## Security Design

Sensitive information such as passwords and credit card numbers are encrypted before storage using **Fernet encryption** from the `cryptography` library. The encryption key is stored locally in `vault.key`. Stored entries are saved in `vault.json`.

This ensures stored secrets are not readable without the encryption key.

---

## API Endpoints

| Endpoint   | Method | Description                     |
| ---------- | ------ | ------------------------------- |
| /generate  | POST   | Generate password or passphrase |
| /save      | POST   | Save credential                 |
| /vault     | GET    | Retrieve stored passwords       |
| /save_card | POST   | Save credit card                |
| /cards     | GET    | Retrieve stored cards           |

---

## Educational Purpose

This project demonstrates:

* password entropy calculation
* secure random generation
* encryption of stored credentials
* input validation
* password manager design principles
* web + backend integration

---


