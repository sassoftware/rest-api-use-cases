import time
import pricing_optimization
import schema_collection
import json
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

prodName = "T1_Tops"
locName = "T1_NC"
planName = prodName + "_" + locName
planVersion = 0
startDate = "2019-04-08"
endDate = "2019-05-05"
prodIDs = ["T1_75", "T1_78", "T1_81", "T1_84"]
prodHierarchy = 1
prodDimensionCode = "PRODUCT"
locIDs = ["T1_40"]
locHierarchy = 1
locDimensionCode = "GEOGRAPHY"
locSplitLevel = "Market"
prodSplitLevel = "Style"
dataParamsObj = {"productName": prodName,
                 "geographyName": locName,
                 "startDate": startDate,
                 "endDate": endDate}
extractType = "scopeExtract"

# Create a session
session = pricing_optimization.PricingPlan('PRICEOPTIMIZATION')

# Create
data = schema_collection.create_plan_schema(planVersion, startDate, endDate, prodIDs, prodHierarchy,
                                            prodDimensionCode, locIDs, locHierarchy, locDimensionCode,
                                            locSplitLevel, prodSplitLevel)
response = session.create_plan(data)
session.check_task_finished("creationRequests", response)
time.sleep(10)

# Execute
data = schema_collection.create_execution_schema(planName + "_" + locName, planVersion, startDate, endDate,
                                                 prodIDs, prodHierarchy, prodDimensionCode, locIDs, locHierarchy,
                                                 locDimensionCode, "testExecution")
response = session.create_execution(data)
session.check_task_finished("executionRequests", response)
time.sleep(30)

# Scope extract
data = schema_collection.create_data_extract_schema("Sample Plan Name Extract Job",
                                                    extractType,
                                                    "multi_test",
                                                    "csv",
                                                    "filesystem",
                                                    "SAS Content / Public / RetailPricing",
                                                    dataParamsObj,
                                                    )
response = session.create_data_extract_job(data)
session.check_task_finished("dataExtracts", response)
