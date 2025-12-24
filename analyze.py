#%%
import pandas as pd
import os
from word_lookup_func import word_lookup
#%%
list = os.listdir("./data_raw")
sites = []
for file in list:
    sites.append(file.split("_")[0])
#%%
for site in sites:
    site_name = site
    db = pd.read_csv("data_raw/" + site_name + "_db.csv")
    names_of_interest = ["Magyar Péter", "Orbán Viktor", "Lázár János", "Trump", "Putyin", "Zelenszkij", "Karácsony Gergely"]
    parties = [["Fidesz", "fidesz"], ["Tisza Párt", "tiszás"], "Mi Hazánk", ["DK", "Demokratikus Koalíció", "déká"], "MSZP", ["Jobbik", "jobbikos"], ["Momentum", "momentum"]]

    for id, body in enumerate(db["body"]):
        print(site)
        if type(body) == float :
            print(f"The body for {db.loc[id, "title"]} is empty.")
            continue
        print(body[:100])
        word_dict = word_lookup(body, names_of_interest)
        for word in word_dict:
            db.loc[id, word] = word_dict[word]
        party_dict = word_lookup(body, parties)
        for word in party_dict:
            db.loc[id, word] = party_dict[word]
    # %%
    db.to_csv("data_processed/" + site_name + "_analyzed.csv", index=False)