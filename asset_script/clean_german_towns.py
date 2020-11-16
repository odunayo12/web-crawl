# %%
from numpy.core.numeric import outer
import pandas as pd
import re

from pandas.core.reshape.merge import merge
# %%
raw_town_csv = pd.read_csv("../data/german_towns.csv")
raw_masters_csv = pd.read_csv("../data/masters_csv_df.csv")
# %%
# raw_town_csv.describe()
raw_town_csv.head()
wip_raw_town_csv = raw_town_csv.copy()
wip_raw_masters_csv = raw_masters_csv.copy()
# %%
wip_raw_masters_csv.head()
# %%
wip_raw_town_csv = pd.DataFrame(wip_raw_town_csv.german_cities.str.rsplit('(', 1).tolist(),
                                columns=['german_cities', 'german_states'])

# %%

wip_raw_town_csv["german_states"] = wip_raw_town_csv["german_states"].str.replace(
    r'\)', '')
# %%
wip_raw_town_csv.head()
# %%
wip_raw_masters_csv = wip_raw_masters_csv.rename(
    {'uni_city': 'german_cities'}, axis=1)
# %%
wip_raw_town_csv.groupby(['german_states'])['german_cities'].count()

# %%
wip_raw_town_csv.to_csv("../data/clean_german_towns.csv")


# %%
# clear trailing spaces
# wip_raw_masters_csv.uni_city = [c.strip()
#                                 for c in wip_raw_masters_csv.uni_city]
wip_raw_town_csv.german_cities = [c.strip()
                                  for c in wip_raw_town_csv.german_cities]
# %%

# g = merged_master_df = wip_raw_town_csv.merge(
#     wip_raw_masters_csv, left_on="german_cities", right_on="uni_city")


g = merged_master_df = wip_raw_masters_csv.merge(
    wip_raw_town_csv, left_on="german_cities", right_on="german_cities")
# %%
g.tail(n=25)
# %%
g.groupby(['german_states'])['tution_fee'].count()

# %%

merged_master_df.to_csv("../data/merged_master_df.csv")

# %%
g.groupby('german_states').filter(lambda group: group.tution_fee == "none")

# %%
