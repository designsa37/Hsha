import requests
from bs4 import BeautifulSoup
import json
import time
import random

all_quotes = []
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}

def scrape_brainyquote():
    print("🔍 BrainyQuote...")
    categories = ["inspirational","motivational","life","love","wisdom","success","happiness","courage","friendship","hope"]
    base = "https://www.brainyquote.com/topics/"
    for cat in categories:
        try:
            r = requests.get(f"{base}{cat}-quotes", headers=headers, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")
            for q,a in zip(soup.find_all("a",class_="b-qt"),soup.find_all("a",class_="bq-aut")):
                txt,auth = q.get_text(strip=True),a.get_text(strip=True)
                if txt and len(txt)>15: all_quotes.append({"text":txt,"author":auth})
            time.sleep(2)
        except: pass
    print(f"✅ BrainyQuote done")

def scrape_azquotes():
    print("🔍 AZQuotes...")
    categories = ["inspirational","motivational","life","love","wisdom","success","happiness","courage"]
    base = "https://www.azquotes.com/quotes/categories/"
    for cat in categories:
        try:
            r = requests.get(f"{base}{cat}.html", headers=headers, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")
            for box in soup.find_all("div",class_="quote-content"):
                q,a = box.find("a",class_="title"),box.find("a",class_="author")
                if q and a:
                    txt,auth = q.get_text(strip=True),a.get_text(strip=True)
                    if txt and len(txt)>15: all_quotes.append({"text":txt,"author":auth})
            time.sleep(2)
        except: pass
    print(f"✅ AZQuotes done")

def fetch_zenquotes():
    print("🔍 ZenQuotes API...")
    try:
        for _ in range(50):
            data = requests.get("https://zenquotes.io/api/random", timeout=15).json()
            for item in data: all_quotes.append({"text":item["q"],"author":item["a"]})
            time.sleep(1)
    except: pass
    print(f"✅ ZenQuotes done")

def scrape_quotes_toscrape():
    print("🔍 QuotesToScrape...")
    for page in range(1,11):
        try:
            r = requests.get(f"https://quotes.toscrape.com/page/{page}/", headers=headers, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")
            for box in soup.find_all("div",class_="quote"):
                txt = box.find("span",class_="text").get_text(strip=True)
                auth = box.find("small",class_="author").get_text(strip=True)
                if txt and len(txt)>15: all_quotes.append({"text":txt,"author":auth})
            time.sleep(1.5)
        except: pass
    print(f"✅ QuotesToScrape done")

if __name__ == "__main__":
    scrape_brainyquote()
    scrape_azquotes()
    fetch_zenquotes()
    scrape_quotes_toscrape()
    unique = list({q["text"]:q for q in all_quotes}.values())
    random.shuffle(unique)
    with open("quotes.json","w",encoding="utf-8") as f:
        json.dump(unique,f,indent=2,ensure_ascii=False)
    print(f"\n🎉 Done! {len(unique)} quotes saved to quotes.json")
