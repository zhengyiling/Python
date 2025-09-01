import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import json
import os
from datetime import datetime

# ---------------- USCIS SCRAPER ---------------- #
def get_uscis_case_status(case_number: str) -> dict:
    url = "https://egov.uscis.gov/casestatus/mycasestatus.do"
    payload = {"appReceiptNum": case_number}
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code != 200:
        return {"case_number": case_number, "status": "Error", "details": "Connection failed."}

    soup = BeautifulSoup(response.text, "html.parser")

    status_elem = soup.find("h1")
    details_elem = soup.find("p")

    if not status_elem or not details_elem:
        return {"case_number": case_number, "status": "Not found", "details": "Check case number."}

    return {
        "case_number": case_number,
        "status": status_elem.get_text(strip=True),
        "details": details_elem.get_text(strip=True)
    }

# ---------------- EMAIL ALERT ---------------- #
def send_email_alert(subject, body, to_email, from_email, from_password, smtp_server="smtp.gmail.com", smtp_port=587):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, [to_email], msg.as_string())



# ---------------- TRACKING LOGIC ---------------- #
def track_case(case_number, config):
    status_file = "uscis_status.json"
    current_status = get_uscis_case_status(case_number)

    # Load last known status
    last_status = {}
    if os.path.exists(status_file):
        with open(status_file, "r") as f:
            last_status = json.load(f)

    old_status = last_status.get(case_number, {}).get("status")

    # Compare with last known
    if old_status != current_status["status"]:
        # Save new status
        last_status[case_number] = current_status
        with open(status_file, "w") as f:
            json.dump(last_status, f, indent=2)

        # Format notification
        alert_msg = (
            f"📌 USCIS Case Status Update ({case_number})\n\n"
            f"Status: {current_status['status']}\n"
            f"Details: {current_status['details']}\n"
            f"Checked on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        # Send email
        send_email_alert(
            subject=f"USCIS Case Update: {case_number}",
            body=alert_msg,
            to_email=config["notify_email"],
            from_email=config["email"],
            from_password=config["email_password"]
        )
        

        print("✅ Status changed! Notifications sent.")
    else:
        print("ℹ️ No change in case status.")


if __name__ == "__main__":
    # --------- CONFIGURATION --------- #
    config = {
        "case_number": "IOE0932174040",       # Change to your USCIS receipt number
        "email": "yiling.zheng.sbu17@gmail.com",      # Sender email
        "email_password": "596969linG",    # App password for Gmail
        "notify_email": "zhengyiling-lin@hotmail.com"# Where to send updates
    }

    track_case(config["case_number"], config)
