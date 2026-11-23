from selenium import webdriver
import time
import random
import traceback
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


video_comments = load_comments("comments_yt.csv")

# ✅ Brave browser settings
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

success_count = 0
failed_urls = []
disabled_comments = []

start_time = datetime.now()

def post_comment(video_url, comment_text):
    try:
        driver.get(video_url)
        print(f"\n🔍 Opening: {video_url}")
        time.sleep(6)

        # Scroll to reveal comments
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(2)

        # ✅ Try to find comment area (if not found = disabled or not loaded)
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "placeholder-area")))
        except:
            print(f"🚫 Comments disabled or not loaded: {video_url}")
            disabled_comments.append(video_url)
            return False

        # Click comment area
        placeholder = driver.find_element(By.ID, "placeholder-area")
        placeholder.click()
        time.sleep(2)

        # Type comment
        comment_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#contenteditable-root"))
        )
        for char in comment_text:
            comment_area.send_keys(char)
            time.sleep(random.uniform(0.05, 0.1))

        # Click post
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "submit-button"))
        )
        post_button.click()

        print(f"✅ Commented on: {video_url}")
        time.sleep(4)
        return True

    except Exception as e:
        print(f"❌ Failed on: {video_url}")
        traceback.print_exc()
        failed_urls.append(video_url)
        driver.save_screenshot("comment_error.png")
        return False

# Run the bot
for url, comment in video_comments:
    if post_comment(url, comment):
        success_count += 1

driver.quit()

# Results
end_time = datetime.now()
duration = end_time - start_time

print("\n🎉 Done!")
print(f"✅ Success: {success_count}")
print(f"❌ Failed: {len(failed_urls)}")
print(f"🚫 Comments Disabled: {len(disabled_comments)}")
print(f"🕒 Time taken: {duration}")

if failed_urls:
    print("\n❌ Failed URLs:")
    for url in failed_urls:
        print(f" - {url}")

if disabled_comments:
    print("\n🚫 Comments Disabled URLs:")
    for url in disabled_comments:
        print(f" - {url}")
