from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from ai_helper import get_ai_answer

# ==============================
# Selenium Setup
# ==============================
def start_browser():
    options = Options()
    options.add_argument("--start-maximized")
    service = Service(r"C:\chromedriver-win64\chromedriver.exe")  # 🔑 update path
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# ==============================
# Dynamic Form Filler
# ==============================
def fill_field_by_label(label, answer, driver=None, question=None, profile=None):
    from selenium.webdriver.support.ui import Select
    
    # --- Standard input handling ---
    try:
        input_elem = label.find_element(By.XPATH, "following::input[1]")
        if input_elem.get_attribute("type") in ["text", "number", "tel", "date", "email", "password"]:
            input_elem.clear()
            input_elem.send_keys(answer)
            return True
    except:
        pass

    try:
        textarea = label.find_element(By.XPATH, "following::textarea[1]")
        textarea.clear()
        textarea.send_keys(answer)
        return True
    except:
        pass

    try:
        select_elem = label.find_element(By.XPATH, "following::select[1]")
        Select(select_elem).select_by_visible_text(answer)
        return True
    except:
        pass

        # --- Multi-checkbox handling ---
    try:
        checkbox_groups = driver.find_elements(By.XPATH, "//div[contains(@class,'multicheckboxes-container')]")

        for group in checkbox_groups:
            try:
                question_label = group.find_element(By.XPATH, ".//preceding::label[1]").text.strip()
            except:
                question_label = "Unknown Checkbox Question"

            # Collect all checkboxes + labels
            checkboxes = group.find_elements(By.XPATH, ".//input[@type='checkbox']")
            options, opt_map = [], {}
            for cb in checkboxes:
                try:
                    lbl = driver.find_element(By.XPATH, f"//label[@for='{cb.get_attribute('id')}']").text.strip()
                except:
                    lbl = cb.get_attribute("value") or "Option"
                options.append(lbl)
                opt_map[lbl.lower()] = cb

            # Skip "No Experience" always
            if "no experience" in [o.lower() for o in options]:
                options = [o for o in options if o.lower() != "no experience"]

            # AI decides what to pick (can be multiple)
            ai_prompt = f'''Question: {question_label}
                            Options: {options}
                            Pick all that apply (comma-separated).'''
            choice = get_ai_answer(ai_prompt, profile).lower().strip()

            # Handle comma-separated answers
            selected = [c.strip() for c in choice.split(",")]

            matches = []
            for sel in selected:
                for opt, cb in opt_map.items():
                    if sel in opt or opt in sel:
                        matches.append(cb)

            # Default: pick the first one if AI messed up
            if not matches and checkboxes:
                matches.append(checkboxes[0])

            for cb in matches:
                driver.execute_script("arguments[0].click();", cb)
            

            print(f"→ Checked: {selected}")
            
            # click Save if exists
            try:
                save_btn = driver.find_element(By.XPATH, "//div[@class='sendMsg' and normalize-space(text())='Save']")
                driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
                driver.execute_script("arguments[0].click();", save_btn)
                print("Clicked Save button")
                time.sleep(1)
            except:
                pass
            return True

    except Exception as e:
        print("Checkbox handling failed:", e)

    # --- Radio button handling (fixed grouping) ---
    try:
        radio_groups = driver.find_elements(By.XPATH, "//div[contains(@class,'ssrc__radio-btn-container')]/ancestor::div[contains(@class,'singleselect-radiobutton-container') or contains(@class,'radio-group')]")

        for group in radio_groups:
            # extract question text more reliably
            try:
                question_label = group.find_element(By.XPATH, ".//preceding::label[1]").text.strip()
                if not question_label:
                    raise Exception("Empty label")
            except:
                try:
                    question_label = group.find_element(By.XPATH, ".//preceding::*[self::div or self::p or self::span][1]").text.strip()
                except:
                    question_label = "Unknown Question"

            # collect all options
            radios = group.find_elements(By.XPATH, ".//input[@type='radio']")
            options, opt_map = [], {}
            for rb in radios:
                try:
                    lbl = driver.find_element(By.XPATH, f"//label[@for='{rb.get_attribute('id')}']").text.strip()
                except:
                    lbl = rb.get_attribute("value") or "Option"
                options.append(lbl)
                opt_map[lbl.lower()] = rb

            # skip junk fields
            if any(jk in question_label.lower() for jk in ["posted", "openings", "applicants"]):
                print(f"Skipping junk field: {question_label}")
                continue

            ai_prompt = f'''Question: {question_label}
                        Options: {options}
                        Pick the best matching option **from the list only**. 
                        Respond with exactly one of the options, nothing else.'''
            print(ai_prompt)
            choice = get_ai_answer(ai_prompt, profile).lower().strip()
            print("AI picked:", choice)

            # match choice
            match = None
            for opt, rb in opt_map.items():
                if choice in opt or opt in choice:
                    match = rb
                    break
            if not match:
                match = radios[-1]

            driver.execute_script("arguments[0].click();", match)
            print(f"→ Picked: {choice}")

            # click Save if exists
            try:
                save_btn = driver.find_element(By.XPATH, "//div[@class='sendMsg' and normalize-space(text())='Save']")
                driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
                driver.execute_script("arguments[0].click();", save_btn)
                print("Clicked Save button")
                time.sleep(1)
            except:
                pass
    except Exception as e:
        print("Radio button handling failed:", e)


    return False
 
    

def fill_dynamic_form(driver, profile):
    labels = driver.find_elements(By.XPATH, "//label")
    for label in labels:
        ques = label.text.strip()
        if not ques:
            continue
        answer = get_ai_answer(ques, profile)
        if fill_field_by_label(label, answer, driver=driver, question=ques, profile=profile):
            print(f"Filled '{ques}' → {answer}")
        else:
            print(f"⚠ Could not fill '{ques}'")
