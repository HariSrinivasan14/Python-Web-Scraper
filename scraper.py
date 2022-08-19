import requests
from bs4 import BeautifulSoup
import pandas as pd


def isFloat(value):
    try:
        float(value)
        return True
    except:
        return False

def clearDict(dict):
    keys = dict.keys()
    for key in keys:
        dict[key] = []

def convertString(value):
    if value is None:
        return value
    elif isFloat(value):
        return float(value)
    else:
        return int(value)

def writeToExcelFile(dataFrame, isHeader, sheetName, fileName, startToRow):
    if isHeader:
        dataFrame.to_excel(fileName, sheet_name=sheetName, encoding="utf-8-sig", header=True, index=False)
    else:
        with pd.ExcelWriter(fileName, mode="a", if_sheet_exists="overlay") as writer:
            dataFrame.to_excel(writer, sheet_name=sheetName, encoding="utf-8-sig", header=False, index=False, startrow=startToRow)

def writeToCSVFile(dataFrame, isHeader, fileName):
    if isHeader:
        dataFrame.to_csv(fileName, mode='a', encoding='utf-8-sig', header=True, index=False) # write the column and row names
    else:
        dataFrame.to_csv(fileName, mode='a', encoding='utf-8', header=False, index= False)

def convertFeetToCM(height):
    heightArr = height.split('-')
    return round(int(heightArr[0]) * 30.48 + int(heightArr[1]) * 2.54, 2)

def mergeStats(playerStats, advancedStats):
    advancedStatsKeys = advancedStats.keys()
    for key in advancedStatsKeys:
        if key == "G":
            if advancedStats[key] == None:
                playerStats["Total Games"].append('-')
            else:
                playerStats["Total Games"].append(advancedStats[key])
        elif key == "GS":
            if advancedStats[key] == None:
                playerStats["Total Games Started"].append('-')
            else:
                playerStats["Total Games Started"].append(advancedStats[key])            
        elif key == "MP":
            if advancedStats[key] == None:
                playerStats["Minutes Per Game"].append('-')
            else:
                playerStats["Minutes Per Game"].append(advancedStats[key])                
        elif key == "FG":
            if advancedStats[key] == None:
                playerStats["Field Goal per Game"].append('-')
            else:
                playerStats["Field Goal per Game"].append(advancedStats[key])                 
        elif key == "FGA":
            if advancedStats[key] == None:
                playerStats["Field Goal Attempts per Game"].append('-')
            else:
                playerStats["Field Goal Attempts per Game"].append(advancedStats[key])    
        elif key == "FG%":
            if advancedStats[key] == None:
                playerStats["Field Goal %"].append('-')
            else:
                playerStats["Field Goal %"].append(advancedStats[key])                
        elif key == "3P":
            if advancedStats[key] == None:
                playerStats["Three Point Field Goal per Game"].append('-')
            else:
                playerStats["Three Point Field Goal per Game"].append(advancedStats[key])
        elif key == "3PA":
            if advancedStats[key] == None:
                playerStats["Three Point Field Goal Attempts per Game"].append('-')
            else:
                playerStats["Three Point Field Goal Attempts per Game"].append(advancedStats[key])    
        elif key == "3P%":
            if advancedStats[key] == None:
                playerStats["Three Point Field Goal %"].append('-')
            else:
                playerStats["Three Point Field Goal %"].append(advancedStats[key])           
        elif key == "2P":
            if advancedStats[key] == None:
                playerStats["Two Point Field Goal per Game"].append('-')
            else:
                playerStats["Two Point Field Goal per Game"].append(advancedStats[key])
        elif key == "2PA":
            if advancedStats[key] == None:
                playerStats["Two Point Field Goal Attempts per Game"].append('-')
            else:
                playerStats["Two Point Field Goal Attempts per Game"].append(advancedStats[key])    
        elif key == "2P%":
            if advancedStats[key] == None:
                playerStats["Two Point Field Goal %"].append('-')
            else:
                playerStats["Two Point Field Goal %"].append(advancedStats[key])      
        elif key == "eFG%":
            if advancedStats[key] == None:
                playerStats["Effective Field Goal %"].append('-')
            else:
                playerStats["Effective Field Goal %"].append(advancedStats[key])      
        elif key == "FT":
            if advancedStats[key] == None:
                playerStats["Free Throw per Game"].append('-')
            else:
                playerStats["Free Throw per Game"].append(advancedStats[key])  
        elif key == "FTA":
            if advancedStats[key] == None:
                playerStats["Free Throw Attempts per Game"].append('-')
            else:
                playerStats["Free Throw Attempts per Game"].append(advancedStats[key])  
        elif key == "FT%":
            if advancedStats[key] == None:
                playerStats["Free Throw %"].append('-')
            else:
                playerStats["Free Throw %"].append(advancedStats[key])  
        elif key == "TRB":
            if advancedStats[key] == None:
                playerStats["Total Rebounds per Game"].append('-')
            else:
                playerStats["Total Rebounds per Game"].append(advancedStats[key])  
        elif key == "AST":
            if advancedStats[key] == None:
                playerStats["Assists per Game"].append('-')
            else:
                playerStats["Assists per Game"].append(advancedStats[key])              
        elif key == "STL":
            if advancedStats[key] == None:
                playerStats["Steals per Game"].append('-')
            else:
                playerStats["Steals per Game"].append(advancedStats[key])              
        elif key == "BLK":
            if advancedStats[key] == None:
                playerStats["Blocks per Game"].append('-')
            else:
                playerStats["Blocks per Game"].append(advancedStats[key])    
        elif key == "TOV":
            if advancedStats[key] == None:
                playerStats["Turnover per Game"].append('-')
            else:
                playerStats["Turnover per Game"].append(advancedStats[key])    
        elif key == "PF":
            if advancedStats[key] == None:
                playerStats["Fouls per Game"].append('-')
            else:
                playerStats["Fouls per Game"].append(advancedStats[key])    
        else:
            # "PTS" case
            if advancedStats[key] == None:
                playerStats["Points per Game"].append('-')
            else:
                playerStats["Points per Game"].append(advancedStats[key])        

def parsePlayerPages(pageList, fileType):
    playerStats = {"Players":[],"Career Start Year":[],"Career End Year":[],"Position":[], "Height":[],"Weight":[], 
    "Birth Date": [], "Colleges": [], 'Total Games':[], "Total Games Started": [], "Minutes Per Game": [], "Field Goal per Game":[], "Field Goal Attempts per Game":[], "Field Goal %":[], 
    "Three Point Field Goal per Game": [], "Three Point Field Goal Attempts per Game": [] ,"Three Point Field Goal %": [], "Two Point Field Goal per Game": [], 
    "Two Point Field Goal Attempts per Game": [] ,"Two Point Field Goal %": [], "Effective Field Goal %": [], "Free Throw per Game": [], "Free Throw Attempts per Game": [],
    "Free Throw %":[], "Total Rebounds per Game": [], "Assists per Game":[],"Steals per Game":[], "Blocks per Game": [], "Turnover per Game": [], "Fouls per Game": [], "Points per Game": []}
    
    header = True
    counter = 0
    numRows = 1 # starts at 1 to account for the header
    for page in pageList:  
        soup = BeautifulSoup(page.content,"html5lib")
        table = soup.find("table", class_= "sortable")
        rows = table.tbody.find_all('tr')
        for row in rows:
            playerName = row.findAll("th")[0]
            playerNameFiltered = playerName.find(text=True)
            playerStats["Players"].append(playerNameFiltered)
            playerAdvancedPageLink = playerName.find('a', href=True)['href']

            playerDetails = row.findAll("td")

            playerStats["Career Start Year"].append(convertString(playerDetails[0].find(text=True)))
            playerStats["Career End Year"].append(convertString(playerDetails[1].find(text=True)))
            playerStats["Position"].append(playerDetails[2].find(text=True))
            playerStats["Height"].append(convertFeetToCM(playerDetails[3].find(text=True)))
            playerStats["Weight"].append(convertString(playerDetails[4].find(text=True)))
            playerStats["Birth Date"].append(playerDetails[5].find(text=True))
            playerStats["Colleges"].append(playerDetails[6].find(text=True))
            advancedStats = getAdvancedPlayerStats(playerAdvancedPageLink)
            mergeStats(playerStats, advancedStats)
            counter += 1
            if counter == 500:
                print("\n\n")
                dataFrame=pd.DataFrame(playerStats)
                print(dataFrame)
                clearDict(playerStats)

                # write to csv file
                if fileType == "C":
                    if header:
                        header = False
                        writeToCSVFile(dataFrame, True, "playerData.csv")
                    else:
                        writeToCSVFile(dataFrame, False, "playerData.csv")
                # write to excel file
                else:
                    if header:
                        header = False
                        writeToExcelFile(dataFrame, True, "players","data.xlsx", 0)
                    else:
                        writeToExcelFile(dataFrame, False, "players","data.xlsx", numRows)
                # need for writing to the excel file
                numRows += counter
                counter = 0

    # print the left over
    if not playerStats["Players"] == []:
        dataFrame=pd.DataFrame(playerStats)
        print(dataFrame)
        if fileType == "C":
            writeToCSVFile(dataFrame, False, "playerData.csv")
        else:
            writeToExcelFile(dataFrame, False, "players","data.xlsx", numRows)

def getAdvancedPlayerStats(playerAdvancedPageLink):
    advancedStats = {"G": None, "GS": None, "MP": None, "FG": None, "FGA": None, "FG%": None, "3P": None, "3PA": None, "3P%": None, "2P": None, "2PA": None, "2P%": None, 
    "eFG%": None, "FT": None, "FTA": None, "FT%": None, "TRB": None, "AST": None, "STL": None, "BLK": None, "TOV": None, "PF": None, "PTS": None}
    
    #stats to skip
    skipStats = ["ORB", "DRB"]
    reply = requests.get('https://www.basketball-reference.com' + playerAdvancedPageLink)
    soup = BeautifulSoup(reply.content,"html5lib")
    careerStatTable = soup.find("table", id= "per_game")

    statNames = careerStatTable.find("tr").find_all("th")
    statNames = statNames[5:]
    careerStats = careerStatTable.find("tfoot").find_all("tr")[0].find_all("td")[4:]
    counter = 0
    for statName in statNames:
        filterStatName = statName.find(text=True)
        if filterStatName in skipStats:
            counter += 1
            continue
        advancedStats[filterStatName] = convertString(careerStats[counter].find(text=True))
        counter += 1
    return advancedStats

def getPlayers(fileType):
    replyList = []
    for char in "abcdefghijklmnpqrstuvwxyz":
        reply = requests.get("https://www.basketball-reference.com/players/" + char)
        replyList.append(reply)
    return parsePlayerPages(replyList, fileType)

def Main():
    print("Please type C to export the data to csv files or type E to export the data to an excel file")
    print("--------------------------------")
    fileType = input("Enter File Type: ")
    while(fileType != "C" and fileType != "E"):
        print("Please type C to export the data to csv files or type E to export the data to an excel file")
        print("--------------------------------")
        fileType = input("Enter File Type: ")
    getPlayers(fileType)

Main()
