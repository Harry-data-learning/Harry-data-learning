# ----------------------------------------------------------
# SpaceX Rocket Launch Data Project Script 4
# Purpose: Build SQLite database, load CSV data, run SQL queries (Jupyter & native)
# Key Concepts: sqlite3 operations, pandas-SQL integration, query demonstrations
# Author: Harry.Zhang
# ----------------------------------------------------------

import sqlite3
import pandas as pd
import os

# Load CSV data
csv_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"
df = pd.read_csv(csv_url)
print("Preview of CSV data:")
print(df.head())

# Create SQLite database
db_file = "my_data1.db"
if os.path.exists(db_file):
    os.remove(db_file)

conn = sqlite3.connect(db_file)
cur = conn.cursor()

# Write to table
df.to_sql("SPACEXTBL", conn, if_exists='replace', index=False, method="multi")
print("Data loaded into table 'SPACEXTBL'")

# Create filtered table (non-null Date)
cur.execute("DROP TABLE IF EXISTS SPACEXTABLE")
conn.commit()
cur.execute("""
    CREATE TABLE SPACEXTABLE AS 
    SELECT * FROM SPACEXTBL 
    WHERE Date IS NOT NULL
""")
conn.commit()
print("Filtered table 'SPACEXTABLE' created")

# Preview
rows = cur.execute("SELECT * FROM SPACEXTABLE LIMIT 5").fetchall()
print("\nPreview rows from SPACEXTABLE:")
for row in rows:
    print(row)

# -----------------------------------------------
# Additional SQL queries (equivalent to %sql notebook usage)
# -----------------------------------------------

print("\nRunning example SQL queries:\n")

queries = [
    ("Unique Launch Sites", "SELECT DISTINCT LaunchSite FROM SPACEXTABLE"),
    ("Launches from CCA sites", "SELECT * FROM SPACEXTABLE WHERE LaunchSite LIKE 'CCA%' LIMIT 5"),
    ("Total Payload by NASA (CRS)", "SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEXTABLE WHERE Customer = 'NASA (CRS)'"),
    ("Avg Payload for F9 v1.1", "SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTABLE WHERE BoosterVersion = 'F9 v1.1'"),
    ("Earliest ground pad landing", "SELECT MIN(Date) FROM SPACEXTABLE WHERE Landing_Outcome = 'Success (ground pad)'"),
    ("Boosters with 4000-6000kg Payload & success on drone ship", 
     "SELECT BoosterVersion FROM SPACEXTABLE WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000"),
    ("Landing outcome counts", "SELECT Landing_Outcome, COUNT(*) FROM SPACEXTABLE GROUP BY Landing_Outcome"),
    ("Booster with max payload", 
     "SELECT BoosterVersion, PAYLOAD_MASS__KG_ FROM SPACEXTABLE WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTABLE)"),
    ("Monthly launches in 2015", 
     "SELECT substr(Date,6,2) AS Month, Landing_Outcome, BoosterVersion, LaunchSite FROM SPACEXTABLE WHERE substr(Date,1,4) = '2015'"),
    ("Landing outcomes between dates (2010-06-04 ~ 2017-03-20)",
     "SELECT Landing_Outcome, COUNT(*) FROM SPACEXTABLE WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY COUNT(*) DESC")
]

for desc, q in queries:
    print(f"-- {desc} --")
    result = cur.execute(q).fetchall()
    for row in result:
        print(row)
    print()

# Close connection
conn.close()
print("\nDatabase connection closed.")
