import os, time
from selenium import webdriver
from selenium.webdriver import ActionChains

import numpy as np
import pandas as pd
from io import StringIO

inputFolder = os.path.abspath(r'..\..')
inputFolder = os.path.join(inputFolder, 'Inputs', 'LearnCharmPro')
xlsx = os.path.join(inputFolder, '【PandasTest】变量导入.xlsx')

org_name = pd.read_excel(xlsx, sheet_name='站长单位')
org_All = pd.DataFrame()

browser = webdriver.Chrome()
# browser = webdriver.Edge()
browser.maximize_window()

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
for i in range(org_name.shape[0]):
    name_i = org_name.iloc[i, 0]

    SearWrite = browser.find_element_by_id('SearWrite')
    actions = ActionChains(browser)
    actions.move_to_element(SearWrite)
    actions.click()
    # actions.send_keys('www.taobao.com')
    actions.send_keys(name_i)
    actions.perform()

    search = browser.find_element_by_id('search')
    search.click()

    # thead = browser.find_element_by_css_selector("thead>tr")
    # # print(thead.text)

    # trlist = browser.find_elements_by_css_selector("tbody>tr")
    # # for tr in trlist:
    # #     print(tr.text)

    tbody = browser.find_element_by_css_selector("tbody")
    # print(tbody.text)

    # table = browser.find_element_by_css_selector("table")
    # # print(table.text)

    table_df = pd.read_csv(StringIO(tbody.text), header=None, sep=' ')
    print(table_df)
    table_df['org'] = name_i
    org_All = org_All.append(table_df, ignore_index=True)
    time.sleep(0.5)
    SearDel = browser.find_element_by_id('SearDel')
    SearDel.click()

# outname = browser.find_element_by_xpath('//*[@id="first"]/li[1]/p/a')
# print(outname.text)

# browser.find_element_by_xpath('//*[@id="SearWrite"]/b').send_keys('浙江淘宝网络有限公司')

fileR = xlsx
tNow = time.strftime("%H%M%S", time.localtime())
fileW = fileR[:fileR.rfind('.')] + '-PANDAS-' + tNow + '.xlsx'

# 单文件单表输出
org_All.to_excel(fileW, sheet_name='ALL')

# browser.close()