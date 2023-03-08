# import pandas as pd

# def read_from_excel():
#     df = pd.read_excel("./Fid-InventoryByLocation_new.xlsx")
#     SKU_locations = {0: None}
#     i = 1
#     for index, row in df.iterrows():
#         SKU_locations[i] = [(row["Row"], row["Bay"], row["Level"], row["Spot"], row["Material Code"])]
#         i += 1
#     return SKU_locations

# df = pd.read_excel("./Fid-InventoryByLocation_new.xlsx")
# SKU_locs = {0: None}
# i = 3
# for index, row in df.iterrows():
#     SKU_locs[i] = [row["Row"]]
#     i -= 1
#     if i == 0:
#         break