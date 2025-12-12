
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass

def send_simulation_emails():
    print("--- Phishing Simulation Email Sender ---")
    print("WARNING: Only send to people who have EXPLICITLY CONSENTED.")
    
    # Configuration
    smtp_server = "smtp.gmail.com" # Example for Gmail
    smtp_port = 587
    
    sender_email = input("Enter your sender email (e.g., your_email@gmail.com): ")
    sender_password = getpass.getpass("Enter your app password: ")
    
    # Target List (Demo) - Ensure these are test accounts or consenting users
    targets = [
        {"email": "test_user@example.com", "name": "Test User"},
        # Add more consenting users here
    ]
    
    # Email Content
    subject = "Security Alert: New Sign-in Detected (Simulation)"
    
    # The links point to localhost. 
    # In a real (authorized) test, this would be your ngrok or server URL.
    server_url = "http://127.0.0.1:5000"
    
    for target in targets:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = target["email"]
        
        text = f"""
        Hi {target['name']},
        
        We detected a clear sign-in attempt to your account.
        Please verify your identity immediately:
        {server_url}/login
        
        Use this link for OAuth verification:
        {server_url}/oauth
        
        
        """
        
        html = f"""
        <html>
          <body>
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h2>Security Alert</h2>
                <p>Hi {target['name']},</p>
                <p>We detected a new sign-in attempt to your account.</p>
                <p>Please verify your identity immediately by clicking the button below:</p>
                
                <a href="{server_url}/login" style="background-color: #0095f6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                    Verify Account (Instagram Style)
                </a>
                
                <p style="margin-top: 20px;">Or verify via OAuth provider:</p>
                <a href="{server_url}/oauth">OAuth Verification Link</a>

                <hr style="margin-top: 30px;">
                <p style="font-size: 12px; color: #777;">
                    <strong>NOTICE:</strong> This includes links to a local <strong>Phishing Simulation</strong>. 
                    Do not enter real credentials. This is an educational exercise.
                </p>
            </div>
          </body>
        </html>
        """
        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        msg.attach(part1)
        msg.attach(part2)
        
        try:
            # Note: This attempts to connect to GMS; might fail without real creds or net access
            # We wrap in try/except to simulate the 'sending' process without crashing if blocked.
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, target["email"], msg.as_string())
            print(f"Email sent to {target['email']}")
        except Exception as e:
            print(f"Failed to send to {target['email']}. Error: {e}")

if __name__ == "__main__":
    send_simulation_emails()
