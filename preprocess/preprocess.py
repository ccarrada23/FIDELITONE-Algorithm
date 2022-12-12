import pandas as pd
import numpy as np
import json

df = pd.read_excel("./sku_breakout.XLSX")

SKU_list = df["Item Number"].unique()
SKU_map = dict()
for i, item in enumerate(SKU_list):
    SKU_map[item] = i
association_mat = np.zeros((len(SKU_list), len(SKU_list)))

for order_number in df["Customer Order Number"].unique():
    curr_df = df[df["Customer Order Number"] == order_number]
    items_in_order = curr_df["Item Number"].unique()
    for item1 in items_in_order:
        for item2 in items_in_order:
            item1Num = SKU_map[item1]
            item2Num = SKU_map[item2]
            if item1Num != item2Num:
                association_mat[item1Num][item2Num] += 1
                
def get_key(val):
    for key, value in SKU_map.items():
        if val == value:
            return key
    return "key doesn't exist"

def argmax(row):
    sku = ""
    max_val = -1
    i_at_max_val = -1
    for i, num in enumerate(row):
        if num > max_val:
            max_val = num
            sku = get_key(i)
            i_at_max_val = i
        row[i_at_max_val] = -1
    return row, sku

top_association_map = dict()
for sku in SKU_map.keys():
    top_association_map[sku] = []

num_top = 4

for i, row in enumerate(association_mat):
    curr_sku = get_key(i)
    for j in range(num_top):
        row, sku = argmax(row)
        top_association_map[curr_sku].append(sku)

json = json.dumps(top_association_map)
 
f = open("top_association_map.json","w")

f.write(json)

f.close()