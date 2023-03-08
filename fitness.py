from distanceFunction import *
from SKUClass import *
from classes import *
import random
from slotLocation_format import *
# @jit(nopython=True)

def exception_same_ass(start_location, goal_location):
    (d1, r1, c1) = start_location
    (d2, r2, c2) =  goal_location
    distance_within_rack = (abs(d1-d2) + abs(r1-r2) + abs(c1-c2))
    return distance_within_rack

def dist_to_closest_same_sku_loc(graph, rack_for_loc ,location, sku_to_putaway, predecessors, shortest_dist):
    
    start_rack = rack_for_loc
    start_loc = location
    locs_of_input_sku = SKU_map[get_key(sku_to_putaway)].findSKU(graph)
    distances = []
    
    # path_start_goal = None
    
    for goal_rack_loc in locs_of_input_sku:
        
        if goal_rack_loc[0].UID == 'M2_12' or goal_rack_loc[0].UID == 'N2_12': #TODO
            continue
        
        distance = 0
        
        path_start_goal = dijkstra_trace_path(graph, start_rack.UID, goal_rack_loc[0].UID, predecessors)
        # since start orientations will change depending on whehther we do l2r or r2l
        # for l2r 
        
        distance += shortest_dist[goal_rack_loc[0].UID]
        
        if start_rack == goal_rack_loc[0]:
            return (goal_rack_loc[1]), None # TODO change this and make it subtract the d-d, r-r, c-c
        
          
        (start_orien, goal_orien) = get_first_last_orientations(graph, path_start_goal)
        # cost_to_exit_start = cost_to_exit_enter_rack(start_rack, start_loc, start_orien)
        cost_to_enter_goal = cost_to_exit_enter_rack(goal_rack_loc[0], goal_rack_loc[1], goal_orien)
        
        cost_to_pass = 0
        
        for rack in path_start_goal:
            if rack == path_start_goal[0] or rack == path_start_goal[len(path_start_goal) - 1]:
                continue
            cost_to_pass += int(cost_to_pass_rack(graph, rack))
         
        distance += cost_to_enter_goal + cost_to_pass
        
        distances.append((distance))
    
    if len(distances) == 0:
        return 0, [] 
     
    return min(distances), start_orien # returns the distance to the closest same 

# @jit(nopython=True)
def dist_closest_same_helper(graph, path_start_goal, start_rack, start_loc):
    
    if len(path_start_goal) == 1 or len(path_start_goal) == 0:
        return 0
    
    (start_orien, goal_orien) = get_first_last_orientations(graph, path_start_goal)
    cost_to_exit_start = cost_to_exit_enter_rack(start_rack, start_loc, start_orien)
    
    return cost_to_exit_start


# TESTING dist_to_closest_same_sku_loc
# print(dist_to_closest_same_sku_loc(rack7, (0,3,0),  SKU003))
# path_start_goal = dijkstra(g, rack1, rack4)[0]
# # print(path_start_goal)
# print(get_first_last_orientations(path_start_goal))
# for rack_loc_idx in SKU003.findSKU(g):
#     goal_rack = rack_loc_idx[0]
#     print(goal_rack.UID)
#     path1 = dijkstra(g, rack4, goal_rack)[0]
#     print(path1)
#     get_first_last_orientations(path1)
#     break
        
# @jit(nopython=True)
def distance_to_most_assoc_sku_locs(graph, rack_for_loc ,location, sku_to_putaway, shortest_dist, predecessors):
    
    
    # what if you want to minimize the sum of distances to the top 3 most assoc items? yes
    distances = [] # dict that stores (key = assocSKu, value = dist)
    # you wanna iterate over this list and find unique keys with min dist
    
    start_rack = rack_for_loc
    start_loc = location
    
    locs_of_assoc_sku = SKU_map[get_key(sku_to_putaway)].findAssocSKUlocs(graph) 
    
    # path_start_goal = None
    
    for goal_rack_loc in locs_of_assoc_sku:
        if goal_rack_loc[0].UID == "M2_12" or goal_rack_loc[0].UID == "N2_12":
            continue
        
        # you need to have a function here that accepts different locations of the start rack
        # so the function will take those locations in fitness and keep changing the start_loc 
        
        distance = 0
        
        path_start_goal = dijkstra_trace_path(graph, start_rack.UID, goal_rack_loc[0].UID, predecessors)
        # makes different paths for each associated sku
        # need start orien for each path, not the path
        
        path_goal_distance = shortest_dist[goal_rack_loc[0].UID]
        
        distance += int(path_goal_distance)
        
        if goal_rack_loc[0].UID == start_rack.UID:
            return  goal_rack_loc[1], None # this would include another function that does the index subtractions because then you're just
        # in the same rack and all you need is the location - location dist
        
        (start_orien, goal_orien) = get_first_last_orientations(graph, path_start_goal)
        # cost_to_exit_start = cost_to_exit_enter_rack(start_rack, start_loc, start_orien)
        
        cost_to_enter_goal = cost_to_exit_enter_rack(goal_rack_loc[0], goal_rack_loc[1], goal_orien)
        
        
        cost_to_pass = 0
        
        for rack in path_start_goal:
            if rack == path_start_goal[0] or rack == path_start_goal[len(path_start_goal) - 1]:
                continue
            cost_to_pass += int(cost_to_pass_rack(graph, rack))
            
        distance += cost_to_enter_goal + cost_to_pass
        
        # print(cost_to_enter_goal, cost_to_exit_start, cost_to_pass)
        
        # print(cost_to_enter_goal, cost_to_pass, cost_to_exit_start)
        distances.append((goal_rack_loc[2], distance, start_orien))
        # [('12', 34, R2L), ('12', 11, L2R), ('32', 9, L2R)]
        
    distances_for_each_assoc_sku = []
    temp = set() 
    
    for tuple in distances:
        if tuple[0] not in temp:
            temp.add(tuple[0]) # has '12', '12', '32'
            
    for sku in temp:
        list_of_dist_for_sku = []
        sku_to_find = sku
        for tuple in distances:
            if sku_to_find in tuple:
                list_of_dist_for_sku.append(tuple[1])
                if list_of_dist_for_sku not in distances_for_each_assoc_sku:
                    distances_for_each_assoc_sku.append(list_of_dist_for_sku)
    
    distance_sum = 0
    
    
    
    dist_to_find = []
    for dist_tuple in distances_for_each_assoc_sku:
        distance_sum = min(dist_tuple)
        dist_to_find.append(distance_sum)
        
    preferred_paths_start_orien = []  
    for tuple in distances:
        for dist in dist_to_find:
            if dist in tuple:
                preferred_paths_start_orien.append(tuple[2])
    
    dist_to_return = sum(dist_to_find)
    
    if distance_sum == 0:
        return 0, preferred_paths_start_orien #todo write function for comparing within same rack
    
    return dist_to_return, preferred_paths_start_orien
            
# if i just returned the start orientations for every path, and in my triple loop inside 
# the fitness function, i add    
# @jit(nopython=True)   
def association_function_helper(graph, start_rack, start_loc, path_start_goal):
    # since the function is called for the same start location, 
    # this function needs to consider different start orientations for
    # different paths that can be made from start rack and goal racks
    # for every path made, this function will return the cost to exit start
    # based on which side is used to exit start node
    # if start orien is l2r, then this function will add cost to exit differently than for r2l
    
    if len(path_start_goal) == 1:
        return 0 # if the size of the path from start to goal is 1, meaning start = goal, there is no cost of 
    # exiting the start rack because youre just there, but there is a goal location and start location 
    # if sl = (0,0,0) and gl = (0,2,1), then we need to add (0-0)+(0-2)+(0-1.75) as the cost within the rack
    else:
        
        (start_orien, goal_orien) = get_first_last_orientations(graph, path_start_goal)
        cost_to_exit_start = cost_to_exit_enter_rack(start_rack, start_loc, start_orien)
    
    return cost_to_exit_start
            
