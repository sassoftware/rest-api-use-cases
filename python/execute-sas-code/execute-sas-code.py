## Execute SAS Code

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

import requests as request
import json
import time

sasserver = ""
access_token = ""
job_url = ""# sample job_url for a Job titled Simple proc print: https://mysasserver.sas.com/SASJobExecution/?_program=/Public/API%20Job%20Exec%20Python/Simple%20proc%20print

# Submit job
url = job_url + '&_action=json&_resultfile=*&_omittextlog=false'

headers = {
    'Authorization': 'bearer ' + access_token,
    'Content-Type': 'application/vnd.sas.job.execution.job.request',
    'Accept': 'application/vnd.sas.job.execution.job'
}

r = request.post(url, headers=headers, verify=False).json()
print(r)

# Construct url to retrieve log and output table

log_uri = sasserver + r['items'][1]['href']
output_uri = sasserver + r['items'][2]['href']

# Generate log file

log_str = request.get(log_uri, headers=headers, verify=False).text

filename = "Log_"+time.strftime("%Y%m%d-%H%M%S")+".txt"

with open(filename, "w") as log:
    log.write(log_str)

# print(log_str) # optional print statement, if you'd like to see the content of the log file

# Generate output table(s) file

output_str = request.get(output_uri, headers=headers, verify=False).text

filename = "Output_"+time.strftime("%Y%m%d-%H%M%S")+".html"

with open(filename, "w") as output_html:
    output_html.write(output_str)

# print(output_str) # optional print statement, if you'd like to see the content of the output file