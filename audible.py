# Scraping Audible book data from the audibe website

import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

headers = {"User-Agent": "Mozilla/5.0"}

def get_title(tag):
    try:
        return tag.find("h3", class_="bc-heading").text.strip()
    except:
        return None

def get_book_url(tag):
    try:
        return "https://www.audible.com" + tag.find("a", class_="bc-link")['href']
    except:
        return None

def get_description(tag):
    try:
        return tag.find("li", class_="subtitle").text.strip()
    except:
        return None

def get_author(tag):
    try:
        return tag.find("li", class_="authorLabel").text.replace("By: ", "").strip()
    except:
        return None

def get_length(tag):
    try:
        return tag.find("li", class_="runtimeLabel").text.replace("Length: ", "").strip()
    except:
        return None

def get_language(tag):
    try:
        return tag.find("li", class_="languageLabel").text.replace("Language: ", "").strip()
    except:
        return None

def get_rating(tag):
    try:
        return tag.find("span", class_="bc-pub-offscreen").text.strip()
    except:
        return None

def get_num_ratings(tag):
    try:
        return tag.find("span", class_="bc-size-small").text.strip()
    except:
        return None

def get_price(tag):
    try:
        price_block = tag.find("p", class_="buybox-regular-price")
        if price_block:
            return price_block.text.strip()
        return None
    except:
        return None

def get_cover_img(tag):
    try:
        return tag.find("img", class_="bc-image-inset-border")["src"]
    except:
        return None


books_data = []

for page in range(1, 6):
    print(f"Scraping page {page}...")
    url = f"https://www.audible.com/search?node=18580606011&pageSize=50&page={page}"
    response = rq.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = bs(response.content, "html.parser")
    book_tags = soup.find_all("li", class_="bc-list-item")

    for tag in book_tags:
        book = {
            "Title": get_title(tag),
            "Description": get_description(tag),
            "Author": get_author(tag),
            "Rating": get_rating(tag),
            "Num Ratings": get_num_ratings(tag),
            "Price": get_price(tag),
            "Language": get_language(tag),
            "Length": get_length(tag),
            "Cover Image": get_cover_img(tag),
            "URL": get_book_url(tag)
        }
        books_data.append(book)

df = pd.DataFrame(books_data)
df.to_csv("audible_sci_fi_fantasy_detailed.csv", index=False)
print("✅ Done. Books saved:", len(df))

