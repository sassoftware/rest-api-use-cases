## Get Access Token
# If you have previously registered a client using the authentication use case, use this script to create an access token.

import requests
import json
import base64

# Global variables
sasserver = ""
username = ""
password = ""
client_id = ""
client_secret = ""

## Get final token for further calls

url = sasserver + "/SASLogon/oauth/token"

data = {
    'grant_type': 'password',
    'username': username,
    'password': password
}

headers = {'Accept': 'application/json'}

response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret), verify=False).json()

access_token = response["access_token"]

print("The access token is: " + access_token)