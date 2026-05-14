from flask import Blueprint, jsonify
from sqlalchemy import func

from models import Destinacija, Klijent, Rezervacija, Zaposlenik
from extensions import db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET"])
def get_dashboard():
    broj_destinacija = Destinacija.query.count()
    broj_klijenata = Klijent.query.count()
    broj_rezervacija = Rezervacija.query.count()
    broj_zaposlenika = Zaposlenik.query.count()

    aktivne_rezervacije = Rezervacija.query.filter_by(status="aktivna").count()

    prosjecna_cijena = db.session.query(func.avg(Destinacija.cijena)).scalar()
    if prosjecna_cijena is None:
        prosjecna_cijena = 0

    return jsonify({
        "broj_destinacija": broj_destinacija,
        "broj_klijenata": broj_klijenata,
        "broj_rezervacija": broj_rezervacija,
        "broj_zaposlenika": broj_zaposlenika,
        "aktivne_rezervacije": aktivne_rezervacije,
        "prosjecna_cijena": round(prosjecna_cijena, 2)
    })