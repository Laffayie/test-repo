
from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os
import uuid

app = Flask(__name__, instance_relative_config=True)

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Database configuration
db_path = os.path.join(app.instance_path, "kurzy.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}".replace("\\", "/")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# SQLAlchemy Models
class Trener(db.Model):
    __tablename__ = "Treneri"
    ID_Trenera = db.Column(db.Integer, primary_key=True)
    Meno = db.Column(db.String, nullable=False)
    Priezvisko = db.Column(db.String, nullable=False)
    Specializacia = db.Column(db.String, nullable=False)
    Telefon = db.Column(db.String, nullable=False)
    Heslo = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Trener {self.Meno} {self.Priezvisko}>"

class Kurz(db.Model):
    __tablename__ = "Kurzy"
    ID_Kurzu = db.Column(db.Integer, primary_key=True)
    Nazov_kurzu = db.Column(db.String, nullable=False)
    Typ_sportu = db.Column(db.String, nullable=False)
    Max_pocet_ucastnikov = db.Column(db.Integer, nullable=False)
    ID_trenera = db.Column(db.Integer, db.ForeignKey("Treneri.ID_Trenera"), nullable=False)

    def __repr__(self):
        return f"<Kurz {self.Nazov_kurzu}>"

class Miesto(db.Model):
    __tablename__ = "Miesta"
    ID_Miesta = db.Column(db.Integer, primary_key=True)
    Nazov_miesta = db.Column(db.String, nullable=False)
    Adresa = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Miesto {self.Nazov_miesta}>"

# Affine encryption function
def affine_encrypt(text, key_a=5, key_b=8):
    result = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.upper()
            x = ord(char) - ord('A')
            encrypted_value = (key_a * x + key_b) % 26
            encrypted_char = chr(encrypted_value + ord('A'))
            if not is_upper:
                encrypted_char = encrypted_char.lower()
            result += encrypted_char
        else:
            result += char
    return result

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registracia_kurzu', methods=['GET'])
def registracia_kurzu():
    return render_template('registracia_kurzu.html')

@app.route('/registracia_kurzu', methods=['POST'])
def registracia_kurza():
    nazov = affine_encrypt(request.form['nazov'], 5, 8)
    typ = affine_encrypt(request.form['typ_sport'], 5, 8)
    capacita = int(request.form['max_poc_uc'])
    id_trenera = int(request.form['id_tre'])

    # Insert into database using SQLAlchemy
    kurz = Kurz(
        Nazov_kurzu=nazov,
        Typ_sportu=typ,
        Max_pocet_ucastnikov=capacita,
        ID_trenera=id_trenera
    )
    db.session.add(kurz)
    db.session.commit()

    return render_template('success.html', message="Kurz bol úspešne zaregistrovaný!")

@app.route('/registracia_trenera', methods=['GET'])
def registracia_form():
    return render_template('registracia_trenera.html')

@app.route('/registracia_trenera', methods=['POST'])
def registracia_trenera():
    meno = request.form['meno']
    priezvisko = request.form['priezvisko']
    specializacia = request.form['specializacia']
    telefon = request.form['telefon']
    heslo = request.form['heslo']

    # Hash password
    heslo_hash = hashlib.sha256(heslo.encode()).hexdigest()

    # Insert into database using SQLAlchemy
    trener = Trener(
        Meno=meno,
        Priezvisko=priezvisko,
        Specializacia=specializacia,
        Telefon=telefon,
        Heslo=heslo_hash
    )
    db.session.add(trener)
    db.session.commit()

    return render_template('success.html', message="Tréner bol úspešne zaregistrovaný!")

@app.route('/kurzy')
def zobraz_kurzy():
    try:
        kurzy = Kurz.query.all()
        return render_template('kurzy.html', kurzy=kurzy)
    except Exception:
        return redirect(url_for('zobraz_error'))

@app.route('/miesta')
def zobraz_miesta():
    try:
        miesta = Miesto.query.all()
        return render_template('miesta.html', miesta=miesta)
    except Exception:
        return redirect(url_for('zobraz_error'))

@app.route('/treneri_a_kurz')
def zobraz_trenerov_kurz():
    try:
        # Assuming VSETCI_TRENERI_A_ICH_KURZY is a view; we'll query it directly
        result = db.session.execute(
            db.text("SELECT * FROM VSETCI_TRENERI_A_ICH_KURZY")
        ).fetchall()
        return render_template('treneri_a_kurz.html', kurzy=result)
    except Exception:
        return redirect(url_for('zobraz_error'))

@app.route('/capacita')
def zobraz_capacitu():
    try:
        suma = db.session.query(
            db.func.sum(Kurz.Max_pocet_ucastnikov)
        ).filter(Kurz.Nazov_kurzu.like('P%')).scalar()
        return render_template('capacita.html', suma=suma)
    except Exception:
        return redirect(url_for('zobraz_error'))

@app.route('/404')
def zobraz_error():
    return render_template('error.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)