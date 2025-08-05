import os
import platform
import shutil
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

# Chrome & ChromeDriver paths
if platform.system() == "Windows":
    # Try to auto-detect chrome path
    default_chrome = shutil.which("chrome") or r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    CHROME_BIN = os.environ.get("CHROME_BIN", default_chrome)
    CHROMEDRIVER_PATH = os.path.join(BASE_DIR, "chromedriver.exe")
else:
    # Render / Linux (assumes chromium and chromedriver are installed via apt or buildpacks)
    CHROME_BIN = os.environ.get("CHROME_BIN", "/usr/bin/chromium")
    CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")

LOGO_PATH = os.path.join(BASE_DIR, "Utils", "Images", "PizzaLogo.jpg")
LOG_FILE = os.path.join(BASE_DIR, "Logs", "pizza_alerts.log")