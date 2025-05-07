# Scraping Audible audiobooks data from the audibe website

import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_text(tag, selector, default=None, remove_prefix=None):
    try:
        element = tag.select_one(selector)
        if element:
            text = element.get_text(strip=True)
            if remove_prefix and text.startswith(remove_prefix):
                return text.replace(remove_prefix, "").strip()
            return text
        return default
    except:
        return default

def extract_attr(tag, selector, attr, default=None):
    try:
        element = tag.select_one(selector)
        return element[attr].strip() if element and attr in element.attrs else default
    except:
        return default

def extract_price(tag):
    try:
        spans = tag.select("p.buybox-regular-price span.bc-text.bc-size-base.bc-color-base")
        for span in spans:
            price = span.get_text(strip=True)
            if "$" in price or "₹" in price:
                return price
        return None
    except:
        return None

def scrape_audible_sci_fi_fantasy(pages=5):
    headers = {"User-Agent": "Mozilla/5.0"}
    books_data = []

    for page in range(1, pages + 1):
        print(f"Scraping page {page}")
        url = f"https://www.audible.com/search?node=18580606011&pageSize=50&page={page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        book_tags = soup.select("li.bc-list-item")

        for tag in book_tags:
            book = {
                "Title": extract_text(tag, "h3.bc-heading"),
                "Description": extract_text(tag, "li.subtitle"),
                "Author": extract_text(tag, "li.authorLabel a"),
                "Rating": extract_text(tag, "li.ratingsLabel span.bc-pub-offscreen"),
                "Num Ratings": extract_text(tag, "li.ratingsLabel span.bc-size-small.bc-color-secondary"),
                "Price": extract_price(tag),
                "Language": extract_text(tag, "li.languageLabel", remove_prefix="Language: "),
                "Length": extract_text(tag, "li.runtimeLabel", remove_prefix="Length: "),
                "Cover Image": extract_attr(tag, "img.bc-image-inset-border", "src"),
                "URL": extract_attr(tag, "a.bc-link", "href")
            }

            if book["URL"]:
                book["URL"] = "https://www.audible.com" + book["URL"]
            books_data.append(book)

    # Convert to DataFrame
    df = pd.DataFrame(books_data)

    # Filter out rows with missing descriptions
    clean_df = df[df['Description'].notna() & (df['Description'].str.strip() != "")]

    # Save to CSV
    df.to_csv("audible_sci_fi_fantasy_raw.csv", index=False)
    clean_df.to_csv("audible_sci_fi_fantasy_cleaned.csv", index=False)

    print(f"Scraping complete!")
    print(f"Total books scraped: {len(df)}")
    print(f"Cleaned books (with description): {len(clean_df)}")

    return clean_df

# Run the scraper
scrape_audible_sci_fi_fantasy(pages=5)
