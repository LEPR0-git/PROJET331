from flask import Blueprint, request, jsonify
from database import db
from model.models import User, UserRole, FreelanceProfile, PortfolioItem, Availability

bp = Blueprint('api', __name__, url_prefix='/api')


# =====================
#       HELPERS
# =====================
def _validate_role(role_str):
    try:
        return UserRole(role_str)
    except ValueError:
        return None


def _to_int(val):
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


# Traduction automatique FR/EN pour disponibilité
AVAILABILITY_MAP = {
    "Disponible": Availability.AVAILABLE,
    "Indisponible": Availability.UNAVAILABLE,
    "Temps partiel": Availability.PART_TIME,
    "AVAILABLE": Availability.AVAILABLE,
    "UNAVAILABLE": Availability.UNAVAILABLE,
    "PART_TIME": Availability.PART_TIME
}


# =====================
#        USERS
# =====================

# GET /api/users
@bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.order_by(User.created_at.desc()).all()
        result = [u.to_dict() for u in users]
        return jsonify({"success": True, "data": result, "count": len(result)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


# GET /api/users/:id
@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"success": False, "message": "Utilisateur introuvable"}), 404
        return jsonify({"success": True, "data": user.to_dict()}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# POST /api/users
@bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')
        role_str = data.get('role', 'FREELANCE')

        if not email or not password:
            return jsonify({"success": False, "message": "email et password sont requis"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"success": False, "message": "Email déjà utilisé"}), 400

        role = _validate_role(role_str)
        if not role:
            return jsonify({"success": False, "message": f"role invalide, doit être {', '.join([r.value for r in UserRole])}"}), 400

        user = User(email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()

        return jsonify({"success": True, "message": "Utilisateur créé", "data": user.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


# PUT /api/users/:id
@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json() or {}
        user = User.query.get(user_id)
        if not user:
            return jsonify({"success": False, "message": "Utilisateur introuvable"}), 404

        if data.get('email'):
            user.email = data['email']
        if data.get('password'):
            user.password = data['password']
        if data.get('role'):
            role = _validate_role(data['role'])
            if not role:
                return jsonify({"success": False, "message": "role invalide"}), 400
            user.role = role

        db.session.commit()
        return jsonify({"success": True, "message": "Utilisateur mis à jour", "data": user.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


# DELETE /api/users/:id
@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"success": False, "message": "Utilisateur introuvable"}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": True, "message": "Utilisateur supprimé"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


# =====================
#   FREELANCE PROFILES
# =====================

# GET /api/freelance/profiles
@bp.route('/freelance/profiles', methods=['GET'])
def get_all_profiles():
    try:
        skills = request.args.get('skills')
        availability = request.args.get('availability')
        min_rate = request.args.get('minRate', type=float)
        max_rate = request.args.get('maxRate', type=float)

        query = FreelanceProfile.query

        if skills:
            skill_list = [s.strip() for s in skills.split(',') if s.strip()]
            query = query.filter(FreelanceProfile.skills.overlap(skill_list))
        if availability:
            query = query.filter_by(availability=availability)
        if min_rate is not None:
            query = query.filter(FreelanceProfile.hourly_rate >= min_rate)
        if max_rate is not None:
            query = query.filter(FreelanceProfile.hourly_rate <= max_rate)

        profiles = query.order_by(FreelanceProfile.created_at.desc()).all()
        result = [p.to_dict(include_user=True, include_portfolio=True) for p in profiles]

        return jsonify({"success": True, "data": result, "count": len(result)}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


# GET /api/freelance/profiles/:id
@bp.route('/freelance/profiles/<int:profile_id>', methods=['GET'])
def get_profile_by_id(profile_id):
    try:
        profile = FreelanceProfile.query.get(profile_id)
        if not profile:
            return jsonify({"success": False, "message": "Profil freelance non trouvé"}), 404
        return jsonify({"success": True, "data": profile.to_dict(include_user=True, include_portfolio=True)}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# POST /api/freelance/profiles
@bp.route('/freelance/profiles', methods=['POST'])
def create_profile():
    try:
        data = request.get_json() or {}

        user_id = _to_int(data.get('userId'))
        first_name = data.get('firstName')
        last_name = data.get('lastName')

        if not user_id or not first_name or not last_name:
            return jsonify({"success": False, "message": "userId, firstName et lastName sont requis"}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({"success": False, "message": "Utilisateur introuvable"}), 404

        existing = FreelanceProfile.query.filter_by(user_id=user_id).first()
        if existing:
            return jsonify({"success": False, "message": "Profil existant déjà pour cet utilisateur"}), 400

        # Conversion
        hourly_rate = None
        if data.get('hourlyRate') is not None:
            try:
                hourly_rate = float(data.get('hourlyRate'))
            except ValueError:
                return jsonify({"success": False, "message": "hourlyRate doit être un nombre"}), 400

        skills = data.get('skills')
        if skills is None:
            skills = []
        elif not isinstance(skills, list):
            return jsonify({"success": False, "message": "skills doit être une liste"}), 400

        availability_input = data.get('availability')
        availability = AVAILABILITY_MAP.get(availability_input, Availability.AVAILABLE)

        prof = FreelanceProfile(
            user_id=user_id,
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            title=data.get('title'),
            description=data.get('description'),
            skills=skills,
            hourly_rate=hourly_rate,
            availability=availability
        )

        db.session.add(prof)
        db.session.commit()

        return jsonify({"success": True, "message": "Profil créé avec succès", "data": prof.to_dict(include_user=True)}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

# PUT /api/freelance/profiles/:id
@bp.route('/freelance/profiles/<int:profile_id>', methods=['PUT'])
def update_profile(profile_id):
    try:
        data = request.get_json() or {}
        prof = FreelanceProfile.query.get(profile_id)
        if not prof:
            return jsonify({"success": False, "message": "Profil freelance non trouvé"}), 404

        if 'firstName' in data:
            prof.first_name = data['firstName'].strip()
        if 'lastName' in data:
            prof.last_name = data['lastName'].strip()
        if 'title' in data:
            prof.title = data['title']
        if 'description' in data:
            prof.description = data['description']
        if 'skills' in data:
            if not isinstance(data['skills'], list):
                return jsonify({"success": False, "message": "skills doit être une liste"}), 400
            prof.skills = data['skills']
        if 'hourlyRate' in data:
            try:
                prof.hourly_rate = float(data['hourlyRate'])
            except ValueError:
                return jsonify({"success": False, "message": "hourlyRate doit être un nombre"}), 400
        if 'availability' in data:
            prof.availability = AVAILABILITY_MAP.get(data['availability'], prof.availability)

        db.session.commit()
        return jsonify({"success": True, "message": "Profil mis à jour avec succès", "data": prof.to_dict(include_user=True)}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


# DELETE /api/freelance/profiles/:id
@bp.route('/freelance/profiles/<int:profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    try:
        prof = FreelanceProfile.query.get(profile_id)
        if not prof:
            return jsonify({"success": False, "message": "Profil freelance non trouvé"}), 404

        db.session.delete(prof)
        db.session.commit()
        return jsonify({"success": True, "message": "Profil supprimé avec succès"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
