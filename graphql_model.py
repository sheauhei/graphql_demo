from ariadne import gql, QueryType, MutationType, make_executable_schema
from utils import read_file, read_json

# Define type definitions (schema) using SDL
type_defs = gql(read_file("schema.graphql"))

# Initialize query
query = QueryType()

# data model
places = read_json("data/sample.json")
# places resolver (return places )
@query.field("places")
def resolver_places(*_):
   return places

def build_schema():
    return make_executable_schema(type_defs, [query,])
