import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import random
import time
from tqdm import tqdm  # Step 1: Import tqdm

### ESTE CASO ES DIFERENTE
### AQUÍ ES NECESARIO ENTRAR AL SITIO DE OJS.AAAI.ORG QUE SE OBTUVO DE FORMA
### RÁPIDA MEDIANTE LA LISTA DE PAPER COPILOT, QUE TAMBIÉN PUEDE OBTENERSE DE
### DBLP.

### HAY QUE ENTRAR A LAS URLS (ej https://ojs.aaai.org/index.php/AAAI/article/view/33519)
### Y OBTENER EL VALOR DEL BOTÓN PDF PARA PODER DESCARGAR LOS DOCUMENTOS.


### TAMBIÉN SE PODRÍA APROVECHAR EL MISMO TEXTO DEL HTML DE ESTE SITIO, PUESTO
### QUE MUESTRA LAS INSTITUCIONES DE LOS AUTORES, PERO NO ESTOY 100% SEGURO SI ES ALGO
### COMPLETO PARA TODOS LOS PAPERS O NO, A DIFERENCIA DE ENTRAR A VER EL DOCUMENTO, QUE ES LA
### FORMA MÁS CERTERA Y SEGURA.

print("hello")

aaai_csv = pd.read_csv("aaai_main_2025.csv")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
}

pdf_urls = []

print(len(aaai_csv))

for paper_url in tqdm(aaai_csv["paper_url"], desc="Scraping PDF URLs"):
    try:
        html_content = requests.get(url=paper_url, headers=headers).text
        soup = BeautifulSoup(html_content, "lxml")

        # Added a check to avoid index errors if the element isn't found
        td_elements = soup.find_all("a", {"class": "obj_galley_link pdf"})

        if td_elements:
            td_element = td_elements[0]
            pdf_urls.append(td_element["href"])
        else:
            pdf_urls.append(None)  # Or handle missing URLs as needed

        time.sleep(random.uniform(1.0, 2.0))

    except Exception as e:
        print(f"Error processing {paper_url}: {e}")
        pdf_urls.append(None)

print(len(pdf_urls))

aaai_csv["conference"] = "aaai"
aaai_csv["year"] = 2025
aaai_csv["paper_url"] = pdf_urls
aaai_csv.to_csv("parsed_data/aaai_2025_with_urls.csv", index=False)
