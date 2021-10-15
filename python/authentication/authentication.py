## Authentication
# The following scripts register a client (one-time process) and generate an access token for use cases in the repository.

# To find the value of the client_token (Consul token) variable:
# In SAS Viya 3.5: cat /opt/sas/viya/config/etc/SASSecurityCertificateFramework/tokens/consul/default/client.token
# In SAS Viya 202x.x:  kubectl -n get secret sas-consul-client -o jsonpath="{.data.CONSUL_TOKEN}" | echo "$(base64 -d)"

import requests
import json
import base64

# Global variables
sasserver = ""
client_token = ""
username = ""
password = ""
client_id = ""
client_secret = ""


#  Get Client Token

url = sasserver+"/SASLogon/oauth/clients/consul?callback=false&serviceId=" + client_id

payload = {}
headers = {
  "X-Consul-Token": client_token
}

response = requests.request("POST", url, headers=headers, data = payload, verify=False).json()

client_access_token = response["access_token"]

print(client_access_token)


#  Register Client

url = sasserver+"/SASLogon/oauth/clients"

payload = {"client_id": client_id, 
           "client_secret": client_secret,
           "scope": ["SASAdministrators", "uaa.admin"], 
           "resource_ids": "none", 
           "authorities": ["uaa.none"], 
           "authorized_grant_types": ["password"],
           "access_token_validity": 36000}

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer ' + client_access_token
}
response = requests.post(url, headers = headers, json = payload, verify=False).json()

print(response)


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
