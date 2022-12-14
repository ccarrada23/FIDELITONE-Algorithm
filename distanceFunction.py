from importlib.resources import path
from multiprocessing.sharedctypes import Value
from re import L
from tkinter.ttk import Entry
from unittest.util import three_way_cmp
import copy
from classes import DEPTH_COEFF, HORIZONAL_COEFF, VERTICAL_COEFF, EntryOrientation, Graph, Rack
# from SKUClass import *
from location import RackLayout
import random
# from dijkstar import Graph, find_path
# from numba import jit


warehouse_racks = {}

# @jit(nopython=True)
def create_single_column(graph, n, name_prefix, depth, rows, cols, orderDownwards = True):
    for i in range(n):
        rack_name = name_prefix + str(i)
        rack = Rack(rack_name, RackLayout(depth, rows, cols).createMesh(), [])
        graph.add_rack(rack)
    
    if orderDownwards:
        i = 1
        while i < n:
            prev_rack_name = name_prefix + str(i - 1)
            prev_rack = graph.get_rack(prev_rack_name)
            
            curr_rack_name = name_prefix + str(i)
            curr_rack = graph.get_rack(curr_rack_name)
            
            graph.add_edge(prev_rack, curr_rack, 1)
            i += 1
    
        return graph
    else:
        i = n - 1
        while i > 0:
            prev_rack_name = name_prefix + str(i - 1)
            prev_rack = graph.get_rack(prev_rack_name)
            
            curr_rack_name = name_prefix + str(i)
            curr_rack = graph.get_rack(curr_rack_name)
            
            graph.add_edge(curr_rack, prev_rack, 1)
            
            i -= 1
            
        return graph

# @jit(nopython=True)
def create_double_column(graph, n, name_prefix1, name_prefix2, depth, rows, cols):
    # left hand side
    for i in range(n):
        rack_name1 = name_prefix1 + str(i)
        rack1 = Rack(rack_name1, RackLayout(depth, rows, cols).createMesh(), [])
        graph.add_rack(rack1)
        
        rack_name2 = name_prefix2 + str(i)
        rack2 = Rack(rack_name2, RackLayout(depth, rows, cols).createMesh(), [])
        graph.add_rack(rack2)
        
    i = 1
    while i < n:
        prev_rack_name = name_prefix2 + str(i - 1)
        prev_rack = graph.get_rack(prev_rack_name)
        
        curr_rack_name = name_prefix2 + str(i)
        curr_rack = graph.get_rack(curr_rack_name)
        
        graph.add_edge(prev_rack, curr_rack, 1)
        i += 1
    
    i = n - 1
    while i > 0:
        prev_rack_name = name_prefix1 + str(i - 1)
        prev_rack = graph.get_rack(prev_rack_name)
        
        curr_rack_name = name_prefix1 + str(i)
        curr_rack = graph.get_rack(curr_rack_name)
        
        graph.add_edge(curr_rack, prev_rack, 1)
        
        i -= 1
    
    return graph
    
# @jit(nopython=True)
def delete_racks(graph, UID):
    rack = graph.get_rack(UID)
    edges = rack.adjacent
    
    while len(edges) > 0:
        edge = edges[0]
        graph.delete_edge(edge.rack1, edge.rack2)
    
    graph.delete_node(rack)
   
# @jit(nopython=True)     
def reshape_rack(graph, UID, depth, height, width):
    rack = graph.get_rack(UID)
    rack.rackLocartions = RackLayout(depth, height, width).createMesh()
    
