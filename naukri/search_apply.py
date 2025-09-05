import time
from helper_functions import wait_for_new_question, get_latest_question
from user_profile import user_profile, JOINING_DATE
from ai_helper import get_ai_answer
from selenium_helper import start_browser, fill_dynamic_form, fill_field_by_label
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# ==============================
# Job Application Automation (Search Mode)
# ==============================
def search_and_apply_jobs(profile, keyword, experience, location=""):
    driver = start_browser()
    external_urls = []  # store company site application links

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

    # Step 2: Go to Dashboard
    driver.get("https://www.naukri.com/mnjuser/homepage")  
    time.sleep(5)

    # Step 3: Open Search Bar
    search_bar = driver.find_element(By.CLASS_NAME, "nI-gNb-sb__main")
    search_bar.click()
    time.sleep(2)

    # Now inputs are active (tabindex=0)
    keyword_input = driver.find_element(By.XPATH, "//input[@placeholder='Enter keyword / designation / companies']")
    keyword_input.clear()
    keyword_input.send_keys(keyword)

    # Experience Dropdown
    exp_input = driver.find_element(By.ID, "experienceDD")
    exp_input.click()
    time.sleep(1)
    if experience == 0:
        exp_option = driver.find_element(By.XPATH, f"//ul[@class='dropdown ']/li[@title='Fresher']")
    else:
        exp_option = driver.find_element(By.XPATH, f"//ul[@class='dropdown ']/li[@title='{experience} years']")
    exp_option.click()

    # Location (optional)
    if location:
        loc_input = driver.find_element(By.XPATH, "//input[@placeholder='Enter location']")
        loc_input.clear()
        loc_input.send_keys(location)

    # Click Search button
    driver.find_element(By.XPATH, "//button[@class='nI-gNb-sb__icon-wrapper']").click()
    time.sleep(6)

    # ==============================
    # Step 4: Process Jobs with Pagination
    # ==============================
    page = 1
    while True:
        print(f"\n📄 Processing Page {page}...")
        job_cards = driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")

        if not job_cards:
            print(f"❌ No jobs found on page {page}, stopping pagination.")
            break

        print(f"Found {len(job_cards)} jobs for '{keyword}' with {experience} years exp.")

        for idx, card in enumerate(job_cards, start=1):
            try:
                print(f"\n--- Opening job #{idx} on page {page} ---")
                card.click()
                time.sleep(3)

                windows = driver.window_handles
                if len(windows) > 1:
                    driver.switch_to.window(windows[-1])

                # Check if "Apply on company site" button exists
                try:
                    external_btn = driver.find_element(By.ID, "company-site-button")
                    external_btn.click()
                    time.sleep(3)

                    # Switch to new window (company site)
                    windows = driver.window_handles
                    if len(windows) > 1:
                        driver.switch_to.window(windows[-1])
                        external_url = driver.current_url
                        print(f"🌐 External job site detected → {external_url}")
                        # external_urls.append(external_url)
                        with open("external_jobs.txt", "a", encoding="utf-8") as f:
                            f.write(external_url + "\n")
                        driver.close()
                        driver.switch_to.window(windows[0])
                        continue
                except:
                    pass


                # Try Apply
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
                    while True:
                        questions = driver.find_elements(By.XPATH, "//div[contains(@class,'botMsg')]")
                        old_count = len(questions)

                        latest_question = get_latest_question(driver)
                        if not latest_question:
                            print("⚠ No valid question found → stopping chatbot.")
                            break
                        print("Bot asked:", latest_question)

                        ans = get_ai_answer(latest_question, profile)
                        print("AI answered:", ans)

                        chat_input = driver.find_element(By.XPATH, "//div[contains(@class,'textArea') and @contenteditable='true']")
                        chat_input.click()
                        chat_input.send_keys(ans)
                        chat_input.send_keys(Keys.ENTER)

                        time.sleep(2)
                        if not wait_for_new_question(driver, old_count, timeout=10):
                            print("No new question → chatbot finished.")
                            break
                    print("✅ Filled chatbot form")

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

        # ==============================
        # Next Page Handling
        # ==============================
        try:
            pagination = driver.find_element(By.CLASS_NAME, "styles_pagination__oIvXh")
            next_button = pagination.find_element(By.XPATH, ".//a[span[text()='Next']]")

            # Check if disabled
            if "disabled" in next_button.get_attribute("class"):
                print("✅ Reached last page.")
                break
            else:
                driver.execute_script("arguments[0].click();", next_button)  # safer than normal click
                time.sleep(5)
                page += 1
                continue
        except:
            print("✅ No more pages found.")
            break

    # Save external job URLs
    # if external_urls:
    #     with open("external_jobs.txt", "w", encoding="utf-8") as f:
    #         for url in external_urls:
    #             f.write(url + "\n")
    #     print(f"\n🌍 Saved {len(external_urls)} external job URLs to external_jobs.txt")

    print("\n🎉 All jobs processed.")
    driver.quit()


# ==============================
# Main Run
# ==============================
if __name__ == "__main__":
    search_and_apply_jobs(
        profile=user_profile,
        keyword="Python Developer",   # <-- Change this
        experience=2,                 # <-- Change this
        location="Hyderabad"          # <-- Optional
    )
