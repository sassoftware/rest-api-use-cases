import time
import pricing_optimization
import schema_collection
import json
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

planName = "testplan2"
planVersion = 0
startDate = "2019-04-08"
endDate = "2019-05-05"
prodIDs = ["T1_32"]
prodHierarchy = 1
prodDimensionCode = "PRODUCT"
locIDs = ["T1_10"]
locHierarchy = 1
locDimensionCode = "GEOGRAPHY"
locSplitLevel = "State"
prodSplitLevel = "Style"

prodName = "T1_Kid's"
locName = "T1_SE"

# Create a session
session = pricing_optimization.PricingPlan('PRICEOPTIMIZATION')

# Create a business plan
data = schema_collection.create_plan_schema(planVersion, startDate, endDate, prodIDs, prodHierarchy,
                                            prodDimensionCode, locIDs, locHierarchy, locDimensionCode, locSplitLevel,
                                            prodSplitLevel)
response = session.create_plan(data)
session.check_create_plan_finished(response)
time.sleep(10)

# Create execution request
data = schema_collection.create_execution_schema(planName + "_" + locName, planVersion, startDate, endDate, prodIDs,
                                                 prodHierarchy, prodDimensionCode, locIDs, locHierarchy,
                                                 locDimensionCode, "testExecution")

response = session.create_execution(data)
session.check_execute_task_finished(response)
time.sleep(30)

# pricingName extract example
dataParamsObj = {"pricingPlanName": "T1_Grill_T1_West Yorkshire_2019-04-08_2019-05-05"}
extractType = "planExtract"
jobName = "myextract_pricingname"
data = schema_collection.create_data_extract_schema("Sample Plan Name Extract Job",
                                                    extractType,
                                                    jobName,
                                                    "csv",
                                                    "fileSystem",
                                                    "/opt/sas/viya/config/data/cpsetl/stagecps/extracted/",
                                                    dataParamsObj,
                                                    )
response = session.create_data_extract_job(data)


# Scope extract example
dataParamsObj = {"productName": prodName,
                 "geographyName": locName,
                 "startDate": startDate,
                 "endDate": endDate}
extractType = "scopeExtract"
jobName = "myextract_scope"
data = schema_collection.create_data_extract_schema("Sample Scope Extract Job",
                                                    extractType,
                                                    jobName,
                                                    "csv",
                                                    "fileSystem",
                                                    "/opt/sas/viya/config/data/cpsetl/stagecps/extracted/",
                                                    dataParamsObj,
                                                    )

response = session.create_data_extract_job(data)

# Business Category Extract
extractType = "businessCategoryExtract"
jobName = "myextract_business"
dataParamsObj = {"businessCategoryName": "T1_Summer_T1_North_08Apr19_05May19"}
data = schema_collection.create_data_extract_schema("test",
                                                    extractType,
                                                    jobName,
                                                    "csv",
                                                    "fileSystem",
                                                    "SAS Content / Public / RetailPricing",
                                                    dataParamsObj,
                                                    )
response = session.create_data_extract_job(data)
