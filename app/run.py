import os
from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import text
from database import init_db, db


def test_connection(app):
    """Teste la connexion à la base de données dans un contexte Flask"""
    try:
        with app.app_context():
            db.session.execute(text("SELECT 1"))
            print("✅ Base de données connectée")
        return True
    except Exception as e:
        print(f"❌ Erreur connexion DB : {e}")
        return False


def create_app():
    """Crée et configure l'application Flask principale"""
    app = Flask(__name__)

    # Charger la configuration depuis config.Config
    app.config.from_object('config.Config')

    # Activer CORS (pour le front-end)
    CORS(app)

    # Initialiser la base de données
    init_db(app)

    # ✅ Créer toutes les tables si elles n'existent pas
    with app.app_context():
        from models import models  # ⚠️ important pour que SQLAlchemy connaisse les modèles
        db.create_all()
        print("✅ Toutes les tables ont été créées (si manquantes)")

    # Tester la connexion
    test_connection(app)

    # Charger les blueprints de routes
    try:
        from api_routes.routes import bp   # ✅ dossier routes/
        app.register_blueprint(bp)
        print("✅ Blueprint '/api/freelance' chargé avec succès")
    except ImportError as e:
        print(f"❌ Erreur lors du chargement du blueprint : {e}")

    # Routes simples
    @app.route('/')
    def home():
        """Endpoint d’accueil de l’API"""
        return jsonify({
            "message": "API Freelance Platform - Flask",
            "status": "OK",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
            "endpoints": {
                "freelances": "/api/freelance/profiles",
                "health": "/health"
            }
        }), 200

    @app.route('/health')
    def health():
        """Endpoint de vérification du statut API/DB"""
        try:
            with app.app_context():
                db.session.execute(text("SELECT 1"))
            return jsonify({
                "status": "OK",
                "database": "Connected",
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }), 200
        except Exception as e:
            return jsonify({
                "status": "ERROR",
                "database": "Disconnected",
                "error": str(e)
            }), 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config["DEBUG"])
