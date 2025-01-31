import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import folium
from folium.plugins import HeatMap
import geopandas as gpd

# Title of the app
st.title("Kenya Maandamano Visualisations")

# Description text
st.write("Welcome to the visualization of maandamano (demonstrations) incidents in Kenya.")

# Upload CSV file
csv_file = 'data/2024-01-01-2025-01-07-Eastern_Africa-Kenya.csv'

# Read CSV data
data = pd.read_csv(csv_file)

# Initialize the map
m = leafmap.Map(center=[-1.2921, 36.8219], zoom=6)  # Coordinates of Kenya

# Prepare the data for visualization
incident_locations = []

# Assuming the CSV contains latitude and longitude columns, we collect the locations
if 'latitude' in data.columns and 'longitude' in data.columns:
    for index, row in data.iterrows():
        lat, lon = row['latitude'], row['longitude']
        incident_locations.append([lat, lon])

# Load Kenya county boundaries from the shapefile
shapefile_path = 'data/kenyacountyboundariesshapefile/Kenya_county_dd.shp'
gdf = gpd.read_file(shapefile_path)

# Add Kenya's county boundaries to the map
folium.GeoJson(gdf).add_to(m)

# Set default basemap to "Google Hybrid"
map_type = st.selectbox(
    "Select a Basemap",
    ("Satellite", "Google Hybrid", "Topographic"),
    index=1  # Default to "Google Hybrid"
)

# Set basemap based on selection
if map_type == "Satellite":
    m.add_basemap("Esri.WorldImagery")
elif map_type == "Google Hybrid":
    m.add_basemap("GoogleHybrid")
elif map_type == "Topographic":
    m.add_basemap("Esri.WorldTopoMap")

# Set default visualization type to "Heatmap"
visualization_type = st.radio(
    "Select Visualization Type",
    ("Bubble Map", "Heatmap"),
    index=1  # Default to "Heatmap"
)

# Add selected visualization to the map
if visualization_type == "Bubble Map":
    for location in incident_locations:
        # Adjust circle size and color based on incident frequency or location
        radius = 5  # Adjust based on your data (e.g., number of incidents)
        color = "blue"  # You can modify this to use different colors based on location or event type
        folium.CircleMarker(location=location, radius=radius, color=color, fill=True, fill_color=color, fill_opacity=0.6).add_to(m)
elif visualization_type == "Heatmap":
    HeatMap(incident_locations).add_to(m)

# Display the map
st.write("Map of Maandamano Incidents in Kenya:")
m.to_streamlit(width=700, height=500)

# Display the first few rows of the data
st.write("Here is a preview of the data:")
st.write(data.head())

# Display the column names to help identify the issue
st.write("Columns in the CSV file:")
st.write(data.columns)
