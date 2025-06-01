import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

BASE_URL = "https://www.lfccro.com/forum/"

def selenium_login(username, password):
    driver = webdriver.Chrome()  # ili Firefox, prema instalaciji
    driver.get(BASE_URL + "index.php?action=login")

    wait = WebDriverWait(driver, 15)
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "user")))
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "passwrd")))

    username_input.send_keys(username)
    password_input.send_keys(password)

    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']")))
    login_button.click()

    # Čekaj dok se pojavi logout link (znači login uspješan)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='action=logout']")))
    print("🔐 Prijavljen putem Seleniuma.")

    selenium_cookies = driver.get_cookies()
    driver.quit()

    session = requests.Session()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain'))

    return session

def get_board_ids(session):
    url = BASE_URL + "index.php"
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    board_links = soup.select("a[href*='index.php?board=']")
    board_ids = set()
    for link in board_links:
        href = link['href']
        if "board=" in href:
            part = href.split("board=")[1]
            board_id = part.split(".")[0]
            if board_id.isdigit():
                board_ids.add(int(board_id))
    print(f"✅ Pronađeno {len(board_ids)} boardova: {sorted(board_ids)}")
    return sorted(board_ids)

def get_topic_ids_from_board(session, board_id, max_pages=3):
    topic_ids = set()
    for start in range(0, max_pages * 15, 15):
        url = f"{BASE_URL}index.php?board={board_id}.{start}"
        response = session.get(url)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, "html.parser")
        topic_links = soup.select("a[href*='index.php?topic=']")
        if not topic_links:
            break
        for link in topic_links:
            href = link['href']
            if "topic=" in href:
                tid = href.split("topic=")[1].split(".")[0]
                if tid.isdigit():
                    topic_ids.add(int(tid))
        time.sleep(1)
    print(f"Board {board_id} ima {len(topic_ids)} topic-a.")
    return sorted(topic_ids)

def extract_posts_from_topic(session, topic_id, max_pages=10):
    posts = []
    for start in range(0, max_pages * 15, 15):
        url = f"{BASE_URL}index.php?topic={topic_id}.{start}"
        response = session.get(url)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, "html.parser")
        post_divs = soup.select("div.post")
        if not post_divs:
            break
        for post_div in post_divs:
            author = post_div.select_one("div.poster > strong") 
            author_name = author.text.strip() if author else "Nepoznato"

            content_div = post_div.select_one("div.post > div.inner")
            content = content_div.get_text(separator="\n").strip() if content_div else ""

            posts.append({
                "topic_id": topic_id,
                "author": author_name,
                "content": content
            })
        time.sleep(1)
    print(f"Topic {topic_id} ima {len(posts)} postova.")
    return posts

def save_posts_to_csv(posts, filename="posts.csv"):
    keys = posts[0].keys() if posts else []
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(posts)
    print(f"📝 Spremio {len(posts)} postova u '{filename}'.")

if __name__ == "__main__":
    USERNAME = "user"
    PASSWORD = "lozinka"

    session = selenium_login(USERNAME, PASSWORD)

    board_ids = get_board_ids(session)

    all_posts = []
    for board_id in board_ids:
        topic_ids = get_topic_ids_from_board(session, board_id, max_pages=2)
        for tid in topic_ids:
            posts = extract_posts_from_topic(session, tid, max_pages=3)
            all_posts.extend(posts)

    if all_posts:
        save_posts_to_csv(all_posts)
    else:
        print("⚠️ Nema postova za spremiti.")
