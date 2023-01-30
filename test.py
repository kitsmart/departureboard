import csv

results = []
final_all_platforms = []

with open('stations.csv', newline='') as f:
    pltfms = csv.reader(f)
    for row in pltfms:
        results.append(row)

del results[0]

for i in range(len(results)):
    pltfms = str(results[i][2]).split("/")

    for j in range(len(pltfms)):
        temp_tup = str(pltfms[j]).split("|")
        pltfms[j] = temp_tup

    actual_plats = []
    actual_plats.append(results[i][0])
    actual_plats.append(results[i][1])
    actual_plats.append(pltfms)
    final_all_platforms.append(actual_plats)

pltfms = final_all_platforms

for i in range(len(pltfms)):
    print("Station ID:", pltfms[i][0])
    print("Station name:", pltfms[i][1])
    for j in range(len(pltfms[i][2])):
        print("Line:", pltfms[i][2][j][0])
        print("Platform:", pltfms[i][2][j][1])