## Automated Machine Learning with SAS Viya MLPA API

# The goal of this guide is to show how to use SAS Viya's Machine Learning Pipeline Automation(MLPA) API to perform the end-to-end machine learning process i.e starting with a tabular data set and ending with a deployed machine learning model in production. 

# The hmeq data set is used in this case and can be downloaded from https://support.sas.com/documentation/onlinedoc/viya/exampledatasets/heart.csv.
 
# This model trained on this data set will be used to predict if a given individua is likely to default on a home equity loan.

# The target for this prediction task is the BAD variable that stands for Binary Applicant Default taking a value of 0 or 1. Hence MLPA will perform the end-to-end process of analytical data prep, feature engineering, model selection, hyperparameter optimization and model deployment. 

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

import requests, json, uuid, time

sasserver            = ""
datasetName          = "HMEQ"
target               = "BAD"
publicUri            = "/dataTables/dataSources/cas~fs~cas-shared-default~fs~Public/tables/"
# access_token       = ""

# Create a unique project name by append uuid to data set name. 

projectName = datasetName + "-" + str(uuid.uuid4())

## Create an Automated Machine Learning Project
# Create MLPA project with a REST request. You can see project parameters printed below. Please note that there is no need to inspect these values in practice. This is for demonstration purposes only.

tokenUri = "/mlPipelineAutomation/projects"

headers = {
    'Authorization': 'Bearer ' + access_token,
    'Accept': "application/vnd.sas.analytics.ml.pipeline.automation.project+json",
    'Content-Type': "application/json"
}

payload = {
    'dataTableUri': publicUri + datasetName,
    'type': 'predictive',
    'name': projectName,
    'description': 'Project generated for test',
    'settings': {
        'autoRun': True,
        'maxModelingTime': 15
    },
    'analyticsProjectAttributes': {
        'targetVariable': target
    }
}

payload_data = json.dumps(payload, indent=4)

response = requests.request("POST", sasserver + tokenUri, data=payload_data, headers=headers, verify=False)

response_txt = response.text

if response.status_code >= 400:
    print("Error in execute Rest Call with status_code: " + str(response.status_code))
    print(response_txt)

mlpaProject = json.loads(response_txt)
print(mlpaProject)

mlpa_proj_id = mlpaProject["id"]
print(mlpa_proj_id)


# Poll every 20 seconds until MLPA project state is completed

projectStateLink = list(filter(lambda x: x["rel"] == "state", mlpaProject["links"]))[0]
headers = {
    'Authorization': 'Bearer ' + access_token,
    'Accept': projectStateLink["type"]
}

attempts = 0

maxAttempts = 60*60/20

while True:
    attempts = attempts + 1
    projectState = requests.request(projectStateLink["method"], sasserver + projectStateLink["uri"], headers=headers, verify=False).text
    print("Polling project state: Attempt " + str(attempts) + ", state is " + projectState)
    if projectState == "completed" or projectState == "failed" or attempts > maxAttempts:
        break;
    time.sleep(20)

print("Final MLPA project state is " + projectState + ', polled for approx ' + str(attempts*20/60) + ' minutes')


# As an optional post processing step, you can print settings and attributes of newly created MLPA project.

for key, val in mlpaProject['settings'].items():
    print(key + '=' + str(val))
for key, val in mlpaProject['analyticsProjectAttributes'].items():
   print(key + '=' + str(val))

## Get Champion Model
# Get the champion model i.e. the model that performs best based on the default performance criterion for this type of machine learning problem 

tokenUri = "/mlPipelineAutomation/projects/" + mlpaProject["id"] + "/championModel"

headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-type': "application/vnd.sas.analytics.ml.pipeline.automation.project.champion.model+json"
}

fullResponse=False

response = requests.request('GET', sasserver + tokenUri, json=[], headers=headers, verify=False)

response_txt = response.text

if response.status_code >= 400:
    print("Error in executing Rest Call with status_code: " + str(response.status_code))
    print(response_txt)

if fullResponse:
    response,champModel =  response, json.loads(response_txt)
else:
    champModel = json.loads(response_txt)

print('Champion model is ' + champModel['championModelName'])

## Model Deployment and Scoring
# Publish champion model to MAS (maslocal destination). Please note that you should have licensed the Model Manager product to utilize this end point. Otherwise, you could score new data either as individual instances or batch in CAS

headers = {
    'authorization': 'Bearer ' + access_token
}

publishChampModelResponse = requests.request(
    "PUT",
    sasserver + tokenUri + "/" + "?action=publish&destinationName=maslocal",
    json=[],
    headers=headers)

print(publishChampModelResponse)

if publishChampModelResponse.status_code == 200:
    print("Publishing champion model to MAS (maslocal destination) successful")
else:
    print("Error in publish champion model call, status_code: " + str(publishChampModelResponse.status_code))
    print(publishChampModelResponse.text)

# Once the model deployment is complete, just test the deployment with new data as shown below. The result of the scoring process is printed below

scoreDatalLink = list(filter(lambda x: x["rel"] == 'scoreData', champModel["links"]))[0]
headers = {
    'authorization': 'Bearer ' + access_token,
    'Content-type': scoreDatalLink["type"] + "+json"
}
scoreRow = {
    "scoreType": "Individual",
    "destinationName" : "maslocal",
    "inputs": [
        {"name": "CLAGE", "value": 300},
        {"name": "CLNO", "value": 21},
        {"name": "DEBTINC", "value": 24.5},
        {"name": "DELINQ", "value": 0},
        {"name": "DEROG", "value": 1},
        {"name": "JOB", "value": "Other"},
        {"name": "REASON", "value": "DebtCon"},
        {"name": "LOAN", "value": 21500},
        {"name": "MORTDUE", "value": 7806},
        {"name": "NINQ", "value": 4},
        {"name": "VALUE", "value": 95678},
        {"name": "YOJ", "value": 4}
    ]
}

response = requests.request(scoreDatalLink["method"], sasserver + scoreDatalLink["uri"], json=scoreRow, headers=headers)
response_txt = response.text
fullResponse=False

if response.status_code >= 400:
    print("Error in executing rest call with status_code: " + str(response.status_code))
    print(response_txt)

if fullResponse:
    fullResponse, scoredData =  response, json.loads(response_txt)
else:
    scoredData =  json.loads(response_txt)

for itm in scoredData["outputs"]:
    if "value" in itm:
        print(itm["name"] + ": " + str(itm["value"]))
