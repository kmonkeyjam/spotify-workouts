from chalice import Chalice, Response, CORSConfig
from ariadne import make_executable_schema, load_schema_from_path, graphql_sync, format_error
from chalicelib.resolvers import get_resolvers
import logging

# Configure the logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = Chalice(app_name='spotify-workouts-web')

# CORS configuration to allow requests from any domain
cors_config = CORSConfig(allow_origin='*', allow_headers=['Authorization', 'Content-Type'],
    expose_headers=['Authorization'], max_age=600, allow_credentials=False)

type_defs = load_schema_from_path("chalicelib/schema.graphql")

schema = make_executable_schema(type_defs, *get_resolvers())

def custom_error_formatter(error, debug=False):
    # Log the error or print it out for debugging purposes
    logger.error("GraphQL Error:", error.message)
    if error.original_error:
        logger.error("Original Error:", str(error.original_error))

    # You can also log other error details if needed
    logger.error("Path:", error.path)
    logger.error("Locations:", error.locations)

    # Format the error for the response
    formatted_error = format_error(error, debug)
    return formatted_error


@app.route('/graphql', methods=['POST'], content_types=['application/json'], cors=cors_config)
def graphql_endpoint():
    request = app.current_request
    data = request.json_body
    errors, result = graphql_sync(
        schema,data, error_formatter=custom_error_formatter
    )

    if errors:
        return Response(status_code=400, body={'result': result.get("errors", [])})

    return {'data': result}
