from bs4 import BeautifulSoup
import requests
import pandas as pd
import regex as re
import os

print(os.getcwd())


html_content = requests.get(url="https://aclanthology.org/events/emnlp-2025/").text
soup = BeautifulSoup(html_content, "html.parser")

tracks = [
    "findings-emnlp",
    "arabicnlp-main",
    "arabicnlp-sharedtasks",
    "babylm-main",
    "blackboxnlp-1",
    "codi-1",
    "crac-1",
    "disrpt-1",
    "finnlp-2",
    "hcinlp-1",
    "mathnlp-main",
    "mrl-main",
    "newsum-main",
    "nllp-1",
    "nlperspectives-1",
    "pals-1",
    "starsem-1",
    "tsar-1",
    "uncertainlp-main",
    "winlp-main",
    "wmt-1",
    "wordplay-1",
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
df["conference"] = "emnlp-sidetracks"
df["year"] = 2025
df.to_csv("parsed_data/emnlp_sidetracks_2025.csv")


# <a class="badge badge-primary align-middle mr-1"
# href="https://aclanthology.org/2025.emnlp-main.0.pdf"
# data-toggle="tooltip"
# data-placement="top"
# title=""
# data-original-title="Open PDF">pdf
# </a>
