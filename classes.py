# from ast import Assign
from decimal import ROUND_HALF_DOWN
from enum import Enum
# from ntpath import join
# from plistlib import UID
# from selectors import EpollSelector
from tkinter import Entry
import copy
import numpy as np
from pyparsing import col
# from numba.experimental import jitclass

from location import RackLayout

HORIZONAL_COEFF = 1 # needs to change
VERTICAL_COEFF = 1.75 # needs to change
DEPTH_COEFF = 1.3 # needs to change 

MEAN_DISTANCE_FROM_OUTBOUND = 27.90888888888889
STD_DEV_DISTANCE_OUTBOUND = 12.090302805358766

class EntryOrientation(Enum):
    LEFT2RIGHT = 0
    RIGHT2LEFT = 1

WEIGHT_PERCENTILE_75 = 0.50408
WEIGHT_PERCENTILE_25 = 0.019230355

VELOCITY_PERCENTILE_75 = 0.6227554024456383
VELOCITY_PERCENTILE_25 = 0.017114666268653878

RACK_OB_PERCENTILE_75 = 3.018948374380017
RACK_OB_PERCENTILE_25 = 1.5404907800774748
        
# say A2 is 4*3; 4 rows and 3 columns
# if you arrive at A2 from the left edge {1}, you are at the bottom row and first col => at [3][0]
# in general, arrival from LEFT at any rack with layout (i,j) => you arrive at index [i-1][0]

# edge_spec = [
#     ('type', )
# ]

# @jitclass
class Edge:
    def __init__(self, rack1, rack2, type, weight = -1):
        self.rack1 = rack1
        self.rack2 = rack2
        self.type = type # either LEFT2RIGHT or RIGHT2LEFT
        self.weight = weight
        
        
    def changeEdge(self, frm, to, type):
        edge = Edge(None, None, None, None)
        edge = self
        edge.type = type
        edge.rack1 = frm
        edge.rack2 = to
        
    # def get_edge_details(self):
    #     racklayout1 = self.rack1.rackLocations
    #     racklayout2 = self.rack2.rackLocations
        
    #     indexDepart = None
    #     indexArrive = None
        
    #     if self.type == EntryOrientation.RIGHT2LEFT: # exited using Right side of rack1, entered using Left side of rack2
    #         dep_idx_dpt = 0
    #         row_idx_dpt = len(racklayout1[0]) - 1 # len(rackLayout) gives number of depths,
    #         col_idx_dpt = len(racklayout1[0][0]) - 1
            
    #         indexDepart = (dep_idx_dpt, row_idx_dpt, col_idx_dpt)
            
    #         dep_idx_arr = 0            
    #         row_idx_arr = len(racklayout2[0]) - 1
    #         col_idx_arr = 0
    #         indexArrive = (dep_idx_arr, row_idx_arr, col_idx_arr)
            
    #         print("index used to leave rack1: " + str(indexDepart))
    #         print("index used to enter rack2: " + str(indexArrive))
            # logic is to 
            
        # else: # EntryOrientation.LEFT2RIGHT
        #     dep_idx_arr = 0
        #     row_idx_arr = len(racklayout1[0]) - 1 
        #     col_idx_arr = len(racklayout1[0][0]) - 1
        #     indexArrive = (row_idx_arr, col_idx_arr)
                        
        #     dep_idx_dpt = 0
        #     col_idx_dpt = 0
        #     row_idx_dpt = len(racklayout2[0]) - 1
        #     indexDepart = (dep_idx_dpt, row_idx_dpt, col_idx_dpt) 
                           
        #     print("index used to leave rack2: " + str(indexDepart))
        #     print("index used to enter rack1: " + str(indexArrive))
            
# @jitclass                  
class Rack:
    def __init__(self, 
                 UID,
                 rackLocations,
                 adjacent = list(), distToOB=-1, distToIB=-1): #a list of adjacent edges
        self.UID = UID
        self.rackLocations = rackLocations # given as RackLayout(i,j).createMatrix()
        self.adjacent = adjacent # this iterable list
        self.distToOB = distToOB
        self.distToIB = distToIB
    # def __str__(self):
    #     return str(self.UID) + ' has edges: ' + str([x.rack1.UID + " -> " + x.rack2.UID for x in self.adjacent])
    
    def add_connecting_edge(self, edge):
        self.adjacent.append(edge)
    
    def get_object(self):
        rack = self
        return rack
    
    def get_connections(self):  
        edges = []
        for edge in self.adjacent:
            edges.append(edge)
        return edges
           
    def get_id(self):
        return self.UID
    
    def assignSKU(self, depthInd,rowInd, colInd, SKUkey): # we fill deeper levels first while assigning SKUs
        mesh = self.rackLocations
        mesh[depthInd][rowInd][colInd] = SKUkey
        
        # assert self.assignLogic() == True
        
    
    def assignLogic(self):
        mesh = self.rackLocations
        depth_to_check = len(mesh) - 1 # index number of depth to check for all keys at every [row][col]
        for dep_idx in range(len(mesh) - 1):
            for row_idx in range(len(mesh[0])):
                for col_idx in range(len(mesh[0][0])):
                    if mesh[dep_idx][row_idx][col_idx] != 0 and mesh[dep_idx][row_idx][col_idx] != mesh[depth_to_check][row_idx][col_idx]:
                        return False
        return True
        
                     
    def get_rack_details(self):
        for edge in self.adjacent:
            print(str(self.UID) + " has an edge of type: " + str(edge.type) + ", and weight: " + str(edge.weight))
        
    def countSKU(self, sku): # going to call this function like countSKU(1, rack1)
        sku_key = sku
        # sku_obj = SKUMap[sku_key]
        sku_count = 0
        for depth in range(len(self.rackLocations)):
            for row in range(len(self.rackLocations[0])):
                for col in range(len(self.rackLocations[0][0])):
                    if self.rackLocations[depth][row][col] == sku_key:
                        sku_count = sku_count + 1
        return sku_count

    def __getitem__(self, key):
        return self.__dict__[key]
    
    def adjList(self):
        # we have 1.5, 1, 2, 3, 2.5(E and B) weights. the weight for the edge that connects racks with
    # outbound or inbound will be >3
    
        rack_list = list() # needs to be a list of (child_node, weight, type) 
        # where type is the type of the edge leaving that rack
        num_outgoing_edges = 0
        num_incoming_edges = 0
        
        # just need this to give child node and weight for outbound and inbound
        
        for edge in self.adjacent:
        
            if edge.rack1 == self:
                num_outgoing_edges += 1
            if edge.rack1 != self:
                num_incoming_edges +=1
                
        
        if num_incoming_edges == 4 and num_outgoing_edges == 4:
            # means its an inbound or outbound rack
            for edge in self.adjacent:
                if edge.rack1 == self: # if outgoing edge from inbound or outbound
                    rack_list.append((edge.rack2, edge.weight, "no type"))
                     
            
            
        if num_outgoing_edges == 1:
            if num_incoming_edges == 2 or num_incoming_edges == 3 or num_incoming_edges == 4: # C1_0, C2_0, D1_0, D2_7 type rack
                for edge in self.adjacent:
                    if edge.weight == 1:
                        rack_list.append((edge.rack1, edge.weight, EntryOrientation.RIGHT2LEFT))
                    if edge.weight == 3 or edge.weight == 1.5:
                        rack_list.append((edge.rack1, edge.weight, EntryOrientation.LEFT2RIGHT))
                    if edge.weight == 2 or edge.weight == 2.5:
                        rack_list.append((edge.rack2, edge.weight, EntryOrientation.LEFT2RIGHT))
                    if edge.weight > 4.5:
                        rack_list.append((edge.rack1, edge.weight, EntryOrientation.LEFT2RIGHT))
                        
                        
        if num_incoming_edges == 1:
            if num_outgoing_edges == 3 or num_outgoing_edges == 2 or num_outgoing_edges == 4: #C1_8, C2_7, D1_0, D2_0
                for edge in self.adjacent:
                    if edge.weight == 1:
                        rack_list.append((edge.rack2, edge.weight, EntryOrientation.LEFT2RIGHT))
                    if edge.weight == 3 or edge.weight == 1.5:
                        rack_list.append((edge.rack2, edge.weight, EntryOrientation.RIGHT2LEFT))
                    if edge.weight == 2 or edge.weight == 2.5:
                        rack_list.append((edge.rack1, edge.weight, EntryOrientation.RIGHT2LEFT))
                    if edge.weight > 4.5:
                        rack_list.append((edge.rack2, edge.weight, EntryOrientation.RIGHT2LEFT))
                        
                        
        if num_incoming_edges == 1 and num_outgoing_edges == 1: # middle rack
            for edge in self.adjacent:
                if edge.rack1 == self:
                    rack_list.append((edge.rack2, edge.weight, EntryOrientation.LEFT2RIGHT))
                else:
                    rack_list.append((edge.rack1, edge.weight, EntryOrientation.RIGHT2LEFT))
                    
        return rack_list
    
    # def adjList(self):

    #     rack_list = list() # should contain [['!=rack, weight], [!=rack, weight],  ] n(subarrays) = n(edges) for that rack
    #     rack_num_edges = len(self.adjacent) # can be either 2 or bigger than 2 
        
    #     if rack_num_edges == 2: # it is a middle rack
            
    #         for edge in self.adjacent:
    #             if edge.rack1 != self:
    #                 rack_list.append((edge.rack1, edge.weight, EntryOrientation.LEFT2RIGHT))
    #             else:
    #                 rack_list.append((edge.rack2, edge.weight, edge.type))
        
    #     if rack_num_edges >= 3:
    #         frm_edges = []
    #         # if you have 3 edges, you can belong to one of two categories depending on number of from and to edges you have 
    #         for edge in self.adjacent:
    #             if edge.rack1 ==  self:
    #                 frm_edges.append(0)
                    
    #         if len(frm_edges) == 2:
    #             for edge in self.adjacent:
    #                 if edge.weight == 2:
    #                     rack_list.append((edge.rack1, edge.weight, EntryOrientation.LEFT2RIGHT))
    #                 if edge.weight == 3:
    #                     rack_list.append((edge.rack2, edge.weight, EntryOrientation.LEFT2RIGHT))
    #                 if edge.weight == 1:
    #                     rack_list.append((edge.rack2, edge.weight, EntryOrientation.RIGHT2LEFT))
            
    #         else:
    #             for edge in self.adjacent:
    #                 if edge.weight == 1:
    #                     rack_list.append((edge.rack1, edge.weight, EntryOrientation.LEFT2RIGHT))
    #                 if edge.weight == 2:
    #                     rack_list.append((edge.rack2, edge.weight, EntryOrientation.RIGHT2LEFT))
    #                 if edge.weight == 3:
    #                     rack_list.append((edge.rack1, edge.weight, EntryOrientation.RIGHT2LEFT))
    #     return rack_list          
                             
# class SKU:
#     def __init__(self, UID, weight, velocity, associationList):
#         self.UID = UID
#         self.weight = weight # in units
#         self.velocity = velocity # frequency of pick in a given period 
#         self.associationList = associationList # list of items it is associated with along with association values

#     def findSKU(self, graph):
#         rack_SKUloc_dict = {}
#         SKU_to_find = self.getKey()
#         for rack in graph.racksDict:
#             rack_with_sku = rack.rackLocations
#             for depth_idx in range(len(rack_with_sku)):
#                 for row_idx in range(len(rack_with_sku[0])):
#                     for col_idx in range(len(rack_with_sku[0][0])):
#                         if rack_with_sku[depth_idx][row_idx][col_idx] == SKU_to_find:
#                             rack_SKUloc_dict[rack.UID] = (depth_idx, row_idx, col_idx)
#         print(rack_SKUloc_dict)       
                        
#     def getKey(self):
#         for key in SKUMap:
#             if SKUMap[key] == self:
#                 return key     
  
# @jitclass
class Graph:
    def __init__(self):
        self.racksDict = {}
        
        self.racks_uid_dict = {} # to make graph subscriptable
        
        self.num_racks = 0
        
    def __iter__(self):
        return iter(self.racksDict.values())
    
    def print_racks(self):
        for rack in self.racksDict.values():
            print(rack.UID)
            for edge in rack.adjacent:
                print(edge.rack1.UID + " -> " + edge.rack2.UID)
            
    
    def add_rack(self, rack_toAdd): # adds racka nd return added rack
        self.num_racks += 1
        rack_name = rack_toAdd.UID
        self.racksDict[rack_name] = rack_toAdd #!!!!!!!
        
        self.racks_uid_dict[rack_name] = rack_toAdd.UID
        
        return rack_toAdd
    
    def get_rack(self, rack_name):
        return self.racksDict[rack_name]

    def get_vertex(self, rack): # return rack object if rack is part of racksDict: the dict that stores the graph, g
        if rack in self.racksDict:
            return self.racksDict[rack]
        else:
            return None
        
    def add_edge(self, frm, to, cost = 0):        
        e1 = Edge(frm, to, EntryOrientation.LEFT2RIGHT, cost)
        # e2 = Edge(frm, to, EntryOrientation.RIGHT2LEFT, cost)
        frm.add_connecting_edge(e1) # added a connecting edge to from object with weight e1
        # TODO: add connecting edge to the dict of uids
        to.add_connecting_edge(e1)
        
        # add_2_from = (to.UID, e1.weight)
        # add_2_to = (frm.UID, e1.weight)
        
        # self.racks_uid_dict[frm.UID] = ((add_2_from))
        # self.racks_uid_dict[to.UID] = ((add_2_to))
    
    def get_dict_list(self, rack):
        # calling this on a rack should give you this 'E_1' : (('E_2', 1), ('D_1', 2))
        # for each key =rack.UID i need to add a list of 
        dict_for_rack = dict()
        child_dict = list()
        
        list_to_add = []
        
        for edge in rack.adjacent:
            if edge.rack1 != rack:
                list_to_add.append((edge.rack1.UID, edge.weight))
                
            else:
                list_to_add.append((edge.rack2.UID, edge.weight))
                
        # to_use = list_to_add[-1]  
        dict_for_rack[rack.UID] = list_to_add
        
        return dict_for_rack
        # return dict_for_rack
            
                
    
    def delete_edge(self, frm, to):
        i = 0
        while i < len(frm.adjacent):
            edge = frm.adjacent[i]
            if edge.rack1 == to or edge.rack2 == to:
                frm.adjacent.pop(i)
                break
            i += 1
        
        i = 0
        while i < len(to.adjacent):
            edge = to.adjacent[i]
            if edge.rack1 == frm or edge.rack2 == frm:
                to.adjacent.pop(i)
                break
            i += 1
    
    def delete_node(self, node):
        assert len(node.adjacent) == 0
        self.racksDict.pop(node.UID)
        
    def edge_rack_orien(self):
        racks = self.racksDict
        for rack in racks:
            for edge in rack.get_connections():
                print("edge is from " + edge.rack1.UID + " to " + edge.rack2.UID + ". COST = " + str(edge.weight))
                edge.get_edge_details()
                
    def mean_distance_from_outbound(self):
        
        pass
    
    def clear_graph(self):
        racks = self.racksDict
        
        for rack_name in racks:
            rack_obj = self.get_rack(rack_name)
            rack_mesh = rack_obj.rackLocations
            
            for dep_idx in range(len(rack_mesh)):
                for row_idx in range(len(rack_mesh[0])):
                    for col_idx in range(len(rack_mesh[0][0])):
                        
                        rack_mesh[dep_idx][row_idx][col_idx] = 0
                        
            
            
            
    # def __getitem__(self, key):
    #     return self.racksDict[key]
"""
n = node()
n.adjacent() == [Edge1, Edge2,...]
for (edge : n.adjacent):
    if (edge.rack1 == n):
        going_to = edge.orientation
    else:
        going_to = opposite of edge.orientation
        
"""
# # edge1_1 = Edge(rack1, rack2, "2->1")

# rack1.assignSKU(2, 1, 2, 4) # 0 is the depth index, 1 is the row index, 2 is col index, 4 corresponds to the SKU object which maps to int=4
# rack1.assignSKU(2, 1, 1, 6) # position(0,1,1) stores SKU that maps to 6.

# # assign SKU implementation needs to change. Since Fidelitone has a rule that all depth must contain the same SKU
# # if you assign a SKU to an n-deep rack, you must maintain same SKUs at every depth for that rack. 
# # i must assert in the assign SKU function that if an assignment to a slot has been made, that same slot at different depths is blocked for the same SKU

# # for depth in mesh:
#     # # now you have one face/level of depth you are dealing with. => matrix only
#     # currDepth = depth
#     # for eachFace in len(depth):
#     #     if eachFace == currDepth:
    
# mesh_1 = rack1.rackLocations # mesh has the depth, row, col of rack1
# # you want to go to every depth, mesh[i], check if mesh[i] == mesh[j] for every j not equal to i
# # for depthLevel in mesh:
# #     curr = depthLevel # curr equals the first depth level inside the mesh
# #     for depthIndex in range(len(mesh)): # depth index will take values 0 first and then 1
# #         print(curr == mesh[depthIndex])



