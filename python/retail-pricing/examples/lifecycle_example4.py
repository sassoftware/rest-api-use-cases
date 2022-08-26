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
priceGridValues = [20.0, 35.0, 50.0, 75.0, 90.0]
dataParamsObj = {"productName": prodName,
                 "geographyName": locName,
                 "startDate": startDate,
                 "endDate": endDate}
extractType = "scopeExtract"

# Create a session
session = pricing_optimization.PricingPlan('PRICEOPTIMIZATION')

# # Create a business plan (if it does not exist)
# data = schema_collection.create_plan_schema(planVersion, startDate, endDate, prodIDs, prodHierarchy,
#                                             prodDimensionCode, locIDs, locHierarchy, locDimensionCode, locSplitLevel,
#                                             prodSplitLevel)
# response = session.create_plan(data)
# session.check_task_finished("creationRequests", response)
# time.sleep(10)

# Get lifecycle plans of product IDs.
response = session.get_lifecycles_by_prod_ids(prodIDs)
lifecycle_ids = session.get_plan_lifecycle_ids(response)
bool_data = [
    {
        "value": True,
        "id": 219
    },
    {
        "value": True,
        "id": 506
    },
    {
        "value": True,
        "id": 528
    },
    {
        "value": True,
        "id": 529
    },
    {
        "value": True,
        "id": 530
    },
    {
        "value": True,
        "id": 531
    }
]

grid_data = schema_collection.create_price_grid_schema(301, 0.0, -1.0, priceGridValues)
for i in range(len(lifecycle_ids)):
    if lifecycle_ids[i][0] == 1:
        response = session.update_lifecycle_numeric_rule(lifecycle_ids[i], 50, 103)
        # print("\n NEW LINE")
        # print(json.dumps(response, indent=4))
        response = session.update_lifecycle_bool_rules(lifecycle_ids[i], bool_data)
        # print("\n NEW LINE")
        # print(json.dumps(response, indent=4))
        response = session.update_lifecycle_price_grid_rule(lifecycle_ids[i], grid_data, 301)
        # print("\n NEW LINE")
        # print(json.dumps(response, indent=4))

# Execute
data = schema_collection.create_execution_schema(planName + "_" + locName, planVersion, startDate, endDate, prodIDs,
                                                 prodHierarchy, prodDimensionCode, locIDs, locHierarchy,
                                                 locDimensionCode, "testExecution")
response = session.create_execution(data)
session.check_task_finished("executionRequests", response)
time.sleep(30)

# Scope extract
data = schema_collection.create_data_extract_schema("Sample Plan Name Extract Job",
                                                    extractType,
                                                    "test",
                                                    "csv",
                                                    "filesystem",
                                                    "SAS Content / Public / RetailPricing",
                                                    dataParamsObj,
                                                    )
response = session.create_data_extract_job(data)
session.check_task_finished("dataExtracts", response)
