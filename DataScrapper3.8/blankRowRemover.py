import csv
allPlayer = []
with open('CSGOData.csv', encoding="utf-8") as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        if len(row) == 0:
            print("hi")
        else:
            allPlayer.append(row)

with open('CSGODataNoSpace.csv', 'w', newline='', encoding="utf-8") as outfile:
    for row in allPlayer:
        writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(row)