from flask import Blueprint

admin_bp = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


from app.admin import admin_routes