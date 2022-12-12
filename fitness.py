from distanceFunction import *
from SKUClass import *
from classes import *

# @jit(nopython=True)
def dist_to_closest_same_sku_loc(graph, rack_for_loc ,location, sku_to_putaway, predecessors, shortest_dist):
    
    
    start_rack = rack_for_loc
    start_loc = location
    locs_of_input_sku = sku_to_putaway.findSKU(graph)
    distances = []
    
    path_start_goal = None
    # for every value in locs_for_input_sku, we will need to run the dijktra with racks
    # in locs_for_input_sku as goal_node and rack_being_checked as start node
    # after that, we need to get orientations for start and goal
    # after getting orientations, will need to calculate cost-to-exit and cost-to-enter for
    # start_node and goal_node respectively
    # we will do these 3 things for every dist we find and add it to the distance array
    for goal_rack_loc in locs_of_input_sku:
        
        # if start_rack == goal_rack_loc[0]:
        #     return 0, path_start_goal
        
        distance = 0
        
        path_to_start = dijkstra_trace_path(graph, start_rack.UID, goal_rack_loc[0].UID, predecessors)
        path_start_goal = path_to_start
        
        distance += shortest_dist[goal_rack_loc[0].UID]
        
        if start_rack == goal_rack_loc[0]:
            return 0, path_start_goal
        
        # path_start_goal = dijkstra(graph, start_rack, goal_rack_loc[0])[0]
        
        # distance += int(dijkstra(graph, start_rack, goal_rack_loc[0])[1]) # update dist
          
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
     
    return min(distances), path_start_goal # returns the distance to the closest same 

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
    
    locs_of_assoc_sku = sku_to_putaway.findAssocSKUlocs(graph) # this will give you several locations assoc sku
    # this looks like this [(rack1, (d,r,c), '12'), (rack4, (d,r,c), '12'), (rack11, (d,r,c), '34')]
    
    path_start_goal = None
    
    for goal_rack_loc in locs_of_assoc_sku:
        
        # you need to have a function here that accepts different locations of the start rack
        # so the function will take those locations in fitness and keep changing the start_loc 
        
        distance = 0
        
        path_start_goal = dijkstra_trace_path(graph, start_rack.UID, goal_rack_loc[0].UID, predecessors)
        # path_start_goal = path_to_start[0]
        path_goal_distance = shortest_dist[goal_rack_loc[0].UID]
        
        distance += int(path_goal_distance)
        
        # path_start_goal = dijkstra(graph, start_rack, goal_rack_loc[0])[0]
        
        # distance += int(dijkstra(graph, start_rack, goal_rack_loc[0])[1]) # just edge distance
        
        # print(distance)
        
        if goal_rack_loc[0].UID == start_rack.UID:
            return 0, path_start_goal
        
        (start_orien, goal_orien) = get_first_last_orientations(graph, path_start_goal)
        # cost_to_exit_start = cost_to_exit_enter_rack(start_rack, start_loc, start_orien)
        
        cost_to_enter_goal = cost_to_exit_enter_rack(goal_rack_loc[0], goal_rack_loc[1], goal_orien)
        
        # print(start_orien, goal_orien)
        
        cost_to_pass = 0
        
        for rack in path_start_goal:
            if rack == path_start_goal[0] or rack == path_start_goal[len(path_start_goal) - 1]:
                continue
            cost_to_pass += int(cost_to_pass_rack(graph, rack))
            
        distance += cost_to_enter_goal + cost_to_pass
        
        # print(cost_to_enter_goal, cost_to_exit_start, cost_to_pass)
        
        # print(cost_to_enter_goal, cost_to_pass, cost_to_exit_start)
        distances.append((goal_rack_loc[2], distance))
        # [('12', 34), ('3', 11), ('32', 9)]
        # print(distances)
    distances_for_each_assoc_sku = []
    temp = set()
    
    for tuple in distances:
        if tuple[0] not in temp:
            temp.add(tuple[0])
            
    for sku in temp:
        list_of_dist_for_sku = []
        sku_to_find = sku
        for tuple in distances:
            if sku_to_find in tuple:
                list_of_dist_for_sku.append(tuple[1])
                if list_of_dist_for_sku not in distances_for_each_assoc_sku:
                    distances_for_each_assoc_sku.append(list_of_dist_for_sku)
    
    distance_sum = 0
    
    for dist_tuple in distances_for_each_assoc_sku:
        distance_sum += min(dist_tuple)
    
    if distance_sum == 0:
        return 0, path_start_goal
    
    return distance_sum, path_start_goal
            
            
