# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 20:42:25 2021

@author: sas
"""

# Text Analytics - Sentiment

## Authentication -- optional step
# If you have registered a client (see the authentication use case), uncomment the code below to generate an access token.
# import requests, json, base64
# sasserver = ""
# username = ""
# password = ""
# client_id = ""
# client_secret = ""
# url = sasserver + "/SASLogon/oauth/token"
# data = {
#     'grant_type': 'password',
#     'username': username,
#     'password': password
# }
# headers = {'Accept': 'application/json'}
# response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret), verify=False).json()
# access_token = response["access_token"]
# print("The access token is: " + access_token)

## Import modules, variable assignment
# The first step of the process is to import the required packages and assign variable values.

import requests
import json

## Variables to assign

sasserver = ""
text = " Today it rained; we didn't go to school\r\n456, Our team won the game\r\n789, The funeral was a sad event\r\n012, The quick brown fox jumped over the lazy dog\r\n345, What a long strange trip it's been\r\n678, The telephone was rang and I handed it to Liz. She said \"This isn't who it would be If it wasn't who it is\"\r\n901, She was having a no good terrible very bad day\r\n234, If I could be the sun I'd radiate like Africa and Smile upon the world Intergalactic love laughter"
access_token = ""

# Create functions

## Create session to start making calls

def getSession(access_token, sasserver):

   headers_sesh = {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + access_token }

   url = sasserver + '/cas-shared-default-http/cas/sessions'

   try:
      r = requests.post(url, headers=headers_sesh, verify=False).json()
      return r
   except requests.exceptions.RequestException as e:
      return e


## Load data from the form to be scored

def csv_load(sessionId, access_token, sasserver, data):

   url = sasserver + "/cas-shared-default-http/cas/sessions/"+sessionId+"/actions/upload"

   payload = "UID,Text\r\n"+data

   headers = {
      'Accept': 'application/json',
      'Content-Type': 'binary/octet-stream',
      'JSON-Parameters': '{"casout":{"caslib":"casuser","name":"tableToScore","replace":true},"importOptions":{"fileType":"csv"}}',
      'Authorization': 'Bearer '+ access_token
   }


   try:
      response = requests.request("PUT", url, headers=headers, data = payload, verify=False)
      return str(response)
   except requests.exceptions.RequestException as e:
      return e

## Run Sentiment Model

def callSentimentModel(sessionId, access_token, sasserver):
   headers_sesh = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": "Bearer " + access_token }

   url = sasserver + '/cas-shared-default-http/cas/sessions/'+sessionId+'/actions/sentimentAnalysis.applySent'

   payload = "{\"table\":{\"caslib\":\"casuser\", \"name\":\"tableToScore\"},\r\n\"docId\":\"uid\",\r\n\"text\":\"text\",\r\n\"language\":\"ENGLISH\",\r\n\"casOut\":{\"caslib\":\"casuser\", \"name\":\"sentimentAnalysis\", \"replace\":true}}"

   try:
      r = requests.post(url, headers=headers_sesh, data=payload, verify=False).json()
      return r
   except requests.exceptions.RequestException as e:
      return e
      

## Get the data using the Fetch action

def getData(sasserver, sessionId, access_token, tblName):
   url = sasserver + "/cas-shared-default-http/cas/sessions/" + sessionId + "/actions/table.fetch"

   payload = "{ \"table\": {\"caslib\":\"casuser\", \"name\":\"" + tblName + "\"} }"

   headers = {
      'Authorization': "Bearer " + access_token,
      'Content-Type': 'application/json'
   }

   try:
      response = requests.request("POST", url, headers=headers, data = payload, verify=False).json()
      return(response)
   except requests.exceptions.RequestException as e:
      return e

## Drop table at end of use case

def dropTable(sasserver, sessionId, oaccess_token):
   url = sasserver + "/cas-shared-default-http/cas/sessions/" + sessionId + "/actions/table.dropTable"

   payload = "{\"caslib\": \"casuser\", \"name\": \"sentimentanalysis\"}"

   headers = {
      'Authorization': "Bearer " + oaccess_token,
      'Content-Type': 'application/json'
   }

   try:
      response = requests.request("POST", url, headers=headers, data=payload, verify=False).json
      return(response)
   except requests.exceptions.RequestException as e:
      return e


## End Session
def endSession(sasserver, sessionId, oaccess_token):
   url = sasserver + "/cas-shared-default-http/cas/sessions/" + sessionId

   headers = {
      'Authorization': "Bearer " + oaccess_token,
      'Content-Type': 'application/json'
   }

   try:
      response = requests.request("DELETE", url, headers=headers, verify=False).json
      return(response)
   except requests.exceptions.RequestException as e:
      return e

# Run funcitons

# Get token
# Use the Authentication project to get the token

# Get Session
sessionId = getSession(access_token, sasserver)
print(sessionId)

# Upload Data
unique_id = 123
parsedData = str(unique_id)+","+text
print(parsedData)

# Load CSV
load_data = csv_load(sessionId["session"], access_token, sasserver, parsedData)
print(load_data)

# Run Sentiment Model
sentiment_output = callSentimentModel(sessionId["session"], access_token, sasserver)
sentiment_output_format = json.dumps(sentiment_output, indent=2)
print(sentiment_output_format) # optional print statement to view output

# Get Sentiment data
sentiment_data = getData(sasserver, sessionId["session"], access_token, "sentimentAnalysis")["results"]
sentiment_format = json.dumps(sentiment_data, indent=2)
print(sentiment_format)

# Drop table
drop_table = dropTable(sasserver, sessionId["session"], access_token)
print(drop_table)

# End session
endSession= endSession(sasserver, sessionId["session"], access_token)
print(endSession)