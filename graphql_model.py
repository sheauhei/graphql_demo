from graphene import ObjectType, String, Schema, Float, Field, List
from data_model import dummy_db



class EdgeType(ObjectType):
    id = String()
    price = Float()
    sell_channel = String()
    source: Field(NodeType)
    target: Field(NodeType)

class NodeType(ObjectType):
    id = String()
    name = String()
    type = String()
    latitude = Float()
    longitude = Float()
    capacity = Float() 
    edges = List(EdgeType)

    def resolve_edges(parent, info):
        edge_ids = parent.get("edge_ids")
        edges = dummy_db.get_edges(edge_ids)
        data = [edge.to_dict() for edge in edges]
        return data

class Query(ObjectType):
    node = Field(NodeType, id=String(required=True))

    def resolve_node(parent, info, id):
        node = dummy_db.get_node(id)
        return node.to_dict()

schema = Schema(query=Query)
