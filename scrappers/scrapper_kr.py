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
    url="https://proceedings.kr.org/2025/", headers=headers
).text

print("got text!")

soup = BeautifulSoup(html_content, "lxml")  # "html.parser")

print("soup done!")

# paper_div = soup.find_all("a", {"href": re.compile(r"^/2025/\d*/")})

paper_div = soup.find_all("div", {"class": "track_paperinfo__1BUI8"})

print(len(paper_div))

childrens = [
    p.findChildren("a", {"href": re.compile(r"^/2025/\d*/")}) for p in paper_div
]

all_titles = [t[0].text for t in childrens[1:]]  # first one is empty

print(len(all_titles))

url_elements = soup.find_all("a", {"href": re.compile(r"^/2025/\d*/kr2025.*.pdf")})

pdf_ids = [u["href"] for u in url_elements]

print(len(pdf_ids))
print(pdf_ids[0])
print(pdf_ids[-1])

pdf_urls = ["https://proceedings.kr.org" + x for x in pdf_ids]

df = pd.DataFrame({"title": all_titles})
df["conference"] = "kr"
df["year"] = 2025
df["paper_url"] = pdf_urls
df.to_csv("parsed_data/kr_2025.csv")
