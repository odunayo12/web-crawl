# %%
import pandas as pd
# %%
k = "https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&fos=&cert=&admReq=&scholarshipLC=&scholarshipSC=&degree%5B%5D=1&langDeAvailable=&langEnAvailable=&lang%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&dur%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&subjects%5B%5D=&limit=10&offset=&display=list&fee=&bgn%5B%5D=".rsplit(
    "offset", 1)

# %%

# parsed_url = f"" + \
#     split_url[0] + "="+"{" + str(target_list)+"}" + \
#     "="+split_url[1]+"="+split_url[2]
