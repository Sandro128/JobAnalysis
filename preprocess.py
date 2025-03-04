import csv
import re
import us  # Import the us library for state abbreviation normalization

def extract_salary(salary):
    """Extract and normalize salary from various formats."""
    if not salary:
        return None

    salary = salary.replace(',', '').lower().strip()  # Remove commas and normalize text

    # Match salary formats ($xx,xxx, $xx.xxxK, xx per hour, etc.)
    match = re.search(r'\$?(\d+(?:\.\d+)?)\s*(k|per hour|hour|usd|a year)?', salary, re.IGNORECASE)

    if match:
        value, unit = match.groups()
        value = float(value)

        if unit == 'k':  # Convert K notation (e.g., 45.9K → 45900)
            value *= 1000
        elif unit in ['per hour', 'hour'] or value < 250:  # Convert hourly and values < 250 to yearly
            value *= 2000

        return round(value, 2)  # Return cleaned salary

    return None

def standardize_location(location):
    """Standardize location names, converting state names to abbreviations or marking remote jobs."""
    if not location:
        return "Remote"
    
    if 'remote' in location.lower():
        return "Remote"

    try:
        location_parts = location.split(',')
        location = location_parts[-1].strip()  # Get the last part of the location (usually the state)

        # Attempt to match the state abbreviation using the us library
        normalized_location = us.states.lookup(location)

        if normalized_location:
            return normalized_location.abbr  # Return the state abbreviation
        else:
            return "Remote"
    except Exception:
        return "Remote"

def process_processed_job_data(file_path):
    """Preprocess job data from processed_job_data.csv."""
    data = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            salary = extract_salary(row.get('Salary', ''))
            if salary:
                location = standardize_location(row.get('Location', ''))
                jobtitle = row.get('Job Name', 'Software Engineering')  # Default to Software Engineering if missing
                
                data.append({
                    'Title': jobtitle,
                    'Location': location,
                    'Skills': row.get('Qualifications', None),
                    'Salary': salary
                })
    return data

def process_flexjobs(file_path):
    """Preprocess job data from flexjobs_jobs.csv with job title renaming."""
    data = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            salary = extract_salary(row.get('Salary Range', ''))
            if salary:
                location = standardize_location(row.get('Remote Option', ''))
                jobtitle = row.get('Job Title', 'Software Engineering').strip()  # Use job title or default
                
                # Rename job titles
                if jobtitle.lower() == "machine learning engineer":
                    jobtitle = "AI/ML"
                elif jobtitle.lower() == "software engineer":
                    jobtitle = "Software Engineering"

                data.append({
                    'Title': jobtitle,
                    'Location': location,
                    'Skills': None,  # FlexJobs does not have qualifications
                    'Salary': salary
                })
    return data

def write_to_csv(data, output_file):
    """Write processed job data to a CSV file."""
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Location', 'Skills', 'Salary'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    processed_data = process_processed_job_data('processed_job_data.csv')
    flexjobs_data = process_flexjobs('flexjobs_jobs.csv')

    combined_data = processed_data + flexjobs_data  # Merge datasets

    write_to_csv(combined_data, 'data.csv')

if __name__ == "__main__":
    main()
