# SAS Retail Pricing API Use Case
The SAS Retail team is developing a pricing optimization solution that focuses on markdown pricing. This solution takes a product scope, geographic scope and a range of dates and returns pricing plans for the given products. Completing the use case using the SAS front-end application is a fairly routine process; however, some customers may want to interact with the APIs directly in order to automate the workflow or integrate it into their own systems.

Reviewing the current documentation, there are individual examples available to customers. However, I find it an effective tool to demonstrate how to string the APIs together to perform a series of tasks that one would do in the GUI.

A detailed walkthrough of how to use and implement the code in this repository is in [this article on the SAS Support Communities](https://communities.sas.com/t5/SAS-Communities-Library/SAS-Retail-Pricing-API-Use-Case/ta-p/823520
).

# Authentication - Create conf.ini file
## Authenticating to the Environment and Retrieving Access Token

In order to create a session, we must start by invoking the class PricingPlan. The PricingPlan class takes one value, which is the name of a profile contained in the conf.ini file. These profiles can be changed, but they have four important values. Name, url, username, and password.
```
[PRICEOPTIMIZATION]
url: http://pricing.pricing-azure-nginx-02cdf9bf.unx.sas.com/
username: FOO
password: BAR
```
So, if the conf.ini file contains a profile called ‘PRICEOPTIMIZATION’, we can then create a session using the configuration.
session = pricing_optimization.PricingPlan('PRICEOPTIMIZATION')
- The URI accessed is {url}/SASLogon/oauth/token
- The payload is grant_type=password&username=FOO&password=BAR
So, when session is initialized, it will take the parameters from the conf.ini file.

**NOTE**: This is not recommended for production environments, but an implementation by an intern to test the pricing solution using different profiles.
