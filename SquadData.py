import requests
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

transfermarkt_river_squad_url = "https://www.transfermarkt.com/ca-river-plate/kader/verein/209/saison_id/2021/plus/1"

def parse_multipleData(dataBunch):

    AgeList = []
    HeightList = []
    FootList = []

    for i in range(1,240,8):
        BirthdayAndAge = dataBunch[i].text
        AgeList.append(int(BirthdayAndAge[-3:-1]))
    for i in range(3,240,8):
        HeightList.append(dataBunch[i].text)
    for i in range(4,240,8):
        FootList.append(dataBunch[i].text)

    return AgeList, HeightList, FootList

def filter_data(Players, Values, MultipleData):

    PlayersList = []
    ValuesList = []

    parsed_multipleData = parse_multipleData(MultipleData)

    for i in range(0,30):
        player = Players[i].text
        player = player[24:46]
        player = player.strip(' ')
        PlayersList.append(player)
        ValuesList.append(Values[i].text)

    return PlayersList, ValuesList, parsed_multipleData[0], parsed_multipleData[1], parsed_multipleData[2]

def create_dataFrame(filtered_data):

    df = pd.DataFrame({"Players":filtered_data[0],"Values":filtered_data[1], "Age":filtered_data[2], "Height":filtered_data[3], "Foot":filtered_data[4]})
    df = df.replace('\n','', regex=True)

    return df

def squad_averages(AgeList, HeightList):

    HeightListNum = []
    temp = [t.replace(',','.') for t in HeightList]
    for i in temp:
        HeightListNum.append(float(i[0:4]))

    return np.average(AgeList), np.average(HeightListNum)

def main():

    headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    pageTree = requests.get(transfermarkt_river_squad_url, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    Players = pageSoup.find_all("td", {"class": "posrela"})
    Values = pageSoup.find_all("td", {"class": "rechts hauptlink"})
    MultipleData = pageSoup.find_all("td", {"class": "zentriert"})

    filtered_data = filter_data(Players, Values, MultipleData)

    df = create_dataFrame(filtered_data)
    print(df)

    averages = squad_averages(filtered_data[2], filtered_data[3])
    print("Squad Average Age: {}".format(averages[0]))
    print("Squad Average Height: {}".format(averages[1]))


main()
