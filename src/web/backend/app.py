from chalice import Chalice, Response, CORSConfig
from graphene import ObjectType, String, Boolean, Schema
import jwt

app = Chalice(app_name='spotify-workouts-web')

# CORS configuration to allow requests from any domain
cors_config = CORSConfig(allow_origin='*', allow_headers=['Authorization', 'Content-Type'],
    expose_headers=['Authorization'], max_age=600, allow_credentials=False)

# Dummy secret for JWT (use your actual secret)
JWT_SECRET = 'your-secret'


# Define your GraphQL schema
class Query(ObjectType):
    is_logged_in = Boolean(token=String(required=True))

    def resolve_is_logged_in(self, info, token):
        try:
            # Decode the token to verify it's valid
            jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False


schema = Schema(query=Query)


@app.route('/graphql', methods=['POST'], content_types=['application/json'], cors=cors_config)
def graphql_endpoint():
    request = app.current_request
    data = request.json_body

    # Extract the token from the Authorization header
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return Response(status_code=401, body={'error': 'Unauthorized'})

    token = auth_header.split(' ')[1]  # Extract the token after 'Bearer '

    # Add the token to the variables if not already present
    if 'variables' not in data:
        data['variables'] = {}

    data['variables']['token'] = token

    # Execute the GraphQL query with the provided schema
    result = schema.execute(data['query'], variables=data['variables'])

    if result.errors:
        return Response(status_code=400, body={'errors': [str(e) for e in result.errors]})

    return {'data': result.data}
