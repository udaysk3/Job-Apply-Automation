from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


# ==============================
# Wait Helper for Chatbot Qs
# ==============================

def wait_for_new_question(driver, old_count, timeout=8):
    """Wait until a new chatbot question appears."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: len(d.find_elements(By.XPATH, "//div[contains(@class,'botMsg')]")) > old_count
        )
        return True
    except:
        return False

def get_latest_question(driver):
    """Return the latest non-junk chatbot question text."""
    msgs = driver.find_elements(By.XPATH, "//div[contains(@class,'botMsg')]")
    for msg in reversed(msgs):  # check newest → oldest
        text = msg.text.strip()
        if not text:
            continue
        # skip junk system messages
        if any(skip in text.lower() for skip in ["posted:", "openings", "applicants"]):
            continue
        return text
    return None
