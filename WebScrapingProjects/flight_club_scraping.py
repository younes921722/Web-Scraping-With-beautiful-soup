from bs4 import BeautifulSoup
import requests
import csv ,math,sys
i=1
# for i in range(35):
page = requests.get("https://www.flightclub.com/sneakers")
src  = page.content
soup = BeautifulSoup(src,'lxml')
# print(soup.prettify())

# found_items = soup.find_all('div',{'class':"sc-jowtIB eOXLoG"})
# main_page = soup.find('div',{'class':'sc-yUtDh gVsmBn'})
main_page = soup.find('div',{'class':'sc-jowtIB eOXLoG'})
# found_item = main_page.find('div',{'class':'sc-jowtIB eOXLoG'})

print(main_page)

# print(len(found_items))
