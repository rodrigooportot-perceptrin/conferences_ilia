from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

html_content = requests.get(url="https://openaccess.thecvf.com/CVPR2025?day=all").text
soup = BeautifulSoup(html_content, "html.parser")

td_elements = soup.find_all("dt", {"class": "ptitle"})
all_title = [e.text for e in td_elements]

print(len(all_title))

urls = soup.find_all("a", {"href": re.compile(r"(paper.pdf)$")})

print(len(urls))

all_urls = ["https://openaccess.thecvf.com" + u["href"] for u in urls]

df = pd.DataFrame({"title": all_title})
df["conference"] = "cvpr"
df["year"] = 2025
df["paper_url"] = all_urls
df.to_csv("parsed_data/cvpr_2025.csv")
