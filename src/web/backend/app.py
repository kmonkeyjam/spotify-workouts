from chalice import Chalice, Response, CORSConfig
from ariadne import make_executable_schema, load_schema_from_path, graphql_sync, format_error
from chalicelib.resolvers import get_resolvers
import logging

# Configure the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Chalice(app_name='spotify-workouts-web')

# CORS configuration to allow requests from any domain
cors_config = CORSConfig(allow_origin='*', allow_headers=['Authorization', 'Content-Type'],
    expose_headers=['Authorization'], max_age=600, allow_credentials=False)

type_defs = load_schema_from_path("chalicelib/schema.graphql")

schema = make_executable_schema(type_defs, *get_resolvers())

def custom_error_formatter(error, debug=False):
    formatted_error = format_error(error, debug)
    return formatted_error

@app.route('/graphql', methods=['POST'], content_types=['application/json'], cors=cors_config)
def graphql_endpoint():
    request = app.current_request
    data = request.json_body
    success, result = graphql_sync(
        schema,data, error_formatter=custom_error_formatter
    )

    if not success:
        return Response(status_code=400, body={'errors': result.get("errors", [])})

    return result
