from itertools import count
import numpy as np
from distanceFunction import *
import pandas as pd
import json
import statistics
from classes import *
from sku_generator import *

# def scale_weights(sku):
    # you will call it on sku
    # get the .weight of the sku
    # you will get the min of those weights first 

# def get_SKU_map():
#     df = pd.read_excel("./velocity_weight.xlsx")
#     association_lists = json_to_dict("./preprocess/top_association_map.json")
#     SKU_map = {0: None}
#     i = 1
#     for index, row in df.iterrows():
#         association_list = []
#         if row["SKU ID"] in association_lists:
#             association_list = association_lists[row["SKU ID"]]
#         SKU_map[index] = SKU(row["SKU ID"], (int(row["Weight Z Score"] + 0.5040787588602963), row["Velocity Z Score"], association_list, index)
#         i+=1
#     return SKU_map

def json_to_dict(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data
# def get_SKU_map():
#     df = pd.read_excel("./updated_vel_weight.xlsx")
#     association_lists = json_to_dict("./preprocess/top_association_map.json")
#     SKU_map = {0: None}
#     i = 1
#     for index, row in df.iterrows():
#         association_list = []
#         if row["SKU ID"] in association_lists:
#             association_list = association_lists[row["SKU ID"]]
#         SKU_map[i] = SKU(row["SKU ID"], row["Z_Weight_scaled"], row["Z_Vel_scaled"], association_list, i)
#         i+=1
#     return SKU_map

# SKU_map = get_SKU_map()


class SKU:
    def __init__(self, UID, weight, velocity, association_list, key):
        self.UID = UID
        self.weight = weight # in units
        self.velocity = velocity # frequency of pick in a given period 
        self.associationList = association_list # list of items it is associated with along with association values
        self.key = key
    
    def findSKU(self, graph):

        values_for_dict = []
        SKU_to_find = self.key
        
        for rack in graph.racksDict.values():
            rack_mesh = rack.rackLocations
            
            for depth_idx in range(len(rack_mesh)):
                for row_idx in range(len(rack_mesh[0])):
                    for col_idx in range(len(rack_mesh[0][0])):
                        if rack_mesh[depth_idx][row_idx][col_idx] == SKU_to_find:
                            to_append = (rack, (depth_idx, row_idx, col_idx))
                            values_for_dict.append(to_append)
                            
        return values_for_dict     
    
  
    def findAssocSKUlocs(self, graph): # find the locations of the associated skus in the graph. helper for 
        assocLocations = []
        # SKU_to_find_UID = self.UID
        key_for_SKU = get_key(self.UID)  
        items_assoc_with_sku = SKU_map[key_for_SKU].associationList
        assoc_key_arr = []
        for item in items_assoc_with_sku:
            assoc_key_arr.append(get_key(item))
        
        # [11,22,34] this needs to come from the top 3 assoc stored in sku objects
        # something like list(self.assocSKUs) which needs to give me 3 ints like [1,23,45]
        
        for rack in graph.racksDict.values():
            rack_mesh = rack.rackLocations
            
            for depth_idx in range(len(rack_mesh)):
                for row_idx in range(len(rack_mesh[0])):
                    for col_idx in range(len(rack_mesh[0][0])):
                        
                        for sku in assoc_key_arr:
                            if rack_mesh[depth_idx][row_idx][col_idx] == sku:
                                locations = (rack, (depth_idx, row_idx, col_idx), str(sku))
                                assocLocations.append(locations)
        return assocLocations
def get_SKU_map():
    df = pd.read_excel("./updated_vel_weight.xlsx")
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
# def json_to_dict(file_path):
#     with open(file_path) as json_file:
#         data = json.load(json_file)
#         return data

# def get_key(val):
#     for key, value in SKU_map.items():
#         if value and val == value.UID:
#             return key
#     return "key doesn't exist"  

    
# def get_SKU_map():
#     df = pd.read_excel("./velocity_weight.xlsx")
#     association_lists = json_to_dict("./preprocess/top_association_map.json")
#     SKU_map = {0: None}
#     i = 1
#     for index, row in df.iterrows():
#         association_list = []
#         if row["SKU ID"] in association_lists:
#             association_list = association_lists[row["SKU ID"]]
            
#         # weight_sku = int(row["Weight Z Score"]) + 0.5040787588602963
        
        
#         SKU_map[index] = SKU(row["SKU ID"], (row["Weight Z Score"]) + 0.5040787588602963, row["Velocity Z Score"], association_list, index)
#         i+=1
#     return SKU_map
##########
# SKU_map = get_SKU_map()
##########
def get_key(val):
    for key, value in SKU_map.items():
        if value and val == value.UID:
            return key
    return "key doesn't exist"  


item_assoc_w_one = SKU_map[54].associationList

# for assoc_item_uid in item_assoc_w_one:
#     print(get_key(assoc_item_uid))      
# use excel file for unique names and assocList
# SKU001 = SKU("001", 40, 60, [], key)
# SKU002 = SKU("002", 32, 87, [], "") 
# SKU003 = SKU("003", 22, 12, [], "")
# SKU004 = SKU("004", 76, 47, [], "")
# SKU005 = SKU("005", 76, 47, [], "")
# SKU006 = SKU("006", 76, 47, [], "")
# SKU007 = SKU("007", 40, 60, [], "")
# SKU008 = SKU("008", 32, 87, [], "")
# SKU009 = SKU("009", 22, 12, [], "")
# SKU010 = SKU("010", 76, 47, [], "")
# SKU011 = SKU("011", 76, 47, [], "")
# SKU012 = SKU("012", 76, 47, [], "")
# SKUMap = {
#     0 : None,
#     1 : SKU001,
#     2 : SKU002,
#     3 : SKU003,
#     4 : SKU004,
#     5 : SKU005,
#     6 : SKU006,
#     7 : SKU007,
#     8 : SKU008,
#     9 : SKU009,
#     10 : SKU010,
#     11 : SKU011,
#     12 : SKU012
# }
# print(rack1.rackLocations
# print(SKU003.findSKU(g))
# print(sku3_list)


# SKU_fitness
# how many things do you need to tak care of?
# weight and velocity (high priority)
# what already happens?
# first-in first-out (highest priority)
# things that expire faster than other items, need better, more accessible slots in the facility
# what are accessible slots?
# highly accessible slots are super close to outbound, inbound, low on the ground, they are in the
# portion of the facility that is close to outbound and inbound
# TODO: represent outbound and inbound locations so that you can get distances from racks to them
# about weight: heavy weight, medium weight, light weight
# about velocity: fast mover, medium mover, slow mover
# weight: a heavy item has high fitness on lower levels, a medium weight item has medium fitness everywhere, 
# a light weight item does not have worse fitness at higher levels, it is just less accessible

# def find_mean_stdev_dist_from_outbound(graph):
#     # BEEN RUN ONCE, NEVER RUN THIS AGAIN.
#     # needs all the racks in the graph
#     # difficulty: Medium
    
#     distances = []
    
#     for rack in graph.racksDict:
#         curr_rack = graph.get_rack(rack)
        
#         distance = 0         
                    
#         (path_start_outbound, distance) = dijkstra(graph, curr_rack, graph.get_rack('Outbound'))
                    
#         cost_to_pass_sum = 0
                    
#         # for rack in path_start_outbound:
#         #     if rack == path_start_outbound[0] or rack == path_start_outbound[len(path_start_outbound) - 1]:
#         #         continue 
#         #     cost_to_pass_sum += cost_to_pass_rack(graph, graph.get_rack(rack))
                        
#         distance += cost_to_pass_sum # this is how far that location is from outbound
                    
#         distances.append((distance)) # list of distances of all locations from outbound
                    
#     mean_dist = statistics.mean(distances)
#     std_dev_dist = statistics.stdev(distances)
    
#     return (mean_dist, std_dev_dist)


def dist_from_outbound_zscore(graph, curr_rack, predecessors):
    
    distance = 0
                    
    (path_start_outbound, distance) = dijkstra_trace_path(graph, graph.get_rack(curr_rack), graph.get_rack('Outbound'), predecessors)
    
                    
    # distance += int(dijkstra(graph, curr_rack, graph.get_rack('Outbound'))[1])
                    
    # start_orien = get_first_last_orientations(graph, path_start_outbound)[0]
    # cost_to_exit_start = cost_to_exit_enter_rack(curr_rack, location, start_orien)
                    
    # cost_to_pass = 0
                    
    # for rack in path_start_outbound:
    #     if rack == path_start_outbound[0] or rack == path_start_outbound[len(path_start_outbound) - 1]:
    #         continue 
    #     cost_to_pass += cost_to_pass_rack(graph, rack)
                        
    # distance += cost_to_exit_start + cost_to_pass
    
    location_zscore = (distance - MEAN_DISTANCE_FROM_OUTBOUND)/(STD_DEV_DISTANCE_OUTBOUND)
    
    return location_zscore
     
        
def get_velocity_score(sku, rack):
    key = get_key(sku)
    z_vel = SKU_map[key].velocity
    z_rack = rack.distToOB # rackScore stores the +ve values for distances to outbound

    if z_vel > VELOCITY_PERCENTILE_75:
        if z_rack > RACK_OB_PERCENTILE_75:
            velocity_score = 0
        if z_rack <= RACK_OB_PERCENTILE_75 and z_rack >= RACK_OB_PERCENTILE_25:
            velocity_score = abs(z_vel + (1/z_rack)) 
        if z_rack < RACK_OB_PERCENTILE_25:
            velocity_score = abs(z_vel + (3/z_rack)) # 0.7 + (2*(1/1.40), = 2.12
            
    if z_vel < VELOCITY_PERCENTILE_25: # slow mover
        if z_rack < RACK_OB_PERCENTILE_25:
            velocity_score = 0 # slow movers when stored close
        if z_rack <= RACK_OB_PERCENTILE_75 and z_rack >= RACK_OB_PERCENTILE_25:
            velocity_score = z_vel + abs(1 - (1/(abs(z_vel - z_rack)))) 
        if z_rack > RACK_OB_PERCENTILE_75:
            velocity_score = (3/abs(z_vel - z_rack) + 3*z_vel)
            # here slower item must have bigger fitness than slow item
    
    if z_vel >= VELOCITY_PERCENTILE_25 and z_vel <= VELOCITY_PERCENTILE_75:
        if z_rack >= RACK_OB_PERCENTILE_25 and z_rack <= RACK_OB_PERCENTILE_75:
            velocity_score = abs(z_vel + (3/z_rack))
        if z_rack < RACK_OB_PERCENTILE_25:
            velocity_score = abs(z_vel + 1*z_rack)
        if z_rack > RACK_OB_PERCENTILE_75:
            velocity_score = 2/(abs(z_vel + z_rack)) + z_vel
            
    return velocity_score
    
    
# (mean, std_dev) = find_mean_stdev_dist_from_outbound(graph) 

# TODO
# def get_location_zscore(rack, location):
#     # TODO: based on the distance of that location from outbound
    
#     start_rack = rack
#     # (depth_idx, row_idx, col_idx) = location
    
#     # goal_rack = outboundRack #TODO
    
#     # now based on these three things you can call the function you need to find accurate distances
#     distance = 0
#     (path_start_goal, edge_dist) = dijkstra(g, start_rack, goal_rack)
#     start_orientation = get_first_last_orientations(path_start_goal)[0]
    
#     distance += int(edge_dist)
#     cost_to_exit_start = cost_to_exit_enter_rack(start_rack, location, start_orientation)
#     cost_to_pass = 0
    
#     for rack in path_start_goal:
#         if rack == path_start_goal[0] or rack == path_start_goal[len(path_start_goal) - 1]:
#             continue
#         cost_to_pass += int(cost_to_pass_rack(rack))
#     distance += cost_to_pass + cost_to_exit_start
#     # this distance is from rackLoc to outbound rack
    
#     # mean = g.find_mean_dist_from_outbound() TODO
#     # std_dev = g.find_distance_std_dev() TODO
#     z_score = (distance - mean) / std_dev
    
#     return z_score
    
    

 
# TODO: given z-score of a velocity, categorize it using the thresholds you defined
# TODO: divide the annex into 3 zones based on the size of each catgeory you defined
# TODO: divide zones based on distance. If a location dist from outbound is above 

def get_weight_zscore(sku):
    sku_weight = sku.weight
    # you get this from the excel file CRISTO
    # difficulty: Easy
    pass


def get_weight_score(sku, row_idx, rack_mesh): 
     # TODO:: need to scale weight scores to all positive by adding the absolute of the most negative thing
    weight = SKU_map[get_key(sku)].weight # can either be positive or negative
    
    # new weight scores, everything is scaled to be positive
    if weight > WEIGHT_PERCENTILE_75:
        if row_idx == 0 or row_idx == 1:
            weight_score = 0
        else:
            weight_score = row_idx * weight
    
    if weight < WEIGHT_PERCENTILE_25:
        if row_idx == len(rack_mesh[0]) - 1 or row_idx == len(rack_mesh[0]) - 2:
            weight_score = 0
        else:
            weight_score = ((len(rack_mesh[0]) - 1) - row_idx) * weight
    
    if weight <= WEIGHT_PERCENTILE_75 and weight >= WEIGHT_PERCENTILE_25:
        if row_idx == 0 or row_idx == (len(rack_mesh[0]) - 1):
            weight_score = 0
        elif row_idx == 1 or row_idx == len(rack_mesh[0]) - 2:
            weight_score = 1 * weight
        else:
            weight_score = row_idx * weight
            
    return weight_score
            
def SKU_fitness(weight_score, velocity_score): 
    # need to come up with some way of adding the weight and velocity score
    # difficulty: Easy
    # just needs to assign a weight to weight_score and velocity_score
    # how do you do the division of weight?
    skufitness = weight_score + velocity_score
    return skufitness

# weight score will look like 
# 2.45 * 3
# velocity score will look like 
# 2.4 + 25 


    