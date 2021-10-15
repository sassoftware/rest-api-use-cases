## Job Execution

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
import time

# Variables to assign

sasserver = ""
access_token = ""
folder = "Public"

# Get public Folder

url = sasserver+"/folders/folders?filter=eq(name,"+folder+")"

payload={}
headers = {
  'Authorization': 'Bearer ' + access_token
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False).json()

folder_id = response["items"][0]["id"]

print("Public folder id: " + folder_id)


# Create Folder

url = sasserver+"/folders/folders?parentFolderUri=/folders/folders/"+folder_id

payload="{\n  \"name\": \"API Job Exec Python\",\n  \"description\": \"My API tests folder.\",\n  \"type\": \"folder\"\n}"
headers = {
  'Content-Type': 'application/vnd.sas.content.folder+json',
  'Accept': 'application/vnd.sas.content.folder+json',
  'Authorization': 'Bearer ' + access_token
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()

parentFolder = response["id"]

print("New folder ID: " + parentFolder)


# Create Job Definition

url = sasserver+"/jobDefinitions/definitions?parentFolderUri=/folders/folders/"+parentFolder

payload="{\n  \"version\":2,\n  \"name\":\"Simple proc print\",\n  \"description\":\"Show the contents of sashelp.class using PROC PRINT\",\n  \"type\":\"Compute\",\n  \"parameters\":[\n        {\n        \"version\": 1,\n        \"name\": \"_contextName\",\n        \"defaultValue\": \"SAS Job Execution compute context\",\n        \"type\": \"CHARACTER\",\n        \"label\": \"Context Name\",\n        \"required\": false\n    }\n  ],\n  \"code\":\"ods html style=HTMLBlue;\\nproc print data=sashelp.class; run; quit;\\nods html close;\"\n}"
headers = {
  'Authorization': 'Bearer ' + access_token,
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()

jobDef = response["id"]

print("Job definition ID: " + jobDef)


# Get Job Definition - just checking it got created

url = sasserver+"/jobDefinitions/definitions/"+jobDef

payload={}
headers = {
  'Authorization': 'Bearer ' + access_token
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False).json()

defId = response["id"]

print("Verified Job Definition ID: " + defId)


# Submit Job Execution

url = sasserver+"/jobExecution/jobs"

payload={"name": "Hello World Execution",
         "description": "Execution of the job we previously created",
         "jobDefinitionUri": "/jobDefinitions/definitions/" + defId
        }

headers = {
  'Authorization': 'Bearer ' + access_token,
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False).json()

execution_id = response["id"]

print("Job execution ID: " + execution_id)


# Get Job Execution State

url = sasserver+"/jobExecution/jobs/"+execution_id+"/state"
   
payload={}
   
headers = {
  'Authorization': 'Bearer ' + access_token
}
   
attempts = 0
maxAttempts =10
while True:
   response = requests.request("GET", url, headers=headers, data=payload, verify=False)

   attempts = attempts + 1
   print("Polloing Job status " + str(attempts) + ", state is " + response.text)
   if response.text == "completed" or response.text == "failed" or attempts > maxAttempts:
       break;
   time.sleep(5)


# Get Job Execution Files

url = sasserver+"/jobExecution/jobs/"+execution_id

payload={}
headers = {
  'Authorization': 'Bearer ' + access_token
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False).json()

files_location = response["logLocation"]

print("Jobe execution result file location: " + files_location)


# Get Execution Results

url = sasserver+files_location+"/content"

payload={}
headers = {
  'Authorization': 'Bearer ' + access_token
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

print("The results are: " + response.text)