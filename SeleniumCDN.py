#%%
import os, time
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import numpy as np
import pandas as pd
from io import StringIO

import TxtOperator
#%%
inputFolder = os.path.abspath(r'..\..')
inputFolder = os.path.join(inputFolder, 'Inputs', 'LearnCharmPro')
txtFile = os.path.join(inputFolder, 'SeleniumCDN.txt')

inputsList = TxtOperator.readTxt2List(txtFile, False)
print(inputsList)

url = inputsList[0]
user = inputsList[1]
passwd = inputsList[2]

seleni_public = inputsList[-1]
seleni_re = inputsList[-2]
#%%
# browser = webdriver.Chrome()
browser = webdriver.Edge()
browser.maximize_window()
browser.implicitly_wait(15)
browser.get(url)

# 点击登录按钮
time.sleep(3)
login = browser.find_element_by_css_selector('a[href]')
login.click()

# 输入账密
username = browser.find_element_by_css_selector('input[name="username"]')
username.send_keys(user)

password = browser.find_element_by_css_selector('input[name="password"]')
password.send_keys(passwd)

browser.find_element(By.NAME, "verifyCode").click()
#%%
# # 等待手工输入验证码
# waitin = input()

# # 输入账密后正式登录
# user_login = browser.find_element_by_css_selector('span.cm-touch-ripple')
# user_login.click()
#%%
# 滑动到带宽
manager = browser.find_element_by_css_selector('li.cm-menu-submenu')
fenxi = browser.find_element_by_css_selector('li.cm-menu-submenu > div > span')
# bandwidth = browser.find_element_by_css_selector('div[data-text="带宽"]')

bandwidth = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/ul/li[2]/ul/li[1]/ul/li[1]/a')
# bandwidth.click()

manager = browser.find_element_by_css_selector('.cm-menu-submenu-title-hover > span > span')


manager = browser.find_element_by_css_selector('#root > div > div.main-layout.cm-layout.cm-layout-has-sider > div.sider.cm-layout-sider > ul > li:nth-child(2)')
browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/ul/li[2]/div')

# fenxi = browser.find_element_by_css_selector('li.cm-menu-submenu > div > span')
# bandwidth = browser.find_element_by_css_selector('div[data-text="带宽"]')

bandwidth = browser.find_element_by_xpath('.cm-menu-item-active > a')
bandwidth = browser.find_element_by_css_selector('.cm-menu-item-active > a')

action = ActionChains(browser)
action.move_to_element(manager)
# action.move_to_element(fenxi)
action.move_to_element(bandwidth)
action.click()
action.perform()
browser.switch_to.frame(0)
#%%
loading = (By.CSS_SELECTOR, "body > div:nth-child(8) > div > div.cm-panel-title > span")
# WebDriverWait(browser,5,0.1).until(expected_conditions.presence_of_element_located(loading))
# print('loading start')
# WebDriverWait(browser,20,0.5).until_not(expected_conditions.visibility_of_element_located(loading))
# print('loading ok')
WebDriverWait(browser, 100, 0.5).until(expected_conditions.invisibility_of_element_located(loading))
print('loading ok')
#%%
# browser.switch_to.frame(0)
# 点击7天
# timebuts = browser.find_element_by_css_selector("#cdn-autoid-23 > div > a")
em = browser.find_element_by_css_selector("#cdn-autoid-23 > div > a:nth-child(3) > span > div > span > div")
action = ActionChains(browser)
action.move_to_element(em)
action.click()
action.perform()
# 等待加载完成
WebDriverWait(browser, 5, 0.1).until(expected_conditions.presence_of_element_located(loading))
print('loading start')
WebDriverWait(browser, 100, 0.5).until(expected_conditions.invisibility_of_element_located(loading))
print('loading ok')
#%%
em = browser.find_element(By.CSS_SELECTOR, "#enterpriseSelect")
action = ActionChains(browser)
action.move_to_element(em)
action.click()
action.perform()

time.sleep(3)
# cps = browser.find_elements_by_css_selector("#enterpriseSelect > div > div > div > ul > li")
cps = browser.find_elements_by_css_selector(
    " #enterpriseSelect > div > div > div > ul > li > a > span > div > span:nth-child(2)")
for cp in cps:
    print(cp.text)
# cps[4].click()

