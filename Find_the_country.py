# Program is sending longitude and latitute to Bing / Google API and API is sending back information about what country it is. 
# If the location is not found, it's skipped and the next location is beeing loaded

import json
import os
import requests
from typing import Dict
import xml.etree.ElementTree as ET
import asyncio

async def main():
    path = "your_json_file.json" # PASTE YOUR JSON FILE WITH LOCATIONS HERE
    if not os.path.exists(path):
        print(f"No file at {path}") 
        return
    

    with open(path, 'r') as f:
        json_data = f.read()
    array = json.loads(json_data)

    list = []

    noumberOfCountries = {}

    for item in array:
        latitude = item["lat"]
        longitude = item["lng"]
        name = await get_country(latitude, longitude)

        if name is None:
            print(f"Failed to read country at lat: {latitude: <20} lng: {longitude: <20}")
            list.append((latitude, longitude))
            continue

        print(f"lat: {latitude: <20} lng: {longitude: <20} => {name}")

        if name in noumberOfCountries:
            noumberOfCountries[name] += 1
        else:
            noumberOfCountries[name] = 1

    print("Found countries:")
    for item in noumberOfCountries.items():
        print(f"- {item[0]}: {item[1]}")
    
    print("Nie znalezione koordynaty: ")

    for i in list:
        print(i)


async def get_country(latitude: float, longitude: float) -> str:
    KEY = "key_code" # PASTE YOUR BING OR GOOGLE API KEY HERE
    url = f"http://dev.virtualearth.net/REST/v1/Locations/{latitude},{longitude}?o=xml&key={KEY}"
    response = requests.get(url)
    xml = response.content.decode('utf-8')
    ns = {"rest": "http://schemas.microsoft.com/search/local/ws/rest/v1"}

    root = ET.fromstring(xml)
    try:
        countryName = root.find(".//rest:CountryRegion", ns).text
    except:
        return None
    
    if countryName is not None:
        return countryName

   
    return None
 

if __name__ ==  "__main__":
    asyncio.run(main())




 
 
