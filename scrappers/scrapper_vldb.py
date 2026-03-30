from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

print("hello")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
    "Referer": "https://dblp.org/",
}

html_content = requests.get(
    url="https://dblp.uni-trier.de/db/journals/pvldb/pvldb18.html", headers=headers
).text

print("got text!")

soup = BeautifulSoup(html_content, "lxml")  # "html.parser")

print("soup done!")

td_elements = soup.find_all("span", {"class": "title"})
all_titles = [re.sub(r".$", r"", e.text) for e in td_elements]

print(len(all_titles))

print(all_titles[0])
print(all_titles[-1])

# https://www.vldb.org/pvldb/vol18/p1-arch.pdf

urls = soup.find_all(
    "a",
    {
        "href": re.compile(r"^https://www.vldb.org/pvldb/vol18/.*.pdf"),
        "itemprop": "url",
    },
)

all_urls = [u["href"] for u in urls]

print(len(all_urls))
print(all_urls[0])
print(all_urls[-1])

df = pd.DataFrame({"title": all_titles})
df["conference"] = "vldb"
df["year"] = 2025
df["paper_url"] = all_urls
df.to_csv("parsed_data/vldb_2025.csv")
