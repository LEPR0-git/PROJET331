import os
from dotenv import load_dotenv

load_dotenv()  # lit le fichier .env si présent

class Config:
    # Variables DB séparées
    DB_USER = os.getenv("DB_USER", "christ")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "12345678")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "freelance")

    # Génération dynamique de l'URL SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # évite les warnings SQLAlchemy

    # Sécurité / JWT
    SECRET_KEY = os.getenv("JWT_SECRET", "ton_secret")

    # Mode debug
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"

    # JSON
    JSON_SORT_KEYS = False  # garde l’ordre des champs JSON

