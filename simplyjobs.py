import time
import csv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import os

def initialize_driver():
    """
    Initialize undetected Chrome WebDriver.
    """
    options = uc.ChromeOptions()
    options.headless = False  # Set True if you want headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def extract_job_data(driver, job_link):
    """
    Navigate to the job link and extract the job data (Job Name, Location, Salary, Qualifications).
    """
    driver.get(job_link)
    time.sleep(3)  # Wait for the page to load

    job_data = {}

    try:
        # Extract Job Name (Title)
        job_name = driver.find_element(By.CSS_SELECTOR, '[data-testid="viewJobTitle"]').text.strip()
        job_data["Job Name"] = job_name
    except NoSuchElementException:
        job_data["Job Name"] = "N/A"

    try:
        # Extract Salary
        salary = driver.find_element(By.CSS_SELECTOR, '[data-testid="viewJobBodyJobCompensation"]').text.strip()
        job_data["Salary"] = salary
    except NoSuchElementException:
        job_data["Salary"] = "N/A"

    try:
        # Extract Location
        location = driver.find_element(By.CSS_SELECTOR, '[data-testid="viewJobCompanyLocation"]').text.strip()
        job_data["Location"] = location
    except NoSuchElementException:
        job_data["Location"] = "N/A"

    try:
        # Extract Qualifications
        qualifications_container = driver.find_element(By.CSS_SELECTOR, '[data-testid="viewJobQualificationsContainer"]')
        qualification_items = qualifications_container.find_elements(By.CSS_SELECTOR, ".chakra-wrap__listitem.css-1yp4ln")
        qualifications = [item.text.strip() for item in qualification_items]
        
        # Ensure qualifications are always saved as a single string joined by semicolons
        job_data["Qualifications"] = "; ".join(qualifications) if qualifications else "N/A"
    except NoSuchElementException:
        job_data["Qualifications"] = "N/A"

    return job_data

def read_job_links_from_csv(file_path):
    """
    Reads the job links from a CSV file.
    """
    job_links = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            job_links.append(row[0])  # Assuming the links are in the first column
    return job_links

def save_job_data_to_csv(job_data, output_file):
    """
    Save the extracted job data into a CSV file.
    """
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["Job Name", "Location", "Salary", "Qualifications"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        # Ensure qualifications are correctly joined into a single string before saving
        for job in job_data:
            # In case the qualifications field contains a tuple or list, convert it to a string
            if isinstance(job["Qualifications"], list):
                job["Qualifications"] = "; ".join(job["Qualifications"])  # Join qualifications with semicolons
            
        writer.writerows(job_data)
    print(f"✅ Saved {len(job_data)} job entries to '{output_file}'.")

def main():
    # Define the job files and their corresponding job titles
    job_files = [
        ("ai_ml_unprocessed_links.csv", "AI/ML"),
        ("data_scientist_unprocessed_links.csv", "Data Scientist"),
        ("software_engineer_unprocessed_links.csv", "Software Engineering")
    ]
    
    # Initialize WebDriver
    driver = initialize_driver()

    # Store job data here
    all_job_data = []

    try:
        # Loop through job files and scrape data
        for job_file, job_title in job_files:
            print(f"Reading job links from {job_file}...")
            job_links = read_job_links_from_csv(job_file)
            
            # Loop through each job link and scrape the data
            for link in job_links:
                print(f"Extracting data for job link: {link}")
                job_data = extract_job_data(driver, link)
                job_data["Job Name"] = job_title  # Set the job title dynamically based on the file
                all_job_data.append(job_data)
                time.sleep(2)  # Add delay between scraping each job

        # Save the extracted job data to a new CSV file
        if all_job_data:
            output_file = "processed_job_data.csv"  # Change the output file name here
            save_job_data_to_csv(all_job_data, output_file)
        else:
            print("⚠ No job data extracted.")

    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error while quitting driver: {e}")

if __name__ == "__main__":
    main()
