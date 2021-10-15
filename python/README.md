# Python

## Overview

Welcome to the Python section of the end-to-end use case repository. Everything you need to run these use cases as Python scripts or in a Jupyter Notebook is here.

Each language directory contains an authentication folder. You may want to start there, especially if it's your first visit. If you have a registered client move directly into your use case of choice.

This directory also contains a project template that you may use to create your own examples.

## Prerequisites

- Python 3.7+
- A Jupyter Notebook (if running the .ipynb files)
- A SAS Viya environment

## Common Variables Used
The test cases use a variety of variables. Below are some guidelines on how to fill them out.

| Variable | Sample value | Notes |
| ---------- | ----------- | ----------- |
| sasserver | https://sasserer.sas.com | SAS Viya server URL |
| client_token | 85989eb1-2237-412a-b889-55cdcfbe7540 | Consul token; see authentication test case on how to find / copy the token value |
| username | sasuser | SAS username |
| password | password | Password for SAS username |
| client_id | myclientid | arbitrary client name used for registration; [refer to this page for more details](https://www.oauth.com/oauth2-servers/client-registration/client-id-secret/) |
| client_secret | myclientsecret | client secret for client ID; [refer to this page for more details](https://www.oauth.com/oauth2-servers/client-registration/client-id-secret/)
