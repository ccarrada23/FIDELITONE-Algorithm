# class Location:
#     def __init__(self, name, height, capacity, status):
#         self.name = name # each level has a name, A B C or D
#         self.height = height # each level is at one of 4 heights depending on its name
#         self.capacity = capacity # each level has a constant capacity of 3
#         self.status = status # false = occupied, true = free
    
#     def introLevel(self):
#         if self.status == True:
#             print("The free level is located in rack-level " + self.name + " with height:" + str(self.height) + " & capacity:" + str(self.capacity))
#         else:
#             print("The occupied level is located in rack-level " + self.name + " with height:" + str(self.height) + " & capacity:" + str(self.capacity)) 
            
# representing locations as a 3*3 matrix with empty. each position [i][j] in the matrix for ith row 
# and jth column is a location where we will calculate fitness. so the location is essentially just a matrix 
# which is 4*3, which means the bottom row is A, top row is D and each row has a capacity equal to the number
# of columns in the row. fitness at each location depends on distance and height. At each rack, levels 
# A, B, C and D all have different heights but the same capacity 
# This is how a rack with capacity/level = 3 looks like
# D : [] [] []
# C : [] [] []
# B : [] [] []
# A : [] [] []
# note there are racks that can have more levels than A, B, C, D and a capacity > 3

import numpy as np

# from SKUClass import SKU

# class SKU:
#     def __init__(self, UID, weight, velocity, associationList):
#         self.UID = UID
#         self.weight = weight # in units
#         self.velocity = velocity # frequency of pick in a given period 
#         # volume maybe? per tray/unit in the pallet 
#         self.associationList = associationList # list of items it is associated with along with association values
        


class RackLayout: # looks like [ [][][], [][][], [][][], [][][] ]
    def __init__(self, 
                 depth,
                 rows,
                 columns): 
        self.depth = depth
        self.rows = rows
        self.columns = columns

        
    def createMesh(self):
        rows = self.rows
        columns = self.columns
        depth = self.depth
        locationMesh = np.zeros((depth, rows, columns), int)
        return locationMesh
        
        
        
# def SKULocationInMatrix(self, row, column, SKUmap): 
# wanna do this: matrix_a.SKULocationInMatrix(rowInd, columnInd, SKU###)
# matrix = RackLayout(rows, columns).createMatrix 
# rowInd = row where we want to put SKU
# columnInd = column where we want to put SKU
# SKU### = int_to_SKU
# matrix_SKU[rowInd][colInd] = int key from         
        
        
# level_a = RackLayout(4,3)
# level_a.createMatrix() # this will create a 4*3 matrix
# item velocity, dump of past orders, current state of the facility, 
# aisle wise data for the racks

# class Rack:
#     def __init__(self, 
#                  UID,
#                  rackLocations,
#                  neighbors = []):
#         self.UID = UID
#         self.rackLocations = rackLocations # empty or full 
#         self.neighbors = neighbors
        
#     def assignSKU(self, 
#                   rowInd, 
#                   colInd, 
#                   SKUkey):
#         matrix = self.rackLocations
#         matrix[rowInd][colInd] = SKUkey
        
#     def addNeighbor(self):
#         pass

# SKU001 = SKU("001", 40, 60, [])
# SKU002 = SKU("002", 32, 87, [])
# SKU003 = SKU("003", 22, 12, [])
# SKU004 = SKU("004", 76, 47, [])
# SKU005 = SKU("005", 76, 47, [])
# SKU006 = SKU("006", 76, 47, [])

# int_to_SKUMap = {
#     0 : None,
#     1 : SKU001,
#     2 : SKU002,
#     3 : SKU003,
#     4 : SKU004,
#     5 : SKU005,
#     6 : SKU006
# }
     
# rack_new = Rack('new', RackLayout(4,3).createMatrix())
# rack_new.assignSKU(0, 2, 4)
# rack_new.assignSKU(3, 1, 1)
# print(rack_new.rackLocations)

# for row in rack_new.rackLocations:
#     for element in row:
#         print(int_to_SKUMap[element])
        
        
        
# rack1 = Rack('A1', RackLayout(4,3).createMatrix())
# print(rack1.rackLocations)

# rack2 = Rack('A2', RackLayout(1,4,3).createMesh()) # you can create racks according to the number of slots you have
# print(rack2.rackLocations)


# class Edge:
#     def __init__(self, rack1, rack2, weight):
#         self.rack1 = rack1
#         self.rack2 = rack2
#         self.weight = weight
        
#     def getEdgeDetails(self):
#         return "Edge: {}<------{}------>{}".format(self.rack1.UID, self.weight, self.rack2.UID)

# # racks we have in the aisle 
# # a rack is created by giving it a unique ID, and a location matrix

# rack_1 = Rack('A1', RackLayout(4,3).createMatrix()) 
# rack_2 = Rack('A2', RackLayout(4,3).createMatrix()) 
# rack_3 = Rack('A3', RackLayout(4,3).createMatrix()) 
# rack_4 = Rack('A4', RackLayout(4,3).createMatrix()) 
# rack_5 = Rack('A5', RackLayout(4,3).createMatrix()) 
# rack_6 = Rack('A6', RackLayout(4,3).createMatrix()) 
# rack_7 = Rack('A7', RackLayout(4,3).createMatrix()) 
# rack_8 = Rack('A8', RackLayout(4,3).createMatrix()) 
# rack_9 = Rack('A9', RackLayout(4,3).createMatrix()) 
# rack_10 = Rack('A10', RackLayout(4,3).createMatrix()) 

# # edges on one side of aisle
# edge_1 = Edge(rack_1, rack_2, 1)
# edge_2 = Edge(rack_2, rack_3, 1)
# edge_3 = Edge(rack_3, rack_4, 1)
# edge_4 = Edge(rack_4, rack_5, 1)

# # edges on the other side of aisle
# edge_5 = Edge(rack_6, rack_7, 1)
# edge_6 = Edge(rack_7, rack_8, 1)
# edge_7 = Edge(rack_8, rack_9, 1)
# edge_8 = Edge(rack_9, rack_10, 1)

# # edges connecting two sides of the aisle. (rack_1, rack_6), (rack_5, rack_10)
# edge_9 = Edge(rack_1, rack_6, 2) 
# edge_10 = Edge(rack_5, rack_10, 2)

# # array of edges, edge_1 to edge_10
# edges  = [edge_1, edge_2, edge_3, edge_4, edge_5, edge_6, edge_7, edge_8, edge_9, edge_10]

# # for edge in edges:
# #     print(edge.getEdgeDetails())

# class Graph:
#     def __init__(self):
#         self.racks = dict()
        

#     def addEdge(self, edge):
#         if edge.rack1 not in self.racks:
#             self.racks[edge.rack1] = []
#         if edge.rack2 not in self.racks:
#             self.racks[edge.rack2] = []
            
#     def printGraph(self):
#         racks_UID = []
#         for rack in self.racks:
#             racks_UID.append(rack.UID)
#         print("Number of vertices in the graph: ", len(self.racks), ". Vertices in the graph:  ", racks_UID)
    
        
# # graph = Graph()
# # for edge in edges:
# #     graph.addEdge(edge)
# # graph.printGraph() 
  
# rack_1 = Rack('A1', RackLayout(4,3).createMatrix())
# rack_1_slots = rack_1.rackLocations
# # print(rack_1_slots)


