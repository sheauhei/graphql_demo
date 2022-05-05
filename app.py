from flask import Flask
from flask_graphql import GraphQLView
from graphql_model import schema
from graphql.utils import schema_printer

def dump_schema(filename):
   my_schema_str = schema_printer.print_schema(schema)
   with open(filename, "w") as fp:
      fp.write(my_schema_str)

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

    return app

dump_schema("schema.graphql")
app = create_app()
app.run()


# # initialize flask app
# app = Flask(__name__)

# # Create a GraphQL Playground UI for the GraphQL schema
# @app.route("/graphql", methods=["GET"])
# def graphql_playground():
#    return PLAYGROUND_HTML

# # Create a GraphQL endpoint for executing GraphQL queries
# @app.route("/graphql", methods=["POST"])
# def graphql_server():
#    data = request.get_json()
#    schema = build_schema()
#    success, result = graphql_sync(schema, data, context_value={"request": request})
#    status_code = 200 if success else 400
#    return jsonify(result), status_code

# # Run the app
# if __name__ == "__main__":
#    app.run(debug=True)