import requests
import json
import configparser
import os
import time
from datetime import datetime, timedelta


class Authorization:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.expires_in = None
        self.token = self.__generate_token()

    def __generate_token(self):
        """
        Function that generates a token to access the API.
        """
        url = self.url + 'SASLogon/oauth/token'
        payload = "grant_type=password&username=" + self.username + "&password=" + self.password

        headers = {
            'Authorization': 'Basic c2FzLmVjOg==',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        print("Generating Token")

        response = requests.post(url, headers=headers, data=payload, verify=False)
        data = response.json()
        self.expires_in = datetime.now() + timedelta(seconds=int(data['expires_in']))
        return 'bearer' + ' ' + data['access_token']

    def get_token(self) -> str:
        """
        Returns an access token for the API.
        Refreshes the token if it is expired.
        """
        if self.expires_in < datetime.now():
            self.token = self.__generate_token()
        return self.token


class PricingPlan:
    def __init__(self, API):
        config = configparser.ConfigParser()
        config.read(os.path.dirname(__file__) + '/conf.ini')
        self.url = config.get(API, 'url')
        self.session = Authorization(self.url, config.get(API, 'username'), config.get(API, 'password'))

    def create_plan(self, data):
        """
        Creates business plan using a filled schema
        """
        url = self.url + "retailAnalytics/creationRequests/jobs"
        payload = json.dumps(data)
        headers = {
            'Authorization': self.session.get_token(),
            'Content-Type': 'application/vnd.sas.retail.creation.request.job.detail+json;charset=UTF-8'
        }
        try:
            response_raw = requests.request("POST", url, headers=headers, data=payload, verify=False)
            response_raw.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        print("Create_plan started")

        response = response_raw.json()
        return response

    def create_data_extract_job(self, data):
        """Create Data Extraction Job"""
        payload = json.dumps(data)
        url = self.url + "retailAnalytics/dataExtracts/jobs"
        headers = {
            'Authorization': self.session.get_token(),
            'Content-Type': 'application/vnd.sas.retail.data.extract.job.detail+json'
        }
        try:
            response_raw = requests.request("POST", url, headers=headers, data=payload, verify=False)
            response_raw.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        print("create_data_extract_job ", data['tasks'][0]['dataExtractName'], " started")

        response = json.loads(response_raw.text)
        return response

    def create_execution(self, data):
        payload = json.dumps(data)
        url = self.url + "/retailAnalytics/executionRequests/jobs"
        headers = {
            'Authorization': self.session.get_token(),
            'Content-Type': 'application/vnd.sas.retail.execution.request.job.detail+json'
        }
        try:
            response_raw = requests.request("POST", url, headers=headers, data=payload, verify=False)
            response_raw.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        print("create_execution task started")

        response = response_raw.json()
        return response

    def delete_plan(self, data):
        payload = json.dumps(data)
        url = self.url + "/"
        pass

    def __get_task_id(self, jobType: str, jobID: str, requestID: str) -> str:
        """Helper function that returns the task ID of a given job & request"""
        url = self.url + "retailAnalytics/" + jobType + "/jobs/" + jobID + "/requests/" + requestID + "/tasks"
        payload = {}
        headers = {
            'Authorization': self.session.get_token()
        }

        response_raw = requests.request("GET", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        # print(json.dumps(response, indent=4))
        taskID = response['items'][0]['id']
        return str(taskID)

    def __get_task_state(self, jobType: str, jobID: str, requestID: str, taskID: str):
        """Gets the status of a job creation task"""
        url = self.url + "retailAnalytics/" + jobType + "/jobs/" + jobID + "/requests/" + requestID + "/tasks/" + \
              taskID + "/state"
        payload = {}
        headers = {
            'Authorization': self.session.get_token()
        }

        # Response is not in json format
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        return response

    def __get_task_state_no_requestID(self, jobType: str, jobID: str, taskID: str):
        """Gets the status of a job creation task"""
        url = self.url + "retailAnalytics/" + jobType + "/jobs/" + jobID + "/tasks/" + taskID + "/state"
        payload = {}
        headers = {
            'Authorization': self.session.get_token()
        }

        # Response is not in json format
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        return response

    def check_task_finished(self, jobType, job):
        """Checks if a given task is finished, requires job type string"""
        if jobType == "dataExtracts":
            jobID, taskID = job['id'], job['tasks'][0]['id']
            while True:
                response = self.__get_task_state_no_requestID(jobType, jobID, taskID)
                print(response.text)
                if response.text != "running":
                    break
                time.sleep(10)
        else:
            jobID, requestID = job['id'], job['requests'][0]['id']
            taskID = self.__get_task_id(jobType, jobID, requestID)
            while True:
                response = self.__get_task_state(jobType, jobID, requestID, taskID)
                print(response.text)
                if response.text != "running":
                    break
                time.sleep(10)
        return

    ####################################################################################################################
    # LIFECYCLE Methods
    ####################################################################################################################
    def get_all_lifecycle_plans(self, query="?limit=10000"):
        """Returns all lifecycle plans, supports querying"""
        url = self.url + "retailPricing/lifecyclePlans" + query

        payload = ""
        headers = {
            'Authorization': self.session.get_token()
        }

        response_raw = requests.request("GET", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def get_lifecycles_by_prod_ids(self, prodIDs):
        """Returns all lifecycle plans related to a product ID"""
        url = self.url + "retailPricing/lifecyclePlans?productMemberCodes="
        length = len(prodIDs)

        for i in range(length):
            url += prodIDs[i]
            if i != length - 1:
                url += ","

        url += "&start=0&limit=10000"

        payload = ""
        headers = {
            'Authorization': self.session.get_token()
        }

        response_raw = requests.request("GET", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()

        return response

    def get_plan_lifecycle_ids(self, data, targetName: str = ''):
        """Extracts the version, name, lifecycleID, and modified time stamp of an object containing a list plans"""
        lifecycleIDs = []
        for plan in data['items']:
            if len(targetName) > 0:
                if plan['name'] == targetName:
                    planPairs = [int(plan['planVersion']), str(plan['planVersionDisplayName']), str(plan['id']),
                                 str(plan['modifiedTimeStamp'])]
                    lifecycleIDs.append(planPairs)
            else:
                planPairs = [int(plan['planVersion']), str(plan['planVersionDisplayName']), str(plan['id']),
                             str(plan['modifiedTimeStamp'])]
                lifecycleIDs.append(planPairs)
        lifecycleIDs.sort()
        return lifecycleIDs

    def get_lifecycle_rules_by_lifecycle_id(self, lifecycleID: str):
        """Returns a JSON of the details of a lifecycle plan by lifecycleID"""
        url = self.url + "retailPricing/lifecyclePlans/" + lifecycleID

        payload = {}
        headers = {
            'Authorization': self.session.get_token()
        }

        response_raw = requests.request("GET", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def get_lifecycle_numeric_rules(self, lifecycleID: str):
        """Return a JSON of the numeric rules of a given lifecycle"""
        url = self.url + "retailPricing/lifecyclePlans/" + lifecycleID + "/rules/numericRules"

        payload = {}
        headers = {
            'Authorization': self.session.get_token()
        }

        response_raw = requests.request("GET", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def update_lifecycle_numeric_rule(self, lifecycle: list, newValue, targetRule):
        """Updates a numeric rule of a lifecycle"""
        url = self.url + "retailPricing/lifecyclePlans/" + lifecycle[2] + "/rules/numericRules/" + str(targetRule)
        data = {
            "value": str(newValue),
            "id": str(targetRule)
        }
        payload = json.dumps(data)

        # FIXME: Time returned from JSON not usable in headers for put requests.
        # mod_time = lifecycle[3]

        # Current workaround
        mod_time = self.__header_date_converter(lifecycle[3])
        headers = {
            'Authorization': self.session.get_token(),
            'If-Unmodified-Since': mod_time,
            'Content-Type': 'application/json'
        }
        response_raw = requests.request("PUT", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def update_lifecycle_numeric_rules_many(self, lifecycle: list, data: list):
        """Updates many numeric rules of a lifecycle"""
        # NOT CURRENTLY WORKING
        url = self.url + "retailPricing/lifecyclePlans/" + lifecycle[2] + "/rules/numericRules"
        payload = json.dumps(data)
        mod_time = self.__header_date_converter(lifecycle[3])
        headers = {
            'Authorization': self.session.get_token(),
            'If-Unmodified-Since': mod_time,
            'Content-Type': 'application/json'
        }
        response_raw = requests.request("PUT", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def __header_date_converter(self, date: str):
        """Converts datetime from ISO8601 to RFC2616"""
        iso_time = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        rfc_time = iso_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return rfc_time

    def get_lifecycle_available_date_rules(self, lifecycleID: str):
        """Returns the available date rules of a given lifecycle plan"""
        url = self.url + "retailPricing/lifecyclePlans/" + lifecycleID + "/rules/availableDates"

        payload = {}
        headers = {
            'Authorization': self.session.get_token()
        }

        response_raw = requests.request("GET", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def update_lifecycle_available_date_rules(self, lifecycle: list, data):
        """Updates lifecycle available date rules"""
        url = self.url + "retailPricing/lifecyclePlans/" + lifecycle[2] + "/rules/availableDates"

        payload = json.dumps(data)
        mod_time = self.__header_date_converter(lifecycle[3])
        headers = {
            'Authorization': self.session.get_token(),
            'If-Unmodified-Since': mod_time,
            'Content-Type': 'application/json'
        }

        response_raw = requests.request("PUT", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def get_lifecycle_date_rules(self, lifecycleID: str):
        """Returns the date rules of a given lifecycle plan"""
        url = self.url + "retailPricing/lifecyclePlans/" + lifecycleID + "/rules/dateRules"

        payload = {}
        headers = {
            'Authorization': self.session.get_token()
        }

        response_raw = requests.request("GET", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def update_lifecycle_date_rules(self, lifecycle: list, data):
        """Updates all lifecycle date rules"""
        url = self.url + "retailPricing/lifecyclePlans/" + lifecycle[2] + "/rules/dateRules"

        payload = json.dumps(data)
        mod_time = self.__header_date_converter(lifecycle[3])
        headers = {
            'Authorization': self.session.get_token(),
            'Content-Type': 'application/vnd.sas.retail.pricing.lifecycle.plan.date.rule+json',
            'If-Unmodified-Since': mod_time
        }

        response_raw = requests.request("PUT", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def get_lifecycle_bool_rules(self, lifecycleID: str):
        """Returns boolean rules of a given lifecycle plan"""
        url = self.url + "retailPricing/lifecyclePlans/" + lifecycleID + "/rules/booleanRules"

        payload = {}
        headers = {
            'Authorization': self.session.get_token()
        }

        response_raw = requests.request("GET", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def update_lifecycle_bool_rules(self, lifecycle: list, data):
        """Updates all lifecycle date rules"""
        url = self.url + "retailPricing/lifecyclePlans/" + lifecycle[2] + "/rules/booleanRules"

        payload = json.dumps(data)
        mod_time = self.__header_date_converter(lifecycle[3])
        headers = {
            'Authorization': self.session.get_token(),
            'Content-Type': 'application/vnd.sas.retail.pricing.lifecycle.plan.boolean.rule+json',
            'If-Unmodified-Since': mod_time
        }

        response_raw = requests.request("PUT", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def get_lifecycle_price_grid_rules(self, lifecycleID: str):
        """Returns price grid rules of a given lifecycle plan"""
        url = self.url + "retailPricing/lifecyclePlans/" + lifecycleID + "/rules/priceGrids"

        payload = {}
        headers = {
            'Authorization': self.session.get_token()
        }

        response_raw = requests.request("GET", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def update_lifecycle_price_grid_rule(self, lifecycle: list, data, targetRule):
        """Updates lifecycle price grid rules by target rule"""
        url = self.url + "retailPricing/lifecyclePlans/" + str(lifecycle[2]) + "/rules/priceGrids/" + str(targetRule)

        payload = json.dumps(data)
        mod_time = self.__header_date_converter(lifecycle[3])
        headers = {
            'Authorization': self.session.get_token(),
            'Content-Type': 'application/vnd.sas.retail.pricing.lifecycle.plan.price.grids+json',
            'If-Unmodified-Since': mod_time
        }

        response_raw = requests.request("PUT", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def get_lifecycle_price_ending_rules(self, lifecycleID: str):
        """Returns price ending rules of a given lifecycle plan"""
        url = self.url + "retailPricing/lifecyclePlans/" + lifecycleID + "/rules/priceEndings"

        payload = {}
        headers = {
            'Authorization': self.session.get_token()
        }

        response_raw = requests.request("GET", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def update_lifecycle_price_ending_rule(self, lifecycle: list, data, targetRule):
        """Updates lifecycle price ending rule by target rule"""
        url = self.url + "retailPricing/lifecyclePlans/" + lifecycle[2] + "/rules/priceEndings/" + targetRule

        payload = json.dumps(data)
        mod_time = self.__header_date_converter(lifecycle[3])
        headers = {
            'Authorization': self.session.get_token(),
            'Content-Type': 'application/vnd.sas.retail.pricing.lifecycle.plan.price.endings+json',
            'If-Unmodified-Since': mod_time
        }

        response_raw = requests.request("PUT", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    ####################################################################################################################
    # Data Loading Methods
    ####################################################################################################################
    def get_retail_analytics(self):
        """
        Get process models for retail analytics
        """
        url = self.url + "retailAnalytics/processModels"
        payload = {}
        headers = {
            'Authorization': self.session.get_token(),
        }
        response_raw = requests.request("GET", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response

    def get_elasticities(self):
        """
        Get elasticities
        """
        url = self.url + "/retailAnalytics/processModels/7_6_LoadFact_FCSTE"
        payload = {}
        headers = {
            'Authorization': self.session.get_token(),
        }
        response_raw = requests.request("GET", url, headers=headers, data=payload, verify=False)
        response = response_raw.json()
        return response
