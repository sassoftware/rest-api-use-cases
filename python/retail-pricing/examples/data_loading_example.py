import time
import pricing_optimization
import json
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)

# Create a session
session = pricing_optimization.PricingPlan('PRICEOPTIMIZATION')

# Get Request
response = session.get_retail_analytics()
print(json.dumps(response, indent=4))

# Get elasticities
response = session.get_elasticities()
print("START HERE")
print(json.dumps(response, indent=4))
