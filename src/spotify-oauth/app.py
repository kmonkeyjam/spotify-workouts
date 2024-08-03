from chalice import Chalice, Response
import requests
from chalicelib.secrets_helper import get_secret

app = Chalice(app_name='spotify-workouts-oauth')
app.api.binary_types.append('*/*')

@app.route('/callback', methods=['GET'], cors=True)
def callback():
    code = app.current_request.query_params.get('code')
    redirect_uri = "https://8fowcc6ppc.execute-api.us-west-2.amazonaws.com/api/callback"
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

    return Response(body={'Access Token': access_token},
                    status_code=200,
                    headers={'Content-Type': 'application/json'})

@app.route('/login', methods=['GET'], cors=True)
def login():
    secret_name = "spotify-workouts"
    region_name = "us-west-2"
    secret_values = get_secret(secret_name, region_name)
    print("Client Secret:", secret_values['SPOTIFY_OAUTH_CLIENT_SECRET'])

    client_id = secret_values['SPOTIFY_OAUTH_CLIENT_ID']
    scope = "user-read-private"
    redirect_uri = "https://8fowcc6ppc.execute-api.us-west-2.amazonaws.com/api/callback"

    return Response(body={'Login URL': f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}"},
                    status_code=302,
                    headers={'Content-Type': 'application/json'})

