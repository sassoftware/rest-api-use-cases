# Authentication

## Overview

The entire SAS Viya authentication process is detailed in the [SAS Viya REST API documentation](https://developer.sas.com/apis/rest/).

This example gets the client token, registers a client, and generates the access token. Client registration is a one-time process, hence, run the first two steps once. You can then generate the access token as needed using the third test in the collection. Note: the same third step is added to each use case as test 0.

This collection uses the password grant_type, which is not recommended for a production environment. For more information about client registration and access token generation, [please see the official SAS documentation on developer.sas.com](https://developer.sas.com/apis/rest/#getting-started).

## Prerequisites

- The first step in the collection requires the client (Consul) token value. Get the token from the SAS Viya server using the following instruction:
  - In SAS Viya 3.5: cat /opt/sas/viya/config/etc/SASSecurityCertificateFramework/tokens/consul/default/client.token
  - In SAS Viya: kubectl -n sse get secret sas-consul-client -o jsonpath="{.data.CONSUL_TOKEN}" | echo "$(base64 -d)"

Take the Consul token and create the client_token variable in Postman. Add the X-Consul-Token parameter in the header, using the client_token variable.

#### Variables to assign:

- sasserver - the SAS Viya server URL, e.g., https://myserver.sas.com
- client_token - consul token from above
- username - your_viya_user
- password - your_viya_password
- client_id	- client to register, e.g., postman_c
- client_secret	- client secret for registered client, e.g., postman_s

## Usage

1. Download the JSON object and import the file into Postman as a collection.
2. Get the consul token contents.
3. Edit your variables to match your environment.
4. Proceed to run the program or Notebook commands.


## Endpoints Used

- [/SASLogon/oauth/clients/consul](https://developer.sas.com/apis/rest/CoreServices/#obtain-an-access-token-to-create-a-client) - authenticate with a Consul token, to obtain an OAuth access token, for registering a new client 
- [/SASLogon/oauth/clients](https://developer.sas.com/apis/rest/CoreServices/#create-client) - create(register) a new client
- [/SASLogon/oauth/token](https://developer.sas.com/apis/rest/CoreServices/#grant-access-using-password) - create an access token using the password grant_type