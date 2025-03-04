import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.metrics import r2_score
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

# Create a MultiLabelBinarizer to transform skills into binary features
mlb = MultiLabelBinarizer()
X = df_combined[['Skills']]
y = df_combined['Salary']

# Transform skills
temp_df = pd.DataFrame(mlb.fit_transform(X['Skills']), columns=mlb.classes_, index=X.index)

# Remove numerical features
filtered_columns = [col for col in temp_df.columns if not re.match(r'^\d+$', col)]
X_filtered = temp_df[filtered_columns]

# Train-test split (ensuring stratification for balanced classes)
X_train, X_test, y_train, y_test = train_test_split(
    X_filtered, y, test_size=0.2, random_state=42, stratify=df_combined['Title']
)

# Model-1: Linear Regression on All Features
model_1 = LinearRegression()
model_1.fit(X_train, y_train)
y_train_pred_1 = model_1.predict(X_train)
y_test_pred_1 = model_1.predict(X_test)
train_r2_1 = r2_score(y_train, y_train_pred_1)
test_r2_1 = r2_score(y_test, y_test_pred_1)

# Feature Selection using SelectKBest (Increase k to select more features)
selector = SelectKBest(score_func=f_regression, k=30)  # Increase k to 30
X_new = selector.fit_transform(X_filtered, y)
selected_features = [filtered_columns[i] for i in selector.get_support(indices=True)]

# Train-test split with selected features
X_train_sel, X_test_sel, y_train_sel, y_test_sel = train_test_split(
    X_filtered[selected_features], y, test_size=0.2, random_state=42, stratify=df_combined['Title']
)

# Model-2: Random Forest Regressor on Selected Features
model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
model_rf.fit(X_train, y_train)
y_train_pred_rf = model_rf.predict(X_train)
y_test_pred_rf = model_rf.predict(X_test)
train_r2_rf = r2_score(y_train, y_train_pred_rf)
test_r2_rf = r2_score(y_test, y_test_pred_rf)

# Display Results
print("Salary Prediction: Model-1 (All Features) - Linear Regression")
print(f"Training Data: R^2 = {train_r2_1:.4f}")
print(f"Test Data: R^2 = {test_r2_1:.4f}\n")

print("Salary Prediction: Model-2 (Selected Features) - Random Forest Regressor")
print(f"Training Data: R^2 = {train_r2_rf:.4f}, Test Data: R^2 = {test_r2_rf:.4f}")

# Extract feature importances for Random Forest
importances = model_rf.feature_importances_
feature_importances_df = pd.DataFrame({
    'Feature': filtered_columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

# Top 25 most important features
top_25_features = feature_importances_df.head(25)

# Bar plot for Top 25 Features
def plot_top_25_features():
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Importance', y='Feature', data=top_25_features, palette='viridis')
    plt.title('Top 25 Most Important Features for Salary Prediction')
    plt.xlabel('Feature Importance')
    plt.ylabel('Features')
    plt.show()

# Menu options
def menu():
    print("\nMenu:")
    print("1. Predict Salary")
    print("2. Print Top 10 Features")
    print("3. View Salary Distribution (Histogram)")
    print("4. View Salary Distribution by Job Role (Box Plot)")
    print("5. View Bar Plot of Top 25 Features")
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

        # Predict salary
        salary_prediction = model_rf.predict(input_data)
        print(f"Predicted Salary: ${salary_prediction[0]:,.2f}")
    
    elif choice == '2':
        # Print top 10 features
        print("\nTop 10 features:")
        print(top_25_features[['Feature', 'Importance']].head(10))
    
    elif choice == '3':
        # Display salary distribution histogram
        plt.figure(figsize=(10,6))
        sns.histplot(y_test_pred_rf, kde=True, color="skyblue")
        plt.title('Salary Distribution for Predicted Salaries')
        plt.xlabel('Predicted Salary')
        plt.ylabel('Frequency')
        plt.show()
    
    elif choice == '4':
        # Display salary distribution by job role (box plot)
        plt.figure(figsize=(10,6))
        sns.boxplot(x='Title', y='Salary', data=df_combined)
        plt.title('Salary Distribution across Job Roles')
        plt.xlabel('Job Title')
        plt.ylabel('Salary')
        plt.show()
    
    elif choice == '5':
        # Show the top 25 features bar plot
        plot_top_25_features()
    
    elif choice == '6':
        print("Exiting...")
        return
    
    else:
        print("Invalid choice. Please try again.")
    
    menu()

# Start the menu
menu()
