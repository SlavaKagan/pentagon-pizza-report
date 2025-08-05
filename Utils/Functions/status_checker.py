import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from Configs.config import USER_AGENT, CHROMEDRIVER_PATH
from Infrastructure.Logging.logger import logger

def get_live_status_text(url: str) -> str | None:
    options = Options()
    options.binary_location = CHROME_BIN
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f'user-agent={USER_AGENT}')
    options.add_argument("--log-level=3")
    options.add_argument("--disable-logging")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--window-size=1920,1080")

    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        logger.info("ממתין לטעינת 'Live' או 'זמן אמת'...")

        wait.until(lambda d: "live" in d.page_source.lower() or "זמן אמת" in d.page_source)

        # חיפוש אלמנט שיש בו Live ולאחריו sibling שמכיל את הטקסט
        logger.info("מאתר את סטטוס ה־Live...")
        live_element = driver.find_elements(
            By.XPATH,
            "//div[contains(text(),'Live') or contains(text(),'זמן אמת')]/following-sibling::div"
        )

        for el in live_element:
            status = el.text.strip()
            if status:
                logger.info(f"סטטוס עומס חי: {status}")
                return status

        # fallback: חפש לפי fontBodySmall אם לא נמצא קודם
        logger.info("ניסיון fallback לזיהוי סטטוס...")
        all_font_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'fontBodySmall')]")
        for i, el in enumerate(all_font_elements):
            text = el.text.strip().lower()
            if text in ["live", "זמן אמת"] and i + 1 < len(all_font_elements):
                next_el = all_font_elements[i + 1]
                status_text = next_el.text.strip()
                if status_text:
                    logger.info(f"סטטוס עומס חי (fallback): {status_text}")
                    return status_text

        logger.info("בודק אם יש מידע על סגירה...")
        closed_el = driver.find_elements(By.XPATH, "//*[contains(text(),'Closed') or contains(text(),'סגור')]")
        if closed_el:
            closed_text = closed_el[0].text.strip()
            if closed_text:
                logger.info(f"המקום סגור: {closed_text}")
                return closed_text

        logger.warning("לא נמצא סטטוס עומס ולא סטטוס סגירה.")
        driver.save_screenshot("no_status_found.png")
        return None

    except Exception as e:
        logger.error(f"שגיאה באיתור סטטוס: {e}")
        driver.save_screenshot("error_status.png")
        return None

    finally:
        driver.quit()
