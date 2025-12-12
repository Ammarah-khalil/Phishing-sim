# How to Get a Permanent Public Address

To get a **permanent** URL (one that doesn't change every time you restart), you have three main options.

## Option 1: Ngrok (Best for Localhost)
Ngrok now offers **one free static domain** for all users. This allows you to keep running the app on your computer, but the URL `https://your-name.ngrok-free.app` will never change.

### Steps:
1.  **Sign Up**: Go to [dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup) and create a free account.
2.  **Get Your Domain**:
    - Go to **Cloud Edge** -> **Domains** in the dashboard.
    - Click **+ New Domain**.
    - It will give you a static domain like `coyote-learning-quickly.ngrok-free.app`.
3.  **Install Ngrok**:
    - Download it from [ngrok.com/download](https://ngrok.com/download).
    - Or, if you have `winget` (Windows Package Manager), run:
      ```powershell
      winget install ngrok
      ```
4.  **Connect Account**:
    - Copy your Authtoken from the dashboard.
    - Run: `ngrok config add-authtoken YOUR_TOKEN_HERE`
5.  **Start the Tunnel**:
    Run this command (replace with your actual domain):
    ```powershell
    ngrok http --domain=your-static-domain.ngrok-free.app 5000
    ```

### Update Your App
Once you have your permanent URL:
```powershell
# 1. Provide the URL to the app
$env:BASE_URL = "https://your-static-domain.ngrok-free.app"

# 2. Clear old QR code
Remove-Item static/qr.png -ErrorAction SilentlyContinue

# 3. Run
python app.py
```

---

## Option 2: Serveo (No Account Needed)
You can request a specific subdomain with Serveo. If it's available, you get it.

1.  **Run with Alias**:
    Pick a unique name (e.g., `my-phishing-test-99`).
    ```powershell
    ssh -R 80:my-phishing-test-99:5000 serveo.net
    ```
    *If the name is taken, it will give you a random one. Try a more unique name.*

2.  **Using it**:
    Your URL will be `https://my-phishing-test-99.serveo.net`.
    Set your `$env:BASE_URL` to this and run your app.

---

## Option 3: Deploy to Cloud (Render.com)
If you want the "Permanent" address to work even when your computer is **off**, you must deploy the code to a cloud server.

**Render.com** is a great free option for Flask apps.
1.  Push your code to GitHub.
2.  Login to Render.com → New Web Service.
3.  Connect your repo.
4.  It will give you `https://phishing-sim.onrender.com` which is permanent and runs 24/7.
