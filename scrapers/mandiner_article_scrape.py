#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd

#%%
mandiner_db = pd.read_csv("../data_raw/mandiner_db.csv")
seen_links = list(mandiner_db["link"])
#%%
url = "https://mandiner.hu/rss"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, 'xml')
article_info = soup.find_all("item")

#%%
article_table = pd.DataFrame(columns=["title", "pub_date", "category", "body", "link"]) 
for id, article in enumerate(article_info):
    url = article.find("link").get_text()
    if url in seen_links:
        print(f"Link already scraped: {url}")
        continue
    print(f"Scraping link: {url}")
    
    article_table.loc[id, "link"] = article.find("link").get_text()
    article_table.loc[id, "title"] = article.find("title").get_text()
    article_table.loc[id, "pub_date"] = pd.to_datetime(article.find("pubDate").get_text())

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_table.loc[id, "category"] = soup.select_one("man-breadcrumb li.breadcrumb-item a").get_text()

    text_blocks = soup.select("man-wysiwyg-box .block-content")

    full_article_text = []

    # 2. Iterate through each text block found
    for block in text_blocks:
        # Extract paragraphs inside this specific block
        paragraphs = block.find_all("p")
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            # Optional: Filter out empty paragraphs if necessary
            if text:
                full_article_text.append(text)

    # 3. Join everything into one string
    article_table.loc[id, "body"] = final_text = " ".join(full_article_text)

# %%
mandiner_db = pd.concat([article_table, mandiner_db])
mandiner_db.to_csv("../data_raw/mandiner_db.csv", index=False)

# %%
