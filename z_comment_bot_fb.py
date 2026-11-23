from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import traceback
import re

# === Facebook Reels & Posts with Comments ===
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


video_comments = load_comments("comments_fb.csv")



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

success_count = 0
failed_urls = []

# === Filter out non-BMP characters (fix emoji crash in ChromeDriver)
def remove_non_bmp(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

def post_comment(url, comment_text):
    try:
        driver.get(url)
        time.sleep(5)
        print(f"\n🔗 Opening: {url}")

        # === Handle Reels ===
        if "/reel/" in url:
            print("🌀 Reels: Clicking comment button...")
            comment_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button'][aria-label='Comment']"))
            )
            comment_btn.click()
            time.sleep(3)

            comment_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox'][contenteditable='true']"))
            )

        # === Handle Posts ===
        else:
            print("🗒️ Post: Locating comment box...")
            driver.execute_script("window.scrollBy(0, 600);")
            time.sleep(2)

            comment_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox'][contenteditable='true']"))
            )

        # === Scroll to and click box
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comment_box)
        comment_box.click()
        time.sleep(1)

        # === Clean and type comment manually
        clean_comment = remove_non_bmp(comment_text)

        for char in clean_comment:
            comment_box.send_keys(char)
            time.sleep(random.uniform(0.04, 0.1))

        comment_box.send_keys(Keys.ENTER)
        print(f"✅ Commented successfully on: {url}")
        return True

    except Exception as e:
        print(f"❌ Failed to comment on: {url}")
        traceback.print_exc()
        driver.save_screenshot(f"fb_error_{int(time.time())}.png")
        return False

# === Run all
for url, comment in video_comments:
    if post_comment(url, comment):
        success_count += 1
    else:
        failed_urls.append(url)
    time.sleep(random.uniform(5, 9))

# === Final summary
print(f"\n🎉 All done!\n✅ Success: {success_count} / {len(video_comments)}")
if failed_urls:
    print("❌ Failed URLs:")
    for u in failed_urls:
        print(" -", u)

driver.quit()
