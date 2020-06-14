from flask import Blueprint

user_bp = Blueprint("user", __name__, template_folder="templates", static_folder="static")


from app.user import user_routes