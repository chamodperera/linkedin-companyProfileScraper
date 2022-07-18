# Tutorial - How to build your own LinkedIn Profile Scraper in 2022
LinkedIn is the world's largest professional network on the internet. You can use LinkedIn to find the right job or internship, connect and strengthen professional relationships, and learn the skills you need to succeed in your career. A complete LinkedIn profile can help you connect with opportunities by showcasing your unique professional story through experience, skills, and education.

In this tutorial, Let's look at how to implement a **web scraper to gather job details and company profiles from a posted jobs list on Linkedin** and save them in a `.JSON` file using **Python**.

This tutorial is a complete beginner guide to web scraping using **python**.

## What is Web Scraping?

Web scraping refers to the extraction of data from a website. This information is collected and then exported into a format that is more useful for the user. Be it a spreadsheet or an API. In most cases, automated tools are preferred when scraping web data as they can be less costly and work at a faster rate.


## Getting started

In order to complete this task, we need these widely used python libraries in web scraping.

1. [Selenium](https://www.selenium.dev/)
2. [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/)

The first one, `Selenium` is used to navigate web pages and interact with them. The other one is widely used to scrape data from web pages.

So let's install them.

```
pip install selenium
```

```
pip install beautifulsoup4
```

## Installing the web driver

To work with `Selenium` you need to install the web driver for your browser. WebDriver is an open source tool for automated testing of web apps across many browsers. It provides capabilities for navigating web pages, user input, JavaScript execution, and more. If you are using chrome, you can download the driver by [this link](https://chromedriver.chromium.org/).

**It's important to check your browser version before downloading the driver.**

## Task explanation

On LinkedIn, a user account is not compulsory to search for jobs. We can simply navigate to [linkedin/jobs](https://www.linkedin.com/jobs/) and search for any job vacancies available in your area.

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ocbbwxrpdw6kh7ge414f.png)

So that our task is to automatically search for jobs on Linkedin and save the job list and company profiles as` .JSON`.

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7un9lnb4dh6vdprnclw3.png)

## Navigating to webpage

As mentioned earlier, we use `Selenium` for navigation purposes. Let's import it into our program.

```
from selenium import webdriver
```
Then we need to establish our web driver as a driver object.

```
driver = webdriver.Chrome(location)
```
Replace `location` with your `web driver location`. Also see [other supported browsers](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/).

Now we can use the `get()` method to locate the website by URL.

```
driver.get("https://www.linkedin.com/jobs") #URL
```
If you run the program now, you can see that it spins up a new browser and navigates to the URL. You'll also notice that it has a address bar saying it is being controlled by automated test software.
![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/awiijtz6cnxailmaa5zm.png)

## Interacting with the page

The next step is to search for jobs. First, let's save the job title and location that we want to search for in separate strings.

```
job_title = 'software engineer' 
job_location = 'sri lanka' 
```
A web page consists of HTML elements. In order to interact with it, we need to find the elements we need to act on and then find the selector or locator information for those elements of interest. The easiest way is to `Inspect` pages using developer tools. Place the cursor anywhere on the webpage, right-click to open a pop-up menu, then select the `Inspect` option. In the `Elements` window, move the cursor over the DOM structure of the page until it reaches the desired element. From there, we can find the HTML tag, the defined attribute, and the attribute values.


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/fnt0yi4bx1lzj5ms4ftn.png)

Next, we need to pass this information to the selenium web driver to simulate user actions on elements. Selenium provides various `find_element` methods to find elements based on their attribute/value criteria or selector value that we supply in our script. For that, the `By` class needs to import from Selenium.

```
from selenium.webdriver.common.by import By
```
These are the various ways the attributes are used to locate elements on a page.

```
find_element(By.ID, "id")
find_element(By.NAME, "name")
find_element(By.XPATH, "xpath")
find_element(By.LINK_TEXT, "link text")
find_element(By.PARTIAL_LINK_TEXT, "partial link text")
find_element(By.TAG_NAME, "tag name")
find_element(By.CLASS_NAME, "class name")
find_element(By.CSS_SELECTOR, "css selector")

```
In our case I am using `XPATH` method to locate the input tags of the title and location.

`XPATH` is the language used for locating nodes in an XML document. As `HTML` can be an implementation of `XML` (XHTML), Selenium users can leverage this powerful language to target elements in their web applications.

You can copy the `XPATH` by right clicking on the element.
![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yqjf0dmazorruqn3ga6y.png)

Now save them in separate variables.

```
search_title = driver.find_element(By.XPATH, '//*[@id="JOBS"]/section[1]/input')
search_location = driver.find_element(By.XPATH, '//*[@id="JOBS"]/section[2]/input')
```
Now to pass the string values to the inputs, we can use `send_keys()` method. 

```
search_title.send_keys(job_title)
search_location.clear()
search_location.send_keys(job_location,Keys.ENTER)
```
The location input is sometimes auto-filled by default with a location based on the IP address. `clear()` method is used clear any default values in the input. 

`Keys.ENTER` argument is used to send ENTER key after passing the input values. Before that `Keys` should be imported.

```
from selenium. webdriver. common. keys import Keys
```
It is important to stop the program for some time as the search results should be properly loaded before the next steps. For this, we can use the inbuilt `time` library.

```
import time
```

```
time.sleep(3) #sleeps for 3 seconds
```
Finally we can get the `UL` which contains the job list by calling the `By.CLASS_NAME` method.

```
jobs_list = driver.find_element(By.CLASS_NAME,'jobs-search__results-list')
```

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/m6rc17wg6vm70kop3hvd.png)

###Scrape data from the web page

Now we can use `BeautifulSoup` to scrape necessary data from the job list. Let's import is first.

```
from bs4 import BeautifulSoup
```
As an initial step, we need to direct the `job_list` to `BeautifulSoup`. 

```
soup = BeautifulSoup(jobs_list.get_attribute('outerHTML'), 'html.parser')
```
Similar to `Selenium` we can retrieve all `li` items in the `UL` by the tag name into a list. See the [Bs4 documentation](https://beautiful-soup-4.readthedocs.io/en/latest/#navigating-the-tree) for more information.

```
jobs = soup('li')
```
Now let's make a list of the information we need to extract from every job item.

- job title
- location
- link to the job details
- link to the company profile

We use a for loop to iterate through each item in the jobs list and retrieve information.

```
data=[]
for job in jobs:
    item ={}
    item["job_title"] = job.find("h3",class_="base-search-card__title").text.strip(" \n")
    item["company"] = job.find("h4",class_="base-search-card__subtitle").text.strip(" \n")
    item["location"] = job.find("span",class_="job-search-card__location").text.strip(" \n")

    job_details = job.find("a",class_="base-card__full-link")
    item["job_details"] = job_details["href"].split('?', 1)[0]

    company_profile = job.find("a",class_="hidden-nested-link")
    item["company_profile"] = company_profile.attrs["href"].split('?', 1)[0]
    data.append(item)
```
In the above code, I declared an empty `data` array to store the information. And In every iteration in the for loop, I used `find` methods to locate the elements which we need to get data from.

`text` method is used to get the innerHTML values of the HTML tags and the `attrs[]` method is used to get the attribute values of an element. `split()` & `split()` methods are used for basic text formatting.

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/jtcy30wpttt2j4bnfy52.png)

In every iteration, all the information is saved in a separate `JSON` object.

###Save data in a JSON file

Now that all the retreived data is passed to the `data` array, we can use the built in `json` library to save them in a new json file.

```
import json
```

```
with open("jobs.json", "w") as writeJSON:
   json.dump(data, writeJSON, indent=4)
```
The final output will look like this.
![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2wwfm7nnt8bx35c4jxs4.png)

###Conclusion
The final program

```
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium. webdriver. common. keys import Keys
from bs4 import BeautifulSoup
import json
import time


job_title = 'software engineer' #replace job title
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

    job_details = job.find("a",class_="base-card__full-link")
    item["job_details"] = job_details["href"].split('?', 1)[0]

    company_profile = job.find("a",class_="hidden-nested-link")
    item["company_profile"] = company_profile.attrs["href"].split('?', 1)[0]
    data.append(item)

with open("jobs.json", "w") as writeJSON:
   json.dump(data, writeJSON, indent=4)

driver.quit()
```
With this program, you can easily scrape job details and company profile URLs on Linkedin.

You can also download the program via my [Github repository](https://github.com/chamodperera/linkedin-companyProfileScraper).

Thank You
