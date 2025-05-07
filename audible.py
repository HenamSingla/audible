# # Scraping Audible book data from the audibe website

# import requests as rq
# from bs4 import BeautifulSoup as bs
# import pandas as pd
# import time

# headers = {"User-Agent": "Mozilla/5.0"}

# def get_title(tag):
#     try:
#         return tag.find("h3", class_="bc-heading").text.strip()
#     except:
#         return None

# def get_book_url(tag):
#     try:
#         return "https://www.audible.com" + tag.find("a", class_="bc-link")['href']
#     except:
#         return None

# def get_description(tag):
#     try:
#         return tag.find("li", class_="subtitle").text.strip()
#     except:
#         return None

# def get_author(tag):
#     try:
#         return tag.find("li", class_="authorLabel").text.replace("By: ", "").strip()
#     except:
#         return None

# def get_length(tag):
#     try:
#         return tag.find("li", class_="runtimeLabel").text.replace("Length: ", "").strip()
#     except:
#         return None

# def get_language(tag):
#     try:
#         return tag.find("li", class_="languageLabel").text.replace("Language: ", "").strip()
#     except:
#         return None

# def get_rating(tag):
#     try:
#         return tag.find("span", class_="bc-pub-offscreen").text.strip()
#     except:
#         return None

# def get_num_ratings(tag):
#     try:
#         return tag.find("span", class_="bc-size-small").text.strip()
#     except:
#         return None

# def get_price(tag):
#     try:
#         price_block = tag.find("p", class_="buybox-regular-price")
#         if price_block:
#             return price_block.text.strip()
#         return None
#     except:
#         return None

# def get_cover_img(tag):
#     try:
#         return tag.find("img", class_="bc-image-inset-border")["src"]
#     except:
#         return None


# books_data = []

# for page in range(1, 6):
#     print(f"Scraping page {page}...")
#     url = f"https://www.audible.com/search?node=18580606011&pageSize=50&page={page}"
#     response = rq.get(url, headers={"User-Agent": "Mozilla/5.0"})
#     soup = bs(response.content, "html.parser")
#     book_tags = soup.find_all("li", class_="bc-list-item")

#     for tag in book_tags:
#         book = {
#             "Title": get_title(tag),
#             "Description": get_description(tag),
#             "Author": get_author(tag),
#             "Rating": get_rating(tag),
#             "Num Ratings": get_num_ratings(tag),
#             "Price": get_price(tag),
#             "Language": get_language(tag),
#             "Length": get_length(tag),
#             "Cover Image": get_cover_img(tag),
#             "URL": get_book_url(tag)
#         }
#         books_data.append(book)

# df = pd.DataFrame(books_data)
# df.to_csv("audible_sci_fi_fantasy_detailed.csv", index=False)
# print("✅ Done. Books saved:", len(df))




















# # Scraping Audible book data from the Audible website

# import requests as rq
# from bs4 import BeautifulSoup as bs
# import pandas as pd
# import time

# headers = {"User-Agent": "Mozilla/5.0"}

# def get_title(tag):
#     try:
#         return tag.find("h3", class_="bc-heading").text.strip()
#     except:
#         return None

# def get_book_url(tag):
#     try:
#         return "https://www.audible.com" + tag.find("a", class_="bc-link")['href']
#     except:
#         return None

# def get_description(tag):
#     try:
#         return tag.find("li", class_="subtitle").text.strip()
#     except:
#         return None

# def get_author(tag):
#     try:
#         return tag.find("li", class_="authorLabel").text.replace("By: ", "").strip()
#     except:
#         return None

# def get_length(tag):
#     try:
#         return tag.find("li", class_="runtimeLabel").text.replace("Length: ", "").strip()
#     except:
#         return None

# def get_language(tag):
#     try:
#         return tag.find("li", class_="languageLabel").text.replace("Language: ", "").strip()
#     except:
#         return None

# def get_rating(tag):
#     try:
#         return tag.find("span", class_="bc-pub-offscreen").text.strip()
#     except:
#         return None

# def get_num_ratings(tag):
#     try:
#         return tag.find("span", class_="bc-size-small").text.strip()
#     except:
#         return None

# def get_price(tag):
#     try:
#         price_block = tag.find("p", class_="buybox-regular-price")
#         if price_block:
#             return price_block.text.strip()
#         return None
#     except:
#         return None

# def get_cover_img(tag):
#     try:
#         return tag.find("img", class_="bc-image-inset-border")["src"]
#     except:
#         return None

# books_data = []

# for page in range(1, 6):
#     print(f"Scraping page {page}...")
#     url = f"https://www.audible.com/search?node=18580606011&pageSize=50&page={page}"
#     response = rq.get(url, headers=headers)
#     soup = bs(response.content, "html.parser")
#     book_tags = soup.find_all("li", class_="bc-list-item")

#     for tag in book_tags:
#         book = {
#             "Title": get_title(tag),
#             "Description": get_description(tag),
#             "Author": get_author(tag),
#             "Rating": get_rating(tag),
#             "Num Ratings": get_num_ratings(tag),
#             "Price": get_price(tag),
#             "Language": get_language(tag),
#             "Length": get_length(tag),
#             "Cover Image": get_cover_img(tag),
#             "URL": get_book_url(tag)
#         }
#         books_data.append(book)

# df = pd.DataFrame(books_data)
# df.to_csv("audible_sci_fi_fantasy_detailed.csv", index=False)
# print("✅ Done. Books saved:", len(df))

import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_text(tag, selector, default=None, remove_prefix=None):
    try:
        element = tag.select_one(selector)
        if element:
            text = element.get_text(strip=True)
            return text.replace(remove_prefix, "") if remove_prefix else text
        return default
    except:
        return default

def extract_attr(tag, selector, attr, default=None):
    try:
        element = tag.select_one(selector)
        return element[attr] if element and attr in element.attrs else default
    except:
        return default

headers = {"User-Agent": "Mozilla/5.0"}
books_data = []

for page in range(1, 6):
    print(f"Scraping page {page}")
    url = f"https://www.audible.com/search?node=18580606011&pageSize=50&page={page}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    book_tags = soup.select("li.bc-list-item")

    for tag in book_tags:
        book = {
            "Title": extract_text(tag, "h3.bc-heading"),
            "Description": extract_text(tag, "li.subtitle"),
            "Author": extract_text(tag, "li.authorLabel", remove_prefix="By: "),
            "Rating": extract_text(tag, "span.bc-pub-offscreen"),
            "Num Ratings": extract_text(tag, "span.bc-size-small"),
            "Price": extract_text(tag, "p.buybox-regular-price"),
            "Language": extract_text(tag, "li.languageLabel", remove_prefix="Language: "),
            "Length": extract_text(tag, "li.runtimeLabel", remove_prefix="Length: "),
            "Cover Image": extract_attr(tag, "img.bc-image-inset-border", "src"),
            "URL": extract_attr(tag, "a.bc-link", "href", default="N/A")
        }
        if book["URL"] != "N/A":
            book["URL"] = "https://www.audible.com" + book["URL"]
        books_data.append(book)

df = pd.DataFrame(books_data)
df.to_csv("audible_sci_fi_fantasy_cleaned.csv", index=False)
print("✅ Done. Books saved:", len(df))


# Load the CSV file
df = pd.read_csv("audible_sci_fi_fantasy_detailed.csv")

# Filter out rows where Description is missing or empty
clean_df = df[df['Description'].notna() & (df['Description'].str.strip() != "")]

clean_df.to_csv("audible_cleaned.csv", index=False)
