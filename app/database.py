from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """
    Initialise la base de données et configure les migrations.
    Crée les tables si elles n'existent pas encore.
    """
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
