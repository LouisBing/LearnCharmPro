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

# 输入账号
username = browser.find_element_by_css_selector('input[name="username"]')
username.send_keys(user)
# 输入密码
password = browser.find_element_by_css_selector('input[name="password"]')
password.send_keys(passwd)
# 鼠标定位至验证码输入框
browser.find_element(By.NAME, "verifyCode").click()
#%%
# 输入验证码后手工登录，不必使用以下自动登录

# # 等待手工输入验证码
# waitin = input()
# # 输入账密后正式登录
# user_login = browser.find_element_by_css_selector('span.cm-touch-ripple')
# user_login.click()
#%%
# 运营管理
manager = browser.find_element_by_css_selector(
    '#root > div > div.main-layout.cm-layout.cm-layout-has-sider > div.sider.cm-layout-sider > ul > li:nth-child(2)')
# 统计分析
bandwidth = manager.find_element_by_css_selector('ul > li:nth-child(1) > a')
# 滑动至统计分析
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
# 7天
seven_day = browser.find_element_by_css_selector(
    "#root > div > div > div:nth-child(2) > div:nth-child(1) > div.search-wrap > div.mb-15 > div > a:nth-child(3)")

action = ActionChains(browser)
action.move_to_element(seven_day)
action.click()
action.perform()

# 等待加载完成
WebDriverWait(browser, 5, 0.1).until(expected_conditions.presence_of_element_located(loading))
print('loading start')
WebDriverWait(browser, 100, 0.5).until(expected_conditions.invisibility_of_element_located(loading))
print('loading ok')
#%%
# em = browser.find_element(By.CSS_SELECTOR, "#enterpriseSelect")
# 企业列表框
enterprise_list = browser.find_element_by_css_selector(
    "#root > div > div > div:nth-child(2) > div:nth-child(1) > div.search-wrap > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)"
)
# 滑动点击
action = ActionChains(browser)
action.move_to_element(enterprise_list)
action.click()
action.perform()

time.sleep(3)

# 获取企业列表并打印企业名称
cps = enterprise_list.find_elements_by_css_selector(
    "div.cm-select.cm-large-select.cm-select-active > div > div > div.cm-scroll > div:nth-child(3) > div > ul > li")
for cp in cps:
    print(cp.text)
# cps[4].click()

cpl = len(cps)
print(cpl)

# 重要：再次滑动点击企业列表框，收起下拉选项
action.perform()
#%%
df_seleni_public = pd.read_excel(seleni_public, sheet_name=None)
df_name = df_seleni_public['客户名称']
df_unit = df_seleni_public['流量单位']
cps_namelist = df_name['name'].tolist()

cps_out = []
for cp in cps:
    print(cp.text)
    if cp.text in cps_namelist:
        cps_out.append(cp)
# cps[4].click()

cpl = len(cps_out)
for cp in cps_out:
    print(cp.text)

lnf = []
for cpi in cps_out:
    # 企业列表框
    enterprise_list = browser.find_element_by_css_selector(
        "#root > div > div > div:nth-child(2) > div:nth-child(1) > div.search-wrap > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)"
    )
    # 滑动点击
    action = ActionChains(browser)
    action.move_to_element(enterprise_list)
    action.click()
    action.perform()
    print('下拉')

    time.sleep(1)

    # 滑动点击cpi
    action = ActionChains(browser)
    action.move_to_element(cpi)
    action.click()
    action.perform()
    # action.perform()
    print('选择企业')

    # cpi_name = enterprise_list.text
    # print(cpi_name)
    # if cpi_name in cps_namelist:
    browser.find_element_by_css_selector(
        "#root > div > div > div:nth-child(2) > div:nth-child(1) > div.search-wrap > div:nth-child(2) > a").click()
    print('查询')

    # 等待加载完成
    # time.sleep(10)
    # print('等待10')
    loading = (By.CSS_SELECTOR, "body > div:nth-child(8) > div > div.cm-panel-title > span")
    WebDriverWait(browser, 5, 0.1).until(expected_conditions.presence_of_element_located(loading))
    print('loading start')
    # WebDriverWait(browser,20,0.5).until_not(expected_conditions.visibility_of_element_located(loading))
    # print('loading ok')
    WebDriverWait(browser, 100, 0.5).until(expected_conditions.invisibility_of_element_located(loading))
    print('loading ok')

    # 获取峰值
    print(enterprise_list.text)
    fengzhi = browser.find_element_by_css_selector("#peak")
    print(fengzhi.text)
    lnf.append(enterprise_list.text + ' ' + fengzhi.text)

browser.quit()
#%%
print(lnf)
snf = pd.Series(lnf)
sdf = snf.str.split(' ', expand=True)
sdf.columns = ['name', 'flow', 'unit']
sdf['flow'] = sdf['flow'].astype(float)
#%%
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