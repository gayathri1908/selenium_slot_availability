import time
import threading
import logging
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ================= EMAIL CONFIG =================
SENDER_EMAIL        = "bollaramgayathri984@gmail.com"
SENDER_APP_PASSWORD = "vvgcbrzpdtryuarz"
RECEIVER_EMAIL      = "bollaramgayathri984@gmail.com"

# ================= LOGGING =================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger()

# ================= SITES =================
SITES = [
    {
        "name"           : "OG Tour Hyderabad - BookMyShow",
        "url"            : "https://in.bookmyshow.com/events/og-tour-india-with-thaman-live-in-hyderabad/ET00494783",
        "type"           : "movie",
        "check_interval" : 10,
    },
    {
        "name"           : "Dr. Pratap Chandra - Apollo",
        "url"            : "https://www.apollohospitals.com/doctors/cardiologist/hyderabad/dr-pratap-chandra-rath",
        "type"           : "doctor",
        "check_interval" : 10,
    },
]

# ================= WORDS THAT MEAN "NOT AVAILABLE" =================
SOLD_OUT_WORDS = [
    "sold out", "houseful", "fully booked", "no slots",
    "no appointments available", "currently unavailable",
    "not available", "coming soon", "waitlist",
]

# ================= WORDS THAT MEAN "AVAILABLE" =================
# Movie / BMS
MOVIE_AVAILABLE = [
    "book now", "buy now", "buy tickets", "book tickets",
    "select seats", "proceed to pay", "add to cart",
    "check availability", "book",
]
# Doctor / Apollo — catches any time like 9:00 AM, 10:30 am etc
SLOT_PATTERN = re.compile(r'\b\d{1,2}:\d{2}\s?[APap][Mm]\b')
DOCTOR_AVAILABLE = [
    "book appointment", "book slot", "available", "select slot",
    "confirm", "schedule", "consult now", "book consultation",
    "appointment available", "slots available",
]

# ================= DRIVER =================
def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

# ================= EMAIL =================
def send_email(site, detail):
    try:
        subject = f"✅ BOOK NOW — {site['name']} is AVAILABLE!"
        body = f"""
🎉 {site['name']} — Available Right Now!

Details : {detail}
URL     : {site['url']}
Time    : {datetime.now().strftime('%d %b %Y %I:%M:%S %p')}

Open the link above and book immediately!
"""
        msg = MIMEMultipart()
        msg["From"]    = SENDER_EMAIL
        msg["To"]      = RECEIVER_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        logger.info(f"📧 Email sent → {site['name']}")
    except Exception as e:
        logger.error(f"❌ Email failed: {e}")

# ================= CHECK MOVIE (BMS) =================
def check_movie(page_text, page_source):
    # If page says sold out → not available
    for word in SOLD_OUT_WORDS:
        if word in page_text:
            return False, None

    # Check for any availability keyword
    for word in MOVIE_AVAILABLE:
        if word in page_text:
            return True, f"Found: '{word}' on page"

    return False, None

# ================= CHECK DOCTOR (APOLLO) =================
def check_doctor(page_text, page_source):
    # If page says no slots → not available
    for word in SOLD_OUT_WORDS:
        if word in page_text:
            return False, None

    # Check for time slots like "10:30 AM"
    slots = SLOT_PATTERN.findall(page_source)
    if slots:
        unique = list(set(slots))
        return True, f"Slots found: {', '.join(unique[:5])}"

    # Check for booking keywords
    for word in DOCTOR_AVAILABLE:
        if word in page_text:
            return True, f"Found: '{word}' on page"

    return False, None

# ================= MONITOR =================
def monitor_site(site):
    logger.info(f"🚀 Started: {site['name']}")
    driver = create_driver()

    try:
        while True:
            try:
                driver.get(site["url"])
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(4)  # wait for JS to render

                page_text   = driver.find_element(By.TAG_NAME, "body").text.lower()
                page_source = driver.page_source

                if site["type"] == "movie":
                    available, detail = check_movie(page_text, page_source)
                else:
                    available, detail = check_doctor(page_text, page_source)

                now = datetime.now().strftime("%H:%M:%S")

                if available:
                    logger.info(f"🎉 AVAILABLE [{now}] → {site['name']} | {detail}")
                    send_email(site, detail)
                    break  # stop checking this site
                else:
                    logger.info(f"⏳ Not yet [{now}] → {site['name']}")

            except Exception as e:
                logger.error(f"⚠️  Error [{site['name']}]: {e}")

            time.sleep(site["check_interval"])

    finally:
        driver.quit()
        logger.info(f"🔴 Stopped: {site['name']}")

# ================= MAIN =================
def main():
    logger.info("=" * 55)
    logger.info("  Monitor running — will email when available")
    logger.info("=" * 55)

    threads = []
    for site in SITES:
        t = threading.Thread(target=monitor_site, args=(site,), daemon=True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    logger.info("✅ All sites done.")

if __name__ == "__main__":
    main()