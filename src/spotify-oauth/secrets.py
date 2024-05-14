import boto3
import json
from botocore.exceptions import ClientError


def get_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        # Attempt to get the secret value
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # Handle the exception based on the error code
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            raise e
        else:
            # Handle any other exceptions
            raise e
    else:
        # Decrypts secret using the associated KMS key
        if 'SecretString' in response:
            secret = response['SecretString']
            return json.loads(secret)
        else:
            # In case the secret is using binary data and not a string
            binary_data = response['SecretBinary']
            return json.loads(binary_data.decode('utf-8'))


# Usage
if __name__ == "__main__":
    secret_name = "spotify-workouts"
    region_name = "us-west-2"

    secret_values = get_secret(secret_name, region_name)
    print("Client ID:", secret_values['SPOTIFY_OAUTH_CLIENT_ID'])
    print("Client Secret:", secret_values['SPOTIFY_OAUTH_CLIENT_SECRET'])
