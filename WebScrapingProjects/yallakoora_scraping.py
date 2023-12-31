import requests
from bs4 import BeautifulSoup
import csv
import sys,pandas as pd


def main():

    date = " "
    def take_date():

        date = input("Please enter a Date in the following format MM/DD/YYYY : ")

        if "/" in date:
            date_elements = date.split("/")
            if int(date_elements[0]) > 12 :
                    print("The months filed should not overcom 12")
                    take_date()
            # elif
        else:
            print("please enter the correct date format")
            take_date()
    take_date()


    page = requests.get(f"https://www.yallakora.com/match-center/?date={date}")

    src = page.content
    soup = BeautifulSoup(src, "lxml")
    matches_details = []

    #the championship is a list contains more than one value each value is a code of special championship
    championships = soup.find_all("div", {'class': 'matchCard'})
    def get_match_info(championships):


        championship_title = championships.contents[1].find("h2").text.strip()#strip() to remove the white spaces in strings #.text is used to bring the text inside the h2
        all_matches=championships.contents[3].find_all("li")
        number_of_matches = len(all_matches)

        #get teams names
        for i in range(number_of_matches):
            teamA=all_matches[i].find('div', {'class':'teamA'}).find('p').text.strip()
            teamB=all_matches[i].find('div', {'class':'teamB'}).find('p').text.strip()

            #get final score
            match_score = all_matches[i].find('div',{'class':'MResult'}).find_all('span',{'class':'score'})
            score = f"{match_score[0].text.strip()} - {match_score[1].text.strip()}"

            # get time
            match_time = all_matches[i].find('div',{'class':'MResult'}).find('span',{'class':'time'}).text.strip()

            #get channel
            channel = all_matches[i].find('div', {'class': 'channel'})

            if channel:
                channel = all_matches [i].find('div',{'class':'channel'}).text.strip()
            else: channel =" --- "
            # add match info to into matches_details
            matches_details.append({'نوع البطولة':championship_title,"الفريق الاول":teamA,"الفريق القاني":teamB," ميعاد المباراة":match_time,"النتيجة":score,"channel":channel})

    for i in range(len(championships)):
        get_match_info(championships[i])
    keys = matches_details[0].keys()

    with open('C:\\Users\\dell\\Desktop\\younes\\test.csv','w',encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print("file created")

def transfers():
    page = requests.get(f"https://www.yallakora.com/transfer-list/جميع-الإنتقالات/0")

    src = page.content
    soup = BeautifulSoup(src, "lxml")
    # print(soup.prettify())

    transfer_details = []
    #get all importante transfers
    all_important_transfers = soup.find('div',{'class':'leftSide'}).find_all("section",{'class':'standing left'})[0]
    numberOfPlayers = len(all_important_transfers.find_all('div',{'class':'wRow'}))

    # all players information
    players_info = all_important_transfers.find_all("div",{'class':'wRow'})
    def player_info(player_info):

        # get players name
        player_name = player_info.find('div',{'class':'item var'}).find('p').text.strip()

        # team the player will move to
        buyer_team = player_info.find('div',{'class':'item var toTeam'}).find('p').text.strip()

        # details about transfer
        transfer_detail = player_info.find_all('div',{'class':'item fixed'})[1].find('p').text.strip()

        transfer_details.append({'player':player_name, 'moved to':buyer_team, 'details':transfer_detail})

    for i in range(numberOfPlayers):
        player_info(players_info[i])
    keys = transfer_details[0].keys()

    with open('C:\\Users\\dell\\Desktop\\younes\\important_transfers.csv', 'w', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(transfer_details)
        print("file created")



# transfers()
main()
