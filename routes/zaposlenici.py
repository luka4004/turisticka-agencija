from flask import Blueprint, request, jsonify
from extensions import db
from models import Zaposlenik

zaposlenici_bp = Blueprint("zaposlenici", __name__)


def zaposlenik_to_dict(zaposlenik):
    return {
        "id": zaposlenik.id,
        "ime": zaposlenik.ime,
        "prezime": zaposlenik.prezime,
        "email": zaposlenik.email,
        "pozicija": zaposlenik.pozicija,
    }


@zaposlenici_bp.route("/zaposlenici", methods=["GET"])
def get_zaposlenici():
    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    query = Zaposlenik.query

    if search:
        query = query.filter(
            (Zaposlenik.ime.like(f"%{search}%")) |
            (Zaposlenik.prezime.like(f"%{search}%")) |
            (Zaposlenik.email.like(f"%{search}%")) |
            (Zaposlenik.pozicija.like(f"%{search}%"))
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": [zaposlenik_to_dict(z) for z in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages
    })


@zaposlenici_bp.route("/zaposlenici/<int:id>", methods=["GET"])
def get_zaposlenik(id):
    zaposlenik = Zaposlenik.query.get_or_404(id)
    return jsonify(zaposlenik_to_dict(zaposlenik))


@zaposlenici_bp.route("/zaposlenici", methods=["POST"])
def create_zaposlenik():
    data = request.get_json()

    novi_zaposlenik = Zaposlenik(
        ime=data["ime"],
        prezime=data["prezime"],
        email=data["email"],
        pozicija=data["pozicija"],
    )

    db.session.add(novi_zaposlenik)
    db.session.commit()

    return jsonify(zaposlenik_to_dict(novi_zaposlenik)), 201


@zaposlenici_bp.route("/zaposlenici/<int:id>", methods=["PUT"])
def update_zaposlenik(id):
    zaposlenik = Zaposlenik.query.get_or_404(id)
    data = request.get_json()

    zaposlenik.ime = data["ime"]
    zaposlenik.prezime = data["prezime"]
    zaposlenik.email = data["email"]
    zaposlenik.pozicija = data["pozicija"]

    db.session.commit()

    return jsonify(zaposlenik_to_dict(zaposlenik))


@zaposlenici_bp.route("/zaposlenici/<int:id>", methods=["DELETE"])
def delete_zaposlenik(id):
    zaposlenik = Zaposlenik.query.get_or_404(id)

    db.session.delete(zaposlenik)
    db.session.commit()

    return jsonify({"message": "Zaposlenik obrisan"})