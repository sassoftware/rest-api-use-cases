
# Run SAS Job and Retrieve Log and Output

## Overview

This example executes an existing Job (and thus, the SAS code within the Job) and get its outputs (HTML output and Log).

## Pre-requisites:

- Refer to the [Authentication Project](../authentication) project in order to get an access token.
- This use case assumes you have created a Job in SAS Viya. [Refer to the documentation for detailed steps](https://go.documentation.sas.com/doc/en/pgmsascdc/9.4_3.4/jobexecug/p1gukmrin5zv1mn1rvb6afi57b88.htm).


#### Variables to assign:

- sasserver - the SAS Viya server URL 
- access_token - get from the authentication project
- job_url - the URL for the job that you want to execute - found in the Job Submit parameter, in the property details, from the JobExecution UI, e.g., https://mysasserver.sas.com/SASJobExecution
  - sample job_url for a Job titled Simple PROC print: https://mysasserver.sas.com/SASJobExecution/?_program=/Public/API%20Job%20Exec%20Python/Simple%20proc%20print

Other variables are assigned programmatically during the REST calls.

### Packages and Python Version

- Python 3.7+
- requests, json, time

## Usage

1. Download the Python program or the Jupyter Notebook file.
2. Edit your variables to match your environment.
3. Proceed to run the program or Notebook commands.
    
## Endpoints 

Specifying the Job URL in this use case, procedurally calls the */jobs* API .
- [/jobExecution/jobs](https://developer.sas.com/apis/rest/Compute/#submit-a-job-request) - submit a job request
