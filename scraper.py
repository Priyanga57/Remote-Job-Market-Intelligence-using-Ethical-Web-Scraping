import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://remoteok.com"
OUTPUT_FILE = "remoteok_raw.csv"
SCROLL_DELAY = 3
MAX_SCROLLS = 25   
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

print("Starting RemoteOK Selenium Scraper")
driver.get(URL)
time.sleep(6)  
job_ids = set()

for scroll in range(MAX_SCROLLS):
    print(f"Scroll {scroll + 1} | Jobs detected: {len(job_ids)}")

    rows = driver.find_elements(By.CSS_SELECTOR, "tr.job")
    for row in rows:
        jid = row.get_attribute("data-id")
        if jid:
            job_ids.add(jid)

    driver.execute_script("window.scrollBy(0, 1200);")
    time.sleep(SCROLL_DELAY)

print(f"Total jobs loaded: {len(job_ids)}")

data = []
rows = driver.find_elements(By.CSS_SELECTOR, "tr.job")

for job in rows:

    # Job Title
    try:
        job_title = job.find_element(By.TAG_NAME, "h2").text.strip()
    except:
        job_title = "N/A"

    # Company
    try:
        company = job.find_element(By.TAG_NAME, "h3").text.strip()
    except:
        company = "N/A"

    # Location
    try:
        location = job.find_element(By.CLASS_NAME, "location").text.strip()
    except:
        location = "Remote"

    # Job Type (Full-time / Contract etc.)
    try:
        job_type = job.find_element(By.CLASS_NAME, "time").text.strip()
    except:
        job_type = "N/A"

    # Skills / Tags
    try:
        skills = ", ".join(
            [t.text.strip() for t in job.find_elements(By.CLASS_NAME, "tag")]
        )
    except:
        skills = "N/A"

    # Date Posted
    try:
        date_posted = job.find_element(By.TAG_NAME, "time").get_attribute("datetime")
    except:
        date_posted = "N/A"

    # Job URL
    try:
        link = job.find_element(By.CSS_SELECTOR, "a.preventLink").get_attribute("href")
        job_url = f"https://remoteok.com{link}"
    except:
        job_url = "N/A"

    data.append({
        "job_title": job_title,
        "company": company,
        "location": location,
        "job_type": job_type,
        "skills": skills,
        "date_posted": date_posted,
        "job_url": job_url
    })

driver.quit()

df = pd.DataFrame(data).drop_duplicates()

df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print(f"Saved {len(df)} records to {OUTPUT_FILE}")
print("Scraping completed ethically.")
