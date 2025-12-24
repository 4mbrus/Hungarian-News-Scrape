#%%
import os
import pandas as pd
#%%
list = os.listdir("../data_raw")
sites = []
for file in list:
    sites.append(file.split("_")[0])
# %%
combined_df = pd.DataFrame(columns=["date","topic"])
for site in sites:
    temp_df = pd.read_csv(f"{site}_binary_mentions.csv")
    var_cols = temp_df.columns[1:]
    temp_df = pd.melt(temp_df, id_vars=["date"], value_vars=var_cols, value_name=site, var_name="topic")
    combined_df = combined_df.merge(temp_df, how="outer", on=["date","topic"])

# %%
var_cols = combined_df.columns[2:]
combined_df = pd.melt(combined_df, id_vars=["date", "topic"], value_vars=var_cols, var_name="news_site", value_name="n_of_articles")
combined_df
#%%
combined_df.to_csv("combined_binary_summary.csv")
# %%
