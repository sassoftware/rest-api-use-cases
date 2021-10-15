# End to End Job Execution

## Overview

This collection leverages multiple SAS Viya APIs to create an end-to-end example for Job Execution. It creates a folder, creates and executes a job definition, and returns logs and job output. The example code shows how to print out the contents of the sashelp.class table. Use this simple example to create your own scenario, using your own SAS code.


## Prerequisites
Refer to the [Authentication Project](../authentication) project in order to get an access token.

### Variables

The Postman collection comes with variables you must assign (either at the collection or environment level). Assign values to the following variables prior to running the collection:
- sasserver - the location of the SAS Viya server, for example: https://myserver.sas.com
- access_token - inherited from the Authentication project

Other variables are assigned programmatically during the REST calls using code in the Postman 'Tests' tab.

## Usage

1. Download the JSON object and import the file into Postman as a collection.
2. Edit your environment variables to match those contained in the collection requests (sasserver, access_token).
3. Be sure to authenticate to your server before testing the endpoints.
4. Proceed to run the requests.

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