# @jit(nopython=True)   
def association_function_helper(graph, start_rack, start_loc, path_start_goal):
    
    if len(path_start_goal) == 1:
        return 0
    else:
        
        (start_orien, goal_orien) = get_first_last_orientations(graph, path_start_goal)
        cost_to_exit_start = cost_to_exit_enter_rack(start_rack, start_loc, start_orien)
    
    return cost_to_exit_start
            
            
                   
# @jit(nopython=True)            
def fittest_location(graph, sku_to_putaway, dijkstra_dict): 
    
    fitness_values = {} # locs -> fitness values
    graph = graph
    
    for rack in graph.racksDict:
        
        if rack == "E2_0" or rack == "E2_4" or rack == "E3_2" or rack == "M1_4":
            continue
        # print("Checking fitness at Rack: " + rack)
        curr_rack = graph.get_rack(rack)
        rack_mesh = curr_rack.rackLocations
        
        shortest_dist, predecessors = dijkstra_dict[rack]
        # dijkstra_helper(graph, curr_rack)
        # velocity_score_for_sku = get_velocity_score(graph, sku_to_putaway, rack, shortest_dist['Outbound'])
        
        
        # distance-to-closest-same-sku-location
        distance_to_closest_same_sku_loc, path_start_goal_1 = dist_to_closest_same_sku_loc(graph, curr_rack, (0, 0, 0), sku_to_putaway, predecessors, shortest_dist) # will be added to the total fitness of the location
        
        
        test = distance_to_most_assoc_sku_locs(graph, curr_rack, (0, 0, 0), sku_to_putaway, shortest_dist, predecessors)
        distance_to_closest_mostassoc_sku_loc, path_start_goal_2 = test
        
        
        for depth_idx in range(len(rack_mesh)):
            
            for row_idx in range(len(rack_mesh[0])):
                
                weight_score_for_sku = get_weight_score(sku_to_putaway, row_idx, rack_mesh)
                if weight_score_for_sku == 0:
                    continue
                
                for col_idx in range(len(rack_mesh[0][0])):
                
                    if rack_mesh[depth_idx][row_idx][col_idx] == 0: # you only wanna calculate fitness at free(0) locations
                        
                        location = (depth_idx, row_idx, col_idx)
                        
                        cost_to_exit_start_2 = association_function_helper(graph, curr_rack, location, path_start_goal_2)
                        cost_to_exit_start_1 = dist_closest_same_helper(graph, path_start_goal_1, curr_rack, location)
                        
                        # sku-fitness-at-a-location
                        # weight_score_for_sku = get_weight_score(sku_to_putaway, row_idx, rack_mesh)
                        
                        velocity_score_for_sku = get_velocity_score(sku_to_putaway, curr_rack)
                        
                        fitness_at_loc_for_sku = weight_score_for_sku + velocity_score_for_sku + cost_to_exit_start_2 + cost_to_exit_start_1
                        
                        # TODO: update distance_to_closest_same_sku_loc & distance_to_closest_mostassoc_sku_loc to account for location inside rack
                        
                        # distance-to-most-associated-sku-location
                        sku_fitness_at_loc = 0
                        # fitness, TODO: needs weights on each additive component
                        
                        fitness_at_loc_for_sku = sku_fitness_at_loc +  (1/(distance_to_closest_mostassoc_sku_loc + 1)) +  (1/(distance_to_closest_same_sku_loc+1))
                        # if distance_to_closest_same_sku_loc == 0 and distance_to_closest_mostassoc_sku_loc == 0:
                        #     fitness_at_loc_for_sku = sku_fitness_at_loc + (1) + (1)
                        # elif distance_to_closest_same_sku_loc == 0:
                        #     fitness_at_loc_for_sku = sku_fitness_at_loc + (1) + (1/distance_to_closest_mostassoc_sku_loc)
                        # elif distance_to_closest_mostassoc_sku_loc == 0:
                        #     fitness_at_loc_for_sku = sku_fitness_at_loc + (1/distance_to_closest_same_sku_loc) + (1)
                        # else:
                        #     fitness_at_loc_for_sku = sku_fitness_at_loc + (1/distance_to_closest_same_sku_loc) + (1/distance_to_closest_mostassoc_sku_loc)
                            
                        fitness_values[(curr_rack.UID, location)] = fitness_at_loc_for_sku
    max_value = max(fitness_values, key=fitness_values.get)
    print(max_value)
    # print(fitness_values)
            
           
