from chalice import Chalice, Response
import requests

app = Chalice(app_name='spotify-oauth')
app.api.binary_types.append('*/*')

@app.route('/callback', methods=['GET'], cors=True)
def callback():
    code = app.current_request.query_params.get('code')
    redirect_uri = "https://your-api-id.execute-api.region.amazonaws.com/Prod/callback"
    token_url = "https://accounts.spotify.com/api/token"
    
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": "your-client-id",
        "client_secret": "your-client-secret"
    }

    response = requests.post(token_url, data=payload)
    access_token = response.json().get("access_token")

    return Response(body={'Access Token': access_token},
                    status_code=200,
                    headers={'Content-Type': 'application/json'})

@app.route('/login', methods=['GET'], cors=True)
def login():
    client_id = "your-client-id"
    scope = "user-read-private"
    redirect_uri = "https://your-api-id.execute-api.region.amazonaws.com/Prod/callback"

    return Response(body={'Login URL': f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}"},
                    status_code=302,
                    headers={'Content-Type': 'application/json'})