"""
        
# AISLE-1 CODE: A
# racks on one side of AISLE-1
rack1 = Rack('A1', RackLayout(1, 4, 3).createMesh(), [])  
rack2 = Rack('A2', RackLayout(1, 4, 3).createMesh(), []) 
rack3 = Rack('A3', RackLayout(1, 4, 3).createMesh(), [])
rack4 = Rack('A4', RackLayout(1, 4, 3).createMesh(), [])
rack5 = Rack('A5', RackLayout(1, 4, 3).createMesh(), [])
rack6 = Rack('A6', RackLayout(1, 4, 3).createMesh(), [])
rack7 = Rack('A7', RackLayout(1, 4, 3).createMesh(), [])
# racks on other side of AISLE-1, rack1 is connected to rack8. rack7 is connected to rack14
rack8 = Rack('A8', RackLayout(1, 4, 3).createMesh(), [])  
rack9 = Rack('A9', RackLayout(1, 4, 3).createMesh(), []) 
rack10 = Rack('A10', RackLayout(1, 4, 3).createMesh(), [])
rack11 = Rack('A11', RackLayout(1, 4, 3).createMesh(), [])
rack12 = Rack('A12', RackLayout(1, 4, 3).createMesh(), [])
rack13 = Rack('A13', RackLayout(1, 4, 3).createMesh(), [])
rack14 = Rack('A14', RackLayout(1, 4, 3).createMesh(), [])

# AISLE-2 CODE: B
# racks on one side of AISLE-2
rack15 = Rack('B15', RackLayout(1, 4, 3).createMesh(), [])
rack16 = Rack('B16', RackLayout(1, 4, 3).createMesh(), []) 
rack17 = Rack('B17', RackLayout(1, 4, 3).createMesh(), [])
rack18 = Rack('B18', RackLayout(1, 4, 3).createMesh(), [])
rack19 = Rack('B19', RackLayout(1, 4, 3).createMesh(), [])
rack20 = Rack('B20', RackLayout(1, 4, 3).createMesh(), [])
rack21 = Rack('B21', RackLayout(1, 4, 3).createMesh(), [])
# racks on other side of AISLE-2
rack22 = Rack('B22', RackLayout(1, 4, 3).createMesh(), [])
rack23 = Rack('B23', RackLayout(1, 4, 3).createMesh(), []) 
rack24 = Rack('B24', RackLayout(1, 4, 3).createMesh(), [])
rack25 = Rack('B25', RackLayout(1, 4, 3).createMesh(), [])
rack26 = Rack('B26', RackLayout(1, 4, 3).createMesh(), [])
rack27 = Rack('B27', RackLayout(1, 4, 3).createMesh(), [])
rack28 = Rack('B28', RackLayout(1, 4, 3).createMesh(), [])

outboundRack = Rack('OutBound', RackLayout(2,2,2).createMesh(), [])
# TODO: connect the appropriate racks in the annex with the outbound rakc
# TODO: outbound rack has the number of slots that equals the capacity of outbound
# TODO: outbound rack has no concept of type, so no need to call adjList() on outbound rack
# TODO: the weighted connections between outbound racks and annex_racks are >3

g = Graph()

# AISLE - 1 racks
g.add_rack(rack1)
g.add_rack(rack2)
g.add_rack(rack3)
g.add_rack(rack4)
g.add_rack(rack5)
g.add_rack(rack6)
g.add_rack(rack7)
g.add_rack(rack8)
g.add_rack(rack9)
g.add_rack(rack10)
g.add_rack(rack11)
g.add_rack(rack12)
g.add_rack(rack13)
g.add_rack(rack14)
# AISLE - 2 racks
g.add_rack(rack15)
g.add_rack(rack16)
g.add_rack(rack17)
g.add_rack(rack18)
g.add_rack(rack19)
g.add_rack(rack20)
g.add_rack(rack21)
g.add_rack(rack22)
g.add_rack(rack23)
g.add_rack(rack24)
g.add_rack(rack25)
g.add_rack(rack26)
g.add_rack(rack27)
g.add_rack(rack28)


# edges connecting two sides of the aisle
# g.add_edge(rack1, rack8, 2) # connecting two sides of the aisle from top
# g.add_edge(rack7, rack14, 2) # connecting two sides of the aisle from bottom

# all weight 1 and 2 circular edges in AISLE-1
g.add_edge(rack1, rack2, 1)
g.add_edge(rack2, rack3, 1)
g.add_edge(rack3, rack4, 1)
g.add_edge(rack4, rack5, 1)
g.add_edge(rack5, rack6, 1)
g.add_edge(rack6, rack7, 1)
g.add_edge(rack7, rack8, 2) # connecting opposite sites of the aisle at the end of row containg racks 1 to 7. 7 -> 8 
g.add_edge(rack8, rack9, 1)
g.add_edge(rack9, rack10, 1)
g.add_edge(rack10, rack11, 1)
g.add_edge(rack11, rack12, 1)
g.add_edge(rack12, rack13, 1)
g.add_edge(rack13, rack14, 1)
g.add_edge(rack14, rack1, 2) # connecting opposite sides on other end of the aisle
# AISLE - 2 edges 
g.add_edge(rack15, rack16, 1)
g.add_edge(rack16, rack17, 1)
g.add_edge(rack17, rack18, 1)
g.add_edge(rack18, rack19, 1)
g.add_edge(rack19, rack20, 1)
g.add_edge(rack20, rack21, 1)
g.add_edge(rack21, rack22, 2) # connecting opposite sites of the aisle at the end of row containg racks 1 to 7. 7 -> 8 
g.add_edge(rack22, rack23, 1)
g.add_edge(rack23, rack24, 1)
g.add_edge(rack24, rack25, 1)
g.add_edge(rack25, rack26, 1)
g.add_edge(rack26, rack27, 1)
g.add_edge(rack27, rack28, 1)
g.add_edge(rack28, rack15, 2) # connecting opposite sides on other end of the aisle
# AISLE - 1 and AISLE - 2 connections
g.add_edge(rack8, rack21, 3) # connects 1 and 2 from one end 
g.add_edge(rack15, rack14, 3) # connects 1 and 2 from the other end 
"""
# IMP: always assign the edges in a rack circularly covering a column and then changing col using the rack that is closest
# for racks that are not in the same aisle, 
# edge connecting two different aisles
# TODO: make outbound rack and connect it with random weights to the racks at the edges



# def adjList(rack):
#     # we have 1.5, 1, 2, 3, 2.5(E and B) weights. the weight for the edge that connects racks with
#     # outbound or inbound will be >3
    
#     rack_list = list() # needs to be a list of (child_node, weight, type) 
#     # where type is the type of the edge leaving that rack
#     num_outgoing_edges = 0
#     num_incoming_edges = 0
    
#     for edge in rack.adjacent:
#         if edge.rack1 == rack:
#             num_outgoing_edges += 1
#         else:
#             num_incoming_edges +=1
            
#     if num_outgoing_edges == 1:
#         if num_incoming_edges == 2 or num_incoming_edges == 3: # C1_0, C2_0, D1_0, D2_7 type rack
#             for edge in rack.adjacent:
#                 if edge.weight == 1:
#                     rack_list.append((edge.rack1, edge.weight, EntryOrientation.RIGHT2LEFT))
#                 if edge.weight == 3 or edge.weight == 1.5:
#                     rack_list.append((edge.rack1, edge.weight, EntryOrientation.LEFT2RIGHT))
#                 if edge.weight == 2 or edge.weight == 2.5:
#                     rack_list.append((edge.rack2, edge.weight, EntryOrientation.LEFT2RIGHT))
        
#     if num_incoming_edges == 1:
#         if num_outgoing_edges == 3 or num_outgoing_edges == 2: #C1_8, C2_7, D1_0, D2_0
#             for edge in rack.adjacent:
#                 if edge.weight == 1:
#                     rack_list.append((edge.rack2, edge.weight, EntryOrientation.LEFT2RIGHT))
#                 if edge.weight == 3 or edge.weight == 1.5:
#                     rack_list.append((edge.rack2, edge.weight, EntryOrientation.RIGHT2LEFT))
#                 if edge.weight == 2 or edge.weight == 2.5:
#                     rack_list.append((edge.rack1, edge.weight, EntryOrientation.RIGHT2LEFT))
    
#     if num_incoming_edges == 1 and num_outgoing_edges == 1: # middle rack
#         for edge in rack.adjacent:
#             if edge.rack1 == rack:
#                 rack_list.append((edge.rack2, edge.weight, EntryOrientation.LEFT2RIGHT))
#             else:
#                 rack_list.append((edge.rack1, edge.weight, EntryOrientation.RIGHT2LEFT))
                
    # for edge in rack.adjacent:
    #     # for outbound (4 connections required) and inbound (5 connections required), 
    #     # connect from outbound and inbound and say if edge.rack1 == inbound/outbound
    #     # if edge.rack1 == outbound:
    #     # rack_list.append((edge.rack2))
    #     continue
    
    

                      
        





















#############
# @jit(nopython=True)
def cost_to_exit_enter_rack(rack, location, type):
    location_mesh = rack.rackLocations 
    cost = 0
    (d_start,r_start,c_start) = location # the index in the location_mesh we start from 
    
    # possible_exit_idx_1 = location_mesh[0][-1][0] if we are moving out from bottom left
    d1_exit = 0
    r1_exit = len(location_mesh[0]) - 1
    c1_exit = 0
    
    # possible_exit_idx_2 = location_mesh[0][-1][-1] if we are moving out from bottom right
    d2_exit = 0
    r2_exit = len(location_mesh[0]) - 1
    c2_exit = len(location_mesh[0][0]) - 1
    
    if type == EntryOrientation.LEFT2RIGHT: # you want to exit from bottom left
        cost = (DEPTH_COEFF*(abs(d1_exit - d_start))) + (VERTICAL_COEFF*(abs(r1_exit - r_start))) + (HORIZONAL_COEFF*(abs(c1_exit - c_start)))
    else: # you want to exit the rack from bottom right
        cost = (DEPTH_COEFF*(abs(d2_exit - d_start))) + (VERTICAL_COEFF*(abs(r2_exit - r_start))) + (HORIZONAL_COEFF*(abs(c2_exit - c_start)))
    
    return cost
       
# @jit(nopython=True)
def cost_to_pass_rack(graph, rack):
    rack_mesh = graph.get_rack(rack).rackLocations
    no_of_col = len(rack_mesh[0][0])
    cost = HORIZONAL_COEFF*(no_of_col)
    return cost 

# Calculate dijkstra's on the whole graph
# returns {node->cost}, precesssor map
# @jit(nopython=True)
def dijkstra_helper(graph, start):
    shortest_distance = {} # records the cost to reach that node. Going to be updated as we move along the graph
    track_pred = {} # to keep track of path that has led us to that node, TODO: some logic about the type of edge leading into that node
    seenNodes = set() # to iterate thru the entire graph, racks 
    infinity = float('inf') # to assign initial distances from start node to +infinty
    
    start_to_use = start.UID
    
    for node in graph.racksDict: # racks in the graph
        shortest_distance[node] = infinity # setting the shortest distacne of all nodes from start as inf
    shortest_distance[start_to_use] = 0 # the shortest distance of start from start is 0
    
    while len(seenNodes) < len(graph.racksDict) - 1: # iterating over racks in the graph
        
        min_dist_node = None # initially there is no min_dist_node from start
        
        for node in graph.racksDict: # this loops just lets us go through the whole graph with a pointer
            if node in seenNodes:
                continue
            
            if min_dist_node is None:
                min_dist_node = node

            elif shortest_distance[node] < shortest_distance[min_dist_node]:
                min_dist_node = node
           
        # path_options = graph[min_dist_node].items() #path options for a rack, needs to have a child and weight that can be called 
        # path_options = min_dist_node.adjList()
        path_better = graph.get_dict_list(graph.get_rack(min_dist_node))[min_dist_node]
        
        # print(path_better)
        
        for (child_node, weight) in path_better:
            if child_node not in seenNodes and weight + shortest_distance[min_dist_node] < shortest_distance[child_node]:
                shortest_distance[child_node] = weight + shortest_distance[min_dist_node] 
                track_pred[child_node] = min_dist_node # because min dist node has led to the child
                
        seenNodes.add(min_dist_node)
        # print("Explored node: " + min_dist_node)
    
    return shortest_distance, track_pred

# @jit(nopython=True)
def dijkstra_trace_path(graph, start_to_use, goal_to_use, track_pred):
    track_path = []
    currentNode = goal_to_use
    # print(shortest_distance[goal])
    
    # not able to track path every time i write 'X_' as start or goal
    while currentNode != start_to_use:
        # print(currentNode.UID)
        try:
            track_path.append(currentNode)
            # print(currentNode.UID)
            currentNode = track_pred[currentNode]
            # print(currentNode.UID)
            
        except KeyError:
            print("path is not reachable")
            break   
    
    track_path.append(start_to_use)
    track_path.reverse()
    # print(arr)
    # if shortest_distance[goal] != infinity:
    #     print("Shortest distance is " + str(shortest_distance[goal]))
    #     print("Optimal path is " + str(list(i.UID for i in track_path)))
    return track_path
    
# def dijkstra(graph, start, goal):
#     shortest_distance = {} # records the cost to reach that node. Going to be updated as we move along the graph
#     track_pred = {} # to keep track of path that has led us to that node, TODO: some logic about the type of edge leading into that node
#     seenNodes = set() # to iterate thru the entire graph, racks 
#     infinity = float('inf') # to assign initial distances from start node to +infinty
#     track_path = [] # going to trace our journey back to source node
    
#     start_to_use = start.UID
#     goal_to_use = goal.UID
    
#     for node in graph.racksDict: # racks in the graph
#         shortest_distance[node] = infinity # setting the shortest distacne of all nodes from start as inf
#     shortest_distance[start_to_use] = 0 # the shortest distance of start from start is 0
    
#     while len(seenNodes) != len(graph.racksDict): # iterating over racks in the graph
        
#         min_dist_node = None # initially there is no min_dist_node from start
        
#         for node in graph.racksDict: # this loops just lets us go through the whole graph with a pointer
#             if node in seenNodes:
#                 continue
#             if min_dist_node is None:
#                 min_dist_node = node
#             elif shortest_distance[node] < shortest_distance[min_dist_node]:
#                 min_dist_node = node
           
#         # path_options = graph[min_dist_node].items() #path options for a rack, needs to have a child and weight that can be called 
#         # path_options = min_dist_node.adjList()
#         path_better = graph.get_dict_list(graph.get_rack(min_dist_node))[min_dist_node]
        
#         # print(path_better)
        
#         for (child_node, weight) in path_better:
#             if child_node not in seenNodes and weight + shortest_distance[min_dist_node] < shortest_distance[child_node]:
#                 shortest_distance[child_node] = weight + shortest_distance[min_dist_node] 
#                 track_pred[child_node] = min_dist_node # because min dist node has led to the child
                
#         seenNodes.add(min_dist_node)
        
#     currentNode = goal_to_use
#     # print(shortest_distance[goal])
    
#     # not able to track path every time i write 'X_' as start or goal
#     while currentNode != start_to_use:
#         # print(currentNode.UID)
#         try:
#             track_path.insert(0, currentNode)
#             # print(currentNode.UID)
#             currentNode = track_pred[currentNode]
#             # print(currentNode.UID)
            
#         except KeyError:
#             print("path is not reachable")
#             break   
    
#     track_path.insert(0, start_to_use) 
#     # print(arr)
#     # if shortest_distance[goal] != infinity:
#     #     print("Shortest distance is " + str(shortest_distance[goal]))
#     #     print("Optimal path is " + str(list(i.UID for i in track_path)))
#     return track_path, shortest_distance[goal.UID]
      
# racks = dijkstra(g, rack6, rack26)
# for rack in racks:
#     print(rack.UID)
# def shortest_dist_path(graph, start, goal):
#     return find_path(graph, start, goal)

# def dist_inb_helper_fitness(num):
#     
#     return num

# def dist_inb_helper_fidel(num):
#     
#     return num

# def 
#     return num

# def dist_subsequent_picks_fitness_helper(num):
#     
#     return num

# def dist_subsequent_picks_fidel_helper(num):
#     
#     return num
    

# @jit(nopython=True)
def get_first_last_orientations(graph, path): # the optimal path
    # TODO: Remove
    # if len(path) == 1:
    #     return 
    
    assert len(path) >= 2
    
    start_node = path[0] # the start node of the dijk
    
    next_node = graph.get_rack(path[1]) # the second node visited that is next to the start 
    adj_start = graph.get_rack(start_node).adjList() # gives us tuples of [(neigbor, weight, type)]
    
    exit_orientation = None
    for neighbor, weight, type in adj_start: # has to be the correct type 
        if neighbor is next_node:
            exit_orientation = type
            break
    
    path_len = len(path)
    dest_node = path[path_len - 1]
    prev_node = graph.get_rack(path[path_len - 2])
    
    adj_dest = graph.get_rack(dest_node).adjList()
    
    entry_orientation = None
    
    for neighbor, weight, type in adj_dest:
        if neighbor is prev_node:
            entry_orientation = type
            break
    # assert entry_orientation is not None
    # print("edge to leave start rack: " + str(exit_orientation) + " " + "edge to enter goal rack: " + str(entry_orientation))
    return exit_orientation, entry_orientation


# def find_dist_to_inb_fitness(sku):
#     to_return = dist_inb_helper_fitness(sku) #since there are large number of items being slotted close tp OB
#     return to_return

# def find_dist_to_inb_fidel(sku):
#     to_return = dist_inb_helper_fidel(sku)
#     return to_return

# def find_pick_dist_ob(sku):
#     to_return = dist_outb_pick_helper(sku)
#     return to_return

# def find_dist_subsequent_picks_fitness(sku):
#     to_return = dist_subsequent_picks_fitness_helper(sku)
#     return to_return

# def find_dist_subsequent_picks_fidel(sku):
#     to_return = dist_subsequent_picks_fidel_helper(sku)
#     return to_return
