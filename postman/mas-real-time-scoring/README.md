# SAS Micro Analytic Service Real-Time Scoring

## Overview

This example walks through all of the steps required to execute a decision using the SAS SAS Micro Analytic Service API. It specifically demonstrates how to score in real-time using new data passed in an API call.


## Prerequisites

- Refer to the [Authentication Project](../authentication) project in order to get an access token.
- Choose one of the following:
  - Deploy a decision model to SAS Micro Analytic Service and test data in JSON format. [Refer to the documentation for details](https://go.documentation.sas.com/doc/en/mdlmgrcdc/v_011/mdlmgrqs/n14x1nvyos2li1n1u4mcndkvvg3w.htm).
  - (preferred) Complete the [modeling-and-deployment](../modeling-and-deployment) use case, which deploys a model to SAS Micro Analytic Service
    - a Postman collection variable *mas_model_name* has been added to capture the SAS Micro Analytic Service module name created in step 13. publish model of the modeling-and-deployment test case


### Deploy a Decision Model
If you choose to create your own model, follow the instructions as outlined in the [VDMML documentation](https://documentation.sas.com/?cdcId=capcdc&cdcVersion=default&activeCdc=vdmmlcdc&docsetId=vdmmlug&docsetTarget=titlepage.htm). This process takes several minutes to complete depending on the data complexity and volume.

### Variables to Assign

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

- [/microanalyticScore/modules/](https://developer.sas.com/apis/rest/DecisionManagement/#get-loaded-modules) - Retrieve SAS Micro Analytic Service module metadata
- [/microanalyticScore/modules/<model_id>/steps](https://developer.sas.com/apis/rest/DecisionManagement/?python#get-module-steps) - Retrieve Model/Decision metadata (inputs and outputs)
- [/microanalyticScore/modules/<model_id>/steps/execute](https://developer.sas.com/apis/rest/DecisionManagement/?python#execute-a-step) - Execute Decision

## Supported Versions

The table below represents use case testing results. 
| SAS Viya Version | Tested |
| ----------- | ----------- |
| 3.5 | <ul><li>[x] </li> |
| 2021.1 | <ul><li>[x] </li> |

## Additional Resources
[SAS Micro Analytics Service documentation](https://go.documentation.sas.com/doc/en/masag/5.2/p0gwwa5e42y6wqn1t1nzwdpv0297.htm)