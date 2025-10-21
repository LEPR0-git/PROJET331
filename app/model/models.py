from datetime import datetime
from enum import Enum
from database import db
from sqlalchemy.dialects.postgresql import ARRAY

# ===== Enums =====
class UserRole(Enum):
    FREELANCE = "FREELANCE"
    CLIENT = "CLIENT"
    ADMIN = "ADMIN"

class Availability(Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    PART_TIME = "PART_TIME"

# ===== Models =====
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.FREELANCE, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    freelance_profile = db.relationship("FreelanceProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    client_profile = db.relationship("ClientProfile", backref="user", uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role.value if self.role else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class FreelanceProfile(db.Model):
    __tablename__ = 'freelance_profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)

    try:
        skills = db.Column(ARRAY(db.String), default=list)
    except Exception:
        skills = db.Column(db.JSON, default=list)

    hourly_rate = db.Column(db.Float, nullable=True)
    availability = db.Column(db.Enum(Availability), default=Availability.AVAILABLE)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), unique=True, nullable=False)
    portfolio_items = db.relationship("PortfolioItem", backref="freelance_profile", cascade="all, delete-orphan")

    def to_dict(self, include_user=False, include_portfolio=False):
        data = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "title": self.title,
            "description": self.description,
            "skills": self.skills or [],
            "hourly_rate": self.hourly_rate,
            "availability": self.availability.value if self.availability else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id
        }
        if include_user and self.user:
            data["user"] = self.user.to_dict()
        if include_portfolio:
            data["portfolio_items"] = [p.to_dict() for p in self.portfolio_items]
        return data

class PortfolioItem(db.Model):
    __tablename__ = 'portfolio_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    project_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    freelance_profile_id = db.Column(db.Integer, db.ForeignKey('freelance_profiles.id', ondelete="CASCADE"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,
            "project_url": self.project_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "freelance_profile_id": self.freelance_profile_id
        }

class ClientProfile(db.Model):
    __tablename__ = 'client_profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "company_name": self.company_name,
            "description": self.description,
            "user_id": self.user_id
        }
