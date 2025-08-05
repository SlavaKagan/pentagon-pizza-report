import os
import platform
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
)

if platform.system() == "Windows":
    CHROMEDRIVER_PATH = os.path.join(BASE_DIR, "chromedriver.exe")
else:
    CHROMEDRIVER_PATH = os.path.join(BASE_DIR, "chromedriver")

LOGO_PATH = os.path.join(BASE_DIR, "Utils", "Images", "PizzaLogo.jpg")
LOG_FILE = os.path.join(BASE_DIR, "Logs", "pizza_alerts.log")