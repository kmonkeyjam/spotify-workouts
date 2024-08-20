# resolvers.py
import jwt
from ariadne import QueryType, MutationType

query = QueryType()
mutation = MutationType()

# Dummy secret for JWT (use your actual secret)
JWT_SECRET = 'your-secret'
LOGIN_URL = 'https://your-login-url.com'  # Replace with your actual login URL

@query.field("login_status")
def resolve_login_status(_, info, token):
    try:
        decode = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return {
            "is_logged_in": True,
            "name": decode["name"]
        }
    except jwt.ExpiredSignatureError:
        return {"is_logged_in": False, "login_url": LOGIN_URL}
    except jwt.InvalidTokenError:
        return {"is_logged_in": False, "login_url": LOGIN_URL}

def get_resolvers():
    return [query]
