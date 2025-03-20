# Project Report: Salary Prediction and Skill Importance Analysis

## 1. Description of the Project

This project aims to predict salaries for various job roles based on job-related attributes, such as required skills. The data is sourced from job postings across different platforms, and the main goal is to develop a machine learning model that can predict the salary of a given job based on these features. Additionally, the project explores the importance of different skills across various job roles in the fields of software engineering, data science, and AI.

## 2. How to Use

To use this tool install main.py file and filtered_data.csv from the github respository.If you wish to scrape data on your own then you can also download other scraper and preprocessing tools from the github repository.

### 2.1. Training

In the training phase, we used two models: Linear Regression and Random Forest Regressor. For Linear Regression, we trained the model using all the features from the transformed skill data and predicted the salary based on the skills present. For the Random Forest Regressor, we selected the top features using SelectKBest and trained the model on those selected features to predict salaries as well. Both models were trained on a training set created from a stratified split of the data to maintain the balance across job titles. After training, we evaluated the performance of both models using R-squared values on the training and test sets.

### 2.2. Inferencing

To use the trained models for making predictions, you can choose Option 1 from the menu. This option will prompt you to input variables such as job title, skills, and other relevant features. Once you provide the necessary information, the model will use the trained data to predict the salary based on the inputs you provide. It’s a simple and interactive way to make salary predictions with the trained models.

## 3. Data Collection
### 3.1. Used Tools
- **Selenium**: For handling dynamic content on websites.
- **Pandas**: For data manipulation and storage.
- **Regex**: For cleaning and extracting specific patterns from raw text data.
  Other libraries for data normalization such as normalizing State abbreviations and Salary.

### 3.2. Data Sources
- **flexjobs.com**
- **simplyjobs.com**

### 3.3. Collected Attributes
- **Job Title**: The position the job posting is advertising (e.g., Software Engineer, Data Scientist).
- **Skills**: The required skills listed in the job description (e.g., Python, SQL, Machine Learning).
- **Location**: Where the job is located (e.g., Remote, New York).
- **Salary**: The estimated or offered salary for the role.

### 3.4. Number of Data Samples
- **1700** data samples were collected for analysis.

## 4. Data Preprocessing
Data was preprocessed by normalizing all the features. First the Titles were split into three categories: Software Engineering, Data Science and AI/ML. Then the locations were normalized by using a library into a state abbreviations such as NY, CA or Remote.
Lastly the salary was normalized into a single integer value. Skills also were normalized and non freequent occuring skills were removing during the preprocessing step.
### 4.1. Data Cleaning
Data was cleaned by removing duplicates and dropping rows that have missing values.

### 4.2. Data Integration
Data was scraped from two job posting website using selenium library and saved into a csv file for further processing.

### 4.3. Data Ingestion
All the data was extracted from the csv library and saved into a dataframe data structure for further processing.

### 4.4. Data Description and Metadata Specification
## 4.4. Data Description and Metadata Specification

| **Title** | **Location** | **Skills** | **Salary** |
|-----------|--------------|------------|------------|
| AI/ML     | CA           | tensorflow; law; scala; pytorch; kotlin; spark; python; machine learning; ai; natural language processing | 137100.0 |
| AI/ML     | OH           | tensorflow; keras; aws; management; data mining; algorithms; ai; google cloud platform; python; prompt engineering; java; data science; experimental design; power bi; nosql; tableau; scala; research; computer science; pytorch; information technology; communication skills; spark; sql; stakeholder management; hadoop; machine learning; r | 116111.0 |
| AI/ML     | AZ           | warehouse experience; google suite; mac os; organizational skills; ai; english | 32000.0 |
| AI/ML     | NY           | communication skills; physical therapy; ai | 110000.0 |

## 5. Feature Engineering

In this step, several feature engineering strategies were applied to the dataset to improve the quality of the features used for predicting salary:

1. **Filtering Relevant Job Titles:** Only job titles related to Software Engineering, Data Science, and AI/ML were retained for the analysis to focus on the desired fields.
   
2. **Handling Missing Values:** Missing values in the 'Skills' column were replaced with an empty string to ensure no rows were dropped during the data preprocessing.

3. **Filtering Experience Keywords:** Experience-related keywords such as 'junior', 'senior', and 'mid-level' were removed from the 'Skills' column. This was done by splitting the skills string on semicolons and filtering out the experience-related terms, ensuring only relevant skills remain.

4. **Binary Transformation of Skills:** A `MultiLabelBinarizer` was used to transform the skills column into binary features, where each skill is represented by a binary value indicating its presence or absence in a job listing.

5. **Feature Selection:** `SelectKBest` was applied to select the top 30 most relevant features from the transformed skill set, based on their correlation with the target variable (Salary).

6. **Model Comparison:** After feature engineering, different models (Linear Regression and Random Forest Regressor) were trained using both all features and the selected features to assess performance and identify the most important factors influencing salary predictions.

## 6. Model Development and Evaluation

### 6.1. Train and Test Data Partition
The dataset was split into training and testing sets using a random 80/20 ratio. The training set was used to train the machine learning models, while the test set was held back for evaluating their generalization performance. Stratification was applied during the split to ensure balanced distribution of job titles across both sets.

### 6.2. Salary Prediction: Model-1

#### 6.2.1. Machine Learning Model
Model-1 utilized **Linear Regression** as the machine learning model. Linear Regression is a simple yet effective model for predicting continuous variables by establishing a linear relationship between the input features and the target variable (Salary).

