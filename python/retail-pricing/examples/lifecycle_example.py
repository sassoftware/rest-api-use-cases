import time
import pricing_optimization
import schema_collection
import json
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

prodName = "T1_Dairy"
locName = "T1_NC"
planName = prodName + "_" + locName
planVersion = 0
startDate = "2019-04-08"
endDate = "2019-05-05"
prodIDs = ["T1_67"]
prodHierarchy = 1
prodDimensionCode = "PRODUCT"
locIDs = ["T1_40"]
locHierarchy = 1
locDimensionCode = "GEOGRAPHY"
locSplitLevel = "Market"
prodSplitLevel = "Class"

prodName = "T1_Dairy"
locName = "T1_NC"
targetPlanName = "T1_Dairy_T1_RDU METRO_2019-04-08_2019-05-05"

# Create a session
session = pricing_optimization.PricingPlan('PRICEOPTIMIZATION')

# Create a business category (if it does not exist)
data = schema_collection.create_plan_schema(planVersion, startDate, endDate, prodIDs, prodHierarchy,
                                            prodDimensionCode, locIDs, locHierarchy, locDimensionCode, locSplitLevel,
                                            prodSplitLevel)
response = session.create_plan(data)
session.check_task_finished("creationRequests", response)
time.sleep(10)

# Execute
data = schema_collection.create_execution_schema(planName + "_" + locName, planVersion, startDate, endDate, prodIDs,
                                                 prodHierarchy, prodDimensionCode, locIDs, locHierarchy,
                                                 locDimensionCode, "testExecution")
response = session.create_execution(data)
session.check_task_finished("executionRequests", response)
time.sleep(30)

# Get lifecycle plans of product IDs.
response = session.get_lifecycles_by_prod_ids(prodIDs)
lifecycle_ids = session.get_plan_lifecycle_ids(response, targetPlanName)
for i in range(len(lifecycle_ids)):
    response = session.update_lifecycle_numeric_rule(lifecycle_ids[i], 90, 103)
    print(json.dumps(response, indent=4))

# Execute
data = schema_collection.create_execution_schema(planName + "_" + locName, planVersion, startDate, endDate, prodIDs,
                                                 prodHierarchy, prodDimensionCode, locIDs, locHierarchy,
                                                 locDimensionCode, "testExecution")
response = session.create_execution(data)
session.check_task_finished("executionRequests", response)
time.sleep(30)
#
# # pricingName extract
# dataParamsObj = {"pricingPlanName": targetPlanName}
# extractType = "planExtract"
# jobName = "myplanextract_pricingname"
#
#
# data = schema_collection.create_data_extract_schema("Sample Plan Name Extract Job",
#                                                     extractType,
#                                                     jobName,
#                                                     "csv",
#                                                     "filesystem",
#                                                     "SAS Content / Public / RetailPricing",
#                                                     dataParamsObj,
#                                                     )
# response = session.create_data_extract_job(data)
# session.check_task_finished("dataExtracts", response)
