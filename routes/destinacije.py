from flask import Blueprint, request, jsonify
from extensions import db
from models import Destinacija

destinacije_bp = Blueprint("destinacije", __name__)


def destinacija_to_dict(destinacija):
    return {
        "id": destinacija.id,
        "naziv": destinacija.naziv,
        "drzava": destinacija.drzava,
        "grad": destinacija.grad,
        "opis": destinacija.opis,
        "cijena": destinacija.cijena,
    }


@destinacije_bp.route("/destinacije", methods=["GET"])
def get_destinacije():
    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    query = Destinacija.query

    if search:
        query = query.filter(
            (Destinacija.naziv.like(f"%{search}%")) |
            (Destinacija.drzava.like(f"%{search}%")) |
            (Destinacija.grad.like(f"%{search}%"))
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": [destinacija_to_dict(d) for d in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages
    })


@destinacije_bp.route("/destinacije/<int:id>", methods=["GET"])
def get_destinacija(id):
    destinacija = Destinacija.query.get_or_404(id)
    return jsonify(destinacija_to_dict(destinacija))


@destinacije_bp.route("/destinacije", methods=["POST"])
def create_destinacija():
    data = request.get_json()

    nova_destinacija = Destinacija(
        naziv=data["naziv"],
        drzava=data["drzava"],
        grad=data["grad"],
        opis=data.get("opis"),
        cijena=data["cijena"],
    )

    db.session.add(nova_destinacija)
    db.session.commit()

    return jsonify(destinacija_to_dict(nova_destinacija)), 201


@destinacije_bp.route("/destinacije/<int:id>", methods=["PUT"])
def update_destinacija(id):
    destinacija = Destinacija.query.get_or_404(id)
    data = request.get_json()

    destinacija.naziv = data["naziv"]
    destinacija.drzava = data["drzava"]
    destinacija.grad = data["grad"]
    destinacija.opis = data.get("opis")
    destinacija.cijena = data["cijena"]

    db.session.commit()

    return jsonify(destinacija_to_dict(destinacija))


@destinacije_bp.route("/destinacije/<int:id>", methods=["DELETE"])
def delete_destinacija(id):
    destinacija = Destinacija.query.get_or_404(id)

    db.session.delete(destinacija)
    db.session.commit()

    return jsonify({"message": "Destinacija obrisana"})