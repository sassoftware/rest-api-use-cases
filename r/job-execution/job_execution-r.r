#############################################
########## authentication ###################
#############################################

### with source("./R/authentication/auth_package.R") you will be able
### to load all functions here defined to facilitate other projects
### how to use example at the end of this file

## Refer to the authentication project

source("../authentication/get-access-token-r.r") 


sasserver  <- "http://your-server"
client_name <- "r_client" ## your client
client_secret <- "r_secret" ## your password
username <- "viya_user"
password <- "viya_password"

tokenDetailed <- authenticate(host = sasserver,
                              username = username,
                              password = password,
                              client_name = client_name,
                              client_secret = client_secret)

token <- tokenDetailed$access_token
token


#############################################
######### get job request list ##############
#############################################


### To execute a job you will need the
### `updated_def1` variable created on `job_definition-crud-r.r`

library("httr")
library("jsonlite")
updated_def1 <- readRDS("updated.Rda")$id # reading the file from job-definition-crud-r to get job id


get_jobRequest_list <- function(host, 
                                access_token, 
                                start = 0,
                                limit = 10,
                                filter = NULL,
                                verbose = FALSE) {
  
  url <- parse_url(host)
  url$path <- "/jobExecution/jobs"
  url$query <- list(
    start = start,
    limit = limit,
    filter = filter
  )
  
  response <- GET(
    url = build_url(url),
    add_headers(
      "accept"="application/vnd.sas.api+json",
      "authorization" = paste("Bearer", access_token)
    ),
    
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  execList <- fromJSON(content(response, as = "text"))
  return(execList)
}

### protip: always that is possible use a filter
### otherwise the endpoint is going to do a full request
### and it is going to take a while

joblist <- get_jobRequest_list(sasserver, 
                         token,
                         start = 1, 
                         limit = 20,
                         filter = "eq(createdBy, 'Demo')"
                         )


joblist
  
##################################################
### Submit a Job Definition for Execution ########
##################################################

execute_job_definition <- function(host, 
                                access_token, 
                                jobDefinitionId,
                                
                                ### following parameters overrides definitions
                                arguments = NULL,
                                ## persistant job needs createdBy, name, desc

                                verbose = FALSE) {
  
  url <- parse_url(host)
  url$path <- "/jobExecution/jobs"

  body <- toJSON(list(
    jobDefinitionUri = paste0("/jobDefinitions/definitions/", jobDefinitionId)
  ),
  auto_unbox = TRUE
  )
  
  response <- POST(
    url = build_url(url),
    add_headers(
      "accept"="application/vnd.sas.api+json",
      "Content-Type" = "application/vnd.sas.job.execution.job.request+json",
      "authorization" = paste("Bearer", access_token)
    ),
    
    body = body, 
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  exec <- fromJSON(content(response, as = "text"))
  exec$etag <- cache_info(response)$etag
  return(exec)
}

### execution is async
exec <- execute_job_definition(sasserver, 
                       token,
                       updated_def1$id ## job created in job_definition.R
                       )
exec

## use defined parameters
exec_param <- execute_job_definition(sasserver, 
                               token,
                               updated_def1$id, ## job created in job_execution.R
                              list(AGE = 14)
                               )

exec_param$jobRequest$arguments

##################################################
############ Get Job execution state #############
##################################################

check_job_state <- function(host, 
                      access_token, 
                      executionId,
                      verbose = FALSE) {
  
  url <- parse_url(host)
  url$path <- paste0("/jobExecution/jobs/", executionId,"/state")
  
  response <- GET(
    url = build_url(url),
    add_headers(
      "accept"="text/plain",
       "authorization" = paste("Bearer", access_token)
    ),
    
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  execState <- content(response, as = "text")
  return(execState)
}

execState <- check_job_state(sasserver, 
                             token,
                             exec$id)
execState

########################################
######## get job state (async) #########
########################################

get_job_state <- function(host, 
                            access_token, 
                            executionId,
                            verbose = FALSE) {
  
  url <- parse_url(host)
  url$path <- paste0("/jobExecution/jobs/", executionId)
  
  response <- GET(
    url = build_url(url),
    add_headers(
      "accept"="application/vnd.sas.job.execution.job+json",
      "authorization" = paste("Bearer", access_token)
    ),
    
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  execState <- fromJSON(content(response, as = "text"))
  return(execState)
}

execStateFull <- get_job_state(sasserver, 
                             token,
                             exec$id)

execStateFull$results ## output files
execStateFull$endTimeStamp
execStateFull$links
execStateFull$elapsedTime ## in seconds?
execStateFull$id

##################################################
############ Update a Job Request ################
##################################################

update_execute_job_definition <- function(host, 
                                   access_token, 
                                   jobReqId, ## requestId (exec)
                                   jobDefinitionId, ## definitionId
                                   etag,
                                   name = NULL,
                                   description = NULL,
                                   arguments = NULL,
                                   verbose = FALSE) {
  
  url <- parse_url(host)
  url$path <- paste0("/jobExecution/jobRequests/", jobReqId)
  
  body <- toJSON(list(
    id = jobReqId,
    name = name,
    description = description,
    jobDefinitionUri = paste0("/jobDefinitions/definitions/", jobDefinitionId),
    arguments = arguments
  ),
  auto_unbox = TRUE
  )
  
  response <- PUT( ### updating changes from POST to PUT
    url = build_url(url),
    add_headers(
      "accept"="application/vnd.sas.api+json",
      "Content-Type" = "application/vnd.sas.job.execution.job.request+json",
      "authorization" = paste("Bearer", access_token),
      "If-Match" = etag
    ),
    
    body = body, 
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  exec <- fromJSON(content(response, as = "text"))
  return(exec)
}

updated_jobExec <- update_execute_job_definition(sasserver,
                              token,
                              jobReqId = exec$id,
                              jobDefinitionId = exec$jobRequest$jobDefinition$id,
                              etag = exec$etag,
                              name = "sashelp.class distribution",
                              description = "ods output with ager 14 cutoff",
                              arguments = list(AGE = "14"))

updated_jobExec

##################################################
################## CleanJob ######################
##################################################


#### Delete a Definition

delete_job_execution <- function(host, 
                                  access_token,
                                  executionId,
                                  verbose = FALSE) {
  
  url <- parse_url(host)
  url$path <- paste0("/jobExecution/jobs/", executionId)
  
  response <- DELETE(
    url = build_url(url),
    add_headers(
      "accept"="application/json",
      "authorization" = paste("Bearer", access_token)
    ),
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  
  if(response$status_code == 204){
    print(paste0("The job execution ", executionId," was successfully deleted."))
  } else {
    print(paste0("The job execution ", executionId," was not deleted."))
  }
  return(response)
}

response <- delete_job_execution(sasserver,
                     token,
                     execStateFull$id)

###################################################
######### Persistent Jobs / jobRequest ############
###################################################


###############################################
### creating persistent job from definition ###
###############################################

persist_job_request <- function(host, 
                                 access_token,
                                 jobDefinitionId,
                                 name = NULL, ## job name
                                 description = NULL, ## description
                                 createdBy, ## application name
                                 arguments = NULL, ## code arguments
                                Uri = TRUE,
                                json_payload = NULL,
                                 verbose = FALSE) {
  ### if Uri = FALSE, dont use JobDefinition
  ### and set a json payload Manually
  ### like if you are creating a job definition
  ### that's useful when you don't want to setup
  ### a jobdef, just create a persistent job directly
    
  url <- parse_url(host)
  url$path <- paste0("/jobExecution/jobRequests")
  
  if(Uri){
  body = toJSON(list(name = name,
              description = description,
              jobDefinitionUri = paste0("/jobDefinitions/definitions/", jobDefinitionId), 
              arguments = arguments,
              createdByApplication = createdBy
              ),
              auto_unbox = TRUE
  )
  } else {
    body = json_payload
  }
  
  response <- POST(
    url = build_url(url),
    add_headers(
      "accept"="application/vnd.sas.job.execution.job.request+json",
      "Content-Type"= "application/vnd.sas.job.execution.job.request+json",
      "authorization" = paste("Bearer", access_token)
    ),
    body = body,
    
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  persJob <- fromJSON(content(response, as = "text"))
  return(persJob)
}


### creating a persistent job from definition
persistentJob <- persist_job_request(sasserver,
                                    token,
                                    jobDefinitionId = updated_def1$id,
                                    name = "sashelp.class distribution",
                                    description = "ods output with ager 15 cutoff",
                                    createdBy = "MyJobUi",
                                    )

persistentJob

## creating a persistent job from Payload

payload <- toJSON(
  list(
    name = "proc print",
    description = "ods output",
    jobDefinition = list(
    version = 1,
    name = "Simple proc print",
    type = "Compute",
    paramenters = list(
      version = 1,
      name = "_contextName",
      defaultValue = 'SAS Job Execution compute context',
      type = "CHARACTER",
      label = "Context Name",
      required = FALSE
    ),
    code = "ods html style=HTMLBlue;\nproc print data=sashelp.class; run; quit;\nods html close;"
    )
  ),
  auto_unbox = TRUE, ### removes [] where is not needed, must be used
)
payload

persistentJob2 <- persist_job_request(sasserver,
                                     token,
                                     Uri = FALSE,
                                     json_payload = payload
)

persistentJob2$jobDefinition ## it had the jobDefinition embedded
persistentJob$jobDefinitionUri ## while through the other method you have the Uri of the original


################################
### Executing persistent job ###

persist_job_execute <- function(host, 
                                access_token,
                                persistentJobId,
                                verbose = FALSE) {
  
  url <- parse_url(host)
  url$path <- paste0("/jobExecution/jobRequests/", persistentJobId, "/jobs")
  
  response <- POST(
    url = build_url(url),
    add_headers(
      "accept"="application/vnd.sas.job.execution.job.request+json",
      "authorization" = paste("Bearer", access_token)
    ),
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  persJobExec <- fromJSON(content(response, as = "text"))
  persJobExec$etag <- cache_info(response)$etag
  return(persJobExec)
}

execPerJob <- persist_job_execute(sasserver,
                                  token,
                                  persistentJob$id)

## Anything that runs on jobs also work for persisted job
execPerJob


###
#### not implemented, but easily done
#### POST /jobRequests/{jobRequestId}/jobs to get list of associated job requests

