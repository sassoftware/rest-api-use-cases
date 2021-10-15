# Template instructions

Use this template as a guide to create new use cases. Follow these steps:
1. create a directory for the new use case
2. copy this README template into the directory
3. fill out each section for your use case in the README - add and remove text as necessary
4. add your Postman collection file
5. add any other supporting files/resources
6. create a pull request for review

## Overview

Add a description of the use case.

## Prerequisites

- [Authentication Project](../authentication) - You need an access token to run API calls.


### Variables

Define any variable assignment prior to running the collection.

## Usage

1. Download the JSON object and import the file into Postman as a collection.
2. Edit your environment variables to match those contained in the collection requests.
3. Be sure to authenticate to your server before testing the endpoints.
4. Proceed to run the requests.


## Endpoints Used

List all API endpoints used in the use case. Link each [SAS Viya](https://developer.sas.com/apis/rest/) or [CAS API](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=allprodsactions) endpoint doc on [developer.sas.com](https://developer.sas.com/home.html). Follow each link with a description. An example of each API type is provided.
- [/folders/folders ](https://developer.sas.com/apis/rest/CoreServices/#get-a-list-of-folders) - get user folder ID
- [/cas/sessions/\<session_id>/actions/table.fetch](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=caspg&docsetTarget=cas-table-fetch.htm) - fetch table

## Supported Versions

The table below represents use case testing results. 
| SAS Viya Version | Tested |
| ----------- | ----------- |
| 3.5 | <ul><li>[x] </li> |
| 2021.1 | <ul><li>[x] </li> |

## Additional Resources
