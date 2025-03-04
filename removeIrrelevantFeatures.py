import csv
from collections import Counter
import re

def count_skills(file_path):
    """Count the frequency of skills in the data.csv file."""
    skills_count = Counter()

    # Define patterns to ignore (e.g., experience level, years of experience, etc.)
    exclude_keywords = [
        r'\d+\+? years',         # Match patterns like "11+ years"
        r'level',                # Exclude keywords like "senior", "junior"
        r'entry',                # Exclude entry level
        r'mid-level',            # Exclude mid-level
        r'senior',               # Exclude senior level
        r'under \d+ year',       # Exclude "under 1 year" or similar
        r'\b(?:bachelor|master|ph\.d|degree|diploma)\b',  # Exclude educational qualifications
        r'\b(?:license|certification)\b',  # Exclude license/certification-related phrases
        r'program management',   # Exclude program management, irrelevant as a skill
        r'windows',              # Exclude platform-related terms, often not a skill itself
        r'microsoft office',     # Exclude suite of programs (e.g., Word, Excel) as they are too general
        r'powerpoint'            # Exclude PowerPoint, which is often just a tool, not a skill
    ]
    exclusion_pattern = '|'.join(exclude_keywords)
    
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        if 'Skills' not in reader.fieldnames:
            print("Error: 'Skills' column not found in the CSV file.")
            return skills_count

        for row in reader:
            skills = row.get('Skills', '')
            if skills:
                # Clean out non-skill parts using regex
                skills_cleaned = re.sub(exclusion_pattern, '', skills, flags=re.IGNORECASE)
                # Split skills by semicolon and standardize them
                skills_list = [skill.strip().lower() for skill in skills_cleaned.split(';') if skill.strip()]
                skills_count.update(skills_list)
    
    return skills_count

def filter_row_skills(row, useless_set, exclusion_pattern):
    """
    Update the row's Skills field by removing any skill that appears in the useless_set.
    Also removes duplicate skills in the same row.
    """
    skills = row.get('Skills', '')
    if skills:
        # Clean the skills using the same exclusion pattern as above.
        skills_cleaned = re.sub(exclusion_pattern, '', skills, flags=re.IGNORECASE)
        skills_list = [skill.strip().lower() for skill in skills_cleaned.split(';') if skill.strip()]
        # Remove duplicates by converting the list to a set and back to a list
        skills_list = list(set(skills_list))
        # Filter out any skills that are in the useless_set
        filtered_skills = [skill for skill in skills_list if skill not in useless_set]
        row['Skills'] = '; '.join(filtered_skills)
    return row

def main():
    input_file = 'data.csv'
    output_file = 'filtered_data.csv'
    
    # Define a set of useless skills (adjust as needed)
    useless_set = {
        "'s", "of science", "doctoral", "doctor of philosophy", "1 year",
        "of business administration", "bachelor", "master", "ph.d", "degree",
        "diploma", "license", "certification", "microsoft office", "powerpoint", "windows",
        "leadership", "associate's", "mentoring", "teaching", 'product management', 'microsoft'
        , 'microsoft word', 'powershell', "driver's", 'snowflake', 'pki', 'journalism', 'transcription'
        , 'grammar experience', 'high school  or ged', 'copywriting'
    }

    # Use the same exclusion pattern as in count_skills
    exclude_keywords = [
        r'\d+\+? years',
        r'level',
        r'entry',
        r'mid-level',
        r'senior',
        r'under \d+ year',
        r'\b(?:bachelor|master|ph\.d|degree|diploma)\b',
        r'\b(?:license|certification)\b',
        r'program management',
        r'windows',
        r'microsoft office',
        r'powerpoint'
    ]
    exclusion_pattern = '|'.join(exclude_keywords)
    
    # Process the CSV file and update each row's Skills field to remove useless skills and duplicates
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            # Drop row if 'Skills' field is empty
            if not row.get('Skills', '').strip():
                continue
            filtered_row = filter_row_skills(row, useless_set, exclusion_pattern)
            writer.writerow(filtered_row)
    
    print(f"Filtered data saved to '{output_file}'.")

    # Re-count skills after filtering
    print("Skill frequencies after filtering (for inspection):")
    skills_count = count_skills(output_file)
    for skill, count in skills_count.most_common(10):
        print(f"{skill}: {count}")

if __name__ == "__main__":
    main()
