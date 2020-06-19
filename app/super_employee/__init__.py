from flask import Blueprint

super_employee_bp = Blueprint("super_employee", __name__, template_folder="templates", static_folder="static")

from app.super_employee import super_employee_routes