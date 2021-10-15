# Text Analytics Sentiment Scoring

## Overview

This app leverages our SAS Viya and CAS APIs. It is a good way to demonstrate how one can operationalize text models (not only ML ones). In this example, we apply the sentiment Text Analytics Models through REST requests.

The sentiment analysis example is self-contained and requires no additional setup outside of the REST calls. To complete the concepts and categories use cases, you must first deploy a text analytics model in SAS. Detailed instructions for both scenarios are contained in the repository.

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
4. Proceed to run the requests. Note: the dropTable call removes the table created during the use case, so the test can be rerun.

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