cpl = len(cps)
print(cpl)
action.perform()
#%%
# cpl = 5
# for cpi in range(1,cpl):
#     em = browser.find_element(By.CSS_SELECTOR, "#enterpriseSelect")
#     action = ActionChains(browser)
#     action.move_to_element(em)
#     action.click()
#     action.perform()
#     print('下拉')

#     cplist = browser.find_elements_by_css_selector("#enterpriseSelect > div > div > div > ul > li")
#     print('cplist')
#     # cpi = 4
#     print(cpi)
#     cp = cplist[cpi]
#     # print(cp.text)
#     cp.click()
#     print('下拉点击')
#     # 点击查询
#     browser.find_element_by_css_selector("#cdn-autoid-43").click()
#     print('查询')
#     # 获取峰值
#     # time.sleep(10)
#     # print('等待10')
#     loading = (By.CSS_SELECTOR,"body > div:nth-child(8) > div > div.cm-panel-title > span")
#     WebDriverWait(browser,5,0.1).until(expected_conditions.presence_of_element_located(loading))
#     print('loading start')
#     # WebDriverWait(browser,20,0.5).until_not(expected_conditions.visibility_of_element_located(loading))
#     # print('loading ok')
#     WebDriverWait(browser,100,0.5).until(expected_conditions.invisibility_of_element_located(loading))
#     print('loading ok')
#     fengzhi = browser.find_element_by_css_selector("#peak")
#     print(fengzhi.text)
lnf = []
for cpi in cps[1:]:
    em = browser.find_element(By.CSS_SELECTOR, "#enterpriseSelect")
    action = ActionChains(browser)
    action.move_to_element(em)
    action.click()
    action.perform()

    time.sleep(1)
    action = ActionChains(browser)
    action.move_to_element(cpi)
    action.click()
    action.perform()
    action.perform()
    print('下拉')

    # cplist = browser.find_elements_by_css_selector("#enterpriseSelect > div > div > div > ul > li")
    # print('cplist')
    # # cpi = 4
    # print(cpi)
    # cp = cplist[cpi]
    # print(cp.text)
    # cpi.click()
    # print('下拉点击')
    # 点击查询
    browser.find_element_by_css_selector("#cdn-autoid-43").click()
    print('查询')
    # 获取峰值
    # time.sleep(10)
    # print('等待10')
    loading = (By.CSS_SELECTOR, "body > div:nth-child(8) > div > div.cm-panel-title > span")
    WebDriverWait(browser, 5, 0.1).until(expected_conditions.presence_of_element_located(loading))
    print('loading start')
    # WebDriverWait(browser,20,0.5).until_not(expected_conditions.visibility_of_element_located(loading))
    # print('loading ok')
    WebDriverWait(browser, 100, 0.5).until(expected_conditions.invisibility_of_element_located(loading))
    print('loading ok')
    print(em.text)
    fengzhi = browser.find_element_by_css_selector("#peak")
    print(fengzhi.text)
    lnf.append(em.text + ' ' + fengzhi.text)

# browser.close()
#%%
print(lnf)
snf = pd.Series(lnf)
sdf = snf.str.split(' ', expand=True)
sdf.columns = ['name', 'flow', 'unit']
sdf['flow'] = sdf['flow'].astype(float)
#%%
# sdf = pd.read_excel(seleni_re, index_col=0)
df_seleni_public = pd.read_excel(seleni_public, sheet_name=None)
df_name = df_seleni_public['客户名称']
df_unit = df_seleni_public['流量单位']

df_RE = df_name.merge(sdf, how='left')
df_RE = df_RE.merge(df_unit, how='left')
df_RE['Gflow'] = df_RE['flow'] * df_RE['系数']
df_RE['Gflow'] = df_RE['Gflow'].map(int, na_action='ignore')
#%%
outfile_xls = inputFolder + '\\' + inputFolder[inputFolder.rfind('\\') + 1:] + '_CDN汇总_' + '.xlsx'
# 如果汇总文件已存在，直接删除
is_outfile_exist = os.path.exists(outfile_xls)
if (is_outfile_exist):
    print('DelExistFile:', outfile_xls)
    os.remove(outfile_xls)

fileW = outfile_xls
# 单文件单表输出
# print(df_RE)
df_RE.to_excel(fileW, sheet_name='all')