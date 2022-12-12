import pandas as pd
from SKUClass import * 
import json

def json_to_dict(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data
def get_SKU_map():
    df = pd.read_excel("./Velocity_And_Weight.xlsx")
    association_lists = json_to_dict("./preprocess/top_association_map.json")
    SKU_map = {0: None}
    i = 1
    for index, row in df.iterrows():
        association_list = []
        if row["SKU ID"] in association_lists:
            association_list = association_lists[row["SKU ID"]]
        SKU_map[i] = SKU(row["SKU ID"], row["Z_Weight_scaled"], row["Z_Vel_scaled"], association_list, i)
        i+=1
    return SKU_map

SKU_map = get_SKU_map()
# print(SKU_map[1].key, (SKU_map[1].associationList))

    
def get_key(val):
    for key, value in SKU_map.items():
        if value and val == value.UID:
            return key
    return "key doesn't exist"

item_assoc_w_one = SKU_map[54].associationList
# for assoc_item_uid in item_assoc_w_one:
#     print(get_key(assoc_item_uid))
# print(get_key(SKU_map[1].UID))

# print(get_SKU_map()[1].associationList)

curr_SKU_list = SKU_map[1].associationList

for sku in curr_SKU_list:
    sku_map_key = get_key(sku)
    # print(sku_map_key == SKU_map[sku_map_key].key)