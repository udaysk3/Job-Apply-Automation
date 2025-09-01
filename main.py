import time
from helper_functions import wait_for_new_question, get_latest_question
from user_profile import user_profile, JOINING_DATE
from ai_helper import get_ai_answer
from selenium_helper import start_browser, fill_dynamic_form, fill_field_by_label
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# ==============================
# Job Application Automation
# ==============================
def apply_jobs(profile):
    driver = start_browser()

    # Step 1: Login
    driver.get("https://www.naukri.com/")
    time.sleep(3)

    try:
        driver.find_element(By.XPATH, "//div[contains(@class,'modal')]/div/button").click()
    except:
        pass

    driver.find_element(By.XPATH, "//a[@title='Jobseeker Login']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']").send_keys(profile["email"])
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys(profile["password"])
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    time.sleep(6)

    # Step 2: Recommended Jobs
    driver.get("https://www.naukri.com/mnjuser/recommendedjobs?tabClusterId=profile")
    time.sleep(5)

    job_cards = driver.find_elements(By.CLASS_NAME, "jobTuple")
    print(f"\nFound {len(job_cards)} jobs to apply.")

    for idx, card in enumerate(job_cards, start=1):
        try:
            print(f"\n--- Opening job #{idx} ---")
            card.click()
            time.sleep(3)

            windows = driver.window_handles
            if len(windows) > 1:
                driver.switch_to.window(windows[-1])

            # Apply
            try:
                driver.find_element(By.XPATH, "//button[contains(text(),'Apply')]").click()
                time.sleep(3)
            except:
                print("No Apply button.")
                driver.close()
                driver.switch_to.window(windows[0])
                continue

            # Chatbot Mode
            try:
                # Keep answering until no new question appears
                while True:
                    questions = driver.find_elements(By.XPATH, "//div[contains(@class,'botMsg')]")
                    old_count = len(questions)

                    latest_question = get_latest_question(driver)
                    if not latest_question:
                        print("⚠ No valid question found → stopping chatbot.")
                        break
                    print("Bot asked:", latest_question)

                    # AI generates answer dynamically
                    ans = get_ai_answer(latest_question, profile)
                    
                    # Find chat input and type the answer
                    chat_input = driver.find_element(By.XPATH, "//div[contains(@class,'textArea') and @contenteditable='true']")
                    chat_input.click()
                    chat_input.send_keys(ans)
                    chat_input.send_keys(Keys.ENTER)

                    time.sleep(2)  # wait for bot to respond
                    if not wait_for_new_question(driver, old_count, timeout=10):
                        print("No new question → chatbot finished.")
                        break
                print("Filled chatbot form")

            except Exception as e:
                print("Chatbot answering failed:", e)
                fill_dynamic_form(driver, profile)


            # Submit
            try:
                driver.find_element(By.XPATH, "//button[contains(text(),'Submit') or contains(text(),'Apply')]").click()
                print("✅ Application Submitted")
            except:
                print("⚠ No final Submit button / Already applied")

            time.sleep(2)
            driver.close()
            driver.switch_to.window(windows[0])
            time.sleep(2)

        except Exception as e:
            print("Error in job #", idx, ":", e)
            driver.switch_to.window(driver.window_handles[0])

    print("\n🎉 All jobs processed.")
    driver.quit()

# ==============================
# Main Run
# ==============================
if __name__ == "__main__":
    apply_jobs(user_profile)
