import requests
import pandas as pd
import os
import time
import glob
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

emnlp_pd_file = pd.read_csv("/mnt-homes/dccnas/cenia/roportot/archive/conferencias_2025/lista_papers/icml_2025.csv")

print(emnlp_pd_file["paper_url"])

save_path = "/mnt-homes/dccnas/cenia/roportot/archive/conferencias_2025/downloaded_papers/icml_2025"

# 1. Use a standard User-Agent to avoid being blocked by OJS
headers = {
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# ### ACM HEADERS

# headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#         "Accept-Language": "en-US,en;q=0.9",
#         "Accept-Encoding": "gzip, deflate, br",
#         "DNT": "1",
#         "Connection": "keep-alive",
#         "Upgrade-Insecure-Requests": "1",
#         "Sec-Fetch-Dest": "document",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-Site": "cross-site",
#         "Referer": "https://dl.acm.org/", # ACM often checks this
#     }

# IEEE HEADERS

# headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#         "Accept": "application/pdf,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#         "Accept-Language": "en-US,en;q=0.9",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Connection": "keep-alive",
#         "Referer": url, # Tells IEEE you are coming from the "Viewer" page
#         "Upgrade-Insecure-Requests": "1",
#         "Sec-Fetch-Dest": "document",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-Site": "same-origin",
#     }

def download_papers(session, url, save_path):
    try:
        # Stream the download to save memory
        response = session.get(url, stream=True, timeout=60, headers=headers)
        response.raise_for_status() # Raises an error for 4xx/5xx responses
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Success: {save_path}")
        return True
        
    except Exception as e:
        print(f"Failed to download {url}. Error: {e}")
        return False

# 1. Setup a session with a retry strategy
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))


index = 0
# 2. Iterate through your files
for x in emnlp_pd_file['paper_url']:
    #name_file = x.split('/')[-1] 

    # if paper from openreview
    name_file = x.split('/')[-1] + ".pdf"  ### IT CHANGES BASED ON THE URL OR PDF FILE

    # Ensure you are appending the filename to your directory path
    full_save_path = f"{save_path}/{name_file}" 
    
    print(full_save_path)

    success = download_papers(session, x, full_save_path)
    
    # 3. The "Be Kind" Pause
    # Randomizing the sleep time makes your t
    time.sleep(random.uniform(1.0, 2.0))

    # if (index + 1) % 15 == 0:
    #     long_pause = random.uniform(20, 40)
    #     print(f"☕ Batch complete. Taking a {long_pause:.2f}s rest to avoid WAF block.")
    #     time.sleep(long_pause)

    # index += 1