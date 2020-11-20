# %%
# pyright: reportUnboundVariable=false
import numpy as np
from numpy.core.numeric import outer
from numpy.lib.function_base import select
import pandas as pd
import re
import glob

from pandas.core.reshape.merge import merge


# %%
# functions
missing_in_german_states = {'Hannover': 'Hanover', 'München': 'Munich', 'Garching b. München': 'Garching bei München', 'Köln': 'Cologne',
                            'Friedberg (Hessen)': 'Friedberg', 'Kempten (Allgäu)': 'Kempten im Allgäu', 'Weidenbach': 'Weiden in der Oberpfalz',
                            'Wedel (Holstein)': 'Wedel', 'Leer (Ostfriesland)': 'Leer', 'Bergholz-Rehbrücke': 'Potsdam',
                            'Bernburg / Saale': 'Bernburg', 'Nürnberg': 'Nuremberg', 'Singapore': 'Munich', 'Köthen / Anhalt': 'Köthen',
                            'Hermannsburg': 'Hanover', 'Hoppstädten-Weiersbach': 'Birkenfeld', 'Eggenstein-Leopoldshafen': 'Karlsruhe', 'Lutherstadt Wittenberg': 'Wittenberg'}


def clean_german_cities():
    """
    read and returns a clean datframe
    """
    wip_raw_town_csv = pd.read_csv("../data/german_towns.csv")
    wip_raw_town_csv = pd.DataFrame(wip_raw_town_csv.german_cities.str.rsplit('(', 1).tolist(),
                                    columns=['german_cities', 'german_states'])
    wip_raw_town_csv["german_states"] = wip_raw_town_csv["german_states"].str.replace(
        r'\)', '')
    wip_raw_town_csv.german_cities = [c.strip()
                                      for c in wip_raw_town_csv.german_cities]
    return wip_raw_town_csv


def read_data_n_merge(data_file_address, clean_germancities):
    """
    read and merge csv
    data_file_address = directory of the to-be read file
    clean_germancities = aclean file with non-changing content to be merged. 
    """
    filename_ = data_file_address.rsplit("_", 2)[0].rsplit("/", 1)[1]
    data_address = pd.read_csv(data_file_address)

    data_address = data_address.rename(
        {'uni_city': 'german_cities'}, axis=1)
    data_address['german_cities_dup'] = data_address['german_cities']
    data_address['german_cities_dup'] = data_address['german_cities_dup'].replace(
        missing_in_german_states)
    merge_out_name = merge(data_address, clean_germancities,
                           left_on="german_cities_dup", right_on="german_cities", how='left')
    if (merge_out_name["german_states"].isnull().sum()) == 0:
        merge_out_name.to_csv(f"../data/merged_{filename_}_df.csv")
    else:
        german_states__nan = merge_out_name[merge_out_name["german_states"].isnull(
        )]
        print(german_states__nan.german_cities_x.unique())


def summary_shape(df_1, df_2, df_1_n_2):
    """
    df_1, df_2 = dfs to merge 
    df_1_n_2 after merge
    the fxtn relates the shape of conctenated or merged dataframe before and after merge,
    """
    print_text = print(
        f"The fisrt dataframe has {df_1.shape}\nThe Second dataframe has {df_2.shape}\nThe merged dataframe has {df_1_n_2.shape}")
    return print_text


# %%
# packing all files
raw_bachelors, raw_masters, raw_phd_csv, raw_prep_csv, raw_lang_course = "../data/bachelor_csv_df.csv", "../data/masters_csv_df.csv", "../data/phd_csv_df.csv", "../data/prep_course_csv_df.csv", "../data/lang_course_csv_df.csv"

complete_file_address = [raw_bachelors, raw_masters,
                         raw_phd_csv, raw_prep_csv, raw_lang_course]
# %%
#
clean_german = clean_german_cities()
for target_list in complete_file_address:
    read_data_n_merge(target_list, clean_german)

# %%

# %%
# test with bachelors
raw_bachelors_csv = pd.read_csv("../data/bachelor_csv_df.csv")
wip_raw_bachelors_csv = raw_bachelors_csv.copy()
raw_town_csv = pd.read_csv("../data/german_towns.csv")
wip_raw_town_csv = raw_town_csv.copy()
# raw_bachelors_csv.head()

wip_raw_town_csv = pd.DataFrame(wip_raw_town_csv.german_cities.str.rsplit('(', 1).tolist(),
                                columns=['german_cities', 'german_states'])
wip_raw_town_csv["german_states"] = wip_raw_town_csv["german_states"].str.replace(
    r'\)', '')
wip_raw_town_csv.german_cities = [c.strip()
                                  for c in wip_raw_town_csv.german_cities]
wip_raw_bachelors_csv = wip_raw_bachelors_csv.rename(
    {'uni_city': 'german_cities'}, axis=1)
wip_raw_bachelors_csv['german_cities_dup'] = wip_raw_bachelors_csv['german_cities']
wip_raw_bachelors_csv['german_cities_dup'] = wip_raw_bachelors_csv['german_cities_dup'].replace(
    missing_in_german_states)
# %%
g = merged_bachelors_df = merge(wip_raw_bachelors_csv, wip_raw_town_csv,
                                left_on="german_cities_dup", right_on="german_cities", how='left')
# %%
# %%
print("wip_raw_masters_csv dimensions: {}".format(wip_raw_bachelors_csv.shape))
print("merged_master_df dimensions: {}".format(merged_bachelors_df.shape))
print("There are {} missing values in merged_master_df".format(
    merged_bachelors_df["german_states"].isnull().sum()))

# %%
german_states__nan = merged_bachelors_df[merged_bachelors_df["german_states"].isnull(
)]

# %%
# concatenating merged files
# stores file address with pattern = "merged"
files_dir = glob.glob(r"../data/*merged*")
len(files_dir)
# %%
bach_to_merge = pd.read_csv(files_dir[0])
# %%
dash_, slash_ = "_", "\\"
# reads the stored file address in to csv
all_df = [pd.read_csv(file_) for file_ in files_dir]

# a dict returning each filename and colum names
all_to_merge = [{f"{file_.rsplit(slash_, 1)[1]}": pd.read_csv(
    file_).columns} for file_ in files_dir]
all_to_merge
all_df[0]
# %%
# select needed columns for masters and bachelors dataframe
bach_n_master = [a[['course_name', 'uni_name',
                    'german_cities_x', 'tution_fee', 'german_cities_dup',
                    'german_cities_y', 'german_states',  'lang_of_instr',
                    'dura_of_study', 'semester_beginning', 'online_course_elemen']] for a in [all_df[0], all_df[2]]]
# bach_n_master[0].head()
bach_n_master_concatD = pd.concat([bach_n_master[0], bach_n_master[1]], axis=0)

# %%
#summary_shape(bach_n_master[0], bach_n_master[1], bach_n_master_concatD)
bach_n_master_concatD.to_csv("../data/bach_n_master_concatD.csv")
# %%
# TODO: refactor columns content to binary or tenary
