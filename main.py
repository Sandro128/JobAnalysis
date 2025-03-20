import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestRegressor
import re

# Read the data from the new folder (e.g., 'filtered_data.csv')
df = pd.read_csv('filtered_data.csv')

# Drop rows with empty values in any column
df = df.dropna()

# Clean the 'Title' column to ensure no leading or trailing spaces
df['Title'] = df['Title'].str.strip()

# Check unique job titles
print(df['Title'].unique())

# Filter for 'Software Engineering', 'Data Scientist', and 'AI/ML' job titles
df_combined = df[df['Title'].isin(['Software Engineering', 'Data Scientist', 'AI/ML'])]

# Handle missing values in 'Skills'
df_combined['Skills'] = df_combined['Skills'].fillna('')

# Define experience keywords to remove exactly (after splitting on semicolon)
experience_keywords = {'senior', 'entry', 'junior', 'mid-level', 'level', 'under', 'of', 'year'}

# Filter out any skill that exactly matches an experience keyword (ignoring case)
def filter_experience(skills_str):
    # Split on semicolon to preserve multi-word skills
    skills = [skill.strip() for skill in skills_str.split(';')]
    # Filter out skills that are exactly one of the experience keywords
    filtered_skills = [skill for skill in skills if skill.lower() not in experience_keywords]
    return filtered_skills

# Apply filtering while preserving semicolon-separated multi-word skills
df_combined['Skills'] = df_combined['Skills'].apply(filter_experience)

# Function to get top 5 skills for each job
def get_top_5_skills(df_combined):
    job_titles = df_combined['Title'].unique()
    top_skills_by_job = {}

    for job_title in job_titles:
        df_filtered = df_combined[df_combined['Title'] == job_title]
        # Flatten the list of skills from the 'Skills' column
        all_skills = [skill for skills_list in df_filtered['Skills'] for skill in skills_list]
        top_skills = pd.Series(all_skills).value_counts().head(5)
        top_skills_by_job[job_title] = top_skills
    
    return top_skills_by_job

# Get the top 5 skills for each job
top_skills_by_job = get_top_5_skills(df_combined)

# Create a DataFrame for plotting
top_skills_df = pd.DataFrame(top_skills_by_job).reset_index()
top_skills_df = top_skills_df.melt(id_vars=["index"], var_name="Job Title", value_name="Frequency")
top_skills_df.rename(columns={"index": "Skill"}, inplace=True)

# Visualize the top 5 skills for each job title
plt.figure(figsize=(10, 6))
sns.barplot(x="Frequency", y="Skill", hue="Job Title", data=top_skills_df, palette="viridis")
plt.title("Top 5 Skills for Each Job Title")
plt.xlabel("Frequency")
plt.ylabel("Skill")
plt.legend(title="Job Title", loc="upper right")
plt.show()

# Clean the 'Title' column to ensure no leading or trailing spaces
df['Title'] = df['Title'].str.strip()

# Check unique job titles
print(df['Title'].unique())

# Filter for 'Software Engineering', 'Data Scientist', and 'AI/ML' job titles
df_combined = df[df['Title'].isin(['Software Engineering', 'Data Scientist', 'AI/ML'])]

# Handle missing values in 'Skills'
df_combined['Skills'] = df_combined['Skills'].fillna('')

# Define experience keywords to remove exactly (after splitting on semicolon)
experience_keywords = {'senior', 'entry', 'junior', 'mid-level', 'level', 'under', 'of', 'year'}

# Filter out any skill that exactly matches an experience keyword (ignoring case)
def filter_experience(skills_str):
    # Split on semicolon to preserve multi-word skills
    skills = [skill.strip() for skill in skills_str.split(';')]
    # Filter out skills that are exactly one of the experience keywords
    filtered_skills = [skill for skill in skills if skill.lower() not in experience_keywords]
    return filtered_skills

# Apply filtering while preserving semicolon-separated multi-word skills
df_combined['Skills'] = df_combined['Skills'].apply(filter_experience)

# Create a MultiLabelBinarizer to transform skills into binary features
mlb = MultiLabelBinarizer()
X = df_combined[['Skills']]
y = df_combined['Salary']

# Transform skills
temp_df = pd.DataFrame(mlb.fit_transform(X['Skills']), columns=mlb.classes_, index=X.index)

# Remove numerical features
filtered_columns = [col for col in temp_df.columns if not re.match(r'^\d+$', col)]
X_filtered = temp_df[filtered_columns]

