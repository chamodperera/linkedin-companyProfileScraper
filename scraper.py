from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium. webdriver. common. keys import Keys
from bs4 import BeautifulSoup
import json
import time


job_title = 'writer' #replace job title
job_location = 'sri lanka' #replace location


driver = webdriver.Chrome('webdriver/chrome/chromedriver') #replace the webdriver location

driver.get("https://www.linkedin.com/jobs")


search_title = driver.find_element(By.XPATH, '//*[@id="JOBS"]/section[1]/input')
search_location = driver.find_element(By.XPATH, '//*[@id="JOBS"]/section[2]/input')
search_title.send_keys(job_title)
search_location.clear()
search_location.send_keys(job_location,Keys.ENTER)
time.sleep(3)

jobs_list = driver.find_element(By.CLASS_NAME,'jobs-search__results-list')
soup = BeautifulSoup(jobs_list.get_attribute('outerHTML'), 'html.parser')

jobs = soup('li')

data=[]
for job in jobs:
    item ={}
    item["job_title"] = job.find("h3",class_="base-search-card__title").text.strip(" \n")
    item["company"] = job.find("h4",class_="base-search-card__subtitle").text.strip(" \n")
    item["location"] = job.find("span",class_="job-search-card__location").text.strip(" \n")

    item["posted_date"] =job.find("time")["datetime"]

    job_details = job.find("a",class_="base-card__full-link")
    item["job_details"] = job_details["href"].split('?', 1)[0]

    company_profile = job.find("a",class_="hidden-nested-link")
    item["company_profile"] = company_profile.attrs["href"].split('?', 1)[0]
    print(item)
    data.append(item)

with open("jobs.json", "w") as writeJSON:
   json.dump(data, writeJSON, indent=4)

driver.quit()