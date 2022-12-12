from distanceFunction import *
from SKUClass import *
from classes import *
from fitness import dist_to_closest_same_sku_loc, dist_closest_same_helper

def fidelitone_slotting(graph, sku_to_putaway, dijkstra_dict): 
    
    fitness_values = {} # locs -> fitness values
    graph = graph
    
    for rack in graph.racksDict:
        
        if rack == "E2_0" or rack == "E2_4" or rack == "E3_2" or rack == "M1_4":
            continue
        
        curr_rack = graph.get_rack(rack)
        rack_mesh = curr_rack.rackLocations

        shortest_dist, predecessors = dijkstra_dict[rack]

        distance_to_closest_same_sku_loc, path_start_goal_1 = dist_to_closest_same_sku_loc(graph, curr_rack, (0, 0, 0), sku_to_putaway, predecessors, shortest_dist) # will be added to the total fitness of the location
        
        

        for depth_idx in range(len(rack_mesh)):
            for row_idx in range(len(rack_mesh[0])):
                weight_score_for_sku = get_weight_score(sku_to_putaway, row_idx, rack_mesh)
                for col_idx in range(len(rack_mesh[0][0])):
                
                    if rack_mesh[depth_idx][row_idx][col_idx] == 0: # you only wanna calculate fitness at free(0) locations
                        
                        location = (depth_idx, row_idx, col_idx)

                        cost_to_exit_start_1 = dist_closest_same_helper(graph, path_start_goal_1, curr_rack, location)
                        
                        fitness_at_loc_for_sku = weight_score_for_sku + cost_to_exit_start_1 + distance_to_closest_same_sku_loc
 
                        fitness_values[(curr_rack.UID, location)] = fitness_at_loc_for_sku
    max_value = max(fitness_values, key=fitness_values.get)
    print(max_value)
