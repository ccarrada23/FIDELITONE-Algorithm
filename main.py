from distanceFunction import *
from SKUClass import *
from classes import *
from fitness import *
import statistics
import numpy as np
from sku_generator import *
from bad_slotting_algo import *
from simulate import *
from processing_locations import *
import json_io
import timeit
import time
from fid_receiving import *

def create_json_file(graph):
    keys = []
    shortest_dists = []
    track_preds = []
    for key in graph.racksDict.keys():
        shortest_dist, track_pred = dijkstra_helper(graph, graph.get_rack(key))
        keys.append(key)
        shortest_dists.append(shortest_dist)
        track_preds.append(track_pred)

    json_io.save_to_json("dikjstra.json", keys, shortest_dists, track_preds)    


if __name__ == "__main__":
    graph = Graph()
    create_single_column(graph, 28, "A_", 3, 4, 2)
    create_single_column(graph, 8, "B_", 4, 4, 2)
    
    
    create_double_column(graph, 9, "C1_", "D1_", 1, 5, 3)
    create_double_column(graph, 8, "C2_", "D2_", 1, 5, 3)
    
    create_double_column(graph, 9, "E1_", "F1_", 1, 5, 3)
    create_double_column(graph, 8, "E2_", "F2_", 1, 5, 3)
    create_double_column(graph, 6, "E3_", "F3_", 1, 5, 3)
    
    create_double_column(graph, 9, "G1_", "H1_", 1, 5, 3)
    create_double_column(graph, 8, "G2_", "H2_", 1, 5, 3)
    create_double_column(graph, 6, "G3_", "H3_", 1, 5, 3)
    
    create_double_column(graph, 9, "I1_", "J1_", 1, 5, 3)
    create_single_column(graph, 8, "I2_", 1, 5, 3, False)
    create_single_column(graph, 8, "J2_", 1, 3, 3, True)
    create_double_column(graph, 5, "I3_", "J3_", 1, 5, 3)
    
    create_double_column(graph, 9, "K1_", "L1_", 1, 5, 3)
    create_single_column(graph, 8, "K2_", 1, 3, 3, False)
    create_single_column(graph, 8, "L2_", 1, 5, 3, True)
    
    create_double_column(graph, 13, "M1_", "N1_", 2, 4, 2)
    create_double_column(graph, 13, "M2_", "N2_", 2, 4, 2)
    
    create_double_column(graph, 9, "O1_", "P1_", 1, 5, 3)
    create_double_column(graph, 8, "O2_", "P2_", 1, 5, 3)
    
    create_double_column(graph, 9, "Q1_", "R1_", 1, 3, 3)
    create_double_column(graph, 8, "Q2_", "R2_", 1, 3, 3)
    
    create_double_column(graph, 9, "S1_", "T1_", 3, 5, 2)
    create_double_column(graph, 6, "S2_", "T2_", 3, 4, 2)
    
    create_double_column(graph, 15, "U_", "V_", 2, 4, 2)
    
    create_double_column(graph, 15, "W_", "X_", 1, 5, 3)
    
    # delete_racks(graph, "E2_0")
    # delete_racks(graph, "E2_4")
    # delete_racks(graph, "E3_2")
    
    # delete_racks(graph, "M1_4")
    
    
    reshape_rack(graph, "M2_0", 2, 4, 1)
    reshape_rack(graph, "N1_4", 2, 4, 1)
    
    # graph.print_racks()

