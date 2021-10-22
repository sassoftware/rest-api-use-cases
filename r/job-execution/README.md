# Creating, managing and executing Jobs

## Overview

These R scripts use SAS Viya APIs to build functions which can be reused as steps to create, manage and execute jobs. The example code shows how to print out the contents of the sashelp.class table. Use this simple example to create your own scenario, using your own SAS code.

The first script `job_definition-crud-r` creates a job definition. The second script `job-execution-r` executes the job. The use case is presented in two forms:  an R program and a Jupyter Notebook (using the R kernel).


## Prerequisities
Refer to the [Authentication Project](../authentication) project in order to get an access token.


### R requirements (libraries)

-   R 3.6+
-   `httr`
-   `jsonlite`

## Usage

The jobs in SAS Viya are made in two steps, first you create the job definition through the `job_definition-crud-r.r` and then you execute this job through the `job_execution.r`, it also has a way of creating and executing a persistent job.

1. Download the R programs or the Jupyter Notebook files.
2. Edit your variables to match your environment.
3. Proceed to run the program or Notebook commands.

## Endpoints Used

-   [/jobDefinitions/definitions](https://developer.sas.com/apis/rest/Compute/#create-a-job-definition)
-   [/jobDefinitions/definitions/{job-id}](https://developer.sas.com/apis/rest/Compute/#get-headers-for-a-job-definition)
-   [/jobExecution/jobs](https://developer.sas.com/apis/rest/Compute/#get-all-jobs)
-   [/jobExecution/jobs/{jobId}](https://developer.sas.com/apis/rest/Compute/#get-a-job)
-   [/jobExecution/jobRequests/](https://developer.sas.com/apis/rest/Compute/#get-a-list-of-job-requests)
-   [/jobExecution/jobRequests/{jobRequestId}](https://developer.sas.com/apis/rest/Compute/#get-a-job-request-summary)
