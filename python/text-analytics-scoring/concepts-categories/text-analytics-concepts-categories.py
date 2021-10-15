# Text Analytics Concepts and Categories

# If you have registered a client (see the authentication use case), uncomment the code below to generate an access token.

# import requests, json, base64
# sasserver = ""
# username = ""
# password = ""
# client_id = ""
# client_secret = ""
# url = sasserver + "/SASLogon/oauth/token"
# data = {
#     'grant_type': 'password',
#     'username': username,
#     'password': password
# }
# headers = {'Accept': 'application/json'}
# response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret), verify=False).json()
# access_token = response["access_token"]
# print("The access token is: " + access_token)

## Import modules, variable assignment
# The first step of the process is to import the required packages and assign variable values.

import requests
import json

## Variables to assign

sasserver = ""
tableToScore = ""
modelCaslib = "" # example value Analytics_Project_23f163ba-474d-4c3f-864c-4f8f6474bf85
modelConceptsTable = "" # example value 8ae8d5be7bfe2eec017c04c43f8c0000_CONCEPT_BINARY
modelCategoriesTable = "" # example value 8ae8d5be7bfe2eec017c04c451190000_CATEGORY_BINARY
access_token = "" # Get from the authentication project

## Create session to start making calls

def getSession(access_token, sasserver):

   headers_sesh = {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + access_token }

   url = sasserver + '/cas-shared-default-http/cas/sessions'

   try:
      r = requests.post(url, headers=headers_sesh, verify=False).json()
      return r
   except requests.exceptions.RequestException as e:
      return e


## Run Concept Model

def callConceptModel(sessionId, access_token, sasserver, modelCaslib, modelConceptsTable):
   headers_sesh = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": "Bearer " + access_token }

   url = sasserver + '/cas-shared-default-http/cas/sessions/'+sessionId+'/actions/textRuleScore.applyConcept'

   payload = "{\"model\":{\"caslib\":\""+ modelCaslib +"\", \"name\":\""+ modelConceptsTable +"\"},\r\n\"table\":{\"caslib\":\"public\", \"name\":\"restaurant_reviews\"},\r\n\"docId\":\"Unique_ID\",\r\n\"text\":\"text\",\r\n\"casOut\":{\"caslib\":\"casuser\", \"name\":\"out_concepts\", \"replace\":\"true\"},\r\n\"factOut\":{\"caslib\":\"casuser\", \"name\":\"out_facts\", \"replace\":\"true\"}}"

   try:
      r = requests.post(url, headers=headers_sesh, data=payload, verify=False).json()
      return r
   except requests.exceptions.RequestException as e:
      return e


## Run Categories Model

def callCategoriesModel(sessionId, access_token, sasserver, modelCaslib, modelCategoriesTable):
   headers_sesh = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": "Bearer " + access_token }

   url = sasserver + '/cas-shared-default-http/cas/sessions/'+sessionId+'/actions/textRuleScore.applyCategory'

   payload = "{\"model\":{\"caslib\":\""+ modelCaslib +"\", \"name\":\""+ modelCategoriesTable +"\"},\r\n\"table\":{\"caslib\":\"public\", \"name\":\"restaurant_reviews\"},\r\n\"docId\":\"Unique_ID\",\r\n\"text\":\"text\",\r\n\"casOut\":{\"caslib\":\"casuser\", \"name\":\"out_categories\", \"replace\":\"true\"},\r\n\"matchOut\":{\"caslib\":\"casuser\", \"name\":\"out_match\", \"replace\":\"true\"},\r\n\"modelOut\":{\"caslib\":\"casuser\", \"name\":\"out_model\", \"replace\":\"true\"}}"

   try:
      r = requests.post(url, headers=headers_sesh, data=payload, verify=False).json()
      return r
   except requests.exceptions.RequestException as e:
      return e



## Get the data using the Fetch action

def getData(sasserver, sessionId, access_token, tblName):
   url = sasserver + "/cas-shared-default-http/cas/sessions/" + sessionId + "/actions/table.fetch"

   payload = "{ \"table\": {\"caslib\":\"casuser\", \"name\":\"" + tblName + "\"} }"

   headers = {
      'Authorization': "Bearer " + access_token,
      'Content-Type': 'application/json'
   }

   try:
      response = requests.request("POST", url, headers=headers, data = payload, verify=False).json()
      return(response)
   except requests.exceptions.RequestException as e:
      return e

# Run functions
# Get token
# Use the Authentication project to get the token

# Get Session
sessionId = getSession(access_token, sasserver)
print(sessionId)

# Run Concepts Model
concept_output = callConceptModel(sessionId["session"], access_token, sasserver, modelCaslib, modelConceptsTable)
print(concept_output)

# Get concept  data
concepts_data = getData(sasserver, sessionId["session"], access_token, "OUT_CONCEPTS")["results"]
concept_format = json.dumps(concepts_data, indent=2)
print("The concepts data: " + concept_format)

# Run Categories Model
categories_output = callCategoriesModel(sessionId["session"], access_token, sasserver, modelCaslib, modelCategoriesTable)
print(categories_output)

# Get Categories data
categories_data = getData(sasserver, sessionId["session"], access_token, "out_model")["results"]
categ_format = json.dumps(categories_data, indent=2)
print("The categories data: " + categ_format)