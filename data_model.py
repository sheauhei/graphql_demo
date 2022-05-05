from utils import read_json 
import os 
from functools import reduce
from operator import add
from datetime import datetime

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

class StreamData():

    def __init__(self, data=None):
        if not data: 
            data = {}
            self.timestamp = None
            self.price = 0
            self.power = 0
            self.energy = 0
            self.predicted_power = 0
            self.predicted_energy = 0
            self.revenue = 0
        else:
            self.timestamp = datetime.strptime(data.get("timestamp"), r"%Y/%m/%d %H:%M")
            self.price = data.get("price", 0)
            self.power = data.get("power", 0)
            self.energy = data.get("energy", 0)
            self.predicted_power = data.get("predicted_power", 0)
            self.predicted_energy = data.get("predicted_energy", 0)
            self.revenue = self.energy * self.price
            
    def to_dict(self):
        data = {
            "timestamp": self.timestamp,
            "price": self.price,
            "power": self.power,
            "energy": self.energy,
            "predicted_power": self.predicted_power,
            "predicted_energy": self.predicted_energy,
            "revenue": self.revenue
        }
        return data
        
    def __add__(self, b):
        target_sd = StreamData() 
        target_sd.timestamp = self.timestamp
        target_sd.power = self.power + b.power # sum([sd.power for sd in stdata_list])
        target_sd.energy = self.energy + b.energy 
        target_sd.predicted_power = self.predicted_power + b.predicted_power 
        target_sd.predicted_energy = self.predicted_energy + b.predicted_energy 
        target_sd.revenue = self.revenue + b.revenue 
        
        if target_sd.energy:
            target_sd.price = target_sd.revenue / target_sd.energy
        else:
            target_sd.price = 0

        return target_sd

class StreamDataList():
    def __init__(self, edge_id=None, time_period=None):
        self.stream_data_list = []

        if edge_id:
            data_series = read_json(f"data/time-series/edge.{edge_id}.json")
            self.stream_data_list = [ StreamData(data) for data in data_series]
        
    def to_dict(self):
        ret = [ obj.to_dict() for obj in self.stream_data_list]
        return ret 

    def __add__(self, b):
        target = StreamDataList()
        length = len(self.stream_data_list)
        
        for i in range(length):
            target.stream_data_list.append(self.stream_data_list[i] + b.stream_data_list[i])

        return target 


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

def get_series_data_by_edge(edge_id):
    series = StreamDataList(edge_id)
    data = series.to_dict() 
    return data

def get_series_data_by_source_node(node_id):
    data = get_node_data(node_id)
    edges_ids = data["edge_ids"]
    edges = get_edges_data(edges_ids)
    
    streamlist = []

    for edge in edges:
        if edge['source_node_id'] == node_id:
            series_data = StreamDataList(edge['id'])
            streamlist.append(series_data)

    stream = reduce(add, streamlist) 
    return stream.to_dict() 

def get_series_data_by_target_node(node_id):
    data = get_node_data(node_id)
    edges_ids = data["edge_ids"]
    edges = get_edges_data(edges_ids)
    
    streamlist = []

    for edge in edges:
        if edge['target_node_id'] == node_id:
            series_data = StreamDataList(edge['id'])
            streamlist.append(series_data)

    stream = reduce(add, streamlist) 
    return stream.to_dict() 