#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd

#%%
mn_db = pd.read_csv("../data_raw/mn_db.csv")
seen_links = list(mn_db["link"])
#%%
url = "https://magyarnemzet.hu/publicapi/hu/rss/magyar_nemzet/articles"
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
    article_container = soup.find('div', class_='article-text-formatter')
    article_table.loc[id, "body"] = article_container.get_text(strip=True)

    breadcrumb = soup.find("ul", class_="breadcrumb")
    if breadcrumb:
        links = breadcrumb.find_all("a", class_="breadcrumb-link")
        if len(links) > 1:
            article_table.loc[id, "category"] = links[1].get_text(strip=True)

# %%
mn_db = pd.concat([article_table, mn_db])
mn_db.to_csv("../data_raw/mn_db.csv", index=False)
