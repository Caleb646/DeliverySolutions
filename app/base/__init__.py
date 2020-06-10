from flask import Blueprint

base_bp = Blueprint("base", __name__, template_folder="templates", static_folder="static")


from app.base import base_routes