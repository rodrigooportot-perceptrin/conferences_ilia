from bs4 import BeautifulSoup
import requests
import pandas as pd
import regex as re
import os

print(os.getcwd())


html_content = requests.get(url="https://aclanthology.org/events/acl-2025/").text
soup = BeautifulSoup(html_content, "html.parser")

tracks = [
    "findings-acl",
    "africanlp-1",
    "analogyangle-1",
    "argmining-1",
    "bea-1",
    "bionlp-1",
    "bionlp-share",
    "bsnlp-1",
    "climatenlp-1",
    "conll-1",
    "fever-1",
    "fieldmatters-1",
    "gebnlp-1",
    "gem-1",
    "iwslt-1",
    "knowllm-1",
    "l2m2-1",
    "law-1",
    "llmsec-1",
    "magmar-1",
    "nlp4pi-1",
    "realm-1",
    "sdp-1",
    "semeval-1",
    # "sicon-1", # ausencia de pdfs y listas de largo desigual, sin embargo no tiene nada de latam
    "sigtyp-1",
    "trl-1",
    "unlp-1",
    "wikinlp-1",
    "woah-1",
    "xllm-1",
]

tracks_titles = []
all_links = []

for track in tracks:
    track_string = rf"^/2025.{track}.\d*/"
    td_elements = soup.find_all(
        "a",
        attrs={
            "class": "align-middle",
            "href": re.compile(track_string),
        },
    )
    all_titles = [e.text for e in td_elements]

    pdf_links = [
        e["href"]
        for e in soup.find_all(
            "a",
            attrs={
                "class": "badge text-bg-primary align-middle me-1",
                "href": re.compile(rf"^https://aclanthology.org/2025.{track}.\d*.pdf"),
            },
        )
    ]

    print(len(all_titles))
    print(len(pdf_links))

    tracks_titles += all_titles
    all_links += pdf_links

df = pd.DataFrame({"title": tracks_titles, "paper_url": all_links})
df["conference"] = "acl-sidetracks"
df["year"] = 2025
df.to_csv("parsed_data/acl_sidetracks_2025.csv")


# <a class="badge badge-primary align-middle mr-1"
# href="https://aclanthology.org/2025.emnlp-main.0.pdf"
# data-toggle="tooltip"
# data-placement="top"
# title=""
# data-original-title="Open PDF">pdf
# </a>
