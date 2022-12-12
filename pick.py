UNIT_DIST = 4

FORKLIFT_SPEED = 22/3

# def pick(self,SKUList,picktimeList):
    
#         djk_dist = 0

#         #dijksta, starting outbound->slot->slot->outbound

#         djk_dist += random.randint(15,275) #dist outbound -> first SKU

#         for i in range(0,len(SKUList) - 1):

#             #dist = SKUList[i] + SKUList[i+1] # use dijkstra from slot to slot

#             dist = random.randint(1,100)

#             djk_dist += dist

#         djk_dist += random.randint(15,275) #dijkstra from last SKU -> outbound

#         path_time = (djk_dist*UNIT_DIST)/FORKLIFT_SPEED

#         yield self.env.timeout(path_time)

#         picktimeList.append(path_time)
        
        
def picking_sim(graph, SKUList, picktimeList):
    
    first_dist = 0 # OB -> FIRST SLOT
    
    distances_SKUList = [] # FIRST SLOT -> SECOND SLOT -> THIRD SLOT
    
    last_dist = 0 # SKUList[-1] -> OB
    
    total_dist = first_dist + distances_SKUList + last_dist
    
    path_time = (total_dist*UNIT_DIST)/FORKLIFT_SPEED
    
    return path_time
    