from ariadne import gql, QueryType, MutationType, make_executable_schema, load_schema_from_path
from utils import read_json
import os

# Define type definitions (schema) using SDL
type_defs = load_schema_from_path("schema.graphql")

# Initialize query
query = QueryType()

@query.field("node")
def resolve_query_node(obj, info, id):
    node = Node(id) 
    data = data = node.to_dict()
    return data 

@query.field("nodes")
def resolve_query_node(*_):
    # enum all ids.
    ids = []
    for root, dirs, files in os.walk("data/nodes"):
        for fn in files: 
            ids.append(fn.split(".")[0])
    
    # get all data from node ids
    data = []
    for id in ids:
        node = Node(id)
        data.append(node.to_dict())
    
    return data

# # data model
# places = read_json("data/sample.json")
# # places resolver (return places )
# @query.field("places")
# def resolver_places(*_):
#    return places

class Node():
    def __init__(self, id):
        data = read_json(f"data/nodes/{id}.json")
        self._data = data
        self._id = data.get("id")
        self._name = data.get("name")
        self._type = data.get("type")
        self._latitude = data.get("latitude")
        self._longitude = data.get("longitude")
        self._capacityv = data.get("capacity")
        self._edges = data.get("edges")

    def to_dict(self):
        return self._data
        
def build_schema():
    return make_executable_schema(type_defs, [query,])
