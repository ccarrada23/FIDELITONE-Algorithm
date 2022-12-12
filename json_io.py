import json


# each node is 
def save_to_json(filename, racks, shortest_dists, track_preds):
    dijkstra_dict = {}
    
    for rack, shortest_dist, track_pred in zip(racks, shortest_dists, track_preds):
        dijkstra_dict[rack] = (shortest_dist, track_pred)
    
    with open(filename, "w") as outfile:
        json.dump(dijkstra_dict, outfile)
    
def load_from_json(filename):
    dijkstra_dict = {}
    
    with open(filename, "r") as infile:
        dijkstra_dict = json.load(infile)
        
    return dijkstra_dict
    