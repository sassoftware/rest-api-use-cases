# EtoE - Open Source Modeling and Deployment

## Overview

This is a Postman collection with all the calls needed for creating, updating, deploying, assessing performance, and executing an Open Source model. In this example, we use a Python xgboost model.

## Prerequisites

- Refer to the [Authentication Project](../authentication) project in order to get an access token.
- Download the four files from the [data](data) directory. They will be used in various steps in the use case.
  - Place these files in the default Postman files directory (assigned in Postman Settings and defaults to C:\Users\\\<user>\Postman\files)

### Variables

The Postman collection comes with variables you must assign (either at the collection or environment level). Assign values to the following variables prior to running the collection:
- sasserver - the location of the SAS Viya server, for example: https://myserver.sas.com
- access_token - inherited from the Authentication project

Other variables are assigned programmatically during the REST calls using code in the Postman 'Tests' tab.

## Usage

1. Download the JSON object and import the file into Postman as a collection.
2. Edit your variables to match those contained in the collection requests (sasserver, access_token).
3. Be sure to authenticate to your server before testing the endpoints.
4. Multiple steps in the collection require a defined path to files from the [data](data) directory. Identify the files and paths and adjust the API calls as needed.
5. Proceed to run the requests.  

## Endpoints Used

### GET

- [/modelRepository/repositories](https://developer.sas.com/apis/rest/DecisionManagement/?python#get-a-list-of-repositories)
-Returns a paginated list of repositories.
- [/modelRepository/models](https://developer.sas.com/apis/rest/DecisionManagement/?python#get-a-list-of-models)
-Returns a list of models that are within the common model repository.
- [/modelRepository/models/mm_model_id](https://developer.sas.com/apis/rest/DecisionManagement/?python#get-a-model)
-Returns the model information for the specified model ID.

### POST

- [/modelRepository/projects](https://developer.sas.com/apis/rest/DecisionManagement/?python#create-a-project)
-Creates a project.
- [/modelRepository/models/mm_model_id](https://developer.sas.com/apis/rest/DecisionManagement/?python#create-a-model)
-Create a model.
- [/modelManagement/performanceTasks](https://developer.sas.com/apis/rest/DecisionManagement/?python#create-a-performance-task-definition)
-Creates a performance task definition (requires body).
- [/modelManagement/performanceTasks/mm_perf_id](https://developer.sas.com/apis/rest/DecisionManagement/?python#execute-a-performance-task)
-Execute the performance task.

### PUT 

- [/modelRepository/projects/_projectid](https://developer.sas.com/apis/rest/DecisionManagement/?python#update-a-project)
-Update a project.

### Multipurpose

- [/modelRepository/models/mm_model_id/contents](https://developer.sas.com/apis/rest/DecisionManagement/#get-model-contents)
-Get/add model contents.
- [/modelRepository/models/mm_model_id/code](https://developer.sas.com/apis/rest/DecisionManagement/#get-model-score-code)
-Get/import model score code.
- [/dataTables/dataSources/~file/path~/tables/_tableID](https://developer.sas.com/apis/rest/DataManagement/#get-a-table)
-Access/import data for scoring.

## Supported Versions

The table below represents use case testing results. 
| SAS Viya Version | Tested |
| ----------- | ----------- |
| 3.5 | <ul><li>[x] </li> |
| 2021.1 | <ul><li>[x] </li> |

## Additional Resources
