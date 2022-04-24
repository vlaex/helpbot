import os
from python_graphql_client import GraphqlClient

client = GraphqlClient(os.environ['GRAPHQL_ENDPOINT_URL'])
