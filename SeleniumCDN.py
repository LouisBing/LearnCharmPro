#%%
import os, time
from selenium import webdriver
from selenium.webdriver import ActionChains

import numpy as np
import pandas as pd
from io import StringIO

import TxtOperator

inputFolder = os.path.abspath(r'..\..')
inputFolder = os.path.join(inputFolder, 'Inputs', 'LearnCharmPro')
txtFile = os.path.join(inputFolder, 'SeleniumCDN.txt')

inputsList = TxtOperator.readTxt2List(txtFile, False)
print(inputsList)

url = inputsList[0]
user = inputsList[1]
passwd = inputsList[2]

# org_name = pd.read_excel(xlsx, sheet_name='站长单位')
# org_All = pd.DataFrame()
#%%
browser = webdriver.Chrome()
# browser = webdriver.Edge()
browser.maximize_window()

browser.get(url)

time.sleep(3)
login = browser.find_element_by_css_selector('a[href]')
login.click()

username = browser.find_element_by_css_selector('input[name="username"]')
username.send_keys(user)

password = browser.find_element_by_css_selector('input[name="password"]')
password.send_keys(passwd)
#%%
waitin = input()

user_login = browser.find_element_by_css_selector('span.cm-touch-ripple')
user_login.click()

time.sleep(3)
bandwidth = browser.find_element_by_css_selector('div[data-text="带宽"]')
bandwidth.click()

# browser.close()