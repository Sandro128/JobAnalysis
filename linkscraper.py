import time
import csv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

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

def extract_job_links_from_page(driver):
    """
    Extracts all job links from the current page.
    """
    job_links = set()  # Using set to avoid duplicates

    # Find all job posting elements with class that might hold job links
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".chakra-button.css-1djbb1k")
    
    for job in job_elements:
        link = job.get_attribute("href")
        if link:
            job_links.add(link)  # Adding link to set ensures no duplicates

    return job_links

def get_next_page_url(driver):
    """
    Tries to find a link with aria-label="Next page" and returns its 'href'.
    If not found, returns None.
    """
    try:
        next_link = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Next page"]')
        return next_link.get_attribute("href")
    except NoSuchElementException:
        return None

def scrape_all_pages(driver, start_url, max_pages=100):
    """
    Scrapes up to `max_pages` pages for job links.
    """
    all_links = set()  # Using set to store unique job links
    driver.get(start_url)
    time.sleep(5)

    page_count = 0

    while page_count < max_pages:
        # Extract job links on current page
        page_links = extract_job_links_from_page(driver)
        if not page_links:
            print("No job links found on this page. Stopping pagination.")
            break

        all_links.update(page_links)  # Use update to add new links without duplicates
        page_count += 1
        print(f"Extracted {len(page_links)} links on this page. Total so far: {len(all_links)}")

        # Attempt to find the next page link
        next_page_url = get_next_page_url(driver)
        if not next_page_url:
            print("No 'Next page' link found. Pagination ended.")
            break

        # Navigate to next page
        print(f"Navigating to: {next_page_url}")
        driver.get(next_page_url)
        time.sleep(3)

    print(f"Stopped after {page_count} pages.")
    return list(all_links)  # Convert set back to list for saving to CSV

def save_links_to_csv(links, filename):
    """
    Saves the extracted job links to a CSV file.
    """
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows([[link] for link in links])  # Writing links without a header
        print(f"✅ Saved {len(links)} links to '{filename}'.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    search_urls = {
        # "software_engineer": "https://www.simplyhired.com/search?q=software+engineer&l=",
        # "data_scientist": "https://www.simplyhired.com/search?q=data+scientist&l=",
        "ai_ml": "https://www.simplyhired.com/search?q=machine+learning+ai&l=",
    }

    driver = None
    try:
        driver = initialize_driver()

        for job_title, url in search_urls.items():
            print(f"Scraping {job_title.replace('_', ' ').title()} jobs...")

            # For Software Engineer, scrape 100 pages; for others, scrape the default max of 50 pages
            if job_title == "software_engineer":
                job_links = scrape_all_pages(driver, url, max_pages=100)
            else:
                job_links = scrape_all_pages(driver, url, max_pages=100)

            # Save to CSV
            if job_links:
                save_links_to_csv(job_links, f"{job_title}_unprocessed_links.csv")
            else:
                print(f"⚠ No links found for {job_title.replace('_', ' ')}.")

    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error while quitting driver: {e}")

if __name__ == "__main__":
    main()
