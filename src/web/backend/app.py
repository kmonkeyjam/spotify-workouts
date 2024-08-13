from chalice import Chalice, Response, CORSConfig
from ariadne import make_executable_schema, load_schema_from_path, graphql_sync
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

@app.route('/graphql', methods=['POST'], content_types=['application/json'], cors=cors_config)
def graphql_endpoint():
    request = app.current_request
    data = request.json_body

    # Extract the token from the Authorization header
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer'):
        logger.debug("Auth Header: {}".format(auth_header))
        return Response(status_code=401, body={'error': 'Unauthorized'})

    if auth_header != 'Bearer':
        token = auth_header.split(' ')[1]  # Extract the token after 'Bearer '

        # Add the token to the variables if not already present
        if 'variables' not in data:
            data['variables'] = {}

        data['variables']['token'] = token
    else:
        # Kinda a hack b/c i don't feel like refactoring
        data['variables']['token'] = "UNAUTHENTICATED"

    errors, result = graphql_sync(
        schema,data
    )

    if errors:
        return Response(status_code=400, body={'errors': [str(e) for e in errors]})

    return {'data': result}
