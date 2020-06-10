from flask import render_template, redirect
from app.base import base_bp


@base_bp.route("/", endpoint="index")
def index():

    return redirect("/home")


@base_bp.route("/home", endpoint="home")
def home():

    return render_template("base/home.html")