from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

html_content = requests.get(url="https://proceedings.mlr.press/v291/").text
soup = BeautifulSoup(html_content, "html.parser")

td_elements = soup.find_all("div", {"class": "paper"})

titles = []
paper_url = []

for paper in td_elements:
    title = paper.findChildren("p", {"class": "title"})[0]
    link = paper.findChildren("p", {"class": "links"})[0].find(
        "a", {"href": re.compile("(.pdf)$")}
    )

    titles.append(title.text)
    paper_url.append(link["href"])

print(len(titles))
print(len(paper_url))

df = pd.DataFrame({"title": titles})
df["conference"] = "colt"
df["year"] = 2025
df["paper_url"] = paper_url
df.to_csv("parsed_data/colt_2025.csv")
