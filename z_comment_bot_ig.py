from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
import traceback
import random

import csv
import os
import sys


def load_comments(default_name):
    """Load (url, comment) rows from a CSV with headers: url,comment.

    File used: 1st command-line argument > default file next to this script > file picker.
    """
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), default_name)
    if not os.path.exists(path):
        from tkinter import Tk, filedialog
        root = Tk()
        root.withdraw()
        path = filedialog.askopenfilename(title=f"Select comments file ({default_name})", filetypes=[("CSV files", "*.csv")])
        root.destroy()
        if not path:
            sys.exit("❌ No comments file selected.")
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = [(r["url"].strip(), (r["comment"] or "").strip()) for r in csv.DictReader(f) if (r.get("url") or "").strip()]
    rows = [(u, c) for u, c in rows if c]
    print(f"📄 Loaded {len(rows)} comments from {path}")
    return rows


video_comments = load_comments("comments_ig.csv")



# ✅ Brave browser profile and binary
chrome_user_path = os.path.join(os.environ["LOCALAPPDATA"], "BraveSoftware", "Brave-Browser", "User Data")
profile_name = "Default"
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

options = webdriver.ChromeOptions()
options.binary_location = brave_path
options.add_argument(f"user-data-dir={chrome_user_path}")
options.add_argument(f"profile-directory={profile_name}")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

def comment_on_instagram(url, comment_text):
    try:
        driver.get(url)
        print(f"\n📷 Opening: {url}")
        time.sleep(5)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[aria-label='Add a comment…']"))
        )
        print("✅ Textarea loaded!")

        # Find fresh textarea
        textarea = None
        for _ in range(3):
            try:
                textarea = driver.find_element(By.CSS_SELECTOR, "textarea[aria-label='Add a comment…']")
                driver.execute_script("arguments[0].focus();", textarea)
                textarea.clear()
                textarea.send_keys(comment_text)
                print(f"💬 Typed full comment: {comment_text}")
                break
            except StaleElementReferenceException:
                print("♻️ Retrying textarea (stale)...")
                time.sleep(1)

        if not textarea:
            raise Exception("❌ Could not access a fresh textarea.")

        # Click the Post button
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form//div[text()='Post']"))
        )
        driver.execute_script("arguments[0].click();", post_button)
        print("✅ Comment posted!")
        return True

    except Exception as e:
        print(f"❌ Failed to comment on: {url}")
        traceback.print_exc()
        driver.save_screenshot(f"ig_error_{int(time.time())}.png")
        return False

# Run all comments
success_count = 0
for url, text in video_comments:
    if comment_on_instagram(url, text):
        success_count += 1
    time.sleep(random.uniform(4, 6))

print(f"\n🎉 Done. {success_count}/{len(video_comments)} comments posted.")
driver.quit()
