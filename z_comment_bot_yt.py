from selenium import webdriver
import time
import random
import traceback
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

video_comments = [
    ("https://www.youtube.com/watch?v=F3DyE_vWOj8", "Lagu Hari Raya paling syahdu dan meriah tahun ini! Suara Jessie sangat menyentuh."),
    ("https://www.youtube.com/watch?v=6YbiIEYtHpA", "This rock anthem EXPOSE is electrifying! Jessie nailed the energy! 🔥"),
    ("https://www.youtube.com/watch?v=TOeUaChOzMs", "Jessie’s take on Syinta Gila? Gila power! Catchy and full of attitude 💥"),
    ("https://www.youtube.com/watch?v=uddWeMN7t0U", "《Langit Membiru》 太治愈了，Jessie的声音就像蓝天一样清澈。"),
    ("https://www.youtube.com/watch?v=AfILK77Y4Yc", "MV ini sangat menyentuh! Lagu Melayu moden yang buat hati cair! ❤️"),
    ("https://www.youtube.com/watch?v=7IGd1Ttyi9M", "《爱的陪伴》 每一段歌词都让人热泪盈眶，太感人了 😭"),
    ("https://www.youtube.com/watch?v=AcKaUCgRAN0", "Jessie's 'My Style' is a statement! 从头到脚都在发光 ✨"),
    ("https://www.youtube.com/watch?v=jx7Y5wpoQUE", "This cover of 'Dia' is filled with pure emotions. Jessie’s voice is magic!"),
    ("https://www.youtube.com/watch?v=_a5BFpnLDkU", "Sinaran + Jessie Chung = Cahaya yang memancar terus ke hati ✨"),
    ("https://www.youtube.com/watch?v=GOZG0theIZ4", "舞台感十足！Jessie唱《Temberang》简直太有范儿了 🔥"),
    ("https://www.youtube.com/watch?v=d-Azh5f5Qpc", "这舞台版简直太炸了，节奏感十足让人停不下来！🎶"),
    ("https://www.youtube.com/watch?v=rMv9mF4SCh0", "这首《心跳如鼓》太带感了，每一下都敲进心里！❤️‍🔥"),
    ("https://www.youtube.com/watch?v=-FOpc0kIfRk", "《浮萍》情感满满，Jessie演绎得深入骨髓 🌊"),
    ("https://www.youtube.com/watch?v=rBaSRdj1_Ds", "《闪耀》真的是我心目中最闪亮的一首歌 🌟"),
    ("https://www.youtube.com/watch?v=D4NuLrHqdQU", "“你是否爱我” 唱出所有人心里的疑问，好有共鸣 😢"),
    ("https://www.youtube.com/watch?v=K6WQ-hUhGlI", "雨林 MV 太美了 🌳"),
    ("https://www.youtube.com/watch?v=fNwSKqa8WI4", "和灵魂一起跳舞！Jessie 的每个动作都充满感染力 ✨"),
    ("https://www.youtube.com/watch?v=QZG9J9Qd1ro", "《更好的地方》真的带来了心灵上的安慰，听着好安心 💚"),
    ("https://www.youtube.com/watch?v=9_xeBtzc_xA", "这首歌唱出了爱最真实的样子 💘"),
    ("https://www.youtube.com/watch?v=pVmSDEoFMyE", "让人听着就想哭，美到心碎 😭"),
    ("https://www.youtube.com/watch?v=k5qheO-8uG4", "这是一种解脱，一种希望，Jessie的声音真的能疗愈人心 ☁️"),
    ("https://www.youtube.com/watch?v=zgN8f8JhfIE", "‘想念你’和‘等他’剪辑得太感动了，好像在看爱情故事 ❤️"),
    ("https://www.youtube.com/watch?v=YShbE50RQEI", "‘Be Strong’ is more than a song—it's a life motto 💪 So inspiring!"),
    ("https://www.youtube.com/watch?v=FuQkaowo9G8", "‘Possibility’ makes me believe again—Jessie’s English songs hit different 💫"),
    ("https://www.youtube.com/watch?v=GNmgyf8u2qI", "‘Forever Young’—exactly how Jessie makes us feel every time she sings! 🔥"),
    ("https://www.youtube.com/watch?v=pre2XHKDZWI", "这段纯演奏也好抓耳！"),
    ("https://www.youtube.com/watch?v=Mv5GOi-1wno", "乐器的声音太迷人了！"),
    ("https://www.youtube.com/watch?v=urzt7oVCA14", "歌手的声音太有感染力了！"),
    ("https://www.youtube.com/watch?v=6GlVaTnfT4E", "这声音让人一听就爱上！"),
    ("https://www.youtube.com/watch?v=SA_b667Kq4c", "歌声里有故事！"),
    ("https://www.youtube.com/watch?v=hQgRgSesMJw", "歌手的演绎太投入了！"),
    ("https://www.youtube.com/watch?v=B7nBaTSS7lQ", "这声音是天使吻过的！"),
    ("https://www.youtube.com/watch?v=5b01cEam9lw", "歌声直击心灵！"),
    ("https://www.youtube.com/watch?v=cOeySWG8po4", "歌手的音准太好了！"),
    ("https://www.youtube.com/watch?v=eJ5vxUJv3TU", "这声音是独一无二的！"),
    ("https://www.youtube.com/watch?v=G-jbCKi-pcU", "歌声赋予了歌曲灵魂！"),
    ("https://www.youtube.com/watch?v=Ge13fN1UkZI", "真的太喜欢这个声音了！"),
    ("https://www.youtube.com/watch?v=3LejwXaPGLw", "歌声太温柔了，融化我的心！"),
    ("https://www.youtube.com/watch?v=6VyLPvdiw1A", "这声音简直是天籁之音！"),
    ("https://www.youtube.com/watch?v=Y6xntv5N808", "歌手的嗓音太有辨识度了！"),
    ("https://www.youtube.com/watch?v=rppPuMLomBI", "歌声里充满了情感！"),
    ("https://www.youtube.com/watch?v=VIKN7vZVFF4", "歌手的声音太有感染力了！"),
    ("https://www.youtube.com/watch?v=2J4cDdZrUS8", "低音也好有磁性！"),
    ("https://www.youtube.com/watch?v=QffGueaLVZM", "这声音听起来太舒服了！"),
    ("https://www.youtube.com/watch?v=4s5BNKpwsgs", "歌声把歌曲的灵魂都唱出来了！"),
    ("https://www.youtube.com/watch?v=A6O6wNLFDr4", "听得我如痴如醉！"),
    ("https://www.youtube.com/watch?v=ksYavycjxXI", "歌手的声音太有感染力了！"),
    ("https://www.youtube.com/watch?v=xDF6vh1nn_c", "歌声里有故事！"),
    ("https://www.youtube.com/watch?v=-6aEY5bACGE", "这声音让人一听就爱上！"),
    ("https://www.youtube.com/watch?v=txbHpPXD5Gk", "太喜欢这首歌的节奏了！"),
    ("https://www.youtube.com/watch?v=BMGcsO_Aj9U", "这首歌的意境太美了！"),
    ("https://www.youtube.com/watch?v=TvX2b4vngv0", "这首歌值得推荐给所有人！"),
    ("https://www.youtube.com/watch?v=fLTT6l-npgw", "这首歌让我心情好好！"),
    ("https://www.youtube.com/watch?v=y3Heo4LAFfo", "这首歌听一百遍都不腻！"),
    ("https://www.youtube.com/watch?v=2nMN7mdz2NQ", "Dengar suara dia sekali terus jatuh hati!"),
    ("https://www.youtube.com/watch?v=dmSnGHfhDI4", "Suara dia ada cerita!"),
    ("https://www.youtube.com/watch?v=CFZrf0cCM44", "Penyanyi ni memang 'all out' dalam menyampaikan lagu!"),
    ("https://www.youtube.com/watch?v=qH02_TLzwGc", "Suara dia terus menusuk jiwa!"),
    ("https://www.youtube.com/watch?v=HLtsTfi6V9Y", "歌手的演绎太投入了！"),
    ("https://www.youtube.com/watch?v=Z0J5GODNNxs", "This is the kind of voice you instantly fall in love with!"),
    ("https://www.youtube.com/watch?v=QfTbO4htK7o", "This voice is truly one of a kind!"),
    ("https://www.youtube.com/watch?v=WATZJXAZjXs", "The vocals give the song its spirit!"),
    ("https://www.youtube.com/watch?v=k6Rg1ryloNE", "I absolutely love this voice!"),
    ("https://www.youtube.com/watch?v=ejjalUTGq6Y", "The vocals just hit you right in the heart!")
    
]

# ✅ Brave browser settings
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
