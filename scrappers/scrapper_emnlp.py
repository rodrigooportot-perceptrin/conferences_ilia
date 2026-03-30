from bs4 import BeautifulSoup
import requests
import pandas as pd
import regex as re

html_content = requests.get(
    url="https://aclanthology.org/volumes/2025.emnlp-main/"
).text
soup = BeautifulSoup(html_content, "html.parser")

td_elements = soup.find_all(
    "a", attrs={"class": "align-middle", "href": re.compile(r"^/2025.emnlp-main.\d*/")}
)
all_title = [e.text for e in td_elements]

pdf_links = [
    e["href"]
    for e in soup.find_all(
        "a",
        attrs={
            "class": "badge badge-primary align-middle mr-1",
            "href": re.compile(r"^https://aclanthology.org/2025.emnlp-main.\d*.pdf"),
        },
    )
]

print(len(all_title))
print(len(pdf_links))

df = pd.DataFrame({"title": all_title, "paper_url": pdf_links})
df["conference"] = "emnlp"
df["year"] = 2025
df.to_csv("conferencias_ilia2026/parsed_data/emnlp_2025.csv")


# <a class="badge badge-primary align-middle mr-1"
# href="https://aclanthology.org/2025.emnlp-main.0.pdf"
# data-toggle="tooltip"
# data-placement="top"
# title=""
# data-original-title="Open PDF">pdf
# </a>
