# Title: meteor_map.py
# Name: Alec Lahey
# Description: This file reads data from a CSV file containing information about meteorite landings, extracts relevant fields 
#              (year and GeoLocation), processes the data to filter out invalid records and separate latitude and longitude values.
#              The map includes markers for each meteorite landing location, with markers clustered when close together. A map is generated 
#              using the Folium library to visualize the meteorite landings. The map is saved as an HTML file for further viewing or embedding in web pages.





import csv
import folium
from folium.plugins import MarkerCluster

filename = 'Meteorite_Landings.csv'

keys = ('year', 'GeoLocation')
records = []

with open(filename, 'r') as datafile:
    reader = csv.DictReader(datafile)
    for row in reader:
        records.append({key: row[key] for key in keys})
 

#seperating longitude and latitude values and assigning to their own variables
for record in records:
    
    #If record is not empty or zeros (invalid) assign the variable to the appropiate
    #attribute in the array
    if(record['GeoLocation']!= '' and record['GeoLocation']!= '(0.0, 0.0)'):
        long, lat = record['GeoLocation'][1:-1].split(", ")
        record['longitude'] = float(long)
        record['latitude'] = float(lat)

    else:
        #if the record is invalid, remove it from the array
        records.remove(record)


#On luanch the map will be centered
map = folium.Map(location=[0,0], zoom_start=2)

#Editing the appearance of the map
folium.TileLayer('cartodbdark_matter').add_to(map)


#Creating a marker cluster and adding it to the map
#Marker clusters group markers together when they are close to eachother
#Markers can then be individually clicked when zoomed in
marker_cluster = MarkerCluster().add_to(map)

#Looping through the records
#Assigning longitude and latitude to a single variable
#Assigning a year to the marker popup and editing the marker icon
for record in records:

    if 'latitude' in record and 'longitude' in record:
        
        coords = (record['longitude'],record['latitude'])

        if(record['year']==''):
            folium.Marker(location=coords,popup="Year Unknown" ,icon=folium.Icon(color="red", prefix="fa", icon="meteor")).add_to(marker_cluster)
        else:
            folium.Marker(location=coords,popup="Year: "+record['year'],icon=folium.Icon(color="red", prefix="fa", icon="meteor")).add_to(marker_cluster)

#Adding marker clusters to the map
marker_cluster.add_to(map)

#Saving the map to an HTML file
map.save("meteor_map.html")


