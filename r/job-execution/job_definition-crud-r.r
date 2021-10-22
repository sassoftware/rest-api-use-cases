#############################################
########## authentication ###################
#############################################

### with source("./R/authentication/authorization-r.r") you will be able
### to load all functions here defined to facilitate other projects
### how to use example at the end of this file

## Refer to the authentication project

#variables to assign
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


#############

library("httr")
library("jsonlite")


### Job definitions are jobs that you can execute
### You first have to create a job definition before
### execute it.

list_job_definitions <- function(host, access_token, 
                                 start = 0,
                                 limit = 10,
                                 filter = NULL,
                                 verbose = FALSE) {
  
  url <- parse_url(host)
  url$path <- "/jobDefinitions/definitions"
  url$query <- list(
    start = start,
    limit = limit,
    filter = filter
  )
    
  response <- GET(
    url = build_url(url),
    add_headers(
      "accept"="application/json",
      "authorization" = paste("Bearer", access_token)
    ),
    
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  jobsList <- fromJSON(content(response, as = "text"))
  return(jobsList$items)
}

job_definitions <- list_job_definitions(sasserver, 
                                        token
#                                        filter = "eq(createdBy, 'Demo')"
                                          )

### infos of a job
job_definitions

### Creating a job definition

create_job_definition <- function(host, 
                                  access_token,
                                  json_payload,
                                  verbose = FALSE
) {
  
  url <- parse_url(host)
  url$path <- paste0("/jobDefinitions/definitions")
  
  response <- POST(
    url = build_url(url),
    add_headers(
      "accept"="application/json",
      "authorization" = paste("Bearer", access_token),
      "Content-Type" = "application/vnd.sas.job.definition+json",
      "Accept" = "application/vnd.sas.job.definition+json"
    ),
    body = json_payload,
    encode = 'json',
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  jobDef <- fromJSON(content(response, as = "text"))
  jobDef$etag <- cache_info(response)$etag
  return(jobDef)
}


## creating a sample code to add to the job definition

payload <- toJSON(
list(
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
    
  ),
  auto_unbox = TRUE, pretty =T  ### removes [] where is not needed, must be used
)

payload

## creating the job definition


def1 <- create_job_definition(sasserver, 
                      token,
                      json_payload = payload
)

def1

### get_job_definition
### do same as above with little more detail
### of a single specific job

get_job_definition <- function(host, 
                               access_token,
                               definitionId,
                               verbose = FALSE) {
  
  url <- parse_url(host)
  url$path <- paste0("/jobDefinitions/definitions/", definitionId)
  
  response <- GET(
    url = build_url(url),
    add_headers(
      "accept"="application/json",
      "authorization" = paste("Bearer", access_token)
    ),
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  jobDef <- fromJSON(content(response, as = "text"))
  jobDef$etag <- cache_info(response)$etag
   return(jobDef)
}

jobDef <- get_job_definition(sasserver, 
                             token,
                             def1$id)

jobDef


### Updating a job definition

update_job_definition <- function(host, 
                                access_token,
                                json_payload,
                                definitionId,
                                etag, ## obatin with get or creating definitions
                                verbose = FALSE
) {
  
  url <- parse_url(host)
  url$path <- paste0("/jobDefinitions/definitions/", definitionId)
  
  response <- PUT(
    url = build_url(url),
    add_headers(
      "accept"="application/json",
      "authorization" = paste("Bearer", access_token),
      "Content-Type" = "application/vnd.sas.job.definition+json",
      "Accept" = "application/vnd.sas.job.definition+json",
      "If-Match" = etag
    ),
    body = json_payload,
    encode = 'json',
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  jobDef <- fromJSON(content(response, as = "text"))
  jobDef$etag <- cache_info(response)$etag
  return(jobDef)
}


### payload as above with some changes
payload_update <- toJSON(
  list(
    version = def1$version + 1, ### lets change version
    id = def1$id,
    name = 'Proc Print From API',
    description = "Show the contents of sashelp.class using PROC PRINT and filtering by AGE.",
    type = "Compute",
    parameters = list(
      list( ## we do double list so the json is created as "parameters: [{}]"
        version = 1,
        name = "_contextName", ## required, don't know why
        defaultValue = "SAS Job Execution compute context",
        type = "CHARACTER",
        label = "Now it is red",
        required = "false"
      ),
      list( ## added variable to the definition
        version = 1,
        name = "AGE",
        defaultValue = "10",
        type= "NUMERIC",
        label = "Lowest age for report",
        required = "false")
      ),
    ### enable filtering by AGE
    code = "ods html style=HTMLBlue;\nproc print data=sashelp.class; where age > &AGE; run; quit;\nods html close;"   
  ),
  auto_unbox = TRUE, ### removes [] where is not needed, must be used,
  pretty = TRUE
  )

payload_update


updated_def1 <- update_job_definition(sasserver, 
                      token,
                      json_payload = payload_update,
                      definitionId = def1$id,
                      etag = def1$etag,
                      )
saveRDS(updated_def1, "updated.Rda") # save job definition id for use in other scripts
updated_def1

#### Delete a Definition

delete_job_definition <- function(host, 
                               access_token,
                               definitionId,
                               verbose = FALSE) {
  
  url <- parse_url(host)
  url$path <- paste0("/jobDefinitions/definitions/", definitionId)
  
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
    print(paste0("The job ", definitionId," was successfully deleted."))
  } else {
    print(paste0("The job ", definitionId," was not deleted."))
  }
  return(response)
}

# Do not run if you're continuing with the job exectuion use case.
# apiResponse <- delete_job_definition(sasserver,
#                       token,
#                       job1$id
#                       )