############# adding remaining edged to graph
# 2 weight edges among As and Cs
    graph.add_edge(graph.get_rack('C1_0'), graph.get_rack('A_0'), 2)
    graph.add_edge(graph.get_rack('A_13'), graph.get_rack('C1_8'), 2)
    graph.add_edge(graph.get_rack('C2_0'), graph.get_rack('A_15'), 2)
    graph.add_edge(graph.get_rack('A_27'), graph.get_rack('C2_7'), 2)

    # 2 weight edges among Ds and Es
    graph.add_edge(graph.get_rack('E1_0'), graph.get_rack('D1_0'), 2)
    graph.add_edge(graph.get_rack('D1_8'), graph.get_rack('E1_8'), 2)
    graph.add_edge(graph.get_rack('E2_0'), graph.get_rack('D2_0'), 2)
    graph.add_edge(graph.get_rack('D2_7'), graph.get_rack('E2_7'), 2)

    # 2 weight edges among Fs and Gs
    graph.add_edge(graph.get_rack('G1_0'), graph.get_rack('F1_0'), 2)
    graph.add_edge(graph.get_rack('F1_8'), graph.get_rack('G1_8'), 2)
    graph.add_edge(graph.get_rack('G2_0'), graph.get_rack('F2_0'), 2)
    graph.add_edge(graph.get_rack('F2_7'), graph.get_rack('G2_7'), 2)

    graph.add_edge(graph.get_rack('G3_0'), graph.get_rack('F3_0'), 2)
    graph.add_edge(graph.get_rack('F3_5'), graph.get_rack('G3_5'), 2)


    # 2 weight edges among Hs and Is
    graph.add_edge(graph.get_rack('I1_0'), graph.get_rack('H1_0'), 2)
    graph.add_edge(graph.get_rack('H1_8'), graph.get_rack('I1_8'), 2)
    graph.add_edge(graph.get_rack('I2_0'), graph.get_rack('H2_0'), 2)
    graph.add_edge(graph.get_rack('H2_7'), graph.get_rack('I2_7'), 2)

    graph.add_edge(graph.get_rack('I3_0'), graph.get_rack('H3_0'), 2)
    graph.add_edge(graph.get_rack('H3_5'), graph.get_rack('I3_4'), 2)


    # 2 weight edges among Js and Ks
    graph.add_edge(graph.get_rack('K1_0'), graph.get_rack('J1_0'), 2)
    graph.add_edge(graph.get_rack('J1_8'), graph.get_rack('K1_8'), 2)
    graph.add_edge(graph.get_rack('K2_0'), graph.get_rack('J2_0'), 2)
    graph.add_edge(graph.get_rack('J2_7'), graph.get_rack('K2_7'), 2)

    # 2 weight edges among Ls and Ms
    graph.add_edge(graph.get_rack('M1_0'), graph.get_rack('L1_0'), 2)
    graph.add_edge(graph.get_rack('L1_8'), graph.get_rack('M1_12'), 2)
    graph.add_edge(graph.get_rack('M2_0'), graph.get_rack('L2_0'), 2)
    graph.add_edge(graph.get_rack('L2_7'), graph.get_rack('M2_12'), 2)

    # 2 weight edges among Ns and Os
    graph.add_edge(graph.get_rack('O1_0'), graph.get_rack('N1_0'), 2)
    graph.add_edge(graph.get_rack('N1_12'), graph.get_rack('O1_8'), 2)
    graph.add_edge(graph.get_rack('O2_0'), graph.get_rack('N2_0'), 2)
    graph.add_edge(graph.get_rack('N2_12'), graph.get_rack('O2_7'), 2)

    # 2 weight edges among Ps and Qs
    graph.add_edge(graph.get_rack('Q1_0'), graph.get_rack('P1_0'), 2)
    graph.add_edge(graph.get_rack('P1_8'), graph.get_rack('Q1_8'), 2)
    graph.add_edge(graph.get_rack('Q2_0'), graph.get_rack('P2_0'), 2)
    graph.add_edge(graph.get_rack('P2_7'), graph.get_rack('Q2_7'), 2)

    # 2 weight edges among Rs and Ss
    graph.add_edge(graph.get_rack('S1_0'), graph.get_rack('R1_0'), 2)
    graph.add_edge(graph.get_rack('R1_8'), graph.get_rack('S1_8'), 2)
    graph.add_edge(graph.get_rack('S2_1'), graph.get_rack('R2_0'), 2)
    graph.add_edge(graph.get_rack('R2_4'), graph.get_rack('S2_5'), 2)

    # 2 weight edges among Ts and Us
    graph.add_edge(graph.get_rack('U_0'), graph.get_rack('T1_0'), 2)
    graph.add_edge(graph.get_rack('T2_5'), graph.get_rack('U_14'), 2)

    # 2 weight edges among Vs and Ws
    graph.add_edge(graph.get_rack('W_0'), graph.get_rack('V_0'), 2)
    graph.add_edge(graph.get_rack('V_14'), graph.get_rack('W_14'), 2)


    # 3 weight edges among Cs and Ds
    graph.add_edge(graph.get_rack('D1_0'), graph.get_rack('C1_0'), 3)
    graph.add_edge(graph.get_rack('C1_8'), graph.get_rack('D1_8'), 3)
    graph.add_edge(graph.get_rack('D2_0'), graph.get_rack('C2_0'), 3)
    graph.add_edge(graph.get_rack('C2_7'), graph.get_rack('D2_7'), 3)

    # 3 weight edges among Es and Fs
    graph.add_edge(graph.get_rack('F1_0'), graph.get_rack('E1_0'), 3)
    graph.add_edge(graph.get_rack('E1_8'), graph.get_rack('F1_8'), 3)

    graph.add_edge(graph.get_rack('F2_0'), graph.get_rack('E2_0'), 3)
    graph.add_edge(graph.get_rack('E2_7'), graph.get_rack('F2_7'), 3)

    graph.add_edge(graph.get_rack('E3_5'), graph.get_rack('F3_5'), 3)
    graph.add_edge(graph.get_rack('F3_0'), graph.get_rack('E3_0'), 3)

    # 3 weight edges among Gs and Hs
    graph.add_edge(graph.get_rack('H1_0'), graph.get_rack('G1_0'), 3)
    graph.add_edge(graph.get_rack('G1_8'), graph.get_rack('H1_8'), 3)

    graph.add_edge(graph.get_rack('H2_0'), graph.get_rack('G2_0'), 3)
    graph.add_edge(graph.get_rack('G2_7'), graph.get_rack('H2_7'), 3)

    graph.add_edge(graph.get_rack('G3_5'), graph.get_rack('H3_5'), 3)
    graph.add_edge(graph.get_rack('H3_0'), graph.get_rack('G3_0'), 3)

    # 3 weight edges among Is and Js
    graph.add_edge(graph.get_rack('J1_0'), graph.get_rack('I1_0'), 3)
    graph.add_edge(graph.get_rack('I1_8'), graph.get_rack('J1_8'), 3)

    graph.add_edge(graph.get_rack('J2_0'), graph.get_rack('I2_0'), 3)
    graph.add_edge(graph.get_rack('I2_7'), graph.get_rack('J2_7'), 3)

    graph.add_edge(graph.get_rack('I3_4'), graph.get_rack('J3_4'), 3)
    graph.add_edge(graph.get_rack('J3_0'), graph.get_rack('I3_0'), 3)

    # 3 weight edges among Ks and Ls
    graph.add_edge(graph.get_rack('L1_0'), graph.get_rack('K1_0'), 3)
    graph.add_edge(graph.get_rack('K1_8'), graph.get_rack('L1_8'), 3)
    graph.add_edge(graph.get_rack('L2_0'), graph.get_rack('K2_0'), 3)
    graph.add_edge(graph.get_rack('K2_7'), graph.get_rack('L2_7'), 3)

    # 3 weight edges among Ms and Ns
    graph.add_edge(graph.get_rack('N1_0'), graph.get_rack('M1_0'), 3)
    graph.add_edge(graph.get_rack('M1_12'), graph.get_rack('N1_12'), 3)
    graph.add_edge(graph.get_rack('N2_0'), graph.get_rack('M2_0'), 3)
    graph.add_edge(graph.get_rack('M2_11'), graph.get_rack('N2_11'), 3)

    # 3 weight edges among Os and Ps
    graph.add_edge(graph.get_rack('P1_0'), graph.get_rack('O1_0'), 3)
    graph.add_edge(graph.get_rack('O1_8'), graph.get_rack('P1_8'), 3)
    graph.add_edge(graph.get_rack('P2_0'), graph.get_rack('O2_0'), 3)
    graph.add_edge(graph.get_rack('O2_7'), graph.get_rack('P2_7'), 3)

    # 3 weight edges among Qs and Rs
    graph.add_edge(graph.get_rack('R1_0'), graph.get_rack('Q1_0'), 3)
    graph.add_edge(graph.get_rack('Q1_8'), graph.get_rack('R1_8'), 3)
    graph.add_edge(graph.get_rack('R2_0'), graph.get_rack('Q2_0'), 3)
    graph.add_edge(graph.get_rack('Q2_7'), graph.get_rack('R2_7'), 3)

    # 3 weight edges among Ss and Ts
    graph.add_edge(graph.get_rack('T1_0'), graph.get_rack('S1_0'), 3)
    graph.add_edge(graph.get_rack('S2_5'), graph.get_rack('T2_5'), 3)

    # 3 weight edges among Us and Vs
    graph.add_edge(graph.get_rack('V_0'), graph.get_rack('U_0'), 3)
    graph.add_edge(graph.get_rack('U_14'), graph.get_rack('V_14'), 3)

    # 3 weight edges among Ws and Xs
    graph.add_edge(graph.get_rack('X_0'), graph.get_rack('W_0'), 3)
    graph.add_edge(graph.get_rack('W_14'), graph.get_rack('X_14'), 3)

    # 2.5 weight edges among Bs and Es and A -> B edge ###### SPECIAL!!!!!
    graph.add_edge(graph.get_rack('E3_0'), graph.get_rack('B_0'), 2.5)
    graph.add_edge(graph.get_rack('B_7'), graph.get_rack('E3_5'), 2.5)
    graph.add_edge(graph.get_rack('B_0'), graph.get_rack('A_27'), 1.5)


    # 1.5 weight edges through blow-through between racks
    graph.add_edge(graph.get_rack('C1_8'), graph.get_rack('C2_0'), 1.5) # C to C
    graph.add_edge(graph.get_rack('D2_0'), graph.get_rack('D1_8'), 1.5) # D to D
    graph.add_edge(graph.get_rack('E1_8'), graph.get_rack('E2_0'), 1.5) # E to E
    graph.add_edge(graph.get_rack('F2_0'), graph.get_rack('F1_8'), 1.5) # F to F
    graph.add_edge(graph.get_rack('G1_8'), graph.get_rack('G2_0'), 1.5) # G to G
    graph.add_edge(graph.get_rack('H2_0'), graph.get_rack('H1_8'), 1.5) # H to H
    graph.add_edge(graph.get_rack('I1_8'), graph.get_rack('I2_0'), 1.5) # I to I
    graph.add_edge(graph.get_rack('J2_0'), graph.get_rack('J1_8'), 1.5) # J to J
    graph.add_edge(graph.get_rack('K1_8'), graph.get_rack('K2_0'), 1.5) # K to K
    graph.add_edge(graph.get_rack('L2_0'), graph.get_rack('L1_8'), 1.5) # L to L
    graph.add_edge(graph.get_rack('M1_12'), graph.get_rack('M2_0'), 1.5) # M to M
    graph.add_edge(graph.get_rack('N2_0'), graph.get_rack('N1_12'), 1.5) # N to N
    graph.add_edge(graph.get_rack('O1_8'), graph.get_rack('O2_0'), 1.5) # O to O
    graph.add_edge(graph.get_rack('P2_0'), graph.get_rack('P1_8'), 1.5) # P to P
    graph.add_edge(graph.get_rack('Q1_8'), graph.get_rack('Q2_0'), 1.5) # Q to Q
    graph.add_edge(graph.get_rack('R2_0'), graph.get_rack('R1_8'), 1.5) # R to R

    graph.add_edge(graph.get_rack('E2_7'), graph.get_rack('E3_0'), 1.5) # E to E
    graph.add_edge(graph.get_rack('F3_0'), graph.get_rack('F2_7'), 1.5) # F to F
    graph.add_edge(graph.get_rack('G2_7'), graph.get_rack('G3_0'), 1.5) # G to G
    graph.add_edge(graph.get_rack('H3_0'), graph.get_rack('H2_7'), 1.5) # H to H
    graph.add_edge(graph.get_rack('I2_7'), graph.get_rack('I3_0'), 1.5) # I to I
    graph.add_edge(graph.get_rack('J3_0'), graph.get_rack('J2_7'), 1.5) # J to J

    # any racks connected with outbound and inbound must say R2L for type of that edge
    graph.add_rack(Rack('Outbound', RackLayout(1,1,1).createMesh(), []))
    graph.add_rack(Rack('Inbound', RackLayout(1,1,1).createMesh(), []))
    
    # edges connecting racks to outbound
    
    # connections with outbound
    graph.add_edge(graph.get_rack('Q2_7'), graph.get_rack('Outbound'), 6)
    graph.add_edge(graph.get_rack('Outbound'), graph.get_rack('R2_7'), 6)
       
    graph.add_edge(graph.get_rack('S2_5'), graph.get_rack('Outbound'), 8)
    graph.add_edge(graph.get_rack('Outbound'), graph.get_rack('T2_5'), 8)
    
    graph.add_edge(graph.get_rack('U_14'), graph.get_rack('Outbound'), 9)
    graph.add_edge(graph.get_rack('Outbound'), graph.get_rack('V_14'), 9)
    
    graph.add_edge(graph.get_rack('W_14'), graph.get_rack('Outbound'), 9.5)
    graph.add_edge(graph.get_rack('Outbound'), graph.get_rack('X_14'), 9.5)
    
    
    # connections with inbound
    graph.add_edge(graph.get_rack('Q2_7'), graph.get_rack('Inbound'), 6)
    graph.add_edge(graph.get_rack('Inbound'), graph.get_rack('R2_7'), 6)
    
    graph.add_edge(graph.get_rack('Inbound'), graph.get_rack('P2_7'), 6)
    graph.add_edge(graph.get_rack('O2_7'), graph.get_rack('Inbound'), 6)
    
    graph.add_edge(graph.get_rack('M2_12'), graph.get_rack('Inbound'), 5)
    graph.add_edge(graph.get_rack('Inbound'), graph.get_rack('N2_12'), 5)
    
    graph.add_edge(graph.get_rack('K2_7'), graph.get_rack('Inbound'), 6)
    graph.add_edge(graph.get_rack('Inbound'), graph.get_rack('L2_7'), 6)
    
    ####STORING OB AND IB DIST IN EVERY RACK
    shortest_dist, track_pred = dijkstra_helper(graph, graph.get_rack('Outbound'))
    for node in shortest_dist.keys():
        # scaled_z_rack = get_rack_z_OB(graph.get_rack(node))
        graph.get_rack(node).distToOB = ((shortest_dist[node] - MEAN_DISTANCE_FROM_OUTBOUND)/STD_DEV_DISTANCE_OUTBOUND) + 2.308369718955168
        
        
    shortest_dist, track_pred = dijkstra_helper(graph, graph.get_rack('Inbound'))
    for node in shortest_dist.keys():
        graph.get_rack(node).distToIB = shortest_dist[node]
    ######
    # SKUs being assigned to slots in the graph
    ########
    # SKUs to be assigned for simulation
    
    ### simple function for assigning SKUs:
    def assigningSKUs(graph, converted_data):
        
        for assignment in converted_data:
            
            rack_name = assignment[0]
            depth = 0
            row = assignment[1]
            column = assignment[2]
            SKUid = assignment[3]
            
            graph.get_rack(rack_name).assignSKU(depth, row, int(column), get_key(SKUid))
            
    # assigningSKUs(graph, )
            
            
    '''
    graph.get_rack('E1_0').assignSKU(0,2,1,get_key('EA30520')) # EA00703 assoc
    graph.get_rack('W_6').assignSKU(0,2,1,get_key('EA30520')) # EA00703 assoc
    graph.get_rack('W_3').assignSKU(0,2,2,get_key('EA30520')) # EA00703 assoc
    graph.get_rack('M1_5').assignSKU(0,0,0,get_key('CSSP50001C')) # key 32 assoc
    graph.get_rack('M1_1').assignSKU(0,1,1,get_key('CSSP50001C')) # key 32 assoc
    graph.get_rack('W_1').assignSKU(0,1,2,get_key('CSSP50001C')) # key 32 assoc
    graph.get_rack('B_3').assignSKU(0,0,1,get_key('DVG39226'))
    graph.get_rack('H2_0').assignSKU(0,0,2,get_key('DVG39226'))
    graph.get_rack('D1_4').assignSKU(0,1,2,get_key('CSSS70051C')) ##
    graph.get_rack('H2_5').assignSKU(0,3,2,get_key('DVG39226'))
    graph.get_rack('G1_3').assignSKU(0,1,2,get_key('CSSS70051C')) ##
    graph.get_rack('W_7').assignSKU(0,0,0,get_key('PK34022BAGr1'))
    graph.get_rack('W_7').assignSKU(0,0,2,get_key('DVG39226'))
    graph.get_rack('X_0').assignSKU(0,2,2,get_key('PK34022BAGr1'))
    graph.get_rack('X_3').assignSKU(0,1,2,get_key('DVG39226'))
    graph.get_rack('C1_6').assignSKU(0,1,2,get_key('CSSS30055C12'))
    graph.get_rack('X_7').assignSKU(0,0,2,get_key('DVG39226'))
    graph.get_rack('G2_3').assignSKU(0,1,2,get_key('CSSS40082C')) ##
    graph.get_rack('M2_3').assignSKU(0,1,1,get_key('DVG39226'))
    graph.get_rack('M2_5').assignSKU(0,1,0,get_key('DVG39226'))
    graph.get_rack('N1_5').assignSKU(0,1,0,get_key('CSSS70051C')) ##
    graph.get_rack('N1_0').assignSKU(0,1,0,get_key('DVG39226'))
    graph.get_rack('L1_0').assignSKU(0,1,2,get_key('DVG39226'))
    graph.get_rack('L2_0').assignSKU(0,0,1,get_key('EA00555'))
    graph.get_rack('A_7').assignSKU(0,1,0,get_key('DVG39226'))
    graph.get_rack('T2_0').assignSKU(0,3,0,get_key('CSDVG70034'))
    graph.get_rack('T1_4').assignSKU(0,1,0,get_key('DVG39226'))
    graph.get_rack('S1_4').assignSKU(0,1,0,get_key('DVG39226'))
    graph.get_rack('S1_0').assignSKU(0,0,1,get_key('CSDVG70034'))
    graph.get_rack('K1_0').assignSKU(0,1,0,get_key('DVG39226'))
    graph.get_rack('E1_0').assignSKU(0,1,2,get_key('DVG39226'))
    graph.get_rack('E2_4').assignSKU(0,4,0,get_key('DVG39226'))
    graph.get_rack('Q1_0').assignSKU(0,1,2,get_key('DVG39226'))
    graph.get_rack('Q1_2').assignSKU(0,1,1,get_key('DAS39211'))
    graph.get_rack('Q2_4').assignSKU(0,0,2,get_key('EA00555'))    
    graph.get_rack('P2_4').assignSKU(0,1,2,get_key('DVG39226'))
    graph.get_rack('I1_0').assignSKU(0,0,0,get_key('DHW39214')) #hjbghjvhvj
    graph.get_rack('W_3').assignSKU(0,1,2,get_key('CSSS70051C')) ##
    graph.get_rack('C1_3').assignSKU(0,1,0,get_key('DVG39226'))
    graph.get_rack('P2_0').assignSKU(0,1,2,get_key('EA91303'))
    graph.get_rack('L1_6').assignSKU(0,0,2,get_key('DVG39226'))
    graph.get_rack('F3_1').assignSKU(0,1,2,get_key('CSDVG70034'))
    graph.get_rack('W_7').assignSKU(0,1,2,get_key('DVG39226'))
    graph.get_rack('J3_0').assignSKU(0,1,2,get_key('DAS39211'))
    graph.get_rack('C1_3').assignSKU(0,2,2,get_key('CSSP40090C')) ##
    graph.get_rack('J2_0').assignSKU(0,1,2,get_key('CSSS40082C')) ##
    graph.get_rack('J1_5').assignSKU(0,3,2,get_key('DVG39226'))
    graph.get_rack('N1_5').assignSKU(0,0,0,get_key('DVG39226'))
    graph.get_rack('K1_1').assignSKU(0,1,2,get_key('DVG39226'))
    graph.get_rack('V_0').assignSKU(0,1,0,get_key('DAS39211'))
    graph.get_rack('C2_1').assignSKU(0,1,2,get_key('CSSS70051C')) ##
    graph.get_rack('U_1').assignSKU(0,1,0,get_key('DVG39226'))
    graph.get_rack('U_7').assignSKU(0,2,0,get_key('DHW39214'))
    graph.get_rack('K1_4').assignSKU(0,1,2,get_key('CSSP40091C'))
    graph.get_rack('U_12').assignSKU(0,2,1,get_key('DVG39226'))
    graph.get_rack('V_12').assignSKU(0,1,0,get_key('DHW39214'))
    graph.get_rack('C1_6').assignSKU(0,1,2,get_key('DVG39226'))
    graph.get_rack('D1_3').assignSKU(0,0,2,get_key('CS42212'))
    graph.get_rack('A_12').assignSKU(0,0,0,get_key('CSDVG70034'))
    graph.get_rack('K1_0').assignSKU(0,1,2,get_key('DVG39226'))
    '''
    # graph.get_rack('W_6').assignSKU(0,1,1,get_key('EA30520'))
    # graph.get_rack('W_6').assignSKU(0,0,1,get_key('EA30520'))
    # graph.get_rack('W_6').assignSKU(0,0,0,get_key('EA30520'))
    ######
    CSSP50001C_obj = SKU_map[get_key('CSSP50001C')]
    # print(graph.get_rack('E1_0').rackLocations)
    # to call any of the sku attributes you need to get that object first
    sku_obj = SKU_map[get_key('EA00703')]
    # print(sku_obj.associationList)
    # print(graph.get_rack('X_10').rackLocations)
    EA00703_obj = SKU_map[get_key('EA00703')]

    # print(dijkstra(graph, graph.get_rack('X_6'), graph.get_rack('Outbound'))[1])
    
    # print(dist_from_outbound_zscore(graph, graph.get_rack('M1_8'),(0,0,0)))
    # print(dijkstra(graph, graph.get_rack('M1_8'), graph.get_rack('Outbound')))
    # print(get_velocity_score(graph, SKU_map[4], graph.get_rack('X_4')))
    
    
    # (dijkstra(graph, graph.get_rack('A_0'), graph.get_rack('Outbound')))
    # (dijkstra(graph, graph.get_rack('E1_1'), graph.get_rack('Outbound'))) # closer to outbound
    # z rack loc = 1.7 (relatively far from outbound)
    # print(SKU_map[4].weight)
    # sku_to_check = SKU_map[4].weight
    rack_W_7 = graph.get_rack('W_7')
    # print(rack_W_7.rackLocations)
    # graph.get_rack(?
    #                )
    
    # BATCH 1 to pick 
    # if you slot these, they will go to their best locations, how do you pick then?
    # if you pick these, picking should take less time because these would be close to their assoc
    # items but for that even associated items need to be picked 
    
    CSSS70051C_obj = SKU_map[get_key('CSSS70051C')]
    CSDVG70034_obj = SKU_map[get_key('CSDVG70034')]
    EA50420_obj = SKU_map[get_key('EA50420')]
    PK34024BAGr1_obj = SKU_map[get_key('PK34024BAGr1')]
    CSDVG70034_obj = SKU_map[get_key('CSDVG70034')]
    
    # BATCH 2 to pick
    EA80733_obj = SKU_map[get_key('EA80733')]
    CS41412_obj = SKU_map[get_key('CS41412')]
    CSSP40090C_obj = SKU_map[get_key('CSSP40090C')]
    CSSP40091C_obj = SKU_map[get_key('CSSP40091C')]
    CFC35202_obj = SKU_map[get_key('CFC35202')]
    
    DVG39226_obj = (SKU_map[get_key('DVG39226')])
    # distance_to_most_assoc_sku_locs(graph, graph.get_rack('M1_3'), (0,2,1), DVG39226_obj, dijkstra_map)
    
    # create_json_file(graph)
    dijkstra_map = json_io.load_from_json("dikjstra.json")
    
    # print(distance_to_most_assoc_sku_locs(graph, graph.get_rack('M1_3'), (0,2,1), DVG39226_obj, dijkstra_map['M1_3'][0], dijkstra_map['M1_3'][1]))
    # print(DVG39226_obj.associationList)
    # fittest_location(graph, DVG39226_obj, dijkstra_map)
    # print(type(list(dijkstra_map.keys())[0]))
    # key = list(dijkstra_map.keys())[0]
    # print(type(dijkstra_map[key]))
    # print(type(dijkstra_map[key][0]))
    # print(type(dijkstra_map[key][1]))
    # print(type(dijkstra_map.values()[0]))
    # print(type(dijkstra_map.values()[0][0]))
    # print(type(dijkstra_map.values()[0][1]))
    
    # save_to_json("djikstra.json", rack, shortest_dist, track_pred)
    
    # fittest_location(graph, CSSS70051C_obj) #('C2_1', (0, 2, 0))
    # print(CSSS70051C_obj.key) # 17
    # print(graph.get_rack('C2_1').rackLocations)
    # ['CSSS70051C', 'CSSP40090C', 'CSDVG60034', 'CSSP50003C']
    
    # FULLY SATISFIED WITH THESE FITNESS VALUES 
    
    # start = time.time()
    # fittest_location(graph, CSSS70051C_obj, dijkstra_map) #('C2_1', (0, 2, 0))
    # end = time.time()
    # print(end - start)
    # print(len(SKU_map))
    
    # fittest_location(graph, PK34024BAGr1_obj) # ('A_7', (0, 0, 0))
    
    # fittest_location(graph, CSSS70051C_obj) #('C2_1', (0, 2, 0))
    
    # fittest_location(graph, CSSP40091C_obj) # ('J2_0', (0, 1, 0))
    # print(PK34024BAGr1_obj.weight, PK34024BAGr1_obj.velocity, PK34024BAGr1_obj.associationList)
    # graph.get_rack('A_7').assignSKU(0,1,0,get_key('DVG39226')) is one of the assoc items
    
    # FULLY SATISFIED WITH THESE FITNESS VALUES 
    # distances = dijkstra_helper(graph, graph.get_rack('A_0'))[0] 
    # print(SKU_map[134].associationList)
    # print(SKU_map[134].velocity)
    # print(SKU_map[134].weight)
    
    # objtocheck = SKU_map[134] #CSSS40081C
    
    # print(objtocheck.UID, objtocheck.weight, objtocheck.velocity, objtocheck.associationList)
    # # 0.43860816474440456 1.058272336325717
    # # 'CSSS40082C', 'CSSP40090C', 'CSSS40080C', 'CSSS70051C']
    # start = time.time()
    
    # fittest_location(graph, SKU_map[134], dijkstra_map) # ('G2_3', (0, 2, 2))
    
    # 2.4073031245567362, 0.03412704649834447, CSCIC35320
    
    # ['CSSS40082C', 'CSSS60060C', 'DAS37321', 'CSSS60050C']
    
    # fittest_location(graph, SKU_map[114], dijkstra_map)
    # fittest_location(graph, SKU_map[33], dijkstra_map)
    # fittest_location(graph, SKU_map[13], dijkstra_map)
    
    # ('G2_3', (0, 2, 2))
    # ('A_7', (0, 2, 0))
    # ('A_0', (0, 0, 0))
    # ('C1_3', (0, 1, 2))
    # fittest_location(graph, SKU_map[14], dijkstra_map)
    # fittest_location(graph, SKU_map[100], dijkstra_map)
    # fittest_location(graph, SKU_map[161], dijkstra_map)
    # print("assoc = " + str(SKU_map[161].associationList))
    # print("weight = " + str(SKU_map[161].weight))
    # print("velocity = " + str(SKU_map[161].velocity))
    
    # fittest_location(graph, SKU_map[86], dijkstra_map)
    
    # print("assoc = " + str(SKU_map[86].associationList))
    # print("weight = " + str(SKU_map[86].weight))
    # print("velocity = " + str(SKU_map[86].velocity))
    rows_num = (len(graph.get_rack('W_7').rackLocations[0]))
    
    # print(test_SKUlocs)
        
    # locations_to_assign = translate_locations_graph(test_SKUlocs, graph)
    # print(locations_to_assign)
    # a = (20.0, 1.0, 'BB', 2.0, 'CS41212')
    # print(bay_map(a))
    
    # wrong: [['P2_7', 4, 2], ['P2_6', 4, 2], ['P2_5', 4, 2], ['P2_4', 4, 2], ['P2_3', 4, 2]]
    # right: [(9, 7, 'AA', 1)], 2: [(9, 7, 'AA', 2)], 3: [(9, 7, 'AA', 3)], 4: [(9, 7, 'BB', 1)]
    # counter1 = 3
    # for index in SKU_locations:
    #     print(SKU_locations[index])
    #     counter1 -= 1
    #     if counter1 == 0:
    #         break
        
    # print(test_SKUlocs[1][0])
    # print(SKU_locations[13][0])
    # print(SKU_locations[875][0])
    # map_to_get = bay_map(SKU_locations[875][0])
    # print(map_to_get)
    # ('C1_3', (0, 1, 2)) for 13
    
    # print((SKU_map[565]))
    # 565 skus in the sku map
    
    all_SKU_IDS = []
    
    for index in SKU_map:
        if index == 0:
            continue
        all_SKU_IDS.append(SKU_map[index].UID)
        
        
    SKUS_that_need_fittest = []   
    
    for index in SKUs_to_slot:
        if index == 0:
            continue
        SKUS_that_need_fittest.append(SKUs_to_slot[index])   
    
    
    def unique(list1):
     
        # initialize a null list
        unique_list = []
        
        # traverse for all elements
        for x in list1:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
        
        return unique_list
    
    # print(len(unique(locs_to_check)))
            
    # unique_need_fitness = unique(SKUS_that_need_fittest)


    # neeed = []
    # for SKU_item in list_to_slot:
    #     curr_SKU = SKU_item
    #     for SKU_item in all_SKU_IDS:
    #         if curr_SKU == SKU_item: 
    #             neeed.append(curr_SKU) # this will only have the SKUs that the main SKU_map has
            
    # need1 = unique(neeed) # this will giv
    # print(len(neeed))
    # print(len(list_to_work_with))
    
    
    # common_needFit_map = []
    
    # for sku_id in unique_need_fitness:
    #     sku = sku_id
    #     # print(sku)
    #     for index in SKU_map:
    #         if index == 0:
    #             continue
    #         # print(SKU_map[index])
    #         if sku == SKU_map[index].UID:
    #             common_needFit_map.append(sku)
                
    # # print(common_skus)
    # # print(get_key('CSSS30056C12'))
    # # print(get_key('CSS35222'))
    
    # one_not_two = set(unique_need_fitness).difference(common_needFit_map) #print 1 and 4
    # print(one_not_two)
    
    # for sku in SKUS_that_need_fittest:
    #     print(get_key(sku))
    
        
    
    # slot_locs = []
    # slot_locs = translate_locations_graph(SKU_locations, graph)   # what is currently inside the facility
    # assigningSKUs(graph, slot_locs)
    
    # print(SKUs_to_slot[1])
    # print(SKUs_to_slot[2])
        
    # need data for these SKUs: {'EA59103', 'CS10529', 'EA56503', 'EA58103', 'EA57603', 'EA58503', 'EA56603'} to run algorithm
    # slot_sku_batch(graph, test_list, dijkstra_map)
    
    # counter11 = 3
    # for rack in graph.racksDict:
    #     print(rack)
    #     print(graph.get_rack(rack).rackLocations)
    #     counter11 -= 1
    #     if counter11 == 0:
    #         break
    
    
    # graph.clear_graph()
    
    # counter11 = 3
    # for rack in graph.racksDict:
    #     print(rack)
    #     print(graph.get_rack(rack).rackLocations)
    #     counter11 -= 1
    #     if counter11 == 0:
    #         break
    
    
    
    
    
    
    
    
    ######################################FIDELITONE##########################################
    
    # ALWAYS CALL THE FUNCTIONS BELOW IN THIS ORDER:
    
    # 1) graph.clear_graph()
    # 2) slot_locs = translate_locations_graph(SKU_locations, graph)
    # 2) assigningSKUs(graph, slot_locs)
    # 3) slot_sku_batch(graph, SKUS_that_need_fittest, dijkstra_map)