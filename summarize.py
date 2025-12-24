#%%
import pandas as pd
import numpy as np
import os
import datetime as dt
#%%
list = os.listdir("./data_raw")
sites = []
for file in list:
    sites.append(file.split("_")[0])

for site in sites:
    site_name = site
    db = pd.read_csv("data_processed/" + site_name + "_analyzed.csv", parse_dates=True)
    db["pub_date"] = pd.to_datetime(db["pub_date"], format="mixed", utc=True)
    db.drop(columns=["title", "body", "link"], inplace=True)
    cols_of_interest = db.columns[2:]
    all_mentions = db.groupby([db["pub_date"].dt.strftime('%Y-%m-%d')])[cols_of_interest].sum()
    all_mentions.sort_index(inplace=True)
    all_mentions.index.name = 'date'
    all_mentions.to_csv("summaries/" + site_name + "_all_mentions.csv")
    # %%
    db_binary = db.copy()
    db_binary[cols_of_interest] = np.where(db_binary[cols_of_interest] != 0,1,0)
    # %%
    binary_mentions = db_binary.groupby([db_binary["pub_date"].dt.strftime('%Y-%m-%d')])[cols_of_interest].sum()
    binary_mentions.sort_index(inplace=True)
    binary_mentions.index.name = 'date'
    binary_mentions.to_csv("summaries/" + site_name + "_binary_mentions.csv")
    # %%