# Function to train the model for each job title and extract top 5 important features
def train_and_extract_top_features(df_combined, job_title):
    # Filter the data by job title
    df_filtered = df_combined[df_combined['Title'] == job_title]

    # Handle missing 'Skills' and prepare data
    df_filtered['Skills'] = df_filtered['Skills'].fillna('')
    X_filtered = pd.DataFrame(mlb.fit_transform(df_filtered['Skills']), columns=mlb.classes_, index=df_filtered.index)
    y = df_filtered['Salary']
    
    # Train Random Forest Regressor
    model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    model_rf.fit(X_filtered, y)
    
    # Get feature importances
    importances = model_rf.feature_importances_
    feature_importances_df = pd.DataFrame({
        'Feature': X_filtered.columns,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    
    # Return top 5 important features
    return feature_importances_df.head(5)

# Train and extract the top 5 features for each job title
job_titles = ['Software Engineering', 'Data Scientist', 'AI/ML']
top_5_features_by_job = {}

for job in job_titles:
    top_5_features_by_job[job] = train_and_extract_top_features(df_combined, job)

# Print the top 5 features for each job title
for job, features in top_5_features_by_job.items():
    print(f"\nTop 5 Features for {job} Salary Prediction:")
    print(features[['Feature', 'Importance']])

# Visualize the top 5 features for each job title as bar plots
def plot_top_5_features_by_job(job, features):
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Importance', y='Feature', data=features, palette='viridis')
    plt.title(f"Top 5 Most Important Features for {job} Salary Prediction")
    plt.xlabel('Feature Importance')
    plt.ylabel('Feature')
    plt.show()

# Visualize the top 5 features for each job title
for job, features in top_5_features_by_job.items():
    plot_top_5_features_by_job(job, features)

# Optional: menu-driven interface
def menu():
    print("\nMenu:")
    print("1. Predict Salary")
    print("2. Print Top 5 Features by Job Title")
    print("3. View Salary Distribution (Histogram)")
    print("4. View Salary Distribution by Job Role (Box Plot)")
    print("5. View Top 5 Skills for Each Job")
    print("6. Exit")  # Added Exit option
    
    choice = input("Enter your choice: ")
    
    if choice == '1':
        # Get user input for prediction
        job_title = input("Enter job title (Software Engineering, Data Scientist, AI/ML): ")
        skills_input = input("Enter skills (separate by semicolon): ")
        
        # Convert input skills to binary features
        skills_list = [skill.strip() for skill in skills_input.split(';')]
        skills_binary = mlb.transform([skills_list])
        input_data = pd.DataFrame(skills_binary, columns=mlb.classes_)

        # Train Random Forest on the full dataset (combined) for prediction
        model_rf_full = RandomForestRegressor(n_estimators=100, random_state=42)
        model_rf_full.fit(X_filtered, y)

        # Predict salary
        salary_prediction = model_rf_full.predict(input_data)
        print(f"Predicted Salary: ${salary_prediction[0]:,.2f}")
    
    elif choice == '2':
        # Print top 5 features for each job title
        for job, features in top_5_features_by_job.items():
            print(f"\nTop 5 Features for {job} Salary Prediction:")
            print(features[['Feature', 'Importance']])
    
    elif choice == '3':
        # Show salary distribution histogram
        plt.figure(figsize=(8, 6))
        sns.histplot(df_combined['Salary'], kde=True, color='blue', bins=30)
        plt.title("Salary Distribution")
        plt.xlabel("Salary")
        plt.ylabel("Frequency")
        plt.show()
    
    elif choice == '4':
        # Show salary distribution by job role
        plt.figure(figsize=(8, 6))
        sns.boxplot(x="Title", y="Salary", data=df_combined, palette="Set2")
        plt.title("Salary Distribution by Job Role")
        plt.xlabel("Job Role")
        plt.ylabel("Salary")
        plt.show()
    
    elif choice == '5':
        # Display top 5 skills for each job title in a bar plot
        top_skills_by_job = get_top_5_skills(df_combined)
        top_skills_df = pd.DataFrame(top_skills_by_job).reset_index()
        top_skills_df = top_skills_df.melt(id_vars=["index"], var_name="Job Title", value_name="Frequency")
        top_skills_df.rename(columns={"index": "Skill"}, inplace=True)

        # Visualize the top 5 skills for each job title
        plt.figure(figsize=(10, 6))
        sns.barplot(x="Frequency", y="Skill", hue="Job Title", data=top_skills_df, palette="viridis")
        plt.title("Top 5 Skills for Each Job Title")
        plt.xlabel("Frequency")
        plt.ylabel("Skill")
        plt.legend(title="Job Title", loc="upper right")
        plt.show()
    
    elif choice == '6':
        print("Exiting...")
        return
    
    else:
        print("Invalid choice. Please try again.")
    
    menu()

# Start the menu
menu()
