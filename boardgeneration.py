import requests
import json
from operator import itemgetter
import pandas as pd
from datetime import datetime
import csv

class DepBoard:
    def __init__(self, transport_type):
        self.transport_type = transport_type.lower()

    def sanitise_data(self):
        
        transport_dict = { 
            "underground" : "stations/ug_stations.csv",
            "dlr" : "stations/dlr_stations.csv"
        }

        results = []
        final_all_platforms = []

        with open(transport_dict[self.transport_type], newline='') as f:
            pltfms = csv.reader(f)
            for row in pltfms:
                results.append(row) # Create 2d array out of CSV file

        del results[0] # Remove table headers

        
        for i in range(len(results)):
            pltfms = str(results[i][2]).split("/") # Separate platforms within stations

            for j in range(len(pltfms)):
                temp_tup = str(pltfms[j]).split("|") # Separate line from platform
                pltfms[j] = temp_tup # Store each line and platform pair together as 2d list entry


            actual_plats = []
            actual_plats.append(results[i][0])
            actual_plats.append(results[i][1])
            actual_plats.append(pltfms)
            final_all_platforms.append(actual_plats) # Merging into one list

        print(final_all_platforms)

        return final_all_platforms

    def departure_board_create(self, station, pltfrm, line, url):
        current_dp = requests.get(url).content # Makes initial request to server to get TFL data
        current_dp = json.loads(current_dp) # Deserialize into py dictionary

        good_deps = [] # This initialises the list where the relevant departures will be stored
        trains_to_display = []

        print("\n\nDepartures for", station+":", pltfrm, line, "line:")
        print("\n------------------------------------------------------\n\n")

        for train in current_dp: # Loop through dictionary to check for only departures that contain the line and platform needed
            if train["platformName"] == pltfrm and train["lineName"] == line:
                good_deps.append(train)

        for i in range(len(good_deps)):
            # Setting current time in the format gathered from TFL
            time_offset = 1
            now = datetime.now()
            now = str(now - pd.DateOffset(hours=time_offset))
            now = now[11:-7]

            # Time from TFL of next train arrival
            cdown = good_deps[i]["expectedArrival"]
            cdown = cdown[11:-1]
            cdown = datetime.strptime(cdown, "%H:%M:%S")
            now = datetime.strptime(now, "%H:%M:%S")

            # Calculate time remaining
            interval = cdown - now
            interval = str(interval)[2:-3]

            try:
                interval = int(interval)
                trains_to_display.append([interval, str(good_deps[i]["towards"])]) # Format to have terminus on board
            except ValueError:
                pass # Simple error handling

        trains_to_display = sorted(trains_to_display, key=itemgetter(0)) # Sort to get trains into chronological order

        for i in range(len(trains_to_display)):
            if trains_to_display[i][0] < 1:
                trains_to_display[i][0] = '<1'
            print(trains_to_display[i][0], "min", trains_to_display[i][1])