# ----------------------------------------------------------
# SpaceX Rocket Launch Data Project Script 3
# Purpose: Perform Data wrangling and generate landing class labels
# Key Concepts: value_counts analysis, classification label generation, data export
# Author: Harry.Zhang
# ----------------------------------------------------------

import pandas as pd  # For data processing
import numpy as np   # For numerical operations

# Load the dataset saved from previous step
df = pd.read_csv("dataset_part_1.csv")

# Preview the first few rows
print(df.head(10))

# Display percentage of missing values
print("Percentage of missing values:")
print(df.isnull().sum() / len(df) * 100)

# Display column data types
print("Column data types:")
print(df.dtypes)

# ----------------------------------------------------------
# TASK 1: Count launches per Launch Site
# ----------------------------------------------------------
launch_counts = df['LaunchSite'].value_counts()
print("Launch counts by Launch Site:")
print(launch_counts)

# ----------------------------------------------------------
# TASK 2: Count launches per Orbit
# ----------------------------------------------------------
orbit_counts = df['Orbit'].value_counts()
print("Launch counts by Orbit:")
print(orbit_counts)

# ----------------------------------------------------------
# TASK 3: Count outcome appearances
# ----------------------------------------------------------
landing_outcomes = df['Outcome'].value_counts()
print("Landing outcome counts:")
print(landing_outcomes)

# Enumerate outcome labels with their index
for i, outcome in enumerate(landing_outcomes.keys()):
    print(i, outcome)

# Identify outcomes considered as failures (indexes may vary per execution)
# Modify index list below based on your printed result
bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])
print("Outcomes considered as failures:")
print(bad_outcomes)

# ----------------------------------------------------------
# TASK 4: Create 'Class' column (1 = success, 0 = failure)
# ----------------------------------------------------------
landing_class = []
for outcome in df['Outcome']:
    if outcome in bad_outcomes:
        landing_class.append(0)
    else:
        landing_class.append(1)
df['Class'] = landing_class

# Preview classification results
print("Landing outcome and class labels:")
print(df[['Outcome', 'Class']].head(8))

# Calculate and print success rate
success_rate = df['Class'].mean()
print("Overall success rate:", success_rate)

# Save the modified dataset to CSV
df.to_csv("dataset_part_2.csv", index=False)
print("Cleaned data with landing class saved to dataset_part_2.csv")
