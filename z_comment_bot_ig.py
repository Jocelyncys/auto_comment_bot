from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
import traceback
import random

video_comments = [
    ("https://www.instagram.com/p/DIF2WjftxEq/", "Absolutely glowing—your beauty is beyond words!"),
    ("https://www.instagram.com/p/DIDkQqAt8_z/", "歌词好触动人心，情感满满！"),
    ("https://www.instagram.com/p/DIBC3EXteV6/", "Satu suara raya yang penuh semangat dan keindahan!"),
    ("https://www.instagram.com/p/DIA74tOt7Yq/", "Love you always! Your presence brings comfort every time ❤️"),
    ("https://www.instagram.com/p/DH-os2MSx5d/", "恭喜登上榜首！实力和魅力兼具！"),
    ("https://www.instagram.com/p/DH75TIxNAJN/", "Hari Raya vibes ✨ Your smile brings all the joy!"),
    ("https://www.instagram.com/p/DH7g-VeSGf_/", "你是全球的骄傲，一直以来都那么优秀！"),
    ("https://www.instagram.com/p/DH5PPDAyT0h/", "这封面真的太高级了，完全是视觉盛宴！"),
    ("https://www.instagram.com/p/DH-gFsxNGhY/", "满满正能量，让人感受到生活的美好🌟"),
    ("https://www.instagram.com/p/DH4z3L1Sld7/", "Jessie 每一次的作品都令人惊艳，太美了！"),
    ("https://www.instagram.com/p/DH2fldYy8Ut/", "Selamat Hari Raya! Moga bahagia sentiasa bersama kamu 💛"),
    ("https://www.instagram.com/p/DH0CIUDtbb2/", "Style + confidence = icon! Totally slaying it 🔥"),
    ("https://www.instagram.com/p/DHzxwpnSO3Z/", "这表现力真的太强了，简直像电影级别！"),
    ("https://www.instagram.com/p/DHxw2sHSJY0/", "Princess vibes on full display—you're radiant! 👑"),
    ("https://www.instagram.com/p/DHvAemrtAkH/", "你的嗓音简直是天籁，每一句都打动我！"),
    ("https://www.instagram.com/p/DHsZEm1Ng6M/", "大事即将发生！5am 注定不凡✨"),
    ("https://www.instagram.com/p/DHsIvrKybhZ/", "这首歌的信息太强烈了，感动人心！"),
    ("https://www.instagram.com/p/DHsIXWRSJE3/", "标准被你重新定义了！佩服！"),
    ("https://www.instagram.com/p/DHpyvFMSZqt/", "你一直都在发光发热，谢谢你的力量💖"),
    ("https://www.instagram.com/p/DHpfxQmtmOQ/", "感恩的心，让你的光芒更闪耀✨"),
    ("https://www.instagram.com/p/DHnod0VyT5q/", "未来一定更加精彩，继续期待你的惊喜！"),
    ("https://www.instagram.com/p/DHnBJDVSmNF/", "每次都大杀四方！超有气场🔥"),
    ("https://www.instagram.com/p/DHmt6XWybgK/", "So cute and full of life! You're sunshine in human form ☀️"),
    ("https://www.instagram.com/p/DHklFxwtYmb/", "这首歌百听不厌，永远的最爱！"),
    ("https://www.instagram.com/p/DHZ3I-SNddM/", "You’ve always been my muse. Inspiring and brilliant."),
    ("https://www.instagram.com/p/DHXetxPt5l9/", "保持知足的心，幸福就会一直在身边。"),
    ("https://www.instagram.com/p/DHU97Z7NDVS/", "Your energy lights up my whole day—thank you! 🌈"),
    ("https://www.instagram.com/p/DHKrd_VNiLk/", "你真的太迷人了，每个细节都值得喜欢！"),
    ("https://www.instagram.com/p/DHNsENGNHve/", "你的舞台能量太炸裂，完全被吸引住了！"),
    ("https://www.instagram.com/p/DHDg9scN8p5/", "You're a shining star in every way! 🌟"),
    ("https://www.instagram.com/p/DHA1VlvNXVR/", "Nailed it again, Jessie! You make everything magical."),
    ("https://www.instagram.com/p/DG7xKm4Ny3B/", "每看一次都让我想努力追梦！"),
    ("https://www.instagram.com/p/DG7v4k2tbQj/", "Chart queen forever! You rule hearts too!"),
    ("https://www.instagram.com/p/DG42EcaNnWx/", "音乐界的王者，你当之无愧！"),
    ("https://www.instagram.com/p/DG2KWYqN29M/", "完美诠释了什么是全能艺人👏"),
    ("https://www.instagram.com/p/DGz9YQ5tKwe/", "每一首都成神曲，实力不允许低调！"),
    ("https://www.instagram.com/p/DGxPBvDN0io/", "🔥 这MV真的是视觉与音乐的双重享受！"),
    ("https://www.instagram.com/p/DGuMzdDNLzJ/", "这MV像电影一样，每个镜头都好美！🎬"),
    ("https://www.instagram.com/p/DGsL46-NH3q/", "词曲情感太足了，完全打动我！🎶"),
    ("https://www.instagram.com/p/DGm-hHLNx3u/", "妳真的是梦中情人那种 vibe！💫"),
    ("https://www.instagram.com/p/DGkV7IhN0Nx/", "你的出现就像阳光照进心里～☀️"),
    ("https://www.instagram.com/p/DGfD0BEtQo1/", "你的音乐真的有治愈心灵的魔法✨"),
    ("https://www.instagram.com/p/DGclAklNyDJ/", "Every note soothes my soul. This album = healing."),
    ("https://www.instagram.com/p/DGcSJijtG4l/", "优雅、自信、美丽的结合体。完美！"),
    ("https://www.instagram.com/p/DGYpYrct4wL/", "你简直统治了整个舞台！太强了！"),
    ("https://www.instagram.com/p/DGVJ7vkySLx/", "感受到了你满满的真情，每句都走心💗"),
    ("https://www.instagram.com/p/DGPo4AnNjEs/", "You're my daily dose of inspiration! Keep soaring!"),
    ("https://www.instagram.com/p/DGK1BFvNmEm/", "新的一季开启了你的光芒旅程✨"),
    ("https://www.instagram.com/p/DGCQNBMNl1O/", "美到像从天上下凡的女神！"),
    ("https://www.instagram.com/p/DGBnjaST04y/", "你甜美又有力量，是个天使无疑💫"),
    ("https://www.instagram.com/p/DF9RTQvtS1T/", "每天看一次，就觉得充满希望✨"),
    ("https://www.instagram.com/p/DFpicMXzmY_/", "从头到脚都时尚到位，太会穿了！"),
    ("https://www.instagram.com/p/DFe64TTyMJZ/", "每次出镜都发光发亮，美得不像话！"),
    ("https://www.instagram.com/p/DF7Ea-bNSph/", "这颜值简直像仙子下凡，美翻天了！"),
    ("https://www.instagram.com/p/DFZxfVPTf1d/", "Jessie 的气场就是女王级别，无敌！"),
    ("https://www.instagram.com/p/DFVfgcNSduP/", "妳的妆容和穿搭总是引领潮流 👗✨"),
    ("https://www.instagram.com/p/DFSFPm1SQEr/", "每个造型都让我惊艳，期待下一套！"),
    ("https://www.instagram.com/p/DFQZw4nSzge/", "这套穿搭完美到不行，太爱了！😍"),
    ("https://www.instagram.com/p/DGwsZsoNxlM/", "好喜欢你的 vibe，真是被你圈粉了～")
]



# ✅ Brave browser profile and binary
chrome_user_path = r"C:\Users\Jocelyn Cheong.DESKTOP-2UCUSM0\AppData\Local\BraveSoftware\Brave-Browser\User Data"
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