#### 6.2.2. Input to Model
The input features for Model-1 included all the transformed skills, represented as binary features, and were derived from the **Skills** column after filtering and binary encoding. Additionally, the location feature was encoded as a binary variable.

#### 6.2.3. Size of Train Data
The training set consisted of 80% of the data, which amounted to approximately **X_train** rows, ensuring a substantial portion of the dataset was used for model training.

#### 6.2.4. Attributes to the Machine Learning Model
The attributes fed into the model included binary representations of skills, location, and any additional relevant features derived from the dataset.

#### 6.2.5. Performance with Training Data
The performance of Model-1 (Linear Regression) on the training data was **R² = 0.7391**, indicating that the model could explain 73.91% of the variance in the training set.

#### 6.2.6. Performance with Test Data
The performance of Model-1 on the test data was **R² = -14.0539**, which suggests that the model performed poorly on unseen data, possibly due to overfitting or the complexity of the problem.

### 6.3. Salary Prediction: Model-2

#### 6.3.1. Machine Learning Model
Model-2 used the **Random Forest Regressor**. This model is an ensemble method that combines multiple decision trees to make predictions. It tends to perform well on complex datasets by reducing overfitting compared to a single decision tree.

#### 6.3.2. Input to Model
The input features for Model-2 included the selected subset of skills derived through feature selection with **SelectKBest**. Only the top 30 most relevant skills were included for training this model, providing a more focused approach.

#### 6.3.3. Size of Train Data
Similar to Model-1, the training data for Model-2 was made up of 80% of the dataset, with approximately **X_train_sel** rows used for training.

#### 6.3.4. Attributes to the Machine Learning Model
The attributes fed into Model-2 were the binary representations of the selected skills, location (if encoded), and any other relevant features.

#### 6.3.5. Performance with Training Data
The Random Forest model performed well on the training data with **R² = 0.8658**, suggesting it could explain 86.58% of the variance in the training set.

#### 6.3.6. Performance with Test Data
On the test data, Model-2 achieved an **R² = 0.2028**, indicating that while the model performs well on the training data, its ability to generalize to new data is limited. This lower R² value suggests there is room for further improvement in the model.

## 7. Skill Importance

### 7.1. Description of the Exploited Feature Importance Techniques
In this analysis, the **Random Forest Regressor** was used to identify the importance of each skill in predicting salary. The model calculates feature importance by assessing how much each skill contributes to reducing the variance in the target variable (Salary). The feature importance is derived from the average decrease in impurity (Gini or entropy) for each skill across all decision trees in the forest. Higher importance values indicate that the skill is more influential in the salary prediction. The **Top 10 skills** were selected based on their relative importance as determined by the model.

### 7.2. Identified Important Skills for 5 Job Roles
The top 5 most important skills across all job categories (Software Engineering, Data Science, and AI/ML) are as follows:
![image](https://github.com/user-attachments/assets/69219ac8-0713-41d7-82b2-37458814b53d)
![image](https://github.com/user-attachments/assets/f209ee04-0fb8-4af1-b0b6-78d58a0975d5)
![image](https://github.com/user-attachments/assets/67283da9-772f-4c59-af69-81098cc435e9)


These skills were found to be the most influential in predicting the salaries for the given job categories, with "english" and "c++" being the top contributors.

## 8. Visualization

### 8.1. Histograms
![image](https://github.com/user-attachments/assets/25fbc69c-6976-430a-8446-678b659071b2)
As we can see most salaries are distributed between 100-150k with outliers being 50k and 250k.

### 8.2. Box Plots
![image](https://github.com/user-attachments/assets/addcfdc5-d844-4f25-841a-114bcf0f844d)

### 8.4. Bar Plots
![image](https://github.com/user-attachments/assets/7af0db94-5b8d-4b74-9d42-117c41f5f303)


## 9. Discussion and Conclusions

### 9.1. Project Findings
The analysis revealed several key trends. One of the most significant findings was that specific skills, such as "English" and "C++," had a high impact on salary predictions across various job roles, with "English" emerging as the most influential feature. This suggests that soft skills, alongside technical expertise, play a crucial role in salary determination. Additionally, skills like "reinforcement learning" and "deep learning" were important for positions in AI and Machine Learning, while "communication skills" appeared consistently important across roles. However, the high number of features, driven by the diversity of skills across job postings, posed challenges for building an effective predictive model.

### 9.2. Challenges Encountered
Several challenges arose throughout the project. One of the most significant issues was the lack of comprehensive information on job listings from websites. The data often contained incomplete or inconsistent details, making it difficult to extract reliable features for model development. Moreover, some job pages would show results from previous pages when navigating to a new page, leading to repeated and redundant data. This further complicated data cleaning and preprocessing. Additionally, each job posting often had a unique set of skills, which led to a massive feature set when one-hot encoding. This large number of features made the model more complex and harder to train, despite the use of feature selection techniques such as PCA and SelectKBest.

### 9.3. Recommendations for Improving the Performance of the Model
To improve the model’s performance in future iterations, a few recommendations can be made. First, it would be beneficial to obtain a much larger dataset—at least 100,000 data points—to provide the model with more varied examples and improve its generalization capabilities. With a larger dataset, the model would have more training instances to better learn the relationships between job skills and salaries. Additionally, reducing the feature space by more effectively grouping similar skills or eliminating infrequent ones could help mitigate the overfitting caused by the large number of features. Another approach could be to use more advanced models, such as gradient boosting or neural networks, which can handle larger, more complex feature sets better than linear models or random forests. Overall, improving data quality and increasing the dataset size will likely be critical steps to building a more accurate and reliable salary prediction model.

