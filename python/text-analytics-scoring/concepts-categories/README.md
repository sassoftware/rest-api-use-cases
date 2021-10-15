# Text Analytics Scoring

## Overview

This app leverages our SAS Viya and CAS APIs. It is a good way to demonstrate how one can operationalize text models (not only ML ones). In this example we apply Concepts and Categories nodes in a model through REST requests.

To complete the concepts and categories use cases, you must first deploy a text analytics model in SAS. Detailed instrucitons for both scenarios follow. The sentiment analysis example is self-contained and requires no additional setup outside of the REST calls. 

## Prerequisites
Refer to the [Authentication Project](../authentication) project in order to get an access token.

### Variables to assign:

The scripts come with variables you must assign. Provide values to the following variables prior to running the projects:

- sasserver - the location of the SAS Viya server, for example: https://myserver.sas.com
- access_token - inherited from the Authentication project
- modelCaslib - see step 4 in teh Build a Text Analytics model instructions
- modelConceptsTable - see step 4 in teh Build a Text Analytics model instructions
- modelCategoriesTable - see step 5 in teh Build a Text Analytics model instructions

Other variables are assigned progamatically during the REST calls.

### Build a SAS Visual Text Analytics model

1. Download the Restaurant Reviews data set and use it in step 2.
2. Follow the instructions on [creating a SAS Visual Text Analytics Model](https://go.documentation.sas.com/doc/en/ctxtcdc/v_006/ctxtug/p0yl2w8o7hucd5n1vpwfwvbgj1bw.htm).
3. When running the pipeline be sure to enter the Topics node and select at least one topic to include as a Category. Then rerun the Category node. Otherwise create your own custom category.
4. In Model Studio-> Restaurant Reviews-> Pipelines-> Concepts node-> Results-> Concepts Score Code, copy the values of the liti_binary_caslib and liti_binary_table_name and create Postman variables modelCaslib and modelConceptsTable, respectively.
5. In Model Studio-> Restaurant Reviews-> Pipelines-> Categories node-> Results-> Categories Score Code, copy the values of the mco_binary_caslib and mco_binary_table_name and create Postman variables modelCaslib (same caslib from step 3; no need to re-create) and modelCategoriesTable, respectively.

## Usage

1. Download the Python program or the Jupyter Notebook file.
2. Edit your variables to match your environment.
3. Proceed to run the program or Notebook commands.

## Endpoints Used

- [/cas/sessions](https://developer.sas.com/apis/cas/rest/current/apidoc.html#Sessions) - Create session to be used in subsequent requests.
- [/actions/table.upload](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=caspg&docsetTarget=cas-table-upload.htm) - Upload a table
- [/actions/textRuleScore.applyConcept](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=casvtapg&docsetTarget=cas-textrulescore-applyconcept.htm) - Performs concept extraction using a concept extraction model (LI file)
- [/actions/textRuleScore.applyCategory](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=casvtapg&docsetTarget=cas-textrulescore-applycategory.htm) - Categorizes text using a category model(MCO file)
- [/actions/table.fetch](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=caspg&docsetTarget=cas-table-fetch.htm) - Fetch rows of a table
- [/actions/table.droptable](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=caspg&docsetTarget=cas-table-droptable.htm) - Drop a table

## Supported Versions

The table below represents use case testing results. 
| SAS Viya Version | Tested |
| ----------- | ----------- |
| 3.5 | <ul><li>[x] </li> |
| 2021.1 | <ul><li>[x] </li> |

## Additional Resources