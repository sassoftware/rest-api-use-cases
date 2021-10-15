# End to End MLPA - Automated Machine Learning Guide

## Overview

The goal of this guide is to show how to use [SAS Viya's Machine Learning Pipeline Automation (MLPA)](https://developer.sas.com/apis/rest/MachineLearningPipeline/) API to perform the end-to-end machine learning process. For example, starting with a tabular data set and ending with a deployed machine learning model in production.

The hmeq data set is used in this case and can be downloaded [from here](https://support.sas.com/documentation/onlinedoc/viya/exampledatasets/hmeq.csv).

The model trained on this data set will be used to predict if a given individual is likely to default on a home equity loan. The target for this prediction task is the BAD variable that stands for Binary Applicant Default taking a value of 0 or 1. Hence MLPA will perform the end-to-end process of analytical data prep, feature engineering, model selection, hyperparameter optimization and model deployment.

## Prerequisites

- Refer to the [Authentication Project](../authentication) project in order to get an access token.
- Load the data set, which is the training data for your project, to the Public caslib using the UI or programmatically. The popular [HMEQ](https://support.sas.com/documentation/onlinedoc/viya/exampledatasets/hmeq.csv) data set is used in this example.

### Packages and Python Version
- python 3.7+
- requests, json, uuid, time

## Usage

1. Download the Python program or the Jupyter Notebook file.
2. Edit your variables to match your environment.
3. Proceed to run the program or Notebook commands.
4. Feel free to customize and test with different data sets, machine learning problem types and even integrating this functionality to your own app.

### Note on the *Create Automation Project* Request

The first call in the collection, *Create Automation Project*, performs multiple tasks as outlined in the [VDMML documentation](https://documentation.sas.com/?cdcId=capcdc&cdcVersion=default&activeCdc=vdmmlcdc&docsetId=vdmmlug&docsetTarget=titlepage.htm): [Creating a New Project](https://documentation.sas.com/?cdcId=capcdc&cdcVersion=default&activeCdc=vdmmlcdc&docsetId=vdmmlug&docsetTarget=p1k3ssjuk9ts7vn1lhypeceqgh3i.htm), [Managing Variable Assignments](https://documentation.sas.com/?cdcId=capcdc&cdcVersion=default&activeCdc=vdmmlcdc&docsetId=vdmmlug&docsetTarget=p0ay9jqraisljen0z813a5hizk2t.htm), [Automated Pipeline Creation](https://documentation.sas.com/?cdcId=capcdc&cdcVersion=default&activeCdc=vdmmlcdc&docsetId=vdmmlug&docsetTarget=n1vviwqa43qwp9n1xvzwy4usgjrk.htm), and [Managing Models](https://documentation.sas.com/?cdcId=capcdc&cdcVersion=default&activeCdc=vdmmlcdc&docsetId=vdmmlug&docsetTarget=p1ngioiguc5mmtn1e1wh8l5cew1r.htm). This process may take several minutes to complete depending on the data complexity and volume. You can monitor progress by running the *Get Project State* API call or by accessing APISampleProject in Model Studio.

## Endpoints Used

- [/mlPipelineAutomation/projects](https://developer.sas.com/apis/rest/MachineLearningPipeline/#create-an-automation-project) - create a new automation project
- [/mlPipelineAutomation/projects/{projectId}](https://developer.sas.com/apis/rest/MachineLearningPipeline/#get-an-automation-project) - get an automation project by an ID
- [/mlPipelineAutomation/projects/{projectId}/championModel](https://developer.sas.com/apis/rest/MachineLearningPipeline/#get-the-champion-model-information-for-a-completed-automation-project) - get champion model information
- [/mlPipelineAutomation/projects/{projectId}/championModel/scoreData](https://developer.sas.com/apis/rest/MachineLearningPipeline/#score-data-with-the-champion-model-of-the-automation-project) - score data with the project's champion model
- [/mlPipelineAutomation/projects/{projectId}/state](https://developer.sas.com/apis/rest/MachineLearningPipeline/#get-current-state-of-an-automation-project) - get current state of an automation job
- [/mlPipelineAutomation/projects/{projectId}/championModel?action=publish&destinationName={destinationName}](https://developer.sas.com/apis/rest/MachineLearningPipeline/#register-or-publish-the-champion-model-of-the-automation-project) - registers the champion model to supported destinations.

## Supported Versions

The table below represents use case testing results. 
| SAS Viya Version | Tested |
| ----------- | ----------- |
| 3.5 | <ul><li>[x] </li> |
| 2021.1 | <ul><li>[x] </li> |

## Additional Resources
