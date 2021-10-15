# **Your examples are welcome and encouraged!** 

## How to Contribute

In addition to our SAS-provided samples we encourage contributions from everyone. have provided a directory [User_and_Aggregated_Samples](User_and_Aggregated_Samples) where you can add your samples as well so that other members of our community can learn fom them too!  We ask only that:

1. You have verified that the sample can work for anyone and is not specific to a particular environment.

2. You open an issue to discuss any questions you have or ideas for contribution.

3. You create a directory under your coding language, with a descriptive name, copy and populate the README template, and add any additional resources.

## Contributing Checklist

API Documentation Crowdsourcing Code Review Checklist

1) Coding Standards
    1) Code Formatting
        - [ ] Are functions defined in the sequence they are called?
    2) Naming Conventions
        - [ ] File names & Directory names: lower case with dashes (id: my-file.py) - No camel case
        - [ ] Variable names: all lower case with underscore (ie: my_variable) - No Camel Case
    3) Code Best Practices
        - [ ] Comments to each of the functions: brief description, parameters and outputs
        - [ ] Create variables for hard coded values. Ex.: passwords, tokens, usernames, hostnames, etc.
    4) Standardizing libraries for a particular language:
        1) javascript -> ajax
        2) R -> httr
        3) Python -> requests
        4) Go -> native library
        5) Java -> OkHttpClient
2) File/Project Organization
    - [ ] Use functions for REST calls for readability and organization; e.g. functions for getting tokens, registering client etc. 
    - [ ] Remove unused directories, files and imports within files
    1) Notebook vs .(extension): Best practice vs readability on browser
        - [ ] Standardize .{ext} across all examples
        - [ ] Submit .{ext} file and the associated notebook for .Py and .R
    2) Avoid config files
        - [ ] As much as possible include all that is necessary in the same place in the repository  
3) Dependencies/Pre-requisites
    - [ ] Remove authentication code and reference the authentication example as a pre-requisite
    - [ ] Required assets (e.g. csv files) in the same repository and imported in the code file 
4) Comments
    1) Add comments with this level of details:
        - [ ] Brief description
        - [ ] Parameters
        - [ ] Outputs

## Contributor License Agreement

Contributions to this project must be accompanied by a signed
[Contributor Agreement](ContributorAgreement.txt).
You (or your employer) retain the copyright to your contribution,
this simply gives us permission to use and redistribute your contributions as
part of the project.

## Code reviews

All submissions, including submissions by project members, require review. We
use GitHub pull requests for this purpose. Consult
[GitHub Help](https://help.github.com/articles/about-pull-requests/) for more
information on using pull requests.