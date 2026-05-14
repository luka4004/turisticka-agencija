from flask import Blueprint, request, jsonify
from datetime import datetime

from extensions import db
from models import Rezervacija, Klijent, Destinacija

rezervacije_bp = Blueprint("rezervacije", __name__)


def rezervacija_to_dict(rezervacija):
    return {
        "id": rezervacija.id,
        "klijent_id": rezervacija.klijent_id,
        "destinacija_id": rezervacija.destinacija_id,
        "datum_rezervacije": rezervacija.datum_rezervacije.strftime("%Y-%m-%d"),
        "broj_osoba": rezervacija.broj_osoba,
        "status": rezervacija.status,
        "klijent": {
            "id": rezervacija.klijent.id,
            "ime": rezervacija.klijent.ime,
            "prezime": rezervacija.klijent.prezime,
            "email": rezervacija.klijent.email,
        },
        "destinacija": {
            "id": rezervacija.destinacija.id,
            "naziv": rezervacija.destinacija.naziv,
            "drzava": rezervacija.destinacija.drzava,
            "grad": rezervacija.destinacija.grad,
        },
    }


@rezervacije_bp.route("/rezervacije", methods=["GET"])
def get_rezervacije():
    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    query = Rezervacija.query.join(Klijent).join(Destinacija)

    if search:
        query = query.filter(
            (Klijent.ime.like(f"%{search}%")) |
            (Klijent.prezime.like(f"%{search}%")) |
            (Destinacija.naziv.like(f"%{search}%")) |
            (Rezervacija.status.like(f"%{search}%"))
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": [rezervacija_to_dict(r) for r in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages
    })


@rezervacije_bp.route("/rezervacije/<int:id>", methods=["GET"])
def get_rezervacija(id):
    rezervacija = Rezervacija.query.get_or_404(id)
    return jsonify(rezervacija_to_dict(rezervacija))


@rezervacije_bp.route("/rezervacije", methods=["POST"])
def create_rezervacija():
    data = request.get_json()

    klijent = Klijent.query.get_or_404(data["klijent_id"])
    destinacija = Destinacija.query.get_or_404(data["destinacija_id"])

    nova_rezervacija = Rezervacija(
        klijent_id=klijent.id,
        destinacija_id=destinacija.id,
        datum_rezervacije=datetime.strptime(data["datum_rezervacije"], "%Y-%m-%d").date(),
        broj_osoba=data["broj_osoba"],
        status=data.get("status", "aktivna"),
    )

    db.session.add(nova_rezervacija)
    db.session.commit()

    return jsonify(rezervacija_to_dict(nova_rezervacija)), 201


@rezervacije_bp.route("/rezervacije/<int:id>", methods=["PUT"])
def update_rezervacija(id):
    rezervacija = Rezervacija.query.get_or_404(id)
    data = request.get_json()

    klijent = Klijent.query.get_or_404(data["klijent_id"])
    destinacija = Destinacija.query.get_or_404(data["destinacija_id"])

    rezervacija.klijent_id = klijent.id
    rezervacija.destinacija_id = destinacija.id
    rezervacija.datum_rezervacije = datetime.strptime(data["datum_rezervacije"], "%Y-%m-%d").date()
    rezervacija.broj_osoba = data["broj_osoba"]
    rezervacija.status = data["status"]

    db.session.commit()

    return jsonify(rezervacija_to_dict(rezervacija))


@rezervacije_bp.route("/rezervacije/<int:id>", methods=["DELETE"])
def delete_rezervacija(id):
    rezervacija = Rezervacija.query.get_or_404(id)

    db.session.delete(rezervacija)
    db.session.commit()

    return jsonify({"message": "Rezervacija obrisana"})