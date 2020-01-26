1)Install Dependencies(& Python3)
pip install selenium
pip install pandas
pip install openpyxl
pip install xlrd
pip install csv
--Exctract flights.zip to a new independent folder
2)Set Chrome Webdriver Path in flights.py,getoneflight.py
-- Use a fresh login as data might be used up, we'll give the creds to you, or use psiphon.
3)Run flights.py
4)Enter Day, Month, Year in format DD, MM(Not Name), YYYY
5)Enter Number of Days(Ideally 7, or we'll let you know)
6)once flights.py is done running, run compile_csv.py
7)Hit Tuli Up for a treat!


 
//
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import datetime
import openpyxl as xl
import csv
import threading
import glob, os
import os
import itertools
xlrd
//