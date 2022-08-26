import time
import pricing_optimization
import schema_collection
import json
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

planName = "SAS_Test_1"
planVersion = 0
startDate = "2019-04-08"
endDate = "2019-05-05"
prodIDs = ["T1_87"]
prodHierarchy = 1
prodDimensionCode = "PRODUCT"
locIDs = ["T1_15-UK"]
locHierarchy = 1
locDimensionCode = "GEOGRAPHY"
locSplitLevel = "Market"
prodSplitLevel = "Style"
prodName = "T1_Summer"
locName = "T1_North"


# Create a session
session = pricing_optimization.PricingPlan('PRICEOPTIMIZATION')


# Create a plan
data = schema_collection.create_plan_schema(planVersion, startDate, endDate, prodIDs, prodHierarchy,
                                            prodDimensionCode, locIDs, locHierarchy, locDimensionCode, locSplitLevel,
                                            prodSplitLevel)
# print(json.dumps(data, indent=4))
response = session.create_plan(data)
# print(json.dumps(response, indent=4))
session.check_task_finished("creationRequests", response)
time.sleep(10)


# Create execution request
data = schema_collection.create_execution_schema(planName + "_" + locName, planVersion, startDate, endDate, prodIDs,
                                                 prodHierarchy, prodDimensionCode, locIDs, locHierarchy,
                                                 locDimensionCode, "testExecution")
# print(json.dumps(data, indent=4))
response = session.create_execution(data)
# print(json.dumps(response, indent=4))
session.check_task_finished("executionRequests", response)
time.sleep(30)


# # Create a data extraction job
# pricingName extract example
# dataParamsObj = {"pricingPlanName": "T1_Grill_T1_West Yorkshire_2019-04-08_2019-05-05"}
# extractType = "planExtract"
# data = schema_collection.create_data_extract_schema("Sample Plan Name Extract Job",
#                                                     extractType,
#                                                     "intern_presentation",
#                                                     "csv",
#                                                     "fileSystem",
#                                                     "SAS Content / Public / RetailPricing",
#                                                     dataParamsObj,
#                                                     )
# print(json.dumps(data, indent=4))
# response = session.create_data_extract_job(data)
# print(json.dumps(response, indent=4))
# session.check_task_finished("dataExtracts", response)


# Scope extract example
dataParamsObj = {"productName": prodName,
                 "geographyName": locName,
                 "startDate": startDate,
                 "endDate": endDate}
extractType = "scopeExtract"
data = schema_collection.create_data_extract_schema("Sample Scope Extract Job", extractType, "intern_presentation2",
                                                    "csv", "fileSystem", "SAS Content / Public / RetailPricing",
                                                    dataParamsObj)
response = session.create_data_extract_job(data)
session.check_task_finished("dataExtracts", response)


# # Business Category Extract
# extractType = "businessCategoryExtract"
# dataParamsObj = {"businessCategoryName": "T1_Summer_T1_North_08Apr19_05May19"}
# data = schema_collection.create_data_extract_schema("Sample Business Category Extract Job",
#                                                     extractType,
#                                                     "test_business_extract",
#                                                     "csv",
#                                                     "fileSystem",
#                                                     "SAS Content / Public / RetailPricing",
#                                                     dataParamsObj,
#                                                     )
# response = session.create_data_extract_job(data)
# session.check_task_finished("dataExtracts", response)
