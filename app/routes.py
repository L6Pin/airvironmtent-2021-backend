from app import app
from flask import render_template

klimaInfo = [{"temp":25.4},{"temp":32.2},{"temp":21.4}]

@app.route("/")
def hello_world():
    return render_template("home.html", klimaInfo=klimaInfo)