# fitness helper, extra implementation for slotting rules

def check_depth_levels(rack_mesh, location):
        
    rack_to_check = rack_mesh
    (d, r, c) = location
    status_list = []
    sku_at_loc = rack_to_check[d][r][c]
        
    for depth_idx in range(len(rack_to_check)):
        if rack_to_check[depth_idx][r][c] == sku_at_loc or rack_to_check[depth_idx][r][c] == 0: #  same sku at a different depth level or no skus at depth levels
            status_list.append("True") # means true we can continue finding fitness
        else: 
            status_list.append("False")
                
    if status_list.count("False") > 0: # even 1 false in status list means there another item at a different depth level
        return False # dont try to find fitness
    else:
        return True # keep trying to find fitness     
                   
# @jit(nopython=True)     
       
def fittest_location(graph, sku_to_putaway, dijkstra_dict): 
    
    fitness_values = {} 
    graph = graph
    
    for rack in graph.racksDict:
        if rack == "E2_0" or rack == "E2_4" or rack == "E3_2" or rack == "M1_4" or rack == "M2_12" or rack == "N2_12" or rack == "Inbound" or rack == "Outbound" or rack[0] == 'X':
            continue
        curr_rack = graph.get_rack(rack)
        rack_mesh = curr_rack.rackLocations
        
        ##
        velocity_score_for_sku = get_velocity_score(sku_to_putaway, curr_rack)
        if velocity_score_for_sku == 0:
            continue
        ## 
        
        shortest_dist, predecessors = dijkstra_dict[rack]
        distance_to_closest_same_sku_loc_OR_goal_loc, start_orien_same = dist_to_closest_same_sku_loc(graph, curr_rack, (0, 0, 0), sku_to_putaway, predecessors, shortest_dist) 
        distance_to_closest_mostassoc_sku_loc_OR_goal_loc, start_oriens_ass = distance_to_most_assoc_sku_locs(graph, curr_rack, (0, 0, 0), sku_to_putaway, shortest_dist, predecessors)        
        
        for depth_idx in range(len(rack_mesh)):
            for row_idx in range(len(rack_mesh[0])):
                
                weight_score_for_sku = get_weight_score(sku_to_putaway, row_idx, rack_mesh)
                # if weight_score_for_sku == 0:
                #     continue
                
                for col_idx in range(len(rack_mesh[0][0])):
                
                    if rack_mesh[depth_idx][row_idx][col_idx] == 0: # free location in the mesh
                       
                        location = (depth_idx, row_idx, col_idx)
                        
                        if check_depth_levels(rack_mesh, location) == False:
                            continue
                        
                        distance_same = 0
                        #HANDLING EXCEPTIONS FOR DIST TO SAME FUNC
                        if isinstance(distance_to_closest_same_sku_loc_OR_goal_loc, (int, float)):
                            distance_same = distance_to_closest_same_sku_loc_OR_goal_loc + cost_to_exit_enter_rack(curr_rack, location, start_orien_same)
                            
                        else:
                            distance_within_rack = exception_same_ass(location, distance_to_closest_same_sku_loc_OR_goal_loc)
                            distance_same = distance_within_rack
                        
                        distance_ass = 0
                        cost_to_exit = 0
                        #HANDLING EXCEPTIONS FOR DIST TO ASS FUNC
                        if isinstance(distance_to_closest_mostassoc_sku_loc_OR_goal_loc, (int, float)):
                            for type in start_oriens_ass:
                                cost_to_exit += cost_to_exit_enter_rack(curr_rack, location, type)
                            distance_ass = distance_to_closest_mostassoc_sku_loc_OR_goal_loc + cost_to_exit
                        else:
                            distance_within_rack = exception_same_ass(location, distance_to_closest_mostassoc_sku_loc_OR_goal_loc)
                            distance_ass = distance_within_rack
                            
                            
                        # cost_to_exit_start_assoc = 0
                        
                        # i am getting different locations but the same path again
                        # and again. this needs to give me a different path everytime because that is what
                        # determines l2r or r2l logic 
                        
                        # cost_to_exit_start_same = dist_closest_same_helper(graph, path_start_goal_1, curr_rack, location)
                        # cost_to_exit_start_same = cost_to_exit_enter_rack(curr_rack, location, start_orien_same)
                        
                        # velocity_score_for_sku = get_velocity_score(sku_to_putaway, curr_rack)
                        
                        sku_fitness_at_loc = velocity_score_for_sku + weight_score_for_sku
                        
                        if distance_ass == 0: # items that have no associated items inside
                            distance_ass = -1
                        if distance_same == 0: # when same item does not exist in the facility
                            distance_same = -1
                            
                       # 
                        fitness_at_loc_for_sku = (1/(distance_ass) + 1) 
                        +  (1/(distance_same) + 1) 
                        + sku_fitness_at_loc 
                        
                        fitness_values[(curr_rack.UID, location, sku_to_putaway)] = fitness_at_loc_for_sku
    max_value = max(fitness_values, key=fitness_values.get) # this gives the key with max value
    # key will look like this ('A_1', (0,1,0), 'CSFG32DF')
    
    graph.get_rack(max_value[0]).assignSKU(max_value[1][0], max_value[1][1], max_value[1][2], get_key(sku_to_putaway))
    
    height_from_bottom = len(graph.get_rack(max_value[0]).rackLocations[0]) - max_value[1][1] 
    
    fid_row_bay = alg_to_fidel[max_value[0]] # this will give you something like (6, 19)
    fid_level = row_to_fidel[height_from_bottom]
    
    if max_value[0][0] == 'A' or max_value[0][0] == 'D' or max_value[0][0] == 'F' or max_value[0][0] == 'H' or max_value[0][0] == 'J' or max_value[0][0] == 'L' or max_value[0][0] == 'N' or max_value[0][0] == 'P' or max_value[0][0] == 'R' or max_value[0][0] == 'T' or max_value[0][0] == 'V':
        fid_spot = max_value[1][2] + 1
    else:
        fid_spot = len(graph.get_rack(max_value[0]).rackLocations[0][0]) - max_value[1][2]
    
    print('NW' + str(fid_row_bay[0]) + str(fid_row_bay[1]) + str(fid_level) + str(fid_spot))
    
    # print("Fittest location for " + str(sku_to_putaway) +" is: " + str(max_value[0]) + ", at " 
    #       + "depth level: " + str(max_value[1][0] + 1) 
    #       + ", height: " + str(height_from_bottom)
    #       + ", column: " + str(max_value[1][2] + 1))

##0 (max_ind - value +1) =height from bottom
##1 @
##2
##3
##4 
##5 
##6 @
## function for batch slotting for SKUs

def slot_sku_batch(graph, skus_to_slot, dijkstra_dict):
    counter = 0
    for sku in skus_to_slot:
        # counter += 1
        # if counter < 29:
        #     continue
        # if sku == 'EA50120' or sku == 'EA50220' or sku == 'EA50420' or sku == 'EA50320' or sku == 'EA51120' or sku == 'EA42112' or sku == 'EA42112' or sku == 'EA51220':
        #     continue
        
        curr_sku_to_putaway = sku
        if curr_sku_to_putaway == 'EA59103' or curr_sku_to_putaway == 'CS10529' or curr_sku_to_putaway == 'EA56503' or curr_sku_to_putaway == 'EA58103' or curr_sku_to_putaway == 'EA57603' or curr_sku_to_putaway == 'EA58503' or curr_sku_to_putaway == 'EA56603':
            continue 
        
        fittest_slots = []
        fittest_slots.append(fittest_location(graph, curr_sku_to_putaway, dijkstra_dict))
        
        
    print(fittest_slots)