# def fittest_location(graph, sku_to_putaway): 
    
#     fitness_values = {} # locs -> fitness values
#     graph = graph
    
#     for rack in graph.racksDict:
        
#         curr_rack = graph.get_rack(rack)
#         rack_mesh = curr_rack.rackLocations
        
#         for depth_idx in range(len(rack_mesh)):
#             for row_idx in range(len(rack_mesh[0])):
#                 for col_idx in range(len(rack_mesh[0][0])):
                
#                     if rack_mesh[depth_idx][row_idx][col_idx] == 0: # you only wanna calculate fitness at free(0) locations
                        
#                         location = (depth_idx, row_idx, col_idx)
                        
#                         # sku-fitness-at-a-location
#                         # TODO:: change get_velocoty score to use new dijkstra helper
#                         velocity_score_for_sku = get_velocity_score(graph, sku_to_putaway, rack)
#                         weight_score_for_sku = get_weight_score(sku_to_putaway, row_idx, rack_mesh)
#                         sku_fitness_at_loc = SKU_fitness(weight_score_for_sku, velocity_score_for_sku) # will be added to the total fitness of the location
                        
#                         # distance-to-closest-same-sku-location
#                         distance_to_closest_same_sku_loc = dist_to_closest_same_sku_loc(graph, curr_rack, location, sku_to_putaway) # will be added to the total fitness of the location
                        
#                         # distance-to-most-associated-sku-location
#                         distance_to_closest_mostassoc_sku_loc = distance_to_most_assoc_sku_locs(graph, curr_rack, location, sku_to_putaway)
                        
#                         # fitness, TODO: needs weights on each additive component
#                         if distance_to_closest_same_sku_loc == 0:
#                             fitness_at_loc_for_sku = sku_fitness_at_loc + (distance_to_closest_same_sku_loc) + (1/distance_to_closest_mostassoc_sku_loc)
                            
#                         elif distance_to_closest_mostassoc_sku_loc == 0:
#                             fitness_at_loc_for_sku = sku_fitness_at_loc + (1/distance_to_closest_same_sku_loc) + (distance_to_closest_mostassoc_sku_loc)
                            
#                         elif distance_to_closest_same_sku_loc == 0 and distance_to_closest_mostassoc_sku_loc == 0:
#                             fitness_at_loc_for_sku = sku_fitness_at_loc + (distance_to_closest_same_sku_loc) + (distance_to_closest_mostassoc_sku_loc)
                        
#                         else:
#                             fitness_at_loc_for_sku = sku_fitness_at_loc + (1/distance_to_closest_same_sku_loc) + (1/distance_to_closest_mostassoc_sku_loc)
                            
#                         fitness_values[(curr_rack.UID, location)] = fitness_at_loc_for_sku
#     max_value = max(fitness_values, key=fitness_values.get)
#     print(max_value)
                        
                        
              