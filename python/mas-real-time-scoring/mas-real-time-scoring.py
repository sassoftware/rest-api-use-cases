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
import pandas as pd

# Variables to assign
host = ""
oauthToken = ""
csv_data = "hmeq_test.csv"

def get_modules(host, oauthToken):
    
    url = host + "/microanalyticScore/modules/"

    headers = {
        'Accept': "application/vnd.sas.collection+json",
        'Authorization': "Bearer " + oauthToken
    }
    
    response = requests.request('GET', url, headers=headers, verify=False).json()
    print("The folliing is a list of modules: ")
    for i in response['items']:
        print(i['name'])

def get_params(host, oauthToken, model_id):
    
    url =  host + "/microanalyticScore/modules/" + model_id + '/steps'
    headers = {
        'Accept': "application/vnd.sas.collection+json",
        'Authorization': "Bearer " + oauthToken
    }
    response = requests.request('GET', url, headers=headers, verify=False)
    
    # Retrieve the inputs and outpus from the last element of the 'items' json object 
    return(json.loads(response.text)['items'][-1])


def format_data(csv_data):
    
    data = pd.read_csv(csv_data)
    
    # Convert test data colums to lowercase to match MAS input parameter names 
    data.columns = map(str.lower, data.columns)
    
    # Fill empty values with 0 
    data = data.fillna(0)
    return(data)
    

def score_in_batch(host, oauthToken, model_id, data, params):

    inputs = params['inputs']
# To execute a decision, use the /steps/execute endpoint. For models use the /steps/score endpoint.
    url =  host + "/microanalyticScore/modules/" + model_id + '/steps/score'
    headers = {
        'Authorization': "Bearer " + oauthToken,
        'Content-Type': "application/vnd.sas.microanalytic.module.step.input+json" 
    }

    # Retrieve values column values from file and dynamically build payload
    for i in range(len(data)): 
        row = data.iloc[i]
        payload = '{"inputs":[ ' 
        for i in range(len(inputs)):
            payload += '{ "name": ' 
            payload += '"' + inputs[i]['name']  + '"'
            payload += ', "value": '
            
            # Check if value input is decimal or character
            if inputs[i]['type'] == 'decimal':
                
                # Add underscore to column names to match MAS parameter format
                payload += str(row[(inputs[i]['name']).replace('_','')])
                
            # Add quotation marks around character input values
            else: 
                # Add underscore to column names to match MAS parameter format
                payload += '"' + str(row[(inputs[i]['name']).replace('_','')])+ '"'
            if i != (len(inputs) -1):
                payload += "},"
            else: 
                payload += "}"
        payload += "] }"

        # Send Request to MAS 
        r = requests.request("POST", url, data = payload, headers = headers, verify=False)
        
        # Print Formatted Request 
        formatted_response = json.dumps(r.json(), indent=2)
        print(formatted_response)
        
      
get_modules(host, oauthToken)
model_id = input("Enter the module name you wish to score from the list above: ")
params = get_params(host, oauthToken, model_id)
formatted_data = format_data(csv_data)
score_in_batch(host, oauthToken, model_id, formatted_data, params)