import re
import time
import lxml
import csv
import requests
from bs4 import BeautifulSoup
from mechanize import Browser

counter = 0
allPlayer = dict()
with open('HLTV_Players.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        allPlayer[row[0]] = row[0]
        counter += 1
        if counter > 10:
            break
with open('CSGODATA.csv', 'w', newline='', encoding="utf-8") as outfile:
    for playerUrl in allPlayer:
        writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })

        b = Browser()
        b.set_handle_robots(False)
        b.addheaders = [('Referer', 'ttps://www.hltv.org'), ('User-agent',
                                                             'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        url = playerUrl
        b.open(url)
        soup = BeautifulSoup(b.response().read(), "lxml")
        g_data = soup.find_all("table", {"class": "stats-table no-sort"})

        playerName = soup.find("span", {"class": "context-item-name"})
        print(playerName.text)
        writer.writerow([playerName.text])
        writer.writerow(
            ["Player's Team", "Player's Opponent", "Rounds Won", "Rounds Lost", "Map", "Kills", "Deaths", "+/-",
             "Rating",
             "Outcome"])

        for child in (g_data[0].findChildren("tbody"))[0].find_all("tr"):
            mapPlayed = child.find("td", {"class": "statsMapPlayed"}).text
            winOrLost = "Nil"
            Kills = "Nil"
            Deaths = "Nil"
            playerRound = "Nil"
            OpponentRound = "Nil"
            playerPlusMinus = "Nil"
            playerRating = "Nil"
            CurrentTeam = "Nil"
            CurrentOpponent = "Nil"
            for a in (child.find_all('td')):
                if a.has_attr('class'):
                    if a['class'][0] == 'statsMapPlayed':
                        mapPlayed = a.text
                    if a['class'][0] == 'statsCenterText':
                        pos = a.text.find("-")
                        Kills = a.text[0:pos - 1]
                        Deaths = a.text[pos + 2:len(a.text)]
                    if a['class'][0] == 'gtSmartphone-only':
                        playerPlusMinus = a.text
                    if a['class'][0] == 'match-lost':
                        winOrLost = "Lost"
                        non_decimal = re.compile(r'[^\d.]+')
                        playerRating = non_decimal.sub('', a.text)
                    if a['class'][0] == 'match-won':
                        winOrLost = "Won"
                        non_decimal = re.compile(r'[^\d.]+')
                        playerRating = non_decimal.sub('', a.text)
                    if a['class'][0] == 'match-tied':
                        winOrLost = "Tied"
                        non_decimal = re.compile(r'[^\d.]+')
                        playerRating = non_decimal.sub('', a.text)
                    if a['class'][0] == 'match-not-yet-finished':
                        winOrLost = "Undecided"
                        non_decimal = re.compile(r'[^\d.]+')
                        playerRating = non_decimal.sub('', a.text)
                else:
                    theClass = a.find("img", {"class": "statsLogo"})
                    theRound = a.find_all("span")
                    if theClass != None:
                        if CurrentTeam == "Nil":
                            CurrentTeam = theClass["title"]
                            playerRound = re.sub('[()]', '', theRound[1].text)
                        else:
                            CurrentOpponent = theClass["title"]
                            OpponentRound = re.sub('[()]', '', theRound[1].text)
            writer.writerow(
                [CurrentTeam, CurrentOpponent, playerRound, OpponentRound, mapPlayed, Kills, Deaths, playerPlusMinus,
                 playerRating, winOrLost])
        writer.writerow([])
