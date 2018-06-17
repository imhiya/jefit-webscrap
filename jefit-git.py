from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
from time import sleep
import csv
import re
sets_re = '[0-9] : ([0-9]*.[0-9]*)x([0-9]*)'
sets_p = re.compile(sets_re)
url = 'https://www.jefit.com/my-jefit/my-logs/log/?dd='

year = 2018
month = 1
day = 1

year_until = 2019
month_until = 06
day_until = 17

driver = webdriver.Chrome('chromedriver.exe')
driver.implicitly_wait(2)
driver.get(url)
driver.find_element_by_class_name("facebookLoginButton").click()
sleep(3)
email = driver.find_element_by_id("email")
password = driver.find_element_by_id("pass")

email.send_keys("email")
password.send_keys("pass")


driver.find_element_by_id("loginbutton").click()
sleep(3)

for l_year in range(year, year_until):
    
    for l_month in range(month,13):
        for l_day in range(day,32):
            new_url = url + str(l_year) + "-" + str(l_month) + "-" + str(l_day)
            print new_url
            driver.get(new_url)
            try:
                exercises = driver.find_element_by_class_name("fixedLogBar")
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                mysession = soup.findAll("span")
                myspans=[]
                for div in mysession:
                    myspans.append(div.text)
                sess_len = myspans[10]
                sess_actual = myspans[11]
                sess_wasted = myspans[12]
                sess_rest = myspans[13]
                sess_exs = myspans[14]
                sess_total = myspans[15]
                with open('jefit_sessions.csv', 'a') as file_jefit:
                            writer = csv.writer(file_jefit, lineterminator='\n')
                            csvRow = [l_year, l_month, l_day, sess_len, sess_actual, sess_wasted, sess_rest, sess_exs, sess_total]
                            writer.writerow(csvRow)
                mydivs = soup.findAll("div", {"class": "fixedLogBar"})
                for div in mydivs:
                    mydivs2 = div.findAll("div", {"class":"fixedLogBarBlock"})
                    ex_id = div.select_one("input[name=logId]")['value']
                    ex_record = div.select_one("input[name=myrecord]")['value']
                    excerise_name = mydivs2[1].text
                    sets =  mydivs2[3].text
                    sets_lst = sets.split("Set")
                    for i in range(1,len(sets_lst)):
                        sets_result = sets_p.findall(sets_lst[i])
                        i=0
                        for result in sets_result:
                            for item in result:
                                if i==0:
                                    set_weight = item
                                if i==1:
                                    set_reps = item
                                i=i+1
                        with open('jefit_excerises.csv', 'a') as file_jefit:
                            writer = csv.writer(file_jefit, lineterminator='\n')
                            csvRow = [l_year, l_month, l_day, ex_id, ex_record, excerise_name.strip(), set_weight, set_reps]
                            writer.writerow(csvRow)
                    
            except:
                pass
    
                        
            
                
