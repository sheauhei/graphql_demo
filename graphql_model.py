from graphene import ObjectType, String, Schema, Float, Field, List
from data_model import get_all_edges_data, get_all_nodes_data, get_node_data, get_edge_data, get_nodes_data, get_edges_data

class NodeType(ObjectType):
    id = String()
    name = String()
    type = String()
    latitude = Float()
    longitude = Float()
    capacity = Float() 
    edge_ids = List(String)
    edges = List(lambda: EdgeType)

    def resolve_edges(parent, info):
        edge_ids = parent.get("edge_ids")
        return get_edges_data(edge_ids)

class EdgeType(ObjectType):
    id = String()
    price = Float()
    sell_channel = String()
    
    source_node_id = String()
    target_node_id = String() 

    source = Field(NodeType)
    target = Field(NodeType)

    def resolve_source(parent, info):
        id = parent.get("source_node_id")
        return get_node_data(id)

    def resolve_target(parent, info):
        id = parent.get("target_node_id")
        return get_node_data(id)

class Query(ObjectType):
    node = Field(NodeType, id=String(required=True))
    nodes = List(NodeType)
    edge = Field(EdgeType, id=String(required=True))
    edges = List(EdgeType)

    def resolve_node(parent, info, id):
        return get_node_data(id)

    def resolve_nodes(parent, info):
        data =  get_all_nodes_data()
        return data

    def resolve_edge(parent, info, id):
        return get_edge_data(id)

    def resolve_edges(parent, info):
        return get_all_edges_data()

schema = Schema(query=Query)
