# SAS Micro Analytic Service Real-Time Scoring

## Overview

This example walks through all of the steps required to execute a decision using the SAS SAS Micro Analytic Service API. It specifically demonstrates how to score in real-time using new data passed in an API call.

## Prerequisites

- Refer to the [Authentication Project](../authentication) project in order to get an access token.
- Deploy a decision model to SAS Micro Analytic Service and a CSV file with test data before starting this project. [Refer to the documentation for details](https://go.documentation.sas.com/doc/en/mdlmgrcdc/v_011/mdlmgrqs/n14x1nvyos2li1n1u4mcndkvvg3w.htm).
  - The model in this example is based on the [HMEQ data set](https://support.sas.com/documentation/onlinedoc/viya/exampledatasets/hmeq.csv).

### Variables to Assign

- host - the SAS Viya server URL
- oauthToken - get from the authentication project
- model_id - name (ID) of the decision that you want to execute - choose from the list produced in the 'Format the output' step
- csv_data - CSV data for use in testing the decision - an HMEQ test set is provided in the project

Other variables are assigned programmatically during the REST calls. 

### Packages and Python Version

- Python 3.7+
- requests, json, pandas 


## Usage

1. Download the Python program or the Jupyter Notebook file.
2. Edit your variables to match your environment.
3. Proceed to run the program or Notebook commands.
   
Note on running the scripts. For this use case you must identify the module you wish to use for scoring. In both the notebook and program, there is a step which lists all modules. The variable assignment occurs as the script runs. You must choose the intended module and assign the model_id variable. 
    
## Endpoints 

- [/microanalyticScore/modules/](https://developer.sas.com/apis/rest/DecisionManagement/#get-loaded-modules) - get first 20 modules deployed to SAS Micro Analytic Service
- [/microanalyticScore/modules/<model_id>/steps](https://developer.sas.com/apis/rest/DecisionManagement/#get-module-steps) - get steps for the specified decision ID
- [/microanalyticScore/modules/<model_id>/steps/execute](https://developer.sas.com/apis/rest/DecisionManagement/#execute-a-step) - submit the data and decision to be executed
