from bs4 import BeautifulSoup
import requests
import pandas as pd
import regex as re

### ACL LONG (VOL 1)

html_content = requests.get(url="https://aclanthology.org/volumes/2025.acl-long/").text
soup = BeautifulSoup(html_content, "html.parser")

td_elements = soup.find_all(
    "a", attrs={"class": "align-middle", "href": re.compile(r"^/2025.acl-long.\d*/")}
)
all_title = [e.text for e in td_elements]

pdf_links = [
    e["href"]
    for e in soup.find_all(
        "a",
        attrs={
            "class": "badge text-bg-primary align-middle me-1",
            "href": re.compile(r"^https://aclanthology.org/2025.acl-long.\d*.pdf"),
        },
    )
]

print(len(all_title))
print(len(pdf_links))

long_df = pd.DataFrame({"title": all_title, "paper_url": pdf_links})
long_df["conference"] = "acl_long"
long_df["year"] = 2025
# df.to_csv("../conferencias_ilia2026/parsed_data/acl_long_2025.csv")


### ACL SHORT VOL 2

html_content = requests.get(url="https://aclanthology.org/volumes/2025.acl-short/").text
soup = BeautifulSoup(html_content, "html.parser")

td_elements = soup.find_all(
    "a", attrs={"class": "align-middle", "href": re.compile(r"^/2025.acl-short.\d*/")}
)
all_title = [e.text for e in td_elements]

pdf_links = [
    e["href"]
    for e in soup.find_all(
        "a",
        attrs={
            "class": "badge text-bg-primary align-middle me-1",
            "href": re.compile(r"^https://aclanthology.org/2025.acl-short.\d*.pdf"),
        },
    )
]

print(len(all_title))
print(len(pdf_links))

short_df = pd.DataFrame({"title": all_title, "paper_url": pdf_links})
short_df["conference"] = "acl"
short_df["year"] = 2025


### ACL DEMONSTRATIONS VOL 3

html_content = requests.get(url="https://aclanthology.org/volumes/2025.acl-demo/").text
soup = BeautifulSoup(html_content, "html.parser")

td_elements = soup.find_all(
    "a", attrs={"class": "align-middle", "href": re.compile(r"^/2025.acl-demo.\d*/")}
)
all_title = [e.text for e in td_elements]

pdf_links = [
    e["href"]
    for e in soup.find_all(
        "a",
        attrs={
            "class": "badge text-bg-primary align-middle me-1",
            "href": re.compile(r"^https://aclanthology.org/2025.acl-demo.\d*.pdf"),
        },
    )
]

print(len(all_title))
print(len(pdf_links))

demo_df = pd.DataFrame({"title": all_title, "paper_url": pdf_links})
demo_df["conference"] = "acl"
demo_df["year"] = 2025

### ACL INDUSTRY VOL 6

html_content = requests.get(
    url="https://aclanthology.org/volumes/2025.acl-industry/"
).text
soup = BeautifulSoup(html_content, "html.parser")

td_elements = soup.find_all(
    "a",
    attrs={"class": "align-middle", "href": re.compile(r"^/2025.acl-industry.\d*/")},
)
all_title = [e.text for e in td_elements]

pdf_links = [
    e["href"]
    for e in soup.find_all(
        "a",
        attrs={
            "class": "badge text-bg-primary align-middle me-1",
            "href": re.compile(r"^https://aclanthology.org/2025.acl-industry.\d*.pdf"),
        },
    )
]

print(len(all_title))
print(len(pdf_links))

industry_df = pd.DataFrame({"title": all_title, "paper_url": pdf_links})
industry_df["conference"] = "acl"
industry_df["year"] = 2025


big_df = pd.concat([long_df, short_df, demo_df, industry_df])

big_df.to_csv("parsed_data/acl_main_tracks.csv")
