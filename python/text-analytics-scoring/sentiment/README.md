NEED TO EDIT FOR PYTHON

# Text Analytics Sentiment Scoring

## Overview

This app leverages our SAS Viya and CAS APIs. It is a good way to demonstrate how one can operationalize text models (not only ML ones). In this example we apply the sentiment Text Anlytics Models through REST requests.

The sentiment analysis example is self-contained and requires no additional setup outside of the REST calls. To complete the concepts and categories use cases, you must first deploy a text analytics model in SAS. Detailed instrucitons for both scenarios are contained in the repository.

## Prerequisites
Refer to the [Authentication Project](../authentication) project in order to get an access token.

### Variables

The scripts come with variables you must assign. Provide values to the following variables prior to running the projects:

- sasserver - the location of the SAS Viya server, for example: https://myserver.sas.com
- access_token - inherited from the Authentication project

Other variables are assigned progamatically during the REST calls.


### Packages and Python version

- python 3.7+
- requests, json

## Usage

1. Download the Python program or the Jupyter Notebook file.
2. Edit your variables to match your environment.
3. Proceed to run the program or Notebook commands.

## Endpoints Used

- [/cas/sessions](https://developer.sas.com/apis/cas/rest/current/apidoc.html#Sessions) - Create session to be used in subsequent requests.
- [/actions/table.upload](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=caspg&docsetTarget=cas-table-upload.htm) - Upload a table
- [/actions/sentimentAnalysis.applySent](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=casvtapg&docsetTarget=cas-sentimentanalysis-applysent.htm) - Computes the document level sentiment polarity (positive, negative, neutral) and sentiment score for the input textual data.
- [/actions/table.fetch](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=caspg&docsetTarget=cas-table-fetch.htm) - Fetch rows of a table
- [/actions/table.droptable](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=default&docsetId=caspg&docsetTarget=cas-table-droptable.htm) - Drop a table


## Supported Versions

The table below represents use case testing results. 
| SAS Viya Version | Tested |
| ----------- | ----------- |
| 3.5 | <ul><li>[x] </li> |
| 2021.1 | <ul><li>[x] </li> |

## Additional Resources