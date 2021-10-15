# End to End Job Execution

## Overview

This program leverages multiple SAS Viya APIs to create an end-to-end example for Job Execution. It creates a folder, creates and executes a job definition, and returns logs and job output. The example code shows how to print out the contents of the sashelp.class table. Use this simple example to create your own scenario, using your own SAS code.

The use case is presented in two forms:  a Python program and a Jupyter Notebook.


## Prerequisites

Refer to the [Authentication Project](../authentication) project in order to get an access token.

#### Variables to assign:

- sasserver - the SAS Viya server URL 
- access_token - get from the authentication project
- folder - existing folder name where code is saved (a new parent folder is created under this folder to store the code)

Other variables are assigned programmatically during the REST calls. Pay attention to the final call - where we get the output files from the Job Execution API.

### Packages and Python Version

- python 3.7+
- requests, json, time

## Usage

1. Download the Python program or the Jupyter Notebook file.
2. Edit your variables to match your environment.
3. Proceed to run the program or Notebook commands.

## Endpoints Used

- [/folders/folders](https://developer.sas.com/apis/rest/CoreServices/#get-a-list-of-folders) - get a folder by its name
- [/folders/folders](https://developer.sas.com/apis/rest/CoreServices/#create-a-new-folder) - create a subfolder inside the previous folder
- [/jobDefinitions/definitions](https://developer.sas.com/apis/rest/Compute/#create-a-job-definition) - create a Job Definition
- [/jobExecution/jobs](https://developer.sas.com/apis/rest/Compute/#get-a-job-definition) - get Job Definition
- [jobDefinitions/definitions/<job_id>](https://developer.sas.com/apis/rest/Compute/#operations-2) - submit Job for execution
- [/jobExecution/jobs/<execution_id>/state](https://developer.sas.com/apis/rest/Compute/#get-the-state-of-the-job) - get job execution state
- [/jobExecution/jobs/<execution_id>](https://developer.sas.com/apis/rest/Compute/#get-a-job) - get job execution files
- [/<files_location>/content](https://developer.sas.com/apis/rest/Compute/#get-a-job) - get job execution results

## Supported Versions

The table below represents use case testing results. 
| SAS Viya Version | Tested |
| ----------- | ----------- |
| 3.5 | <ul><li>[x] </li> |
| 2021.1 | <ul><li>[x] </li> |

## Additional Resources
