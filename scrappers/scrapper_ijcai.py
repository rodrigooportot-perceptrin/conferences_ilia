import re
from bs4 import BeautifulSoup
import requests
import pandas as pd

print("hello")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
    "Referer": "https://dblp.org/",
}

html_content = requests.get(
    url="https://dblp.uni-trier.de/db/conf/ijcai/ijcai2025.html", headers=headers
).text

print("got text!")

soup = BeautifulSoup(html_content, "lxml")  # "html.parser")

print("soup done!")

td_elements = soup.find_all("span", {"class": "title"})
all_title = [re.sub(r".$", r"", e.text) for e in td_elements]

print(len(all_title))

print(all_title[0])
print(all_title[-1])
# https://doi.org/10.24963/ijcai.2025/1
urls = soup.find_all(
    "a",
    {
        "href": re.compile(r"^https://doi.org/10.24963/ijcai.2025/\d*"),
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

pdf_urls = [pdf.replace("forum", "pdf") for pdf in all_urls]


## ALTER URLS FROM IJCAI SITE TO PDF URL
def create_url(x):
    x_len = len(x)
    while x_len < 4:
        x = "0" + x
        x_len = len(x)

    return "https://www.ijcai.org/proceedings/2025/" + x + ".pdf"


pdf_ids = [create_url(x.split("/")[-1]) for x in pdf_urls]

df = pd.DataFrame({"title": all_title})
df["conference"] = "ijcai"
df["year"] = 2025
df["paper_url"] = pdf_ids
df.to_csv("parsed_data/ijcai_2025.csv")
