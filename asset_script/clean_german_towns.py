# %%
import pandas as pd
import re
# %%
raw_town_csv = pd.read_csv("../data/german_towns.csv")
# %%
# raw_town_csv.describe()
raw_town_csv.head()
wip_raw_town_csv = raw_town_csv.copy()
# %%

# %%
wip_raw_town_csv = pd.DataFrame(wip_raw_town_csv.german_cities.str.rsplit('(', 1).tolist(),
                                columns=['german_cities', 'german_states'])

# %%

wip_raw_town_csv["german_states"] = wip_raw_town_csv["german_states"].str.replace(
    r'\)', '')
# %%

wip_raw_town_csv.groupby(['german_states'])['german_cities'].count()

# %%
wip_raw_town_csv.to_csv("../data/clean_german_towns.csv")

# %%
