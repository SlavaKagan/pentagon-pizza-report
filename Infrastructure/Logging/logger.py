import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("ENV", "prod").lower()
log_level = logging.DEBUG if env == "dev" else logging.INFO

LOG_DIR = os.path.join(os.getcwd(), "Logs")
os.makedirs(LOG_DIR, exist_ok=True)

today_str = datetime.now().strftime("%Y-%m-%d")
LOG_FILE = os.path.join(LOG_DIR, f"pizza_alerts_{today_str}.log")

logger = logging.getLogger(__name__)
logger.setLevel(log_level)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

if env == "dev":
    try:
        from colorlog import ColoredFormatter

        color_formatter = ColoredFormatter(
            fmt="%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(color_formatter)
    except ImportError:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
else:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
