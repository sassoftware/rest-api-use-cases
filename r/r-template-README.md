# Template instructions
Use this template as a guide to create new use cases. Follow these steps:
1. create a directory for the new use case
2. copy this README template into the directory
3. fill out each section for your use case in the README - add and remove text as necessary
4. add your Python code; Jupyter notebook version of code is optional
5. add any other supporting files/resources
6. create a pull request for review

# Title of the end-to-end example

## Overview

- Give your app a overview of what you developed.
- Add a more detailed description of what you worked on - the main topics users will expect to see in the code.

## Prerequisites

- Instructions on what to do before running the example.
- List any required packages.
- List any R version requirements or dependencies.
- Mention the authentication project

### Variables

Define any variable assignment prior to running the collection.

## Usage
- List step-by-step instruciton on how to run the use case.
- Execute this code in order to make it run: `your-script here`

## Endpoints Used
List all API endpoints used in the use case. Link each [SAS Viya](https://developer.sas.com/apis/rest/) or [CAS API](https://go.documentation.sas.com/doc/en/pgmcdc/8.11/allprodsactions/titlepage.htm) endpoint doc on [developer.sas.com](https://developer.sas.com/home.html). Follow each link with a description. An example of each API type is provided.
- [/folders/folders ](https://developer.sas.com/apis/rest/CoreServices/#get-a-list-of-folders) - get user folder ID
- [/cas/sessions/\<session_id>/actions/table.fetch](https://go.documentation.sas.com/?cdcId=pgmcdc&cdcVersion=8.11&docsetId=caspg&docsetTarget=cas-table-fetch.htm&locale=en) - fetch table

## Supported Versions
The table below represents use case testing results. 
| SAS Viya Version | Tested |
| ----------- | ----------- |
| 3.5 | <input type="checkbox" disabled checked /> |
| 2020.1 | <input type="checkbox" disabled /> |
