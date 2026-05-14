from extensions import db


class Destinacija(db.Model):
    __tablename__ = "destinacije"

    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False)
    drzava = db.Column(db.String(100), nullable=False)
    grad = db.Column(db.String(100), nullable=False)
    opis = db.Column(db.Text, nullable=True)
    cijena = db.Column(db.Float, nullable=False)

    rezervacije = db.relationship("Rezervacija", back_populates="destinacija")


class Klijent(db.Model):
    __tablename__ = "klijenti"

    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(100), nullable=False)
    prezime = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    telefon = db.Column(db.String(50), nullable=True)

    rezervacije = db.relationship("Rezervacija", back_populates="klijent")


class Zaposlenik(db.Model):
    __tablename__ = "zaposlenici"

    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(100), nullable=False)
    prezime = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    pozicija = db.Column(db.String(100), nullable=False)


class Rezervacija(db.Model):
    __tablename__ = "rezervacije"

    id = db.Column(db.Integer, primary_key=True)
    klijent_id = db.Column(db.Integer, db.ForeignKey("klijenti.id"), nullable=False)
    destinacija_id = db.Column(db.Integer, db.ForeignKey("destinacije.id"), nullable=False)
    datum_rezervacije = db.Column(db.Date, nullable=False)
    broj_osoba = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="aktivna")

    klijent = db.relationship("Klijent", back_populates="rezervacije")
    destinacija = db.relationship("Destinacija", back_populates="rezervacije")