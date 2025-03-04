import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# List to store all job data
all_job_data = []

# Function to initialize and restart WebDriver
def initialize_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

# Function to scrape job data from a given URL
def scrape_jobs(url, job_title, driver):
    driver.get(url)

    # Allow the page to load
    time.sleep(5)  # Adjust the sleep time based on how long the page takes to load

    # Find all job elements (update the CSS selectors as per the HTML structure)
    jobs = driver.find_elements(By.CSS_SELECTOR, 'div.sc-jv5lm6-0.jqvXcB')

    # Loop through each job element and scrape the data
    for job in jobs:
        job_info = {'Job Title': job_title}  # Include the job title to differentiate between job types
        
        try:
            # Extract the job name, handling cases where the element might not exist
            job_name_tag = job.find_element(By.CSS_SELECTOR, 'a.fQyPIb.textWrap')
            job_info['Job Name'] = job_name_tag.text.strip() if job_name_tag else 'N/A'
        except:
            job_info['Job Name'] = 'N/A'
        
        try:
            # Extract the job description
            job_description_tag = job.find_element(By.CSS_SELECTOR, 'p.dAsgtY')
            job_info['Description'] = job_description_tag.text.strip() if job_description_tag else 'N/A'
        except:
            job_info['Description'] = 'N/A'
        
        try:
            # Extract the remote option (if present)
            remote_option_tag = job.find_element(By.CSS_SELECTOR, 'li[id^="remoteoption"]')
            job_info['Remote Option'] = remote_option_tag.text.strip() if remote_option_tag else 'N/A'
        except:
            job_info['Remote Option'] = 'N/A'
        
        try:
            # Extract the salary range (if present)
            salary_range_tag = job.find_element(By.CSS_SELECTOR, 'li[id^="salartRange"]')
            job_info['Salary Range'] = salary_range_tag.text.strip() if salary_range_tag else 'N/A'
        except:
            job_info['Salary Range'] = 'N/A'
        
        # Append the job data to the all_job_data list
        all_job_data.append(job_info)

# Define the search URLs for Data Scientist, Software Engineer, and Machine Learning Engineer jobs
urls = [
    "https://www.flexjobs.com/search?searchkeyword=Data%20Scientist&useclocation=true",  # Corrected to Data Scientist
    "https://www.flexjobs.com/search?searchkeyword=Software%20Engineer&useclocation=true",
    "https://www.flexjobs.com/search?searchkeyword=Machine%20Learning%20Engineer&useclocation=true"
]

# Scrape Data Scientist jobs
driver = initialize_driver()  # Restart WebDriver
scrape_jobs(urls[0], 'Data Scientist', driver)

# Scrape Software Engineer jobs
driver.quit()  # Close current driver
driver = initialize_driver()  # Restart WebDriver
scrape_jobs(urls[1], 'Software Engineer', driver)

# Scrape Machine Learning Engineer jobs
driver.quit()  # Close current driver
driver = initialize_driver()  # Restart WebDriver
scrape_jobs(urls[2], 'Machine Learning Engineer', driver)

# Write the collected job data to a single CSV file
filename = 'flexjobs_jobs.csv'
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Job Title', 'Job Name', 'Description', 'Remote Option', 'Salary Range']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Write the job data rows
    for job in all_job_data:
        writer.writerow(job)

# Print a confirmation message
print(f"Job data for Data Scientist, Machine Learning Engineer, and Software Engineer has been saved to '{filename}'.")

# Close the driver
driver.quit()
