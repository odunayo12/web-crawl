# %%
import numpy as np
from numpy.core.numeric import outer
import pandas as pd
import re

from pandas.core.reshape.merge import merge
# %%
raw_town_csv = pd.read_csv("../data/german_towns.csv")
raw_masters_csv = pd.read_csv("../data/masters_csv_df.csv")
# %%
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

wip_raw_town_csv.german_cities = [c.strip()
                                  for c in wip_raw_town_csv.german_cities]

wip_raw_masters_csv['german_cities_dup'] = wip_raw_masters_csv['german_cities']
# %%

# wip_raw_town_csv.groupby(['german_states'])['german_cities'].count()

# %%
# wip_raw_town_csv.to_csv("../data/clean_german_towns.csv")


# %%
# clear trailing spaces
# wip_raw_masters_csv.uni_city = [c.strip()
#                                 for c in wip_raw_masters_csv.uni_city]

# %%
missing_in_german_states = {'Hannover': 'Hanover', 'München': 'Munich', 'Garching b. München': 'Garching bei München', 'Köln': 'Cologne',
                            'Friedberg (Hessen)': 'Friedberg', 'Kempten (Allgäu)': 'Kempten im Allgäu', 'Weidenbach': 'Weiden in der Oberpfalz',
                            'Wedel (Holstein)': 'Wedel', 'Leer (Ostfriesland)': 'Leer', 'Bergholz-Rehbrücke': 'Potsdam',
                            'Bernburg / Saale': 'Bernburg', 'Nürnberg': 'Nuremberg', 'Singapore': 'Munich', 'Köthen / Anhalt': 'Köthen',
                            'Hermannsburg': 'Hanover', 'Hoppstädten-Weiersbach': 'Birkenfeld'}

# names_in_german_towns = ['Hanover', 'Munich', 'Garching bei München', 'Cologne',
#                          'Friedberg', 'Kempten im Allgäu', 'Weiden in der Oberpfalz',
#                          'Wedel', 'Leer', 'Potsdam',
#                          'Bernburg', 'Nuremberg', 'Munich', 'Köthen']
#len(missing_in_german_states) == len(names_in_german_towns)
# %%
# for missing_ in missing_in_german_states:
#     for names_ in names_in_german_towns:
#         wip_raw_masters_csv['german_cities_dup'] = np.where(
#             wip_raw_masters_csv['german_cities_dup'] == missing_,
#             names_,
#             wip_raw_masters_csv['german_cities_dup']
#         )

wip_raw_masters_csv['german_cities_dup'] = wip_raw_masters_csv['german_cities_dup'].replace(
    missing_in_german_states)
# %%

g = merged_master_df = merge(wip_raw_masters_csv, wip_raw_town_csv,
                             left_on="german_cities_dup", right_on="german_cities", how='left')
# %%
g.tail(n=25)
# %%
# bachelors
raw_bachelors_csv = pd.read_csv("../data/bachelor_csv_df.csv")
wip_raw_bachelors_csv = raw_bachelors_csv.copy()
raw_bachelors_csv.head()
wip_raw_bachelors_csv = wip_raw_bachelors_csv.rename(
    {'uni_city': 'german_cities'}, axis=1)
wip_raw_bachelors_csv['german_cities_dup'] = wip_raw_bachelors_csv['german_cities']
wip_raw_bachelors_csv['german_cities_dup'] = wip_raw_bachelors_csv['german_cities_dup'].replace(
    missing_in_german_states)
g = merged_bachelors_df = merge(wip_raw_bachelors_csv, wip_raw_town_csv,
                                left_on="german_cities_dup", right_on="german_cities", how='left')
# %%
# %%
print("wip_raw_masters_csv dimensions: {}".format(wip_raw_bachelors_csv.shape))
print("merged_master_df dimensions: {}".format(merged_bachelors_df.shape))
print("There are {} missing values in merged_master_df".format(
    merged_bachelors_df["german_states"].isnull().sum()))

# %%
# german_states__ = merged_master_df.german_states[
#     merged_master_df.isnull().any(axis=1)]

german_states__nan = merged_bachelors_df[merged_bachelors_df["german_states"].isnull(
)]

# %%
g.groupby(['german_states'])['tution_fee'].count()
# %%

merged_master_df.to_csv("../data/merged_master_df.csv")

# %%
#g.groupby('german_states').filter(lambda group: group.tution_fee == "none")

# %%
