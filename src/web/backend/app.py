import requests
from chalice import Chalice, Response, CORSConfig
from ariadne import make_executable_schema, load_schema_from_path, graphql_sync, format_error
from chalicelib.resolvers import get_resolvers
import logging

from chalicelib.secrets_helper import get_secret

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

@app.route('/login-callback', methods=['GET'])
def callback():
    logging.info(f"Request: {app.current_request.to_dict()}")

    code = app.current_request.query_params.get('code')
    redirect_uri = "https://d27hv4mf8axlyg.cloudfront.net/api/login-callback"
    token_url = "https://accounts.spotify.com/api/token"

    secret_name = "spotify-workouts"
    region_name = "us-west-2"
    secret_values = get_secret(secret_name, region_name)

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": secret_values['SPOTIFY_OAUTH_CLIENT_ID'],
        "client_secret": secret_values['SPOTIFY_OAUTH_CLIENT_SECRET']
    }

    response = requests.post(token_url, data=payload)
    access_token = response.json().get("access_token")

    # Set the cookie and redirect
    headers = {
        'Location': 'https://d27hv4mf8axlyg.cloudfront.net/',
        'Set-Cookie': f'token={access_token}; Path=/; HttpOnly; Secure'
    }
    return Response(body='', status_code=302, headers=headers)
