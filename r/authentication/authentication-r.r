#############################################
########## authentication package ###########
#############################################

### with source(./r/authentication/auth_package.R) you will be able
### to load all functions here defined to facilitate other projects
### how to use example at the end of this file
### If you use source(), remember to comment out the unwanted function calls at the end 

###################################################
################ Create functions #################
###################################################

library("httr")
library("jsonlite")

#  Get Client Token
#  Parameters: 
#     - host = hostname 
#     - consul_token (get on your SAS ViyaServer)
#  Outputs:
#     - This call will generate a token, save it for the next call (where it says 'token_from_call_above')

#  Call: 

get_access_token <- function(host, client_token, verbose = FALSE) {

url <- parse_url(host)
url$path <- "/SASLogon/oauth/clients/consul"
url$query <- list(
  "callback" = "false",
  "serviceId" = "app"
)

response <- POST(
  url = build_url(url),
  add_headers(
    "X-Consul-Token"= client_token
  ),
  
  if(verbose) verbose()
)

stop_for_status(response)
idToken <- fromJSON(content(response, as = "text", encoding = "UTF-8"))
return(idToken)

}


#  Register Client
#  Parameters: 
#     - host = hostname
#     - idToken = access token from consul idToken$access_token
#     - client_name
#     - client_secret
#  Outputs:
#      - It will return the client created

# Call:

register_client <- function(host, idToken, client_name, client_secret, 
                            verbose = FALSE, scope = "openid") {
  
  url <- parse_url(host)
  url$path <- "/SASLogon/oauth/clients"
  
  body <- list(
    "client_id" = client_name,
    "scope" = scope,
    "access_token_validity" = 36000,
    "client_secret" = client_secret,
    "resource_ids" = "none",
    "authorities" = "uaa.none",
    "authorized_grant_types"= "password"
  )
  
  response <- POST(
    url = build_url(url),
    add_headers(
      "Content-Type"="application/json",
      "authorization" = paste("Bearer", idToken)
      ),
    body = toJSON(body, auto_unbox = T),
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  registered_client <- fromJSON(content(response, as = "text", encoding = "UTF-8"))
  return(registered_client)
}



#  Get API call token
#  Paremeters:
#     - your_server
#     - (Base64) encoded_client_secret
#     - your_username
#     - your_passwordc
#  Outputs:
#     - It will return a JSON, you will use the access_token for future calls

# Call:


authenticate <- function(host, username, password,
                         client_name, client_secret, 
                         verbose = FALSE) {
  
  client_info <- base64_enc(paste0(client_name, ":", client_secret))
  
  url <- parse_url(host)
  url$path <- "/SASLogon/oauth/token"
  url$query <- list(
    grant_type = "password",
    username = username,
    password = password 
  )
  
  response <- GET(
    url = build_url(url),
    add_headers(
      "Content-Type" = "application/x-www-form-urlencoded",
      "accept"="application/json",
      "authorization" = paste("Basic", client_info)
    ),
    
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  registered_clients <- fromJSON(content(response, as = "text", encoding = "UTF-8"))
  return(registered_clients)
}
################ Optional functions #################

#  List available Clients
#  Parameters: 
#     - host = hostname
#     - idToken = access token from consul idToken$access_token
#     - startIndex = starting intex from the client results
#     - count = number of clients to return
#     - cliunt_id_filter = simple regex filter for name search
#  Outputs:
#      - It will return a list of clients with its properties

# Call:

list_clients <-  function(host, idToken,
                          startIndex = 1, count = 30, 
                          clind_id_filter = "",
                          verbose = FALSE) {
  
  url <- parse_url(host)
  url$path <- "/SASLogon/oauth/clients"
  url$query <- list(
    filter = paste0('client_id co "', clind_id_filter, '"'),
    sortBy = "client_id",
    startIndex = startIndex,
    count = count
  )
  
  response <- GET(
    url = build_url(url),
    add_headers(
      "accept"="application/json",
      "authorization" = paste("Bearer", idToken)
    ),
    
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  registered_clients <- fromJSON(content(response, as = "text", encoding = "UTF-8"))
  return(registered_clients)
}

#  Delete Client
#  Parameters: 
#     - host = hostname
#     - access_token = access token obtained with authenticate()
#     - the access_token client must have one of these scopes:
#       uaa.admin clients.write clients.admin zones.uaa.admin
#     - client_id = client_name
#  Outputs:
#      - It will return a list of clients with its properties

# Call:

delete_client <-  function(host, access_token,
                           client_id,
                           verbose = FALSE) {
  
  url <- parse_url(host)
  url$path <- paste0("/SASLogon/oauth/clients/", client_id)
  
  response <- DELETE(
    url = build_url(url),
    add_headers(
      "accept"="application/json",
      "authorization" = paste("Bearer", access_token)
    ),
    
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  deleted_client <- fromJSON(content(response, as = "text", encoding = "UTF-8"))
  return(deleted_client)
}

#  Update Client Secret
#  Parameters: 
#     - host = hostname
#     - access_token = access token obtained with authenticate()
#     - the access_token client must have one of these scopes:
#       uaa.admin clients.secret clients.admin zones.uaa.admin
#     - client_id = client_name
#  Outputs:
#      - It will return a list of clients with its properties

# Call:

update_client_secret <-  function(host, access_token,
                           client_id,
                           new_secret,
                           verbose = FALSE) {
  
  url <- parse_url(host)
  url$path <- paste0("/SASLogon/oauth/clients/", client_id, "/secret")
  
  body <- list(clientId = client_id,
               secret = new_secret)
  
  response <- PUT(
    url = build_url(url),
    add_headers(
      "Content-Type" = "application/json",
      "accept"="application/json",
      "authorization" = paste("Bearer", access_token)
    ),
    body = toJSON(body, auto_unbox = T),
    
    if(verbose) verbose()
  )
  
  stop_for_status(response)
  secret_update <- fromJSON(content(response, as = "text", encoding = "UTF-8"))
  return(secret_update)
}

###################################################
################ Run functions ####################
###################################################

#####################################################
### registering client should be done only once #####
#####################################################

sasserver  <- "http://your-server"
client_token <- "consul_token" # get from SAS Viya server
client_name <- "r_client" ## create your client
client_secret <- "r_secret" ## create your password
username <- "viya_user"
password <- "viya_password"

idToken <- get_access_token(host = sasserver ,
                            client_token = client_token)
idToken

client <- register_client(host = sasserver ,
                idToken = idToken$access_token,
                client_name = client_name,
                client_secret = client_secret)
client

## Once your client is created only need to authenticate

token <- authenticate(host = sasserver ,
                      username = username,
                      password = password,
                      client_name = client_name,
                      client_secret = client_secret)

token$access_token ## what to use in other calls
token

### functions to be used with access_token NOT consul_token

client_list <- list_clients(host = sasserver ,
                      idToken = idToken$access_token)
client_list

del_cli <- delete_client(sasserver,
                        access_token = token$access_token,
                        client_id = client_name)

## if error 403, the client doesn't have permission
## to delete other clients, must be any of the following
## uaa.admin clients.write clients.admin zones.uaa.admin

secret_up <- update_client_secret(sasserver,
                                  access_token = token$access_token,
                                  client_id = client_name,
                                  new_secret = "new_r_secret",
                                  verbose = FALSE)

## if error 403, the client doesn't have permission
## to change secrets, scope must be any of the following
## uaa.admin clients.secret clients.admin zones.uaa.admin


