import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

print("hello")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
    "Referer": "https://dblp.org/",
}

html_content = requests.get(
    url="https://dblp.uni-trier.de/db/conf/icra/icra2025.html", headers=headers
).text

print("got text!")

soup = BeautifulSoup(html_content, "lxml")  # "html.parser")

print("soup done!")

td_elements = soup.find_all("span", {"class": "title"})
all_title = [re.sub(r".$", r"", e.text) for e in td_elements]

print(len(all_title))

print(all_title[0])
print(all_title[-1])

# https://doi.org/10.1109/ICRA55743.2025.11127445

# papers ICDE

urls = soup.find_all(
    "a",
    {
        "href": re.compile(r"^https://doi.org/10.1109/ICRA\d*.2025.\d*"),
        "itemprop": "url",
    },
)

all_urls = [u["href"] for u in urls]

print(len(all_urls))
print(all_urls[0])
print(all_urls[-1])

# REMOVE FIRST ITEM OF ALL_TITLES LIST SINCE IT'S JUST THE NAME OF THE CONFERENCE (PROCEEDINGS)

del all_title[0]

pdf_ieee_urls = []

# https://ieeexplore.ieee.org/document/11112978/
# https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11112978 url from web browser
# https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?arnumber=11112978 url gemini suggests
for pdf in all_urls:
    ieee_html_content = requests.get(url=pdf, headers=headers)
    pdf_url_id = ieee_html_content.url.split("document/")[1].replace("/", "")
    pdf_ieee_urls.append(
        "https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?arnumber=" + pdf_url_id
    )
    print(ieee_html_content.status_code, pdf_url_id)
    time.sleep(1)

df = pd.DataFrame({"title": all_title})
df["conference"] = "icra"
df["year"] = 2025
df["paper_url"] = pdf_ieee_urls
df.to_csv("parsed_data/icra_2025.csv")
