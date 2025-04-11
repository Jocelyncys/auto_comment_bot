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
video_comments = [
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02eNNqitRNDV9Thb49Hge9W4p26eSfv2xADDr5ZsZVGvBjNzC8Um9mdz8Xk7LbFp1sl", "這張封面設計超有個性，完全彰顯了你的獨特魅力，真的好棒"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid034ZqVacACXwi38k1iEvmd5gujLPH9JnHembh3kCMauKMWryU9P7bWBotAdiD3nfbRl", "這首歌我循環播放一整天了，旋律太抓耳，你的嗓音簡直天籟"),
    ("https://www.facebook.com/jessiechung.official/videos/1785059595576952/", "已經開始倒數演唱會的日子了！你的現場表演總是無與倫比"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid0zCMuZSKTDfrMzkWTEPcnopfSZgexNgLf2g7FYAnRhBXHNrTuF1Gnxx1Gfs8b6un1l", "看到你稱霸樂壇真的讓我們好驕傲，繼續發光發熱吧"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid035FNU9yNcbtHY9X6gLfbMjag3dBJxXwkAPQKnr42szpvnxeXwMSzyp7fRskqoMv1Zl", "你不斷突破自我，每次作品都展現真正的藝術家風範"),
    ("https://www.facebook.com/reel/1442991067072334", "開齋節快樂！願你和家人度過充滿歡樂的美好時光"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02G8iTcpPtwRMPXzGQdWTnoDXMVACbPQEuXZeQcUP69DKByFz1ReRpEcqkumsFDDZfl", "你的馬來歌曲太完美了，歌聲中的情感每次都讓我起雞皮疙瘩"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02G6kSjAoxEJMyn5GKVmw6XYSVKm14HVhaHmKWBff5tQAzvTLqNRsyR5G7QbtroojXl", "開齋節快樂！願你的家中充滿愛與歡笑"),
    ("https://www.facebook.com/reel/629714583252247", "怎麼可以這麼美？你的美麗是由內而外散發的"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid0xmFbFCxxjDRsok7XRrnQPJBsEaKhB2SjvkvuEqJw52yz6LcQf6MMehc4soNqrQftl", "全國都為你的音樂著迷，這就是真正的實力"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid0pKt6u3zrhsLswgMbp1APT8UpjAMVCbV78GNv29okx2CYcomuUDmS2KXx3ZaU4tLpl", "你的音樂跨越國界！世界需要聽到更多你美妙的聲音"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02UBDv35gQnoosEfR5cFpMFhuJgqjpSWTa8DJFrsPZjESzNjKsRKp9bAeghW9xGg1sl", "你青春的活力和魅力太有感染力了，總是能照亮我們的日子"),
    ("https://www.facebook.com/reel/1048602107111784", "預告片讓我對新作品超級期待！你的創意總是無限"),
    ("https://www.facebook.com/reel/1440125846956052", "5am這首歌太有創意了，氛圍感十足，絕對是我的新寵"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid0iGt18Se764UqsoAS7WaybSk46VZSNexPzpowyrYuBvU2qFUhuFXnv4FwxCKDgH74l", "這張專輯發行後就一直在我的播放清單裡，每首歌都是傑作"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid0fQZ4Z1pT29fFMFcgSwf8p7JkiqTBYB3Y9ZkLEEAsDLyCe4rvmoGvEZfHfTe84KiUl", "你正在創造歷史！看到你在全球崛起真的好驕傲"),
    ("https://www.facebook.com/jessiechung.official/videos/1065265055455173/", "你的聲音一直是我人生的配樂，請繼續創造奇蹟"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02ABW6aBgJN78rFA3zNrZjH1C3wNbc6ghAFudJNdBtaRzBWJG74L2LX4E6rC4tLWZSl", "Text me, 这首歌太完美了，歌詞、旋律和你的嗓音都無可挑剔"),
    ("https://www.facebook.com/reel/1181043136994011", "這短视频太感人了，讓我熱淚盈眶"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid029qqwfhpsFvGnzzzZ5z1mq8UZQcm7tGy2f2jpwTqAyfR3FyPwP36KgzNtcVivFk7Cl", "又一次完美的演出！你從來不會讓人失望"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid035K5qAs2xAiyo5MioGQSDLLvfPoE843DS9fZ7HAGBcuZLz1iTvP7GqWFq8GAb1GTVl", "稱霸排行榜對你來說輕而易舉！實力說明一切"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid0LYbVZezuherYKGjiD5rVStCjngRX3Zjsf7PWVhUbnecNvC18SX1m6WZ8Siaztau4l", "等待這首新歌讓我度日如年！你的音樂總是能治癒我的心靈"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid034MPNWGUnrrphqEwUnQkReB5KzpTWJmxZ9zouvr3cZ9LXbnvtowhL3gaFEAGbYx8ql", "你的馬來歌曲與眾不同！歌聲中的情感和力量無人能及"),
    ("https://www.facebook.com/reel/1571328280035677", "你的每次表演都讓我的心跳漏一拍，舞台魅力太強了"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid0kPJegsLZdN8MnN2KoZkzUHtdbZ4NLgvXEeZ1ENsdD8FgYs3GLWHVbNyV9DgMnkrYl", "已經買好票了！親身感受你的魔力是無可替代的體驗"),
    ("https://www.facebook.com/reel/1707511336861883", "關於感恩的這段話真的觸動我的心，謝謝你的提醒"),
    ("https://www.facebook.com/reel/1226939435623156", "有你出現的每個畫面都是藝術！你的視覺效果總是令人驚艷"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02Dy1p1YhJPPxQ53v961QAoTeugB4BnpyKn4G4UB5dQuEhq4i4B6wksYACfjeL7DRml", "期待值爆表！等不及看你為我們準備了什麼驚喜"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02xCpFeZGdjXncMFh276iwkDr4AeRZQVjVvPFrz22JSmuJMJwN5LvfWT3xvJ3vwU9Sl", "這可能是你至今最棒的作品！製作水準太高了"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid0YUzFyof9QNQv7MuonWKcLrY2S7koqGeFfag98uWE56zRAq1UvPebSHWRoGYCBGq2l", "倒數計時MV上線的每一分鐘！你的視覺效果總是經典"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02HpTZECtBq2T6mBJfLywMM679NoEm3ch2BaEgU7hKtfSvz6NTM93MMcPDehqyKa8Xl", "演唱會倒數開始！準備好現場體驗音樂的完美"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid0dUBBeUCMj1bTUNVAzwZq7ktc1kWyQkd12Zj6pZ4ZKyec7YZSAsEHTKvqG5nYujUVl", "你的演出總是傳奇"),
    ("https://www.facebook.com/reel/664627099425799", "這首歌就像音頻黃金！你的聲音如蜜般甜美"),
    ("https://www.facebook.com/reel/610841571826266", "MV的美學太棒了，簡直是視覺傑作"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02ahrYDjM3T3GBFK9JcAWiAHgZm5wTNdyy3kPhZiMfZwDZnMfL8xR89SwLmrzU3rCZl", "靠近你這張專輯不斷循環播放！每首歌都很精彩"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid07U8bRN1E1sRb12ayJqWTvS6aGK9YqeAAYXAGC14yMSo1keGhKp7UPpk2njUmYDe7l", "這支MV的未來概念太震撼了，超前時代"),
    ("https://www.facebook.com/reel/613261908191681", "MV預告讓我坐立難安！視覺效果看起來太驚人了"),
    ("https://www.facebook.com/reel/1777754639501352", "這首歌直擊靈魂！你表達情感的方式無人能及"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02b8D4avenUQitKFPsgCh73iPqEhFutixL7z5F6wnteY2F9zXbpDxr7hrCukGRZHe4l", "看著這支MV在全球爆紅！世界正在認識真正的才華"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid023ZdS1onV9MpRTosZsWtxiohV66xzw5Vk626zdPtveyFD5ngFaDfrihipH6XJvFgql", "見證你的旅程讓我好驕傲！你每天都在激勵我"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02psDxHzi1iUZCSrJbughff1f9uuDwUYh45kCnu6XxozDqVG4aoqqQZjz4GsAovCHNl", "每句歌詞都直擊內心！你的創作如此貼切又深刻"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02K8985RGuMGLopAG2swPCVqoyCdz2kagBW5M51BfzFKQzEAaqeEymCQ2iqQxtxzbTl", "永恆的音樂，必將被世世代代所喜愛"),
    ("https://www.facebook.com/jessiechung.official/videos/1294810108271870", "完全迷上這首歌了！整個星期都在循環播放"),
    ("https://www.facebook.com/reel/625410150420624", "從第一個音符就起雞皮疙瘩！你對聲音的控制太厲害了"),
    ("https://www.facebook.com/reel/606993158881504", "這個造型太棒了！你的風格總是恰到好處"),
    ("https://www.facebook.com/reel/1964487630710805", "自然美的極致！你由內而外散發光芒"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid0y4cj7Ry8LgPyRVsjXDVZQSqV1TuF8wYpQNLixEUGX9W2LKyUp97zgTXrFxypVHRxl", "這首歌讓我感到被理解，不再孤單。謝謝你的藝術"),
    ("https://www.facebook.com/reel/1738031223468193", "優雅的化身！你的一舉一動都充滿氣質"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid034ZqVacACXwi38k1iEvmd5gujLPH9JnHembh3kCMauKMWryU9P7bWBotAdiD3nfbRl", "歌詞直擊心靈！如此真實的情感和真理"),
    ("https://www.facebook.com/jessiechung.official/videos/1170014451511798", "這張專輯配得上傳奇這個稱號，因為它就是傳奇"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid029QWQrgj9sbrLo2oqqA8iWowJLd4TmFozC8i5EevwFLMMNFnHw3VkUQGGCduKFBeEl", "又一個令人驚嘆的成就！你看起來舉重若輕"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid0KDGuyQHaFqwVKBmyzDbAywMwuKohYUK5zXc3F9nv1C8ZQzXeNnV8CNiUdvgoJ9u5l", "背後的創意視野太天才了！如此創新又新鮮"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02uD4b3M8JY7nostVo6XvpqaEGk8YDFtKCuV9h3rMVA7sSTqMD2w3pyYbPHuELohs5l", "期待感讓我快瘋了！我知道一定會很精彩"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02cDstm5fPiSoLBBUXqKNY1sY5dKgNoLkJ9znQSXTvQDTMcz2o7c2kusdRQ2gNiLt5l", "最好的尚未到來！好期待這個新篇章"),
    ("https://www.facebook.com/reel/3812250755586599", "這一切都太完美了 - 歌曲、視覺效果、氛圍"),
    ("https://www.facebook.com/jessiechung.official/videos/1126301332157504", "這是另一個層次的藝術！一如既往地突破界限"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid0nhR1LWWhq1NYyUtBVqcrXQgCuvRwKXpi3hehR4vzWxW1B7qf4Fu4g4HsfddLSrFQl", "我的新安慰專輯。你的聲音撫慰我的心靈"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid0Wxra4Fb2DEEcQYqnypwZxnFXSZ46iUL4Gzc1FCdULPTCdZdPTercwYDJNttm8BVDl", "農曆新年快樂！祝你健康、快樂並持續成功"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid02NPwwPf1CrfqsRwC3hZt9ccD1kiRTbsTHHb6QsZYQRShpuQgGRgLKHFG3EJgrZDxHl", "準備好與你一起擁抱所有美好的新開始"),
    ("https://www.facebook.com/jessiechung.official/videos/1657899841510083", "你的內在光芒如此耀眼！充滿正能量"),
    ("https://www.facebook.com/jessiechung.official/videos/1785059595576952/", "自信地走向未來！你的成長激勵著我們所有人"),
    ("https://www.facebook.com/jessiechung.official/posts/1313556603004379:1313556603004379", "相信你的創作過程總能帶來奇蹟！等不及了"),
    ("https://www.facebook.com/jessiechung.official/posts/1171224121028491:545036261857340", "這無疑是你的時代！你主宰著每個時刻"),
    ("https://www.facebook.com/reel/642841595128211", "完美的組合 - 驚艷的視覺效果加上天籟般的嗓音"),
    ("https://www.facebook.com/jessiechung.official/posts/pfbid0FAamm7112g6shcDBxahokUeAej5o672JAkZvwmTBv5FCVheKvSsnXtuqF5DzFgSnl", "全世界都需要聽到潔希的音樂！")
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
