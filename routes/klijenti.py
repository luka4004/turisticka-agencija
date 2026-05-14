from flask import Blueprint, request, jsonify
from extensions import db
from models import Klijent

klijenti_bp = Blueprint("klijenti", __name__)


def klijent_to_dict(klijent):
    return {
        "id": klijent.id,
        "ime": klijent.ime,
        "prezime": klijent.prezime,
        "email": klijent.email,
        "telefon": klijent.telefon,
    }


@klijenti_bp.route("/klijenti", methods=["GET"])
def get_klijenti():
    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    query = Klijent.query

    if search:
        query = query.filter(
            (Klijent.ime.like(f"%{search}%")) |
            (Klijent.prezime.like(f"%{search}%")) |
            (Klijent.email.like(f"%{search}%"))
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": [klijent_to_dict(k) for k in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages
    })


@klijenti_bp.route("/klijenti/<int:id>", methods=["GET"])
def get_klijent(id):
    klijent = Klijent.query.get_or_404(id)
    return jsonify(klijent_to_dict(klijent))


@klijenti_bp.route("/klijenti", methods=["POST"])
def create_klijent():
    data = request.get_json()

    novi_klijent = Klijent(
        ime=data["ime"],
        prezime=data["prezime"],
        email=data["email"],
        telefon=data.get("telefon"),
    )

    db.session.add(novi_klijent)
    db.session.commit()

    return jsonify(klijent_to_dict(novi_klijent)), 201


@klijenti_bp.route("/klijenti/<int:id>", methods=["PUT"])
def update_klijent(id):
    klijent = Klijent.query.get_or_404(id)
    data = request.get_json()

    klijent.ime = data["ime"]
    klijent.prezime = data["prezime"]
    klijent.email = data["email"]
    klijent.telefon = data.get("telefon")

    db.session.commit()

    return jsonify(klijent_to_dict(klijent))


@klijenti_bp.route("/klijenti/<int:id>", methods=["DELETE"])
def delete_klijent(id):
    klijent = Klijent.query.get_or_404(id)

    db.session.delete(klijent)
    db.session.commit()

    return jsonify({"message": "Klijent obrisan"})