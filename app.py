from ariadne.constants import PLAYGROUND_HTML
from ariadne import graphql_sync
from flask import Flask, request, jsonify

from graphql_model import build_schema

# initialize flask app
app = Flask(__name__)

# Create a GraphQL Playground UI for the GraphQL schema
@app.route("/graphql", methods=["GET"])
def graphql_playground():
   return PLAYGROUND_HTML

# Create a GraphQL endpoint for executing GraphQL queries
@app.route("/graphql", methods=["POST"])
def graphql_server():
   data = request.get_json()
   schema = build_schema()
   success, result = graphql_sync(schema, data, context_value={"request": request})
   status_code = 200 if success else 400
   return jsonify(result), status_code

# Run the app
if __name__ == "__main__":
   app.run(debug=True)