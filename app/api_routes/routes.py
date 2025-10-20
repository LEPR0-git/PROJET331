# routes/routes.py
from flask import Blueprint, request, jsonify
from database import db
from models.models import User, FreelanceProfile, PortfolioItem, ClientProfile

bp = Blueprint('freelance', __name__, url_prefix='/api/freelance')

# Helper pour parser int
# def _to_int(value, default=None):
#     try:
#         return int(value)
#     except (TypeError, ValueError):
#         return default

# GET /api/freelance/profiles
@bp.route('/profiles', methods=['GET'])
def get_all_profiles():
    try:
        skills = request.args.get('skills')
        availability = request.args.get('availability')
        min_rate = request.args.get('minRate', type=float)
        max_rate = request.args.get('maxRate', type=float)

        query = FreelanceProfile.query

        if skills:
            skill_list = [s.strip() for s in skills.split(',') if s.strip()]
            # overlap requires ARRAY type in Postgres
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
@bp.route('/profiles/<int:profile_id>', methods=['GET'])
def get_profile_by_id(profile_id):
    try:
        profile = FreelanceProfile.query.filter_by(id=profile_id).first()
        if not profile:
            return jsonify({"success": False, "message": "Profil freelance non trouvé"}), 404
        return jsonify({"success": True, "data": profile.to_dict(include_user=True, include_portfolio=True)}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# POST /api/freelance/profiles
# @bp.route('/profiles', methods=['POST'])
# def create_profile():
#     try:
#         data = request.get_json() or {}
#         user_id = _to_int(data.get('userId'))
#         first_name = data.get('firstName')
#         last_name = data.get('lastName')

#         if not user_id or not first_name or not last_name:
#             return jsonify({"success": False, "message": "userId, firstName et lastName sont requis"}), 400

#         # check user exists
#         user = User.query.get(user_id)
#         if not user:
#             return jsonify({"success": False, "message": "Utilisateur introuvable"}), 404

#         # unique constraint user_id (one profile per user)
#         existing = FreelanceProfile.query.filter_by(user_id=user_id).first()
#         if existing:
#             return jsonify({"success": False, "message": "Profil existant déjà pour cet utilisateur"}), 400

#         prof = FreelanceProfile(
#             user_id=user_id,
#             first_name=first_name,
#             last_name=last_name,
#             title=data.get('title'),
#             description=data.get('description'),
#             skills=data.get('skills') or [],
#             hourly_rate=float(data.get('hourlyRate')) if data.get('hourlyRate') is not None else None,
#             availability=data.get('availability') or None
#         )
#         db.session.add(prof)
#         db.session.commit()

#         return jsonify({"success": True, "message": "Profil créé avec succès", "data": prof.to_dict(include_user=True)}), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"success": False, "message": str(e)}), 500

def _to_int(val):
    try:
        return int(val)
    except (TypeError, ValueError):
        return None

@bp.route('/profiles', methods=['POST'])
def create_profile():
    try:
        data = request.get_json() or {}

        # Récupération des champs requis
        user_id = _to_int(data.get('userId'))
        first_name = data.get('firstName')
        last_name = data.get('lastName')

        if not user_id or not first_name or not last_name:
            return jsonify({
                "success": False,
                "message": "userId, firstName et lastName sont requis"
            }), 400

        # Vérification de l'existence de l'utilisateur
        user = User.query.get(user_id)
        if not user:
            return jsonify({"success": False, "message": "Utilisateur introuvable"}), 404

        # Vérification qu'il n'y a pas déjà un profil pour cet utilisateur
        existing = FreelanceProfile.query.filter_by(user_id=user_id).first()
        if existing:
            return jsonify({"success": False, "message": "Profil existant déjà pour cet utilisateur"}), 400

        # Conversion des champs optionnels
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

        # Création du profil
        prof = FreelanceProfile(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            title=data.get('title'),
            description=data.get('description'),
            skills=skills,  # Assurez-vous que la colonne DB est JSON ou ARRAY
            hourly_rate=hourly_rate,
            availability=data.get('availability')
        )

        db.session.add(prof)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Profil créé avec succès",
            "data": prof.to_dict(include_user=True)
        }), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        print(traceback.format_exc())
        return jsonify({"success": False, "message": str(e)}), 500

# PUT /api/freelance/profiles/:id
@bp.route('/profiles/<int:profile_id>', methods=['PUT'])
def update_profile(profile_id):
    try:
        data = request.get_json() or {}
        prof = FreelanceProfile.query.get(profile_id)
        if not prof:
            return jsonify({"success": False, "message": "Profil non trouvé"}), 404

        prof.first_name = data.get('firstName', prof.first_name)
        prof.last_name = data.get('lastName', prof.last_name)
        prof.title = data.get('title', prof.title)
        prof.description = data.get('description', prof.description)
        prof.skills = data.get('skills', prof.skills or [])
        prof.hourly_rate = float(data.get('hourlyRate')) if data.get('hourlyRate') is not None else prof.hourly_rate
        prof.availability = data.get('availability', prof.availability)

        db.session.commit()
        return jsonify({"success": True, "message": "Profil mis à jour avec succès", "data": prof.to_dict(include_user=True)}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

# DELETE /api/freelance/profiles/:id
@bp.route('/profiles/<int:profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    try:
        prof = FreelanceProfile.query.get(profile_id)
        if not prof:
            return jsonify({"success": False, "message": "Profil non trouvé"}), 404
        db.session.delete(prof)
        db.session.commit()
        return jsonify({"success": True, "message": "Profil supprimé avec succès"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

# POST /api/freelance/profiles/:id/portfolio
@bp.route('/profiles/<int:profile_id>/portfolio', methods=['POST'])
def add_portfolio_item(profile_id):
    try:
        data = request.get_json() or {}
        title = data.get('title')
        if not title:
            return jsonify({"success": False, "message": "Le titre est requis"}), 400

        prof = FreelanceProfile.query.get(profile_id)
        if not prof:
            return jsonify({"success": False, "message": "Profil non trouvé"}), 404

        item = PortfolioItem(
            title=title,
            description=data.get('description'),
            image_url=data.get('imageUrl'),
            project_url=data.get('projectUrl'),
            freelance_profile_id=profile_id
        )
        db.session.add(item)
        db.session.commit()
        return jsonify({"success": True, "message": "Élément de portfolio ajouté", "data": item.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

# DELETE /api/freelance/portfolio/:itemId
@bp.route('/portfolio/<int:item_id>', methods=['DELETE'])
def remove_portfolio_item(item_id):
    try:
        item = PortfolioItem.query.get(item_id)
        if not item:
            return jsonify({"success": False, "message": "Portfolio item non trouvé"}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({"success": True, "message": "Élément de portfolio supprimé"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
