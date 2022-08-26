import jsonschema


def create_plan_schema(planVersion, startDate, endDate, prodID: list, prodHierarchy, prodDimensionCode,
                       locID: list, locHierarchy, locDimensionCode, locSplitLevel,
                       prodSplitLevel, planName="Creating new plans", userDefinedName="plan creation", description=""):
    schema = {"name": planName,
              "version": planVersion,
              "startDate": startDate,
              "endDate": endDate,
              "product": {
                  "members": prodID,
                  "hierarchy": prodHierarchy,
                  "dimensionCode": prodDimensionCode
              },
              "location": {
                  "members": locID,
                  "hierarchy": locHierarchy,
                  "dimensionCode": locDimensionCode
              },
              "requests": [
                  {
                      "version": 0,
                      "requestName": "pricingPlanCreationRequestType",
                      "userDefinedName": userDefinedName,
                      "description": description,
                      "parameters": {
                          "locationSplitLevelName": locSplitLevel,
                          "planVersions": [0, 1],
                          "productSplitLevelName": prodSplitLevel
                      }
                  }
              ]
              }
    valid_schema = validate_plan_schema(schema)
    if valid_schema is True:
        return schema
    else:
        return


def validate_plan_schema(data):
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "version": {"type": "integer"},
            "startDate": {
                "type": "string",
                "format": "date"
            },
            "endDate": {
                "type": "string",
                "format": "date"
            },
            "product": {
                "type": "object",
                "properties": {
                    "members": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "hierarchy": {"type": "integer"},
                    "dimensionCode": {
                        "type": "string",
                        "enum": ["PRODUCT"]
                    }
                }
            },
            "location": {
                "type": "object",
                "properties": {
                    "members": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "hierarchy": {"type": "integer"},
                    "dimensionCode": {"enum": ["GEOGRAPHY"]}
                }
            },
            "requests": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "version": {"type": "integer"},
                        "requestName": {"type": "string"},
                        "userDefinedName": {"type": "string"},
                        "description": {"type": "string"},
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "locationSplitLevelName": {"type": "string"},
                                "planVersions": {
                                    "type": "array",
                                    "items": {
                                        "type": "integer",
                                        "enum": [0, 1]
                                    }
                                },
                                "productSplitLevelName": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    }
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        return False
    return True


def create_data_extract_schema(jobName, jobType, extractName, fileType, locType, locToSave, params):
    schema = {
        "name": jobName,
        "tasks": [
            {
                "dataExtractName": jobType,
                "userDefinedExtractName": extractName,
                "format": fileType,
                "locationType": locType,
                "location": locToSave,
                "parameters": params
            }
        ]
    }

    valid_schema = validate_data_extract_schema(schema)
    if valid_schema is True:
        return schema
    else:
        return


def validate_data_extract_schema(data):
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "tasks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "dataExtractName": {
                            "type": "string"
                        },
                        "userDefinedExtractName": {"type": "string"},
                        "format": {"type": "string"},
                        "locationType": {"type": "string"},
                        "location": {"type": "string"},
                        "parameters": {"type": "object"}
                    }
                }
            }
        }
    }
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        return False
    return True


def create_execution_schema(execName, execVer, startDate, endDate, prodMembers: list, prodHierarchy, prodDimensionCode,
                            locMembers: list, locHierarchy, locDimensionCode, reqDefinedName, description=""):
    schema = {
        "name": execName,
        "version": execVer,
        "startDate": startDate,
        "endDate": endDate,
        "product": {
            "members": prodMembers,
            "hierarchy": prodHierarchy,
            "dimensionCode": prodDimensionCode
        },
        "location": {
            "members": locMembers,
            "hierarchy": locHierarchy,
            "dimensionCode": locDimensionCode
        },
        "requests": [
            {
                "requestName": "pricingPlanExecutionRequestType",
                "userDefinedName": reqDefinedName,
                "description": description,
                "parameters": {"executionType": "OPTIMIZATION"}
            }
        ]
    }
    valid_schema = validate_data_extract_schema(schema)
    if valid_schema is True:
        return schema
    else:
        return


def validate_execution_schema(data):
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "version": {"type": "number"},
            "startDate": {"type": "string",
                          "format": "date"},
            "endDate": {"type": "string",
                        "format": "date"},
            "product": {
                {"type": "object",
                 "properties": {
                     "members": {"type": "array",
                                 "items": {"type": "string"}},
                     "hierarchy": {"type": "string"},
                     "dimensionCode": {"type": "string"}
                 }}},
            "location": {
                "members": {"type": "array",
                            "items": {"type": "string"}},
                "hierarchy": {"type": "string"},
                "dimensionCode": {"type": "string"}
            },
            "requests": {
                "type": "array",
                "items": {
                    "requestName": {"type": "string"},
                    "userDefinedName": {"type": "string"},
                    "description": {"type": "string"},
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "executionType": {"type": "string"}
                        }
                    }
                }
            }
        }
    }
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        return False
    return True


def create_price_grid_schema(priceGridRule, startRange: float, endRange: float, gridValues: list,
                             priceGridName: str = "new_price_grid", description: str = "new price grid"):
    schema = {
        "id": priceGridRule,
        "name": priceGridName,
        "description": description,
        "priceGrid": [
            {
                "startRange": startRange,
                "endRange": endRange,
                "values": gridValues
            }
        ]
    }
    valid_schema = validate_price_grid_schema(schema)
    if valid_schema is True:
        return schema
    else:
        return


def validate_price_grid_schema(data):
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "priceGrid": {"type": "array",
                          "items": {
                              "startRange": {"type": "float"},
                              "endRange": {"type": "float"},
                              "values": {"type": "array"}
                          }
                          }
        }
    }
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        return False
    return True
