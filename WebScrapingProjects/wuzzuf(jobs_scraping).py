from bs4 import BeautifulSoup
import requests
import csv ,math,sys

job = input("Enter the job you are looking for : ").split()

while len(job) == 0:
    job = input("Enter the job you are looking for : ").split()
job.append("")
page = requests.get(f"https://wuzzuf.net/search/jobs/?a=navbg%7Cspbg&q={job[0]}%20{job[1]}")
src = page.content
soup = BeautifulSoup(src, 'lxml')
number_of_jobs = soup.find('strong').text.strip().replace(',','')  # replace() : we used it to replace comma if exist to empty word so that we convert it easly to integer
number_of_pages = math.ceil(int(number_of_jobs)/15)
print(number_of_jobs)
print(number_of_pages)

jobs_details = []
def main(i):

    page = requests.get(f"https://wuzzuf.net/search/jobs/?a=navbg%7Cspbg&q={job[0]}%20{job[1]}&start={i}")
    src = page.content
    soup = BeautifulSoup(src, 'lxml')


    found_jobs = soup.find_all('div',{'class':'css-1gatmva e1v1l3u10'})

    def job_info(found_job):

        # get the job name
        job_name = found_job.find('div',{'class':'css-laomuu'}).find('a').text.strip()

        # get the company name
        company = found_job.find('div',{'class':'css-d7j1kk'}).find('a').text.strip()

        #get City, Country name
        city_country = found_job.find('span',{'class':'css-5wys0k'}).text.strip().split(',')   #in html code the city and country are in the same class so we split it
        city = city_country[0]
        country = city_country[1]

        # get publishing time
        if found_job.find('div',{'class':'css-4c4ojb'}):
            publishing_time = found_job.find('div',{'class':'css-4c4ojb'}).text.strip()
        elif found_job.find('div',{'class':'css-do6t5g'}):
            publishing_time = found_job.find('div',{'class':'css-do6t5g'}).text.strip()


        # get the type of job
        job_type = found_job.find('span',{'class':'css-1ve4b75 eoyjyou0'}).text.strip()

        # get the job requirements
        job_requi = found_job.find('div',{'class':'css-y4udm8'}).find_all("div")[1].text.strip()

        jobs_details.append({'Job name':job_name, 'Company':company, 'City':city, 'Country':country,'Publishing time':publishing_time,'Type':job_type, 'Requirements':job_requi})

    for i in range(len(found_jobs)):  #fill the rows
        job_info(found_jobs[i])



for i in range(number_of_pages):
    main(i)


keys = jobs_details[0].keys()
with open('C:\\Users\\dell\\Desktop\\younes\\wuzzuf_jobs_scraping.csv','w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(jobs_details)
        print("file created")