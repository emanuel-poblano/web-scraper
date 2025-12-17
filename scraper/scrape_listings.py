import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = "https://www.redfin.com/city/14240/AZ/Phoenix"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

cards = soup.select("div.bp-Homecard")

print(f"Found {len(cards)} listings")

data = []

for card in cards:
    try:
        price = card.select_one(".bp-Homecard__Price--value").get_text(strip=True)
        beds = card.select_one(".bp-Homecard__Stats--beds").get_text(strip=True)
        baths = card.select_one(".bp-Homecard__Stats--baths").get_text(strip=True)
        sqft = card.select_one(".bp-Homecard__Stats--sqft").get_text(" ", strip=True)

        address_tag = card.select_one(".bp-Homecard__Address")
        address = address_tag.get_text(strip=True)
        url = "https://www.redfin.com" + address_tag["href"]

        data.append({
            "price": price,
            "beds": beds,
            "baths": baths,
            "sqft": sqft,
            "address": address,
            "url": url
        })

    except AttributeError:
        continue

df = pd.DataFrame(data)
df.to_csv("data/listings.csv", index=False)

print("Saved listings.csv")