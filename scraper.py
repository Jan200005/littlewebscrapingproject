import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

BASE_URL = "http://books.toscrape.com/"
DELAY = 0.5

def parse_book_card(card):
    title = card.h3.a['title']
    price = card.select_one(".price_color").text
    availability = card.select_one(".availability").text.strip()
    rating = card.p['class'][1]
    link = urljoin(BASE_URL, card.h3.a['href'])
    return {"title": title, "price": price, "availability": availability, "rating": rating, "link": link}

def scrape_books(max_pages=3):
    page_url = BASE_URL
    results = []
    for page in range(max_pages):
        r = requests.get(page_url)
        soup = BeautifulSoup(r.text, "html.parser")
        for card in soup.select("article.product_pod"):
            results.append(parse_book_card(card))
        next_btn = soup.select_one("li.next a")
        if next_btn:
            page_url = urljoin(page_url, next_btn['href'])
            time.sleep(DELAY)
        else:
            break
    # save CSV
    keys = results[0].keys()
    with open("books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved {len(results)} records to books.csv")

if __name__ == "__main__":
    scrape_books()

