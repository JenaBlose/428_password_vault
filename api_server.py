from flask import Flask, request, jsonify
from flask_cors import CORS

from card_utils import detect_card_type, luhn_check, validate_expiration, validate_cvc
from vault import save_card, get_cards

from password_generator import generate_password, generate_passphrase
from password_core import evaluate_password, load_dictionary_words
from vault import save_entry, get_entries

app = Flask(__name__)
CORS(app)

dictionary = load_dictionary_words("dictionary2.txt")


@app.route("/generate", methods=["POST"])
def generate():

    data = request.json
    mode = data["mode"]

    if mode == "characters":

        password = generate_password(
            data["length"],
            data["upper"],
            data["lower"],
            data["numbers"],
            data["symbols"],
            data["avoid_ambiguous"]
        )

    else:

        password = generate_passphrase(
            data["words"],
            data["separator"],
            data["caps"],
            data["digits"]
        )

    result = evaluate_password(password, dictionary, mode)

    return jsonify({
        "password": password,
        "entropy": result.entropy,
        "strength": result.label,
        "color": result.color
    })


@app.route("/save", methods=["POST"])
def save():

    data = request.json

    save_entry(
        data["site"],
        data["username"],
        data["password"]
    )

    return jsonify({"status":"saved"})

@app.route("/save_card", methods=["POST"])
def save_card_api():

    data = request.json

    number = data["number"]
    exp = data["exp"]
    cvc = data["cvc"]
    name = data["name"]

    card_type = detect_card_type(number)

    if card_type == "Unknown":
        return jsonify({"error":"Unknown card type"}), 400

    if not luhn_check(number):
        return jsonify({"error":"Invalid card number"}), 400

    if not validate_expiration(exp):
        return jsonify({"error":"Invalid expiration date"}), 400

    if not validate_cvc(card_type, cvc):
        return jsonify({"error":"Invalid CVC"}), 400

    save_card(name, number, exp, cvc, card_type)

    return jsonify({"status":"saved"})

@app.route("/cards", methods=["GET"])
def cards():
    return jsonify(get_cards())


@app.route("/vault", methods=["GET"])
def vault():

    return jsonify(get_entries())


if __name__ == "__main__":
    app.run(port=5000)