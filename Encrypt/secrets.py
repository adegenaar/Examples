import os
import json
import boto3
from botocore.exceptions import ClientError
class SecretsGateway:
    def get_secrets(self) -> dict:
        return self.from_json() or self.from_aws('<secrets-name>')
    def from_json(self) -> dict:
        filename = os.path.join('secrets.json')
        try:
            with open(filename, mode='r') as f:
                return json.loads(f.read())
        except FileNotFoundError:
            return {}
    def from_aws(self, secret_name: str) -> dict:
        region_name = os.environ['AWS_REGION']
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)
        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            print(e.response['Error']['Code'])
            return {}
        else:
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
                secret = json.loads(secret)
                return secret
secrets_gateway = SecretsGateway()
secrets = secrets_gateway.get_secrets()