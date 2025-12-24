#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd

#%%
telex_db = pd.read_csv("../data_raw/telex_db.csv")
seen_links = list(telex_db["link"])
#%%
url = "https://telex.hu/rss"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, 'xml')
article_info = soup.find_all("item")

#%%
article_table = pd.DataFrame(columns=["title", "pub_date", "category", "body", "link"]) 
for id, article in enumerate(article_info):
    url = article.find("link").get_text()
    if url in seen_links:
        print(f"Link already analyzed: {url}")
        continue
    print(f"Scraping link: {url}")
    
    article_table.loc[id, "link"] = article.find("link").get_text()
    article_table.loc[id, "category"] = article.find("category").get_text()
    article_table.loc[id, "title"] = article.find("title").get_text()
    article_table.loc[id, "pub_date"] = pd.to_datetime(article.find("pubDate").get_text())

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_container = soup.find('div', class_='article-html-content')
    article_table.loc[id, "body"] = article_container.get_text(strip=True)

# %%
telex_db = pd.concat([article_table, telex_db])
telex_db
# %%
telex_db.to_csv("../data_raw/telex_db.csv", index=False)