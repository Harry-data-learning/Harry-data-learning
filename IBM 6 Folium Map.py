# ----------------------------------------------------------
# SpaceX Rocket Launch Data Project Script 6
# Purpose: Visualize launch site and success/failure markers using Folium
# Key Concepts: marker clusters, dynamic color icons, distance lines, coordinate tracking
# Author: Harry.Zhang
# ----------------------------------------------------------

import pandas as pd
import folium
from folium.plugins import MarkerCluster, MousePosition
from folium.features import DivIcon
from math import sin, cos, sqrt, atan2, radians

# Load launch data (CSV must be downloaded and placed locally)
spacex_df = pd.read_csv("spacex_launch_geo.csv")

# Compute center coordinates for each launch site
launch_sites_df = spacex_df.groupby('Launch Site', as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]

# Initialize base map centered on NASA JSC
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

# Add circular markers and text labels for each launch site
for index, row in launch_sites_df.iterrows():
    lat, lon, site = row['Lat'], row['Long'], row['Launch Site']
    folium.Circle([lat, lon], radius=1000, color='blue', fill=True).add_child(folium.Popup(site)).add_to(site_map)
    folium.map.Marker(
        [lat, lon],
        icon=DivIcon(icon_size=(20,20), icon_anchor=(0,0),
                     html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % site)
    ).add_to(site_map)

# Add markers for all launches, colored by success/failure
marker_cluster = MarkerCluster().add_to(site_map)
spacex_df['marker_color'] = spacex_df['class'].apply(lambda x: 'green' if x == 1 else 'red')

for index, record in spacex_df.iterrows():
    folium.Marker(
        location=[record['Lat'], record['Long']],
        icon=folium.Icon(color=record['marker_color'])
    ).add_to(marker_cluster)

# Add coordinate reader tool
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright', separator=' Long: ',
    prefix='Lat:', lat_formatter=formatter, lng_formatter=formatter)
site_map.add_child(mouse_position)

# Distance calculation function (Haversine formula)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Example: draw distance from LC-40 to coastline
launch_site_lat, launch_site_lon = 28.562302, -80.577356
coastline_lat, coastline_lon = 28.56367, -80.57163
distance = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)

folium.Marker(
    [coastline_lat, coastline_lon],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%.2f KM</b></div>' % distance
    )
).add_to(site_map)

# Draw connecting line
lines = folium.PolyLine(locations=[[launch_site_lat, launch_site_lon], [coastline_lat, coastline_lon]], weight=2)
site_map.add_child(lines)

# Export map to HTML
site_map.save('spacex_launch_map.html')
print("Map saved as spacex_launch_map.html. Open it in a browser to view.")
