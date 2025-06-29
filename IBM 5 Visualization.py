# ----------------------------------------------------------
# SpaceX Rocket Launch Data Project Script 5
# Purpose: Perform EDA visualizations using seaborn & matplotlib
# Key Concepts: scatter plots, bar charts, trend lines, one-hot encoding
# Author: Harry.Zhang
# ----------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set seaborn style
sns.set(style="whitegrid")

# Load dataset
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

# Task 1: Flight Number vs Launch Site
plt.figure(figsize=(12, 6))
sns.catplot(x="FlightNumber", y="LaunchSite", hue="Class", data=df, kind="scatter", aspect=2)
plt.xlabel("Flight Number", fontsize=14)
plt.ylabel("Launch Site", fontsize=14)
plt.title("Flight Number vs Launch Site by Class")
plt.tight_layout()
plt.savefig("task1_flight_vs_launchsite.png")
plt.close()

# Task 2: Payload Mass vs Launch Site
plt.figure(figsize=(10, 6))
sns.scatterplot(x="PayloadMass", y="LaunchSite", hue="Class", data=df)
plt.xlabel("Payload Mass (kg)", fontsize=14)
plt.ylabel("Launch Site", fontsize=14)
plt.title("Payload Mass vs Launch Site by Class")
plt.tight_layout()
plt.savefig("task2_payload_vs_launchsite.png")
plt.close()

# Task 3: Success rate by Orbit
orbit_success = df.groupby("Orbit")["Class"].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x="Orbit", y="Class", data=orbit_success)
plt.xlabel("Orbit Type", fontsize=14)
plt.ylabel("Success Rate", fontsize=14)
plt.title("Success Rate by Orbit Type")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("task3_success_by_orbit.png")
plt.close()

# Task 4: Flight Number vs Orbit
plt.figure(figsize=(12, 6))
sns.scatterplot(x="FlightNumber", y="Orbit", hue="Class", data=df)
plt.xlabel("Flight Number", fontsize=14)
plt.ylabel("Orbit", fontsize=14)
plt.title("Flight Number vs Orbit by Class")
plt.tight_layout()
plt.savefig("task4_flight_vs_orbit.png")
plt.close()

# Task 5: Payload Mass vs Orbit
plt.figure(figsize=(12, 6))
sns.scatterplot(x="PayloadMass", y="Orbit", hue="Class", data=df)
plt.xlabel("Payload Mass (kg)", fontsize=14)
plt.ylabel("Orbit", fontsize=14)
plt.title("Payload Mass vs Orbit by Class")
plt.tight_layout()
plt.savefig("task5_payload_vs_orbit.png")
plt.close()

# Task 6: Yearly success trend
df['Year'] = df['Date'].apply(lambda x: int(x.split("-")[0]))
yearly_success = df.groupby("Year")["Class"].mean().reset_index()
plt.figure(figsize=(10, 6))
plt.plot(yearly_success["Year"], yearly_success["Class"], marker='o')
plt.xlabel("Year", fontsize=14)
plt.ylabel("Success Rate", fontsize=14)
plt.title("Launch Success Trend by Year")
plt.grid(True)
plt.tight_layout()
plt.savefig("task6_success_trend_by_year.png")
plt.close()

# Task 7: One-hot encode categorical variables
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'LandingPad',
               'GridFins', 'Reused', 'Legs', 'Block', 'ReusedCount', 'Serial']]
features_one_hot = pd.get_dummies(features, columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])

# Task 8: Convert to float64 and save as CSV
features_one_hot = features_one_hot.astype('float64')
features_one_hot.to_csv("dataset_part_3.csv", index=False)
print("dataset_part_3.csv successfully saved")
print("All charts saved as .png files in current directory")
