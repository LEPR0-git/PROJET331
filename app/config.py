import os
from dotenv import load_dotenv

load_dotenv()  # lit le fichier .env si présent

class Config:
    # Connexion DB
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://christ:12345678@localhost:5432/freelance"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # évite les warnings SQLAlchemy

    # Sécurité / JWT
    SECRET_KEY = os.getenv("JWT_SECRET", "ton_secret")

    # Mode debug
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"

    # JSON
    JSON_SORT_KEYS = False  # garde l’ordre des champs JSON
