# EtoE Modeling and Deployment

## Overview

This collection leverages multiple API (both SAS Viya and CAS) to create an end to end example for modeling. It creates folders, uploads data to CAS, imputes missing data, trains a decision tree model, creates a repository for deployment, deploys the model to Micro Analytics Services (MAS) and scores new data.

## Prerequisites

- Refer to the [Authentication Project](../authentication) project in order to get an access token.
- Download [hmeq.csv](https://support.sas.com/documentation/onlinedoc/viya/exampledatasets/hmeq.csv) data set

## Usage

1. Download the JSON object and import the file into Postman as a collection.
2. Edit your variables to match those contained in the collection requests (sasserver, access_token).
3. Be sure to authenticate to your server before testing the endpoints.
4. Step 2 in the collection, *upload data*, requires a defined path to the hmeq.csv data set (downloaded in the pre-reqs).
5. Proceed to run the requests.  

### Variables

The Postman collection comes with variables you must assign (either at the collection or environment level). Assign values to the following variables prior to running the collection:
- sasserver - the location of the SAS Viya server, for example: https://myserver.sas.com
- access_token - inherited from the Authentication project

Other variables are assigned programmatically during the REST calls using code in the Postman 'Tests' tab.

## Endpoints Used

- [/casManagement/servers/\<server-name>/sessions](https://developer.sas.com/apis/rest/v3.5/Compute/#get-a-list-of-sessions) - Create CAS session
- [/dataTables/dataSources/\<server-table-name>/tables](https://developer.sas.com/apis/rest/v3.5/DataManagement/#create-a-new-table) - upload table
- [/cas/sessions/<session_id>/actions/datapreprocess.impute](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=casanpg&docsetTarget=cas-datapreprocess-impute.htm) - impute missing
- [/cas/sessions/\<session_id>/actions/decisionTree.dtreeTrain](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=casanpg&docsetTarget=cas-decisiontree-dtreetrain.htm) - train decision tree
- [/cas/sessions/\<session_id>/actions/decisionTree.dtreeCode](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=casanpg&docsetTarget=cas-decisiontree-dtreecode.htm) - generate decision tree code
- [/cas/sessions/\<session_id>/actions/table.fetch](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=caspg&docsetTarget=cas-table-fetch.htm) - fetch the score code
- [/folders/folders](https://developer.sas.com/apis/rest/CoreServices/#get-a-list-of-folders) - get a folder id by name
- [/files/files#rawUpload](https://developer.sas.com/apis/rest/CoreServices/#create-new-file-resource) - create a file
- [/modelPublish/destinations](https://developer.sas.com/apis/rest/v3.5/DecisionManagement/#get-a-list-of-publishing-destinations) - create publishing destination for the model
- [/modelRepository/models](https://developer.sas.com/apis/rest/v3.5/DecisionManagement/#get-a-list-of-models) - create the model
- [/modelRepository/models/<model_id>/contents](https://developer.sas.com/apis/rest/v3.5/DecisionManagement/#get-model-contents) - upload the code to the model structure
- [/modelManagement/publish](https://developer.sas.com/apis/rest/v3.5/DecisionManagement/#publish-models) -  publish the model
- [/modelPublish/models/<publishing-id>](https://developer.sas.com/apis/rest/v3.5/DecisionManagement/#get-published-models) - check the published model
- [/microanalyticScore/modules/<publishing-name>/steps/score](https://developer.sas.com/apis/rest/v3.5/DecisionManagement/#get-module-steps) - score new data

## Supported Versions

The table below represents use case testing results. 
| SAS Viya Version | Tested |
| ----------- | ----------- |
| 3.5 | <ul><li>[x] </li> |
| 2021.1 | <ul><li>[x] </li> |

## Additional Resources
