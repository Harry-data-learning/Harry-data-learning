# -----------------------------------------------------
#  SpaceX Rocket Launch Data Project Script
# Purpose: Retrieve SpaceX API data using requests, clean and process with pandas, save to CSV
# Key Concepts: API requests, JSON parsing, pandas processing, missing value handling
# Author: Harry.Zhang
# -----------------------------------------------------

import requests  # For HTTP requests
import pandas as pd  # For data processing
import numpy as np  # For numerical operations and missing value handling
import datetime  # For working with date fields

# Set pandas display options to avoid truncation in output
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

# Step 1: Request SpaceX data from static JSON URL
static_json_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
response = requests.get(static_json_url)

# Check if request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
else:
    print("Request failed. Status code:", response.status_code)
    exit()

# Normalize JSON data into pandas DataFrame
df = pd.json_normalize(data)
print(df.head())

# Keep only selected columns of interest
data = df[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# Remove records with multiple payloads or cores
data = data[data['cores'].map(len) == 1]
data = data[data['payloads'].map(len) == 1]

# Extract the single element from payloads and cores list columns
data['cores'] = data['cores'].map(lambda x: x[0])
data['payloads'] = data['payloads'].map(lambda x: x[0])

# Convert date_utc to datetime and extract date only
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# Filter records with date before or equal to 2020-11-13
data = data[data['date'] <= datetime.date(2020, 11, 13)]

# Initialize global lists to store extracted values
BoosterVersion = []
Longitude = []
Latitude = []
LaunchSite = []
PayloadMass = []
Orbit = []
Block = []
ReusedCount = []
Serial = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []

# Fetch rocket name by rocket ID
def getBoosterVersion(data):
    for rocket_id in data['rocket']:
        if rocket_id:
            response = requests.get("https://api.spacexdata.com/v4/rockets/" + str(rocket_id)).json()
            BoosterVersion.append(response['name'])

# Fetch launchpad details (name, lat, lon) by ID
def getLaunchSite(data):
    for pad_id in data['launchpad']:
        if pad_id:
            response = requests.get("https://api.spacexdata.com/v4/launchpads/" + str(pad_id)).json()
            Longitude.append(response['longitude'])
            Latitude.append(response['latitude'])
            LaunchSite.append(response['name'])

# Fetch payload mass and orbit by payload ID
def getPayloadData(data):
    for payload_id in data['payloads']:
        if payload_id:
            response = requests.get("https://api.spacexdata.com/v4/payloads/" + str(payload_id)).json()
            PayloadMass.append(response.get('mass_kg'))
            Orbit.append(response.get('orbit'))

# Fetch core-related information
def getCoreData(data):
    for core in data['cores']:
        if core.get('core') is not None:
            response = requests.get("https://api.spacexdata.com/v4/cores/" + str(core['core'])).json()
            Block.append(response.get('block'))
            ReusedCount.append(response.get('reuse_count'))
            Serial.append(response.get('serial'))
        else:
            Block.append(None)
            ReusedCount.append(None)
            Serial.append(None)
        Outcome.append(str(core.get('landing_success')) + ' ' + str(core.get('landing_type')))
        Flights.append(core.get('flight'))
        GridFins.append(core.get('gridfins'))
        Reused.append(core.get('reused'))
        Legs.append(core.get('legs'))
        LandingPad.append(core.get('landpad'))

# Execute API fetch functions
getBoosterVersion(data)
getLaunchSite(data)
getPayloadData(data)
getCoreData(data)

# Construct final DataFrame with all extracted information
launch_dict = {
    'FlightNumber': list(data['flight_number']),
    'Date': list(data['date']),
    'BoosterVersion': BoosterVersion,
    'PayloadMass': PayloadMass,
    'Orbit': Orbit,
    'LaunchSite': LaunchSite,
    'Outcome': Outcome,
    'Flights': Flights,
    'GridFins': GridFins,
    'Reused': Reused,
    'Legs': Legs,
    'LandingPad': LandingPad,
    'Block': Block,
    'ReusedCount': ReusedCount,
    'Serial': Serial,
    'Longitude': Longitude,
    'Latitude': Latitude
}

launch_df = pd.DataFrame(launch_dict)
print(launch_df.head())

# Filter out Falcon 1 flights
data_falcon9 = launch_df[launch_df['BoosterVersion'] != 'Falcon 1'].copy()

# Reset flight number starting from 1
data_falcon9.loc[:, 'FlightNumber'] = list(range(1, data_falcon9.shape[0] + 1))

# Check for missing values
print(data_falcon9.isnull().sum())

# Compute mean PayloadMass and fill missing values
payload_mean = data_falcon9['PayloadMass'].mean()
print("Average PayloadMass:", payload_mean)
data_falcon9['PayloadMass'].fillna(payload_mean, inplace=True)

# Re-check for missing values
print(data_falcon9.isnull().sum())

# Save final cleaned dataset to CSV
data_falcon9.to_csv('dataset_part_1.csv', index=False)
print("Cleaned data saved to dataset_part_1.csv")

