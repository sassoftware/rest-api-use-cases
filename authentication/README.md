# Authenication to SAS Viya
This page contains details on authentication to SAS Viya along with scripts to get you started.

The process for registering a client, generating an access token and using refresh tokens is covered in detail in [Authentication to SAS Viya: a couple of approaches](https://blogs.sas.com/content/sgf/2023/02/07/authentication-to-sas-viya/). The scripts in this repository support various methods discussed in the blog post.

In SAS Viya 2023.x, the use of the SAS Configuration Server (Consul) token is no longer required to generate an access token for use in client (application) registration. Rather, a user in the SASAdministrators group can generate the token.

How the SAS admin generates the access token to register the client depends on how security is set up in the SAS environment. If single sign on-is used, then the SAS admin needs to use the auth code grant type. [Here is a link](/scripts/registerClient_generateToken_AuthCode.ipynb) to the scripts for the entire process in this scenario.

If the SAS environment is set up for a more traditional username:password login, the SAS admin can use their credentials to generate the token. [This script](/scripts/registerClient_generateToken_AdminUser.ipynb) allows the admin user to securely enter credentials (removing the pw once it's used).

