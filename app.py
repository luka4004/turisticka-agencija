from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db, migrate
import models

from routes.destinacije import destinacije_bp
from routes.klijenti import klijenti_bp
from routes.zaposlenici import zaposlenici_bp
from routes.rezervacije import rezervacije_bp
from routes.dashboard import dashboard_bp
app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(destinacije_bp, url_prefix="/api")
app.register_blueprint(klijenti_bp, url_prefix="/api")
app.register_blueprint(zaposlenici_bp, url_prefix="/api")
app.register_blueprint(rezervacije_bp, url_prefix="/api")
app.register_blueprint(dashboard_bp, url_prefix="/api")
@app.route("/")
def home():
    return {"message": "Backend radi i spojen je na konfiguraciju baze"}

if __name__ == "__main__":
    app.run(debug=True)