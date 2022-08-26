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
planVersion = 1
startDate = "2019-04-08"
endDate = "2019-05-05"
prodIDs = ["T1_29"]
prodHierarchy = 1
prodDimensionCode = "PRODUCT"
locIDs = ["T1_40"]
locHierarchy = 1
locDimensionCode = "GEOGRAPHY"
locSplitLevel = "Market"
prodSplitLevel = "Class"

prodName = "T1_Dairy"
locName = "T1_NC"
target = "T1_Dairy_T1_CHARLOTTE-ROCK HILL METRO_2019-04-08_2019-05-05"

# Create a session
session = pricing_optimization.PricingPlan('PRICEOPTIMIZATION')

# # Create a business plan (if it does not exist)
# data = schema_collection.create_plan_schema(planVersion, startDate, endDate, prodIDs, prodHierarchy,
#                                             prodDimensionCode, locIDs, locHierarchy, locDimensionCode, locSplitLevel,
#                                             prodSplitLevel)
# response = session.create_plan(data)
# session.check_task_finished("creationRequests", response)
# time.sleep(10)
#
# Get lifecycle plans of product IDs.
response = session.get_lifecycles_by_prod_ids(prodIDs)
lifecycle_ids = session.get_plan_lifecycle_ids(response, target)
date_rules = [
  {
    "id": 701,
    "availableDates": [
        {
            "startDate": "2019-04-08",
            "endDate": "2019-04-21"
        }
    ]
  },
  {
    "id": 1101,
    "availableDates": [
        {
            "startDate": "2019-04-22",
            "endDate": "2019-05-05"
        }
    ]
  }
]
for i in range(len(lifecycle_ids)):
    session.update_lifecycle_numeric_rule(lifecycle_ids[i], 90, 103)
    session.update_lifecycle_available_date_rules(lifecycle_ids[i], date_rules)
    print(lifecycle_ids[i], "updated")

# # Execute
# execParamsObj = {"executionType": "OPTIMIZATION"}
# data = schema_collection.create_execution_schema(planName + "_" + locName, planVersion, startDate, endDate, prodIDs,
#                                                  prodHierarchy, prodDimensionCode, locIDs, locHierarchy,
#                                                  locDimensionCode, "testExecution", execParamsObj)
# response = session.create_execution(data)
# session.check_task_finished("executionRequests", response)
# time.sleep(30)
#
# # pricingName extract
# dataParamsObj = {"pricingPlanName": target}
# data = schema_collection.create_data_extract_schema("Sample Plan Name Extract Job",
#                                                     "planExtract",
#                                                     "test",
#                                                     "csv",
#                                                     "filesystem",
#                                                     "SAS Content / Public / RetailPricing",
#                                                     dataParamsObj,
#                                                     )
# response = session.create_data_extract_job(data)
# session.check_task_finished("dataExtracts", response)
