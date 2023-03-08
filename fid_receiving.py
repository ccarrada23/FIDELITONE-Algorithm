# read the column that has all the SKU_ids written
# you want to know which SKUs are not in my system 
# don't run the algorithm on those that are not in the system

import pandas as pd


def read_from_excel():
    df = pd.read_excel("./Fid-Receiving.xlsx")
    SKUs_to_slot = {0: None}
    i = 1
    for index, row in df.iterrows():
        SKUs_to_slot[i] = row["Material Code"]
        i += 1
    return SKUs_to_slot

SKUs_to_slot = read_from_excel()

# now you want to check if all unique SKUs in this list are on your SKU_map
# get a list of what's not there, run the algorithm on what is there. 
# even if you give jeff 90% of the total slotting positions from the file
# it will work

