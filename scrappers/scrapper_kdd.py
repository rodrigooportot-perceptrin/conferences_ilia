from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

print("hello")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
    "Referer": "https://dblp.org/",
}

# https://dblp.uni-trier.de/db/conf/kdd/kdd2025-2.html
# KDD 1, 2

html_content = requests.get(
    url="https://dblp.uni-trier.de/db/conf/kdd/kdd2025-2.html", headers=headers
).text

print("got text!")

soup = BeautifulSoup(html_content, "lxml")  # "html.parser")

print("soup done!")

td_elements = soup.find_all("span", {"class": "title"})
all_title = [re.sub(r".$", r"", e.text) for e in td_elements]

print(len(all_title))

print(all_title[0])
print(all_title[-1])

# https://doi.org/10.1145/3711896.3736799
# https://doi.org/10.1145/3711896.3736883

urls = soup.find_all(
    "a",
    {
        "href": re.compile(r"^https://doi.org/10.1145/3711896.\d*"),
        "itemprop": "url",
    },
)

all_urls = [u["href"] for u in urls]

print(len(all_urls))
print(all_urls[0])
print(all_urls[-1])

# REMOVE FIRST ITEM OF ALL_TITLES LIST SINCE IT'S JUST THE NAME OF THE CONFERENCE (PROCEEDINGS)

del all_title[0]

# REPLACE FORUM WITH PDF IN URLS TO CHECK PDF FASTER

pdf_ids = [x.split("/")[-1] for x in all_urls]

# "?download=true"
pdf_urls = ["https://dl.acm.org/doi/pdf/10.1145/" + pdf for pdf in pdf_ids]

df = pd.DataFrame({"title": all_title})
df["conference"] = "kdd"
df["year"] = 2025
df["paper_url"] = pdf_urls
df.to_csv("parsed_data/kdd_2_2025.csv")
