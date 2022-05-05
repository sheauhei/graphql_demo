from utils import read_json 
import os 

# # dummy data base
# class DummyToplogyDB():
#     def __init__(self):
#         self._nodes = {}
#         self._edges = {}

#     def _load_node(self, _id):
#         node = self._nodes.get("_id")
#         if not node: 
#             node = Node(_id)
#             self._nodes['_id'] = node
#         return node

#     def _load_edge(self, _id):
#         edge = self._edges.get("_id")
#         if not edge: 
#             edge = Edge(_id)
#             self._edges['_id'] = edge
#         return edge

#     def get_node(self, _id):
#         if not _id:
#             return None 
#         return self._load_node(_id)
    
#     def get_edge(self, _id):
#         if not _id:
#             return None 

#         return self._load_edge(_id)

#     def get_nodes(self, id_list):
#         if not id_list:
#             return []

#         return [self.get_node(id) for id in id_list]

#     def get_edges(self, id_list):
#         if not id_list:
#             return []

#         return [self.get_edge(id) for id in id_list]

#     def close(self):
#         self._nodes = {}
#         self._edges = {}
        
# dummy_db = DummyToplogyDB()

# data definitions
class Node():
    def __init__(self, id):
        data = read_json(f"data/nodes/{id}.json")
        self._data = data
        self._id = data.get("id")
        self._name = data.get("name")
        self._type = data.get("type")
        self._latitude = data.get("latitude")
        self._longitude = data.get("longitude")
        self._capacity = data.get("capacity")

        # prepare the edges
        self._edge_ids = data.get("edges")

    def to_dict(self):
        data = {
            "id": self._id,
            "name": self._name, 
            "type": self._type, 
            "latitude": self._latitude,
            "longitude": self._longitude, 
            "capacity": self._capacity,
            "edge_ids": self._edge_ids
        }
        # preparing edge data
        return data

class Edge():
    def __init__(self, id):
        data = read_json(f"data/edges/{id}.json")
        self._data = data
        self._id = data.get("id")
        self._price = data.get("price")
        self._sell_channel = data.get("sell_channel")

        self._source_node_id = data.get("source")
        self._target_node_id = data.get("target")

    def to_dict(self):
        data = {
            "id": self._id,
            "source_node_id": self._source_node_id,
            "target_node_id": self._target_node_id,
            "price": self._price,
            "sell_channel": self._sell_channel
        }

        # preparing edge data
        return data

def get_node_data(id):
    node = Node(id)
    # node = dummy_db.get_node(id)
    return node.to_dict()

def get_nodes_data(id_list):
    return [ get_node_data(id) for id in id_list]

def get_all_nodes_data():
    ids = []
    for root, dirs, files in os.walk("data/nodes"):
        for fn in files: 
            ids.append(fn.split(".")[0])
    
    # get all data from node ids
    data = get_nodes_data(ids)
    return data

def get_edge_data(id):
    edge = Edge(id)
    # edge = dummy_db.get_edge(id)
    return edge.to_dict()

def get_edges_data(id_list):
    return [ get_edge_data(id) for id in id_list]

def get_all_edges_data():
    ids = []
    for root, dirs, files in os.walk("data/edges"):
        for fn in files: 
            ids.append(fn.split(".")[0])
    
    # get all data from node ids
    return get_edges_data(ids)