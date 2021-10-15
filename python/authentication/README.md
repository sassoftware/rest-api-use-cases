# Authentication

## Overview

The entire SAS Viya authentication process is detailed in the [SAS Viya REST API documentation](https://developer.sas.com/apis/rest/).

In order to connect to SAS Viya via REST APIs you must have an access token. There are two artifacts in this repository for generating an access token. The **authorization** script registers a client (a one-time process) and generates an access token. The **get-access-token** script assumes you have a registered client and only generates the access token. This collection uses the password grant_type, which is not recommended for a production environment. For more information about client registration and access token generation, [please see the official SAS documentation on developer.sas.com](https://developer.sas.com/apis/rest/#getting-started).

## Prerequisites

- The first step in the collection requires the client (Consul) token value. Get the token from the SAS Viya server using the following instruction:
  - In SAS Viya 3.5: cat /opt/sas/viya/config/etc/SASSecurityCertificateFramework/tokens/consul/default/client.token
  - In SAS Viya: kubectl -n sse get secret sas-consul-client -o jsonpath="{.data.CONSUL_TOKEN}" | echo "$(base64 -d)"

Use the value returned for the client_token variable below.

#### Variables to Assign:

- sasserver - the SAS Viya server URL, e.g., https://myserver.sas.com
- client_token - consul token from above
- username - your_viya_user
- password - your_viya_password
- client_id	- client to register, e.g., python_c
- client_secret	- client secret for registered client, e.g., python_s


### Packages and Python Version

- python 3.7+
- requests, json, base64

## Usage

1. Download the Python program or the Jupyter Notebook file.
2. Get the consul token contents.
3. Edit your variables to match your environment.
4. Proceed to run the program or Notebook commands.

## Endpoints Used

- [/SASLogon/oauth/clients/consul](https://developer.sas.com/apis/rest/CoreServices/#obtain-an-access-token-to-create-a-client) - get client token
- [/SASLogon/oauth/clients](https://developer.sas.com/apis/rest/CoreServices/#create-client) - register client
- [/SASLogon/oauth/token](https://developer.sas.com/apis/rest/CoreServices/#grant-access-using-password) - obtain access token
