import os, time
from selenium import webdriver
from selenium.webdriver import ActionChains

import numpy as np
import pandas as pd
from io import StringIO


browser = webdriver.Chrome()
url = 'http://icp.chinaz.com/'
browser.get(url)

txtname = browser.find_element_by_id('txtname')
txtname.click()
browser.find_element_by_xpath('//*[@id="SearChoese-show"]/li[3]/a').click()


SearWrite = browser.find_element_by_id('SearWrite')
# SearWrite.click()
# write = browser.find_element_by_id('s')
# write.send_keys('www.baidu.com')

# Actions actions = new Actions(browser)
# actions.moveToElement(SearWrite)
# actions.click()
# actions.sendKeys('www.taobao.com')
# actions.build().perform()

actions = ActionChains(browser)
actions.move_to_element(SearWrite)
actions.click()
# actions.send_keys('www.taobao.com')
actions.send_keys('北京微梦创科网络技术有限公司')
actions.perform()

search = browser.find_element_by_id('search')
search.click()

thead = browser.find_element_by_css_selector("thead>tr")
print(thead.text)

trlist = browser.find_elements_by_css_selector("tbody>tr")
for tr in trlist:
    print(tr.text)

tbody = browser.find_element_by_css_selector("tbody")
print(tbody.text)

table = browser.find_element_by_css_selector("table")
print(table.text)

table_df = pd.read_csv(StringIO(tbody.text),header=None,sep=' ')

# outname = browser.find_element_by_xpath('//*[@id="first"]/li[1]/p/a')
# print(outname.text)

# browser.find_element_by_xpath('//*[@id="SearWrite"]/b').send_keys('浙江淘宝网络有限公司')

browser.close()
