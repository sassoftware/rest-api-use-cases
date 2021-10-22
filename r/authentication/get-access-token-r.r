## Get Access Token
# If you have previously registered a client using the authentication use case, use this script to create an access token.

# Import modules, assign variables
library("httr")
library("jsonlite")

#Global variables to assign - uncomment and assign values if using this script as stand-alone
#sasserver  <- "http://your-server"
#client_name <- "r_client" ## your client
#client_secret <- "r_secret" ## your password
#username <- "viya_user"
#password <- "viya_password"

# Get access token for calls
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
  registered_clients <- fromJSON(content(response, as = "text"))
  return(registered_clients)
}

# Run get access token function - commented out for use in other scripts
# Get Access Token
# token <- authenticate(host = sasserver ,
#                      username = username,
#                      password = password,
#                      client_name = client_name,
#                      client_secret = client_secret)#

# token$access_token ## for use in other calls
# token