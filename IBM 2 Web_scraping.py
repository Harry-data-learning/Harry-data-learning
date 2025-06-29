# ----------------------------------------------------------
# SpaceX Rocket Launch Data Project Script 2
# Purpose: Scrape Falcon 9 launch records from Wikipedia using BeautifulSoup
# Steps: HTML request → parse table → fill dictionary → convert to DataFrame → save as CSV
# Author: Harry.Zhang
# ----------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd

# Helper function: extract date and time from table cell
def date_time(table_cells):
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

# Helper function: extract booster version string
def booster_version(table_cells):
    out = ''.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i % 2 == 0][0:-1])
    return out

# Helper function: extract landing status from cell
def landing_status(table_cells):
    out = [i for i in table_cells.strings][0]
    return out

# Helper function: clean payload mass value (extract in kg)
def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass = mass[0:mass.find("kg") + 2]
    else:
        new_mass = 0
    return new_mass

# Helper function: extract and clean column name from header
def extract_column_from_header(row):
    if row.br:
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
    colunm_name = ' '.join(row.contents)
    if not (colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name

# Request HTML from static Wikipedia snapshot
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
response = requests.get(static_url)

# Create BeautifulSoup object to parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Print page title to verify successful loading
print("Page title:", soup.title.string)

# Extract all tables from page
html_tables = soup.find_all('table')

# Select the 3rd table (target launch data table)
first_launch_table = html_tables[2]
print("Preview of launch table structure:")
print(first_launch_table)

# Extract column names
column_names = []
for th in first_launch_table.find_all('th'):
    name = extract_column_from_header(th)
    if name is not None and len(name) > 0:
        column_names.append(name)

print("Extracted column names:")
print(column_names)

# Create initial launch dictionary from column names
launch_dict = dict.fromkeys(column_names)

# Remove undesired column if exists
if 'Date and time ( )' in launch_dict:
    del launch_dict['Date and time ( )']

# Initialize all fields as empty lists
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
launch_dict['Version Booster'] = []
launch_dict['Booster landing'] = []
launch_dict['Date'] = []
launch_dict['Time'] = []

# Loop through all target tables and extract row data
extracted_row = 0
for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
    for rows in table.find_all("tr"):
        if rows.th:
            if rows.th.string:
                flight_number = rows.th.string.strip()
                flag = flight_number.isdigit()
        else:
            flag = False

        row = rows.find_all('td')
        if flag:
            extracted_row += 1

            launch_dict['Flight No.'].append(flight_number)

            datatimelist = date_time(row[0])
            date = datatimelist[0].strip(',')
            time = datatimelist[1]
            launch_dict['Date'].append(date)
            launch_dict['Time'].append(time)

            bv = booster_version(row[1])
            if not bv:
                bv = row[1].a.string
            launch_dict['Version Booster'].append(bv)

            launch_site = row[2].a.string
            launch_dict['Launch site'].append(launch_site)

            payload = row[3].a.string
            launch_dict['Payload'].append(payload)

            payload_mass = get_mass(row[4])
            launch_dict['Payload mass'].append(payload_mass)

            orbit = row[5].a.string
            launch_dict['Orbit'].append(orbit)

            customer = row[6].a.string
            launch_dict['Customer'].append(customer)

            launch_outcome = list(row[7].strings)[0]
            launch_dict['Launch outcome'].append(launch_outcome)

            booster_landing = landing_status(row[8])
            launch_dict['Booster landing'].append(booster_landing)

# Convert dictionary to pandas DataFrame
df = pd.DataFrame({key: pd.Series(value) for key, value in launch_dict.items()})

# Show preview
print("Preview of constructed DataFrame:")
print(df.head())

# Save DataFrame to CSV
df.to_csv('spacex_web_scraped.csv', index=False)
print("Data saved to spacex_web_scraped.csv")
