# resolvers.py
from urllib.parse import urlencode

import jwt
from ariadne import QueryType, MutationType
from chalicelib.secrets_helper import get_secret
import logging
import datetime

# Configure the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

query = QueryType()
mutation = MutationType()

# Dummy secret for JWT (use your actual secret)
JWT_SECRET = 'your-secret'
REDIRECT_URI = "https://d27hv4mf8axlyg.cloudfront.net/api/login-callback"


@query.field("login_status")
def resolve_login_status(_, info, token):
    try:
        decode = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return {"is_logged_in": True, "name": "Tina Huang"}
    except jwt.ExpiredSignatureError:
        return {"is_logged_in": False, "login_url": get_login_url()}
    except jwt.InvalidTokenError:
        return {"is_logged_in": False, "login_url": get_login_url()}


def get_login_url():
    secret_name = "spotify-workouts"
    region_name = "us-west-2"
    secret_values = get_secret(secret_name, region_name)
    logger.info("Client Secret:" + secret_values['SPOTIFY_OAUTH_CLIENT_SECRET'])

    client_id = secret_values['SPOTIFY_OAUTH_CLIENT_ID']
    scope = "user-read-private"

    params = {"response_type": "code", "client_id": client_id, "scope": scope, "redirect_uri": REDIRECT_URI}

    url = f"https://accounts.spotify.com/authorize?{urlencode(params)}"
    logger.info("URL: " + url)
    return url

def create_jwt(access_token, user_id, name):
    payload = {
        "sub": user_id,
        "name": name,
        "access_token": access_token,
        "iat": datetime.datetime.utcnow(),  # Issued at
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)  # Expiration time (1 hour from now)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    logger.info("Token: " + token)
    return token


def get_resolvers():
    return [query]
