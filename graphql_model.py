from graphene import ObjectType, String, Schema, Float, Field, List, DateTime
from data_model import get_all_edges_data, get_all_nodes_data, get_node_data, get_edge_data, get_nodes_data, get_edges_data, get_series_data_by_edge, get_series_data_by_source_node, get_series_data_by_target_node

class NodeType(ObjectType):
    id = String()
    name = String()
    type = String()
    latitude = Float()
    longitude = Float()
    capacity = Float() 
    edge_ids = List(String)
    edges = List(lambda: EdgeType)

    in_time_series = List(lambda: StreamDataType)
    out_time_series = List(lambda: StreamDataType)

    def resolve_edges(parent, info):
        edge_ids = parent.get("edge_ids")
        return get_edges_data(edge_ids)

    def resolve_in_time_series(parent, info): 
        id = parent.get("id")
        return get_series_data_by_target_node(id)

    def resolve_out_time_series(parent, info): 
        id = parent.get("id")
        return get_series_data_by_source_node(id)

class EdgeType(ObjectType):
    id = String()
    price = Float()
    sell_channel = String()
    
    source_node_id = String()
    target_node_id = String() 

    source = Field(NodeType)
    target = Field(NodeType)

    time_series = List(lambda: StreamDataType)

    def resolve_source(parent, info):
        id = parent.get("source_node_id")
        return get_node_data(id)

    def resolve_target(parent, info):
        id = parent.get("target_node_id")
        return get_node_data(id)

    def resolve_time_series(parent, info): 
        return get_series_data_by_edge(parent.get("id"))
    

class StreamDataType(ObjectType):
    timestamp = DateTime()
    power = Float() 
    energy = Float() 
    predicted_power = Float()
    predicted_energy = Float()
    price = Float() 
    revenue = Float() 
    

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
