# import simpy as sp

# import pandas as pd

# import random

# import statistics
# from distanceFunction import *


# #Constants

# NUM_FORKLIFTS = 4

# SIM_DAYS = 100 #Number of days simulated

# SIM_TIME = SIM_DAYS*9*60*60 #total time simulated in seconds, do not change

# INBOUND_INTERVAL = 9*60*60 #Interval of new pallets coming in, daily.

# FORKLIFT_SPEED = 22/3 #ft/s, equals 5 mph

# UNIT_DIST = 4 #every weight of distance corresponds to 4 ft

# INITIAL_SKUS = 40 #Actual might be 40

# PERIODIC_SKUS = 30



# #Lists used for tracking times (slotting/picking)

# slotTimes = []

# pickTimes = []

# # slotLocs = {}



# rSlotTimes = []

# rPickTimes = []

# # rSlotLocs = {}



# #Gets list of orders and unique SKUs

# dataframe = pd.read_excel("./data.xlsx")
# df = dataframe



# orderNum = df.order

# SKUNum = df.item

# orderNum = list(orderNum)

# SKUNum = list(SKUNum)

# orderList = []



# checked_order = orderNum[0]

# ordr = []

# for i in range(0, len(SKUNum)):

#     if (orderNum[i] == checked_order):

#         ordr.append(SKUNum[i])

#     else:

#         checked_order = orderNum[i]

#         orderList.append(ordr)

#         ordr = []

#         ordr.append(SKUNum[i])

# orderList.append(ordr)

# uniqueSKU = []

# for sku in SKUNum:

#     if sku not in uniqueSKU:

#         uniqueSKU.append(sku)

# # print(len(uniqueSKU))



# #############################WAREHOUSE OBJ######################################

# class Warehouse(object): #create the warehouse

#     def __init__(self, env, num_forklifts):

#         self.env = env

#         self.forklift = sp.Resource(env, num_forklifts)

#         self.slotLocs = {}

#         #self.graph = graph #This needs to be added when stuff is combined



#     def slot(self, SKU,slottimeList):

#         #skuName = str(SKU)

#         #Find SKU slot function here (basically the algorithm)

#         djk_dist = find_dist_to_inb_fitness(sku) #dijkstra's path weight from inbound->slots

#         path_time = (djk_dist*UNIT_DIST)/FORKLIFT_SPEED 

#         if self.env.now == 0:

#             yield self.env.timeout(0)

#         else:

#             yield self.env.timeout(path_time)

#         slottimeList.append(path_time)

#         #assign SKU

#         # if (SKU not in slotLocs.keys()):

#         #     slotLocs[SKU] = [slot]

#         # else:

#         #     slotLocs[SKU].append(slot)



#     def rand_slot(self, SKU, slottimeList):

#         #skuName = str(SKU)

#         #random select rack, rack row, and depth

#         #rack = random.choice(dict.keys()) #select a random rack

#         #rack_row = random.randrange(rack.rows)

#         #rack_col = random.randrange(rack.columns)

#         djk_dist = find_dist_to_inb_fidel(sku) #dijkstra's path weight from inbound->random slot

#         path_time = (djk_dist*UNIT_DIST)/FORKLIFT_SPEED 

#         if self.env.now == 0:

#             yield self.env.timeout(0)

#         else:

#             yield self.env.timeout(path_time)

#         slottimeList.append(path_time)

#         #assign SKU

#         # if (SKU not in slotLocs.keys()):

#         #     slotLocs[SKU] = [slot]

#         # else:

#         #     slotLocs[SKU].append(slot)

    

#     def pick(self,SKUList,picktimeList):

#         djk_dist = 0

#         #dijksta, starting outbound->slot->slot->outbound

#         djk_dist += find_pick_dist_ob(SKUList[0]) #dist outbound -> first SKU

#         for i in range(0,len(SKUList) - 1):

#             #dist = SKUList[i] + SKUList[i+1] # use dijkstra from slot to slot

#             dist = find_dist_subsequent_picks_fitness(i)

#             djk_dist += dist

#         djk_dist += find_pick_dist_ob(SKUList[-1]) #dijkstra from last SKU -> outbound

#         path_time = (djk_dist*UNIT_DIST)/FORKLIFT_SPEED

#         yield self.env.timeout(path_time)

#         picktimeList.append(path_time)

#         #unassign SKU?

    

#     def rand_pick(self,SKUList,picktimeList):

#         djk_dist = 0

#         #dijksta, starting outbound->slot->slot->outbound

#         djk_dist += find_pick_dist_ob(SKUList[0]) #dist outbound -> first SKU

#         for i in range(0,len(SKUList) - 2):

#             #dist = SKUList[i] + SKUList[i+1] # use dijkstra from slot to slot

#             dist = find_dist_subsequent_picks_fidel(SKUList[i]) #Put the random one here

#             djk_dist += dist

#         djk_dist += find_pick_dist_ob(SKUList[-1]) #dijkstra from last SKU -> outbound

#         path_time = (djk_dist*UNIT_DIST)/FORKLIFT_SPEED

#         yield self.env.timeout(path_time)

