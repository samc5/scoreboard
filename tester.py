## Run selenium and chrome driver to scrape data from cloudbytes.dev
import time
import json
import pprint
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#function
# api_url = None

def process_browser_logs_for_network_events(logs):
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
            "Network.response" in log["method"]
            or "Network.request" in log["method"]
            or "Network.webSocket" in log["method"]
        ):
            yield log

def process_browser_logs_for_network_events2(logs):
    for entry in logs:
        log = json.loads(entry["message"])["message"]           
        if ("Network.responseReceived" in log["method"]):
            if ("response" in log["params"]):
                if ("url" in log["params"]["response"]):
                    if ("push" in log["params"]["response"]["url"]):
                        return log["params"]["response"]["url"]
                        


# #Desired Capabilities
# capabilities = DesiredCapabilities.CHROME
# capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+

# ## Setup chrome options
# chrome_options = Options()
# chrome_options.add_argument("--headless") # Ensure GUI is off
# chrome_options.add_argument("--no-sandbox")

# # Set path to chromedriver as per your configuration
# homedir = os.path.expanduser("~")
# webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

# # Choose Chrome Browser
# browser = webdriver.Chrome(service=webdriver_service, options=chrome_options, desired_capabilities=capabilities)

# # # Get page
# # browser.get("https://cloudbytes.dev")

# # # Extract description from page and print
# # description = browser.find_element(By.NAME, "description").get_attribute("content")
# # print(f"{description}")

# # gamechanger start
# browser.get("https://gc.com/game-640b6eb0d181fcd24100008d")
# logs = browser.get_log("performance")
# print(logs)
# events = process_browser_logs_for_network_events(logs)
# with open("log_entries.txt", "wt") as out:
#     for event in events:
#         pprint.pprint(event, stream=out)

# title = browser.find_element(By.NAME, "description").get_attribute("content")
# print(f"{title}")
# api_url = process_browser_logs_for_network_events2(logs)
# print(f"Api url: {api_url}")
# #Wait for 10 seconds


# time.sleep(10)
# browser.quit()


def getPushURL(game_url):
    #Desired Capabilities
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+

    ## Setup chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    # Set path to chromedriver as per your configuration
    homedir = os.path.expanduser("~")
    webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

    # Choose Chrome Browser
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options, desired_capabilities=capabilities)
    browser.get(game_url)
    logs = browser.get_log("performance")
    api_url = process_browser_logs_for_network_events2(logs)
    time.sleep(10)
    browser.quit()
    return api_url