import jwt
import datetime

# Secret key to sign the JWT
secret_key = "your_secret_key"

# Payload data
payload = {
    "sub": "user_id",  # Subject (usually the user ID)
    "name": "John Doe",
    "iat": datetime.datetime.utcnow(),  # Issued at
    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)  # Expiration time (1 hour from now)
}

# Generate the JWT token
token = jwt.encode(payload, secret_key, algorithm="HS256")

print("Generated JWT Token:")
print(token)

try:
    decode = jwt.decode(token, secret_key, algorithms=["HS256"])
    print(decode["name"])
except jwt.ExpiredSignatureError:
    # Signature has expired
    print("JWT expired")