#         picktimeList.append(path_time)

#         #unassign SKU?



# ################################SLOTTING##########################################

# def inbound_pallet(env, skuName, wh,slotList): #create inbound pallets, requests a forklift

#     with wh.forklift.request() as request:

#         yield request

#         yield env.process(wh.slot(skuName,slotList))



# def rand_inbound(env, skuName, wh, slotList):

#     with wh.forklift.request() as request:

#         yield request

#         yield env.process(wh.rand_slot(skuName,slotList))



# #################################ORDERS########################################

# def inbound_order(env, SKUlist,wh,pickList):

#     with wh.forklift.request() as request:

#         yield request

#         yield env.process(wh.pick(SKUlist,pickList))



# def every_order(env,wh,pickList):

#     for order in orderList:

#         yield env.process(inbound_order(env,order,wh,pickList))



# def rand_order(env, SKUlist,wh,pickList):

#     with wh.forklift.request() as request:

#         yield request

#         yield env.process(wh.rand_pick(SKUlist,pickList))



# def rand_every(env,wh,pickList):

#     for order in orderList:

#         yield env.process(rand_order(env,order,wh,pickList))



# #################################SETUP#########################################

# def setup(env, num_forklifts, i_inter,slotList,pickList):

#     #Create the warehouse

#     warehouse = Warehouse(env,num_forklifts)



#     #Create initial SKUs

#     for i in range(INITIAL_SKUS):

#         sku = random.choice(uniqueSKU)

#         env.process(inbound_pallet(env,sku,warehouse,slotList))



#     #Always process orders, create new SKUs in intervals

#     while True:

#         env.process(every_order(env,warehouse,pickList))

#         yield env.timeout(i_inter)

#         for i in range(PERIODIC_SKUS):

#             sku = random.choice(uniqueSKU)

#             env.process(inbound_pallet(env,sku,warehouse,slotList))



# def rand_setup(env, num_forklifts, i_inter,slotList,pickList):

#     #Create the warehouse

#     warehouse = Warehouse(env,num_forklifts)



#     #Create initial SKUs

#     for i in range(INITIAL_SKUS):

#         sku = random.choice(uniqueSKU)

#         env.process(rand_inbound(env,sku,warehouse,slotList))



#     #Always process orders, create new SKUs in intervals

#     while True:

#         env.process(rand_every(env,warehouse,pickList))

#         yield env.timeout(i_inter)

#         for i in range(PERIODIC_SKUS):

#             sku = random.choice(uniqueSKU)

#             env.process(rand_inbound(env,sku,warehouse,slotList))



# ####################ALGORITHM##EXECUTION####################################

# env = sp.Environment()

# env.process(setup(env,NUM_FORKLIFTS,INBOUND_INTERVAL,slotTimes,pickTimes))

# env.run(until=SIM_TIME)



# #Slotting

# skus_processed = len(slotTimes)

# avg_slot_time = statistics.mean(slotTimes)

# slotMedian = statistics.median(slotTimes)

# slotStdDev = statistics.stdev(slotTimes)



# #Picking

# orders_processed = len(pickTimes)

# avg_pick_time = statistics.mean(pickTimes)

# pickMedian = statistics.median(pickTimes)

# pickStdDev = statistics.stdev(pickTimes)



# print("Num SKUs Processed: " + str(skus_processed))

# print("Average Slot Time: " + str(avg_slot_time))

# print("Slot Time Median: " + str(slotMedian))

# print("Slot Time Std Dev: " + str(slotStdDev))

# print("Num Orders Processed: " + str(orders_processed))

# print("Average Pick Time: " + str(avg_pick_time))

# print("Pick Time Median: " + str(pickMedian))

# print("Pick Time Std Dev: " + str(pickStdDev))



# ####################FIDELITONE##EXECUTION###########################

# env2 = sp.Environment()

# env2.process(rand_setup(env2,NUM_FORKLIFTS,INBOUND_INTERVAL,rSlotTimes,rPickTimes))

# env2.run(until=SIM_TIME)



# #Slotting

# r_skus_processed = len(rSlotTimes)

# r_avg_slot_time = statistics.mean(rSlotTimes)

# r_slotMedian = statistics.median(rSlotTimes)

# r_slotStdDev = statistics.stdev(rSlotTimes)



# #Picking

# r_orders_processed = len(rPickTimes)

# r_avg_pick_time = statistics.mean(rPickTimes)

# r_pickMedian = statistics.median(rPickTimes)

# r_pickStdDev = statistics.stdev(rPickTimes)


# print("-------------")
# print("Num SKUs Processed (Random): " + str(r_skus_processed))

# print("Average Slot Time (Random): " + str(r_avg_slot_time))

# print("Slot Time Median (Random): " + str(r_slotMedian))

# print("Slot Time Std Dev (Random): " + str(r_slotStdDev))

# print("Num Orders Processed (Random): " + str(r_orders_processed))

# print("Average Pick Time (Random): " + str(r_avg_pick_time))

# print("Pick Time Median (Random): " + str(r_pickMedian))

# print("Pick Time Std Dev (Random): " + str(r_pickStdDev))