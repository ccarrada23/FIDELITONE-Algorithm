import pandas as pd 
from classes import Graph

# SKU_locations = {0: None}

def read_from_excel():
    df = pd.read_excel("./Fid-InventoryByLocation_updated.xlsx")
    SKU_locations = {0: None}
    i = 1
    for index, row in df.iterrows():
        SKU_locations[i] = [(row["Row"], row["Bay"], row["Level"], row["Spot"], row["Material Code"])]
        i += 1
    return SKU_locations

SKU_locations = read_from_excel()


# test_SKUlocs = {0: None,
#                 1: SKU_locations[875],
#                 2: SKU_locations[876],
#                 3: SKU_locations[877],
#                 4: SKU_locations[878]}
           
# what you need from A : [(2, 1, 'BB', 2)]
# A[0] = needs to translate to the correct row 
# A_ and B_ : 23
# C_ : 22
# D_ : 21
# E_ : 20
# F_ : 19
# G_ : 18    this has to be the other way around actually
# you need a map for these
# you need a map that tells the correct column 
# A[1] = needs to translate to the rack in the row being talked about
# so you have to map the bay to the correct rack
# 2 gives row, 1 gives rack 
# A gives row, _ gives nothing, 1 gives rack
'''
def row_map(SKU_location): # called using one row of SKU_locations
    # you need to go to SKU_locations and identify the 2nd index
    # as the bay to make decision about whether the correct map is
    # one with 23: A or 23: B
    SKU_loc = SKU_location
    if SKU_loc[0] == 23: # sku in either A_ or B_
        if SKU_loc[1] <= 8: # TODO: means bay is situated in B_ 
            map_for_rows = {23: 'B',
                            22: 'C',
                            21: 'D',
                            20: 'E',
                            19: 'F',
                            18: 'G',
                            17: 'H',
                            16: 'I',
                            15: 'J',
                            14: 'K',
                            13: 'L',
                            12: 'M',
                            11: 'N',
                            10: 'O',
                            9: 'P',
                            8: 'Q',
                            7: 'R',
                            6: 'S',
                            5: 'T',
                            4: 'U',
                            3: 'V',
                            2: 'W',
                            1: 'X' } 
        else:
            map_for_rows = {23: 'A',
                            22: 'C',
                            21: 'D',
                            20: 'E',
                            19: 'F',
                            18: 'G',
                            17: 'H',
                            16: 'I',
                            15: 'J',
                            14: 'K',
                            13: 'L',
                            12: 'M',
                            11: 'N',
                            10: 'O',
                            9: 'P',
                            8: 'Q',
                            7: 'R',
                            6: 'S',
                            5: 'T',
                            4: 'U',
                            3: 'V',
                            2: 'W',
                            1: 'X' }
    else:
        map_for_rows = {23: 'A',
                            22: 'C',
                            21: 'D',
                            20: 'E',
                            19: 'F',
                            18: 'G',
                            17: 'H',
                            16: 'I',
                            15: 'J',
                            14: 'K',
                            13: 'L',
                            12: 'M',
                            11: 'N',
                            10: 'O',
                            9: 'P',
                            8: 'Q',
                            7: 'R',
                            6: 'S',
                            5: 'T',
                            4: 'U',
                            3: 'V',
                            2: 'W',
                            1: 'X' }  
    return map_for_rows

'''
# unimportant function

# next task is to correlate the bay in [1] index to the correct _# in my code
# [(2, 3, CC, 1)] 
def bay_map(one_SKU_location): # is being called on only one row of the dict 
    # SKU_location_dict = SKU_locations
    bay_map_toreturn = {}
    
    # you can have maps for rows 23, 22, 21, 20, 19, 
    # 18, 17, 14, 13, 12, 11, 10, 9, 8, 7
    if one_SKU_location[0] == 6 or one_SKU_location[0] == 5 or one_SKU_location[0] == 1:
        # to_check = one_SKU_location[0]
        return
    
### 
    if one_SKU_location[0] == 2:
        
        w1 = 1
        for i in range(1, 16):
            bay_map_toreturn[i] = 'W_' + str(15 - w1)
            w1 += 1

###

    if one_SKU_location[0] == 3:
        
        v1 = 1
        for i in range(1, 16):
            bay_map_toreturn[i] = 'V_' + str(15 - v1)
            v1 += 1
            
###

    if one_SKU_location[0] == 4:
        
        u1 = 1
        for i in range(1, 16):
            bay_map_toreturn[i] = 'U_' + str(15 - u1)
            u1 += 1
            
###   
    if one_SKU_location[0] == 23:
        bay_map_toreturn = {1: 'B_7',
                            2: 'B_6',
                            3: 'B_5',
                            4: 'B_4',
                            5: 'B_3',
                            6: 'B_2',
                            7: 'B_1',
                            8: 'B_0'
                            }
        
        a = 9
        for i in range(9, 37):
            curr_A_bay_num = i
            bay_map_toreturn[curr_A_bay_num] = 'A_' + str(36 - a)
            a += 1
### 
    if one_SKU_location[0] == 15:
        
        j3 = 1
        for i in range(1, 6):
            bay_map_toreturn[i] = 'J3_' + str(5 - j3)   
            j3 += 1
            
        j2 = 1
        for i in range(7, 15):
            bay_map_toreturn[i] = 'J2_' + str(8 - j2)
            j2 += 1
            
        j1 = 1
        for i in range(16, 25):
            bay_map_toreturn[i] = 'J1_' + str(9 - j1)
            j1 += 1

##  

    if one_SKU_location[0] == 16:
        
        i3 = 1
        for i in range(1, 6):
            bay_map_toreturn[i] = 'I3_' + str(5 - i3)   
            i3 += 1
            
        i2 = 1
        for i in range(7, 15):
            bay_map_toreturn[i] = 'I2_' + str(8 - i2)
            i2 += 1
            
        i1 = 1
        for i in range(16, 25):
            bay_map_toreturn[i] = 'I1_' + str(9 - i1)
            i1 += 1
            
##
     
    if one_SKU_location[0] == 22:
        # all follow the same idea mostly
        # all of these rows have the same number of bays situated at the correct places
        # or SKU_location[0] == 21 or SKU_location[0] == 14 or SKU_location[0] == 13 or SKU_location[0] == 10 or SKU_location[0] == 9 or SKU_location[0] == 8 or SKU_location[0] == 7:
        c2 = 1
        for i in range(1, 9):
            curr_C_bay_num = i
            bay_map_toreturn[curr_C_bay_num] = 'C2_' + str(8 - c2)
            c2 += 1
            
        c1 = 1
        for i in range(10, 19):
            curr_C_bay_num = i
            bay_map_toreturn[curr_C_bay_num] = 'C1_' + str(9 - c1)
            c1 += 1
###           
    if one_SKU_location[0] == 21:
        
        d2 = 1
        for i in range(1, 9):
            curr_D_bay_num = i
            bay_map_toreturn[curr_D_bay_num] = 'D2_' + str(8 - d2)
            d2 += 1
            
        d1 = 1
        for i in range(10, 19):
            curr_D_bay_num = i
            bay_map_toreturn[curr_D_bay_num] = 'D1_' + str(9 - d1)
            d1 += 1
    
###
    if one_SKU_location[0] == 14:
        
        k2 = 1
        for i in range(1, 9):
            curr_K_bay_num = i
            bay_map_toreturn[curr_K_bay_num] = 'K2_' + str(8 - k2)
            k2 += 1
            
        k1 = 1
        for i in range(10, 19):
            curr_K_bay_num = i
            bay_map_toreturn[curr_K_bay_num] = 'K1_' + str(9 - k1)
            k1 += 1
        
###       
    if one_SKU_location[0] == 13:
        
        l2 = 1
        for i in range(1, 9):
            curr_L_bay_num = i
            bay_map_toreturn[curr_L_bay_num] = 'L2_' + str(8 - l2)
            l2 += 1
            
        l1 = 1
        for i in range(10, 19):
            curr_L_bay_num = i
            bay_map_toreturn[curr_L_bay_num] = 'L1_' + str(9 - l1)
            l1 += 1

###
    if one_SKU_location[0] == 10:
        
        o2 = 1
        for i in range(1, 9):
            curr_O_bay_num = i
            bay_map_toreturn[curr_O_bay_num] = 'O2_' + str(8 - o2)
            o2 += 1
            
        o1 = 1
        for i in range(10, 19):
            curr_O_bay_num = i
            bay_map_toreturn[curr_O_bay_num] = 'O1_' + str(9 - o1)
            o1 += 1        

###
    if one_SKU_location[0] == 9:
        
        p2 = 1
        for i in range(1, 9):
            curr_P_bay_num = i
            bay_map_toreturn[curr_P_bay_num] = 'P2_' + str(8 - p2)
            p2 += 1
            
        p1 = 1
        for i in range(10, 19):
            curr_P_bay_num = i
            bay_map_toreturn[curr_P_bay_num] = 'P1_' + str(9 - p1)
            p1 += 1       
    
###
    if one_SKU_location[0] == 8:
        
        q2 = 1
        for i in range(1, 9):
            curr_Q_bay_num = i
            bay_map_toreturn[curr_Q_bay_num] = 'Q2_' + str(8 - q2)
            q2 += 1
            
        q1 = 1
        for i in range(10, 19):
            curr_Q_bay_num = i
            bay_map_toreturn[curr_Q_bay_num] = 'Q1_' + str(9 - q1)
            q1 += 1   
        
###
    if one_SKU_location[0] == 7:
        
        r2 = 1
        for i in range(1, 9):
            curr_R_bay_num = i
            bay_map_toreturn[curr_R_bay_num] = 'R2_' + str(8 - r2)
            r2 += 1
            
        r1 = 1
        for i in range(10, 19):
            curr_R_bay_num = i
            bay_map_toreturn[curr_R_bay_num] = 'R1_' + str(9 - r1)
            r1 += 1
        
### three other cases left 
# for rows 20 to 17, which is 20, 19, 18, 17, the logic is the same 
# you have to go from 3 to 1 for the following letters E,F,G,H
# 
    if one_SKU_location[0] == 20:
        
        e3 = 1
        for i in range(1, 7):
            curr_E_bay_num = i
            bay_map_toreturn[curr_E_bay_num] = 'E3_' + str(6 - e3)
            e3 += 1             
            
        e2 = 1
        for i in range(8, 16):
            bay_map_toreturn[i] = 'E2_' + str(8 - e2)
            e2 += 1
            
        e1 = 1
        for i in range(17, 26):
            bay_map_toreturn[i] = 'E1_' + str(9 - e1)
            e1 += 1
        
###

    if one_SKU_location[0] == 17:
        
        h3 = 1
        for i in range(1, 7):
            curr_E_bay_num = i
            bay_map_toreturn[curr_E_bay_num] = 'H3_' + str(6 - h3)
            h3 += 1             
            
        h2 = 1
        for i in range(8, 16):
            bay_map_toreturn[i] = 'H2_' + str(8 - h2)
            h2 += 1
            
        h1 = 1
        for i in range(17, 26):
            bay_map_toreturn[i] = 'H1_' + str(9 - h1)
            h1 += 1
            
###

    if one_SKU_location[0] == 18:
        
        g3 = 1
        for i in range(1, 7):
            curr_G_bay_num = i
            bay_map_toreturn[curr_G_bay_num] = 'G3_' + str(6 - g3)
            g3 += 1             
            
        g2 = 1
        for i in range(8, 16):
            bay_map_toreturn[i] = 'G2_' + str(8 - g2)
            g2 += 1
            
        g1 = 1
        for i in range(17, 26):
            bay_map_toreturn[i] = 'G1_' + str(9 - g1)
            g1 += 1
            
###

    if one_SKU_location[0] == 19:
        
        f3 = 1
        for i in range(1, 7):
            curr_E_bay_num = i
            bay_map_toreturn[curr_E_bay_num] = 'F3_' + str(6 - f3)
            f3 += 1             
            
        f2 = 1
        for i in range(8, 16):
            bay_map_toreturn[i] = 'F2_' + str(8 - f2)
            f2 += 1
            
        f1 = 1
        for i in range(17, 26):
            bay_map_toreturn[i] = 'F1_' + str(9 - f1)
            f1 += 1
        
### the only left now is M row and N row
# facts about M and N:  M1_0 to M1_12 and M2_0 to M2_11 
# 13 for the M1 row and 12 for the M2 row; same logic with N

###
    if one_SKU_location[0] == 12:
        
        m2 = 1
        for i in range(1, 14):
            bay_map_toreturn[i] = 'M2_' + str(13 - m2)
            m2 += 1
            
        m1 = 1
        for i in range(14, 27):
            bay_map_toreturn[i] = 'M1_' + str(13 - m1)
            m1 += 1
        
###
    if one_SKU_location[0] == 11:
        
        n2 = 1
        for i in range(1, 14):
            bay_map_toreturn[i] = 'N2_' + str(13 - n2)
            n2 += 1
            
        n1 = 1
        for i in range(14, 27): # we want this at 14: 
            bay_map_toreturn[i] = 'N1_' + str(13 - n1)
            n1 += 1
    
    return bay_map_toreturn     
# this function below must call the bay_func to know which rack is being talked about from the map
# when we obtain say M1_3 from using the bay map from above by doing mesh = graph.get_rack('M1_3').rackLocations
# within these rack locations you know the last row index 'AA' : len(mesh[0]) - 1
# you keep increasing the decrement of one and go on until we get to something like FF which doesnt exist and will never be assigned
# 

# call the function on rack_name like 'M_1'
# now use the rack to get what you want
def find_row_and_spot(rack_name, graph, SKU_location): # (1, 2, AA, 2) its being called on this 
    
    correct_level = SKU_location[2]
    
    annex = graph
    rack_mesh = annex.get_rack(rack_name).rackLocations
    rows_num_in_rack = len(rack_mesh[0])
    
    level_map = { 
        'AA': rows_num_in_rack - 1,
        'BB': rows_num_in_rack - 2,
        'CC': rows_num_in_rack - 3,
        'DD': rows_num_in_rack - 4,
        'EE': rows_num_in_rack - 5, 
        'FF': rows_num_in_rack - 6,
        'GG' : rows_num_in_rack - 7
    }
    
    row_idx_toreturn = level_map[correct_level]
    
    # now we have the right rack and row, 
    # for finding spot, you need to relate number to column in that row
    # meaning you will still need rack_mesh[0][0]
    
    # column logic works normally for odd numbered rows on the right of the double columns
   

    if SKU_location[0] == 23 or SKU_location[0] == 21 or SKU_location[0] == 19 or SKU_location[0] == 17 or SKU_location[0] == 15 or SKU_location[0] == 13 or SKU_location[0] == 11 or SKU_location[0] == 9 or SKU_location[0] == 7 or SKU_location[0] == 5 or SKU_location[0] == 3 or SKU_location[0] == 1:
            
        col_idx_toreturn = SKU_location[3] - 1
             
    else:
        col_idx_toreturn = len(rack_mesh[0][row_idx_toreturn]) - SKU_location[3]
          
            
    return row_idx_toreturn, col_idx_toreturn


# def translate_locations_graph(SKU_locs, graph):
    
#     # SKU_locs = SKU_locations
#     translated_locations = []
#     # you wanna say that if the next iteratoin has the same number in row as the last one use the
#     # same graph_dict
#     # but if not, we will call bay_map again and create an appropriate graph
#     # every loc_index has a location stored in [(row, bay, level, spot)] structure
#     # you want to say if the new loc index stores the same row that the previous loc_index 
#     # don't call bay_map, use the grpah dict that was created for the last loc idex exlplored
#     # you only call bay_map for the indices that don't have the same row stored in the previous loc index 
#     for loc_index in SKU_locs:
#         # loc_prev = loc_index - 1
#         if loc_index == 0:
#             # one_SKU_location[0] == 16 or one_SKU_location[0] == 15 or one_SKU_location[0] == 6 or one_SKU_location[0] == 5 or one_SKU_location[0] == 4 or one_SKU_location[0] == 3 or one_SKU_location[0] == 2 or one_SKU_location[0] == 1:
#             continue
#         loc_prev = loc_index - 1
        
#         graph_dict = bay_map(SKU_locs[loc_index][0]) # this dictionary contains the information that translates the [0] index 'row' and [1] index 'bay'
        
#         rack_index = SKU_locs[loc_index][0][1]
#         correct_rack = graph_dict[rack_index] # get correct rack here
        
#         row_idx, col_index = find_row_and_spot(correct_rack, graph, SKU_locs[loc_index][0])
#         translated_locations.append([correct_rack, row_idx, col_index])
        
#     return translated_locations

# TODO: make more efficient by not generating a new map every row.
# TODO: 

def translate_locations_graph(SKU_locs, graph):
    
    # SKU_locs = SKU_locations
    translated_locations = []
    # you wanna say that if the next iteratoin has the same number in row as the last one use the
    # same graph_dict
    # but if not, we will call bay_map again and create an appropriate graph
    # every loc_index has a location stored in [(row, bay, level, spot)] structure
    # you want to say if the new loc index stores the same row that the previous loc_index 
    # don't call bay_map, use the grpah dict that was created for the last loc idex exlplored
    # you only call bay_map for the indices that don't have the same row stored in the previous loc index 
    prev_graph_dict = None
    
    for loc_index in SKU_locs:
        
        if loc_index == 3586:
            return translated_locations
        
        if loc_index == 0:
            continue
        
        loc_prev = loc_index - 1
        
        # when keyError is raised for the top no bottom rack
        # you need to skip the iterations that will raise it
        # bay = 9 for row R and Q will raise it
        
        if SKU_locs[loc_index][0][0] == 7 or SKU_locs[loc_index][0][0] == 8 or SKU_locs[loc_index][0][0] == 13 or SKU_locs[loc_index][0][0] == 14 or SKU_locs[loc_index][0][0] == 9 or SKU_locs[loc_index][0][0] == 10:
            if SKU_locs[loc_index][0][1] == 9:
                continue
            
        if SKU_locs[loc_index][0][0] == 15 or SKU_locs[loc_index][0][0] == 16:
            if SKU_locs[loc_index][0][1] == 6 or SKU_locs[loc_index][0][1] == 15:
                continue
            
        if SKU_locs[loc_index][0][0] == 17 or SKU_locs[loc_index][0][0] == 18 or SKU_locs[loc_index][0][0] == 19 or SKU_locs[loc_index][0][0] == 20:
            if SKU_locs[loc_index][0][1] == 7 or SKU_locs[loc_index][0][1] == 16:
                continue
        
        if SKU_locs[loc_index][0][0] == 21 or SKU_locs[loc_index][0][0] == 22:
            if SKU_locs[loc_index][0][1] == 9:
                continue
        
        if loc_prev != 0:
            if SKU_locs[loc_index][0][0] == SKU_locs[loc_prev][0][0]:
                graph_to_use = prev_graph_dict
                rack_index = SKU_locs[loc_index][0][1]
                correct_rack = graph_to_use[rack_index] # get correct rack here
            
                row_idx, col_index = find_row_and_spot(correct_rack, graph, SKU_locs[loc_index][0])
                translated_locations.append([correct_rack, row_idx, col_index, SKU_locs[loc_index][0][4]])
                
        graph_dict = bay_map(SKU_locs[loc_index][0]) # this dictionary contains the information that translates the [0] index 'row' and [1] index 'bay'
        
        rack_index = SKU_locs[loc_index][0][1]
        correct_rack = graph_dict[rack_index] # get correct rack here
        
        row_idx, col_index = find_row_and_spot(correct_rack, graph, SKU_locs[loc_index][0])
        translated_locations.append([correct_rack, row_idx, col_index, SKU_locs[loc_index][0][4]])
        
        prev_graph_dict = graph_dict
        
    return translated_locations