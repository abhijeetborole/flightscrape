from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import datetime
import openpyxl as xl
import csv
import threading

chrome_path = 'C:/bin/chromedriver.exe'
browser1 = webdriver.Chrome(executable_path=chrome_path)



i = 0
dep_times_list = None
arr_times_list = None
airlines_list = None
price_list = None
durations_list = None
stops_list = None
layovers_list = None
idpath = None
#Arrival Airpot
a = 'TLV'
#Departure Airport
b = 'BOM'
#Date
day = '19' 
month = '12'
year = '2019'

#Setting ticket types paths
return_ticket = "//label[@id='flight-type-roundtrip-label-hp-flight']"
one_way_ticket = "//label[@id='flight-type-one-way-label-hp-flight']"
multi_ticket = "//label[@id='flight-type-multi-dest-label-hp-flight']"

def ticket_chooser(ticket,browser):
    global idpath
    try:
        if(ticket == one_way_ticket):
            idpath = "//input[@id='flight-departing-single-hp-flight']"
        else:
            idpath = "//input[@id='flight-departing-hp-flight']"
        ticket_type = browser.find_element_by_xpath(ticket)
        ticket_type.click()
    except Exception as e:
        pass

def dep_country_chooser(dep_country,browser):
    fly_from = browser.find_element_by_xpath("//input[@id='flight-origin-hp-flight']")
    time.sleep(1)
    fly_from.clear()
    time.sleep(1.5)
    fly_from.send_keys('  ' + dep_country)
    time.sleep(1.5)
    first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(1.5)
    first_item.click()
    
def arrival_country_chooser(arrival_country,browser):
    fly_to = browser.find_element_by_xpath("//input[@id='flight-destination-hp-flight']")
    time.sleep(1)
    fly_to.clear()
    time.sleep(1.5)
    fly_to.send_keys('  ' + arrival_country)
    time.sleep(1.5)
    first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(1.5)
    first_item.click()

def dep_date_chooser(month, day, year,browser):
    dep_date_button = browser.find_element_by_xpath(idpath)
    dep_date_button.clear()
    dep_date_button.send_keys(month + '/' + day + '/' + year)

def return_date_chooser(month, day, year,browser):
    return_date_button = browser.find_element_by_xpath("//input[@id='flight-returning-hp-flight']")
    for i in range(11):
        return_date_button.send_keys(Keys.BACKSPACE)
    return_date_button.send_keys(month + '/' + day + '/' + year)

def one_way_help(browser):
    search = browser.find_element_by_xpath("//button[@class='trigger-utility menu-trigger btn-utility btn-secondary dropdown-toggle theme-standard pin-left menu-arrow gcw-component gcw-traveler-amount-select gcw-component-initialized']")
    search.click()

def search(browser):
    search = browser.find_element_by_xpath("//button[@class='btn-primary btn-action gcw-submit']")
    search.click()
    time.sleep(10)
    print('Results ready!')

df = pd.DataFrame() 
def compile_data(browser):
    global df
    global dep_times_list
    global arr_times_list
    global airlines_list
    global price_list
    global durations_list
    global stops_list
    global layovers_list
    #departure times
    dep_times = browser.find_elements_by_xpath("//span[@data-test-id='departure-time']")
    dep_times_list = [value.text for value in dep_times]
    #arrival times
    arr_times = browser.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
    arr_times_list = [value.text for value in arr_times]
    #airline name
    airlines = browser.find_elements_by_xpath("//span[@data-test-id='airline-name']")
    airlines_list = [value.text for value in airlines]
    #prices
    prices = browser.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
    price_list = [value.text for value in prices]
    #durations
    durations = browser.find_elements_by_xpath("//span[@data-test-id='duration']")
    durations_list = [value.text for value in durations]
    #stops
    stops = browser.find_elements_by_xpath("//span[@class='number-stops']")
    stops_list = [value.text for value in stops]
    #layovers
    layovers = browser.find_elements_by_xpath("//span[@data-test-id='layover-airport-stops']")
    layovers_list = [value.text for value in layovers]
    now = datetime.datetime.now()
    current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
    current_time = (str(now.hour) + ':' + str(now.minute))
    current_price = 'price' + '(' + current_date + '---' + current_time + ')'
    for i in range(len(dep_times_list)):
        try:
            df.loc[i, 'departure_time'] = dep_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'arrival_time'] = arr_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'airline'] = airlines_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'duration'] = durations_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'stops'] = stops_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'layovers'] = layovers_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'price'] = price_list[i]
        except Exception as e:
            pass
    print('Excel Sheet Created!')

now = datetime.datetime.now()
current_date = (str(now.year) + str(now.month) + str(now.day))
current_time = (str(now.hour) + ':' + str(now.minute))
current_price = 'price' + '(' + current_date + '---' + current_time + ')'
def main(day,month,year,browser):
    try:
        global i
        date = day+month+year
        l=[]
        d={}
        d2={}
        with open("airport_codes.csv", 'r') as csvfile2: 
            csvreader2 = csv.reader(csvfile2) 
            for row in csvreader2:
                if row[3]=='India':
                    l.append(row[1])

        with open("routes.csv", 'r') as csvfile: 
            csvreader = csv.reader(csvfile) 
            for row in csvreader: 
                if row[2] not in l and row[4] not in l:
                    continue
                if row[2] in d:
                    d[row[2]].add(row[4])
                else:
                    d[row[2]]={row[4]}
                
        with open("airport_codes.csv", 'r') as csvfile3: 
            csvreader3 = csv.reader(csvfile3) 
            for row in csvreader3:
                if row[1] in d.keys():
                    d2[row[1]]=row[0]

    except Exception as e:
        print(e)
        print('_main')

    try: 
        global a
        global b
        link = 'https://www.expedia.co.in/'
        browser.get(link)
        time.sleep(1)
        #choose flights only
        flights_only = browser.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
        flights_only.click()

        ticket_chooser(one_way_ticket,browser)
        if a in d2:
            dep_country_chooser(d2[a],browser)
        else:
            dep_country_chooser(a,browser)
                
        if b in d2:
            arrival_country_chooser(d2[b],browser)
        else:
            arrival_country_chooser(b,browser)
        dep_date_chooser(day,month,year,browser)
        #return_date_chooser('05', '01', '2020')
        one_way_help(browser)
        search(browser)
        compile_data(browser)
        current_values = df.iloc[0]
        cheapest_dep_time = current_values[0]
        cheapest_arrival_time = current_values[1]
        cheapest_airline = current_values[2]
        cheapest_duration = current_values[3]
        cheapest_stops = current_values[4]
        cheapest_price = current_values[-1]
        print('run {} completed!'.format(i))
        df.to_excel('flights'+a+'_'+b+current_date+'_'+date+'.xlsx')
        time.sleep(1)
    except Exception as e:
            print(e)

if __name__ == "__main__":
    print('Enter Departure Airport')
    a = input()
    print('Enter Arrival Airport')
    b = input()
    print('Enter Day')
    day = int(input())
    print('Enter Month')
    month = int(input())
    print('Enter Year')
    year = int(input())
    main(day,month,year,browser1)
