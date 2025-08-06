from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from Infrastructure.Logging.logger import logger

def get_live_status_text(driver, url: str) -> str | None:
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        logger.info("ממתין לטעינת 'Live' או 'זמן אמת'...")
        wait.until(lambda d: "live" in d.page_source.lower() or "זמן אמת" in d.page_source)

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
        try:
            driver.save_screenshot("error_status.png")
        except Exception as screenshot_error:
            logger.warning(f"שגיאה ביצירת Screenshot: {screenshot_error}")
        return None
