from app import app
from flask import render_template
from app import db

from app.models import Measurement


@app.route("/")
def hello_world():
    klimaInfo = db.session.query(Measurement).all()
    return render_template("home.html", klimaInfo=klimaInfo)
