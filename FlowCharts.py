#%%
import os
import time
from math import ceil
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

import FileOperator
import TxtOperator

# ------------------------------------------------------------------------------------------
# 场景：从TXT文件中输入变量
inputFolder = os.path.abspath(r'..\..')
inputFolder = os.path.join(inputFolder, 'Inputs', 'LearnCharmPro')

txtFile = os.path.join(inputFolder, 'FlowCharts.txt')
inputsList = TxtOperator.readTxt2List(txtFile, False)
print(inputsList)

header_file = inputsList[0]
code_file = inputsList[1]
read_file = inputsList[2]
folder = inputsList[3]

# 全局表头文件，用于替换表头。如果哪个场景需要替换表头，可以使用此表数据
sidf_header = pd.read_excel(header_file, sheet_name=3, header=0, index_col=0)
#%%
outfile_xls = folder + '\\' + folder[folder.rfind('\\') + 1:] + '_PANDAS汇总_' + '.xlsx'
# 如果汇总文件已存在，直接删除
isx = os.path.exists(outfile_xls)

# 获取目录下所有文件名，并汇总xls文件
xlslist = []
fileList = FileOperator.getAllFiles(folder, notDeeep=True)
# print(len(fileList))
for file in fileList:
    if ('.xls' in file) and ('~$' not in file):
        print(file)
        xlslist.append(file)
iscon = len(xlslist)

boss_df = pd.DataFrame()
pivotable_df = pd.DataFrame()
pivProvince_df = maxDateFlow_df = pivFlow_df = pd.DataFrame()
timestep = 6
step = int(timestep * 60 / 5)
if (isx == False or iscon > 1):
    print('需要合并和重新生成')
    # 数据保量相关变量
    exlist = []
    # 设置表头行数
    headerrows = 1
    headerlist = []

    # 数据导入-依次读取每个Excel文件并进行连接
    for file in xlslist:
        sf = pd.read_excel(file, sheet_name=0, header=None, skiprows=range(headerrows), dtype={2: str})
        sfH = pd.read_excel(file, sheet_name=0, header=None, nrows=headerrows)
        exlist.append(sf)
        headerlist.append(sfH)

    # 数据规整-连接
    boss_df = pd.concat(exlist, sort=False, ignore_index=True)
    sf_Header = pd.concat(headerlist, sort=False, ignore_index=True)

    # 替换表头
    headerindex = 5
    title = sidf_header.loc[headerindex, :]
    title.dropna(inplace=True)
    print(title.values)
    boss_df.rename(columns=title, inplace=True)
    print(boss_df.info())
    pivotable_df = boss_df.pivot_table(index=['product_id', 'begin_time'], values=['flow'], aggfunc=['sum', 'count'])
    pivotable_df.columns = ['flow', 'count-flow']
    pivotable_df['bandwidth-icp'] = pivotable_df['flow'] * 8 * 1024 / 300 / 1000 / 1000
    pivotable_df['bandwidth-cm'] = pivotable_df['flow'] * 8 / 300 / 1024
    pivotable_df['bandwidth-cm'] = pivotable_df['bandwidth-cm'].map(ceil)
    pivotable_df.reset_index(inplace=True)
    pivotable_df['date'] = pivotable_df['begin_time'].str.slice(0, 8)
    pivotable_df['time'] = pivotable_df['begin_time'].str.slice(8, )

    # 时间刻度间隔，单位小时
    code_time = pd.read_excel(code_file, sheet_name=0, dtype={'time': str})
    code_province = pd.read_excel(code_file, sheet_name=1)
    code_time.loc[::step, 'xtick'] = 1
    code_time.loc[code_time['time'] == '000000', 'xtick'] = 0

    pivotable_df = pd.merge(pivotable_df, code_time, how='left', on='time')
    # pivotable_df.set_index(['product_id', 'begin_time'],inplace=True)

    pivProvince_df = boss_df.pivot_table(index=['product_id', 'province'], values=['flow'], aggfunc='sum')
    pivProvince_df.reset_index(inplace=True)
    pivProvince_df = pd.merge(pivProvince_df, code_province, how='left', on='province')
    pivProvince_df.sort_values(['product_id', 'flow'], ascending=False, inplace=True)

    pivFlow_df = boss_df.pivot_table(index=['product_id'], values=['flow'], aggfunc='sum')

    group_df = pivotable_df.groupby(['product_id', 'date'])
    maxDateFlow_df = group_df.apply(lambda x: x.nlargest(2, 'bandwidth-cm'))

elif (isx == True and iscon == 1):
    print('直接读取汇总透视')
    # pivotable_df = pd.read_excel(outfile_xls, sheet_name='汇总透视', header=[0,1],index_col=[0,1])
    pivotable_df = pd.read_excel(outfile_xls, sheet_name='汇总透视', header=[0], index_col=[0], dtype={'begin_time': str})

#%%
# boss_df['DT'] = boss_df['begin_time'].apply(str)
# boss_df['date'] = boss_df['DT'].str.slice(0,8)
# boss_df['time'] = boss_df['DT'].str.slice(8,)

# pivotable_df = boss_df.pivot_table(index=['product_id', 'begin_time'], values=['flow'], aggfunc=['sum', 'count'])
# le0 = pivotable_df.index.get_level_values(0)
# le0 = le0.drop_duplicates()
# product_ids = pivotable_df.index.levels[0]
product_ids = pivotable_df['product_id'].drop_duplicates()
axlen = len(product_ids)

for id, product_id in enumerate(product_ids):
    # idx = pd.IndexSlice
    # plot_data = pivotable_df.loc[idx[9001035304],idx['sum']]
    flow_df = pivotable_df.loc[pivotable_df['product_id'] == product_id]
    # flow_df.reset_index(inplace=True)
    # flow_df['datetime'] = flow_df['begin_time'].apply(str)
    # flow_df['date'] = flow_df['datetime'].str.slice(0, 8)
    # flow_df['time'] = flow_df['datetime'].str.slice(8, )
    # flow_df['begin_time'] = flow_df['begin_time']-20191011000000

    # flow_df = pd.merge(flow_df, code_time, how='left', on='time')

    # ax = plt.subplot(axlen,1,id+1)
    # ax.plot('datetime', 'flow', data=flow_df, color="red",label="S-OUT")
    plt.plot(flow_df['begin_time'], flow_df['bandwidth-cm'], label=product_id)

    # ax1=plt.subplot(411)
    # ax2=plt.subplot(412)
    # ax3=plt.subplot(413)
    # ax4=plt.subplot(414)

    # ax1.plot(pivotable_df.loc[idx[le0[0],:],idx['sum','flow']].values, color="red", label=le0[0])
    # ax1.plot('flow', data=flow_df, color="red", label=product_ids[0])
    # ax2.plot('begin_time', 'flow', data=flow_df, color='blue', label='OK', linestyle='--')
    # ax3.scatter(flow_df.index, flow_df['flow'], color="red",label="S-OUT")
    # ax4.scatter('datetime', 'flow', data=flow_df, color="red",label="S-OUT")

    # xloc_date = flow_df[flow_df['xtick'].isin([0])]
    # plt.xticks(ticks=xloc_date['datetime'],labels=xloc_date['date'],rotation=90)

    # x = [pivotable_df.iloc[0,0],pivotable_df.iloc[-1,0]]
    # y = pivotable_df.loc[pivotable_df['95']=='OK','Traffic_In(Mbps)']
    # y = [y.iloc[0],y.iloc[0]]
    # plt.plot(x,y,label='95',color="red")

# xloc_date = flow_df[flow_df['xtick'].isin([0])]
# plt.xticks(ticks=xloc_date['datetime'],labels=xloc_date['date'],rotation=45)

# xloc_date = pivotable_df['begin_time'].drop_duplicates()

# xloc_date = pivotable_df.index.levels[1].astype(str)
xloc_date = pivotable_df['begin_time'].drop_duplicates()
xloc_date = xloc_date[::step]
# plt.xticks(ticks=xloc_date['datetime'],rotation=45)

plt.xticks(ticks=xloc_date, rotation=40)

plt.legend()
plt.show()

#%%
# 根据输入文件名自动生成输出文件名
# fileR = read_file
# tNow = time.strftime("%H%M%S", time.localtime())
# fileW = fileR[:fileR.rfind('.')]+'-PANDAS-' + tNow + '.xlsx'

if (isx and iscon > 1):
    print('删除历史汇总文件:', outfile_xls)
    os.remove(outfile_xls)

if (isx and iscon == 1):
    print('不需要重新写入')
else:
    print('重新写入中···')
    # 单文件多表输出
    writer = pd.ExcelWriter(outfile_xls, engine='xlsxwriter')
    boss_df.to_excel(writer, index=False, sheet_name='汇总数据')
    sf_Header.to_excel(writer, sheet_name='表头汇总')

    pivotable_df.to_excel(writer, merge_cells=False, sheet_name='汇总透视')
    pivProvince_df.to_excel(writer, merge_cells=False, sheet_name='省份透视')
    pivFlow_df.to_excel(writer, merge_cells=False, sheet_name='总流量透视')
    maxDateFlow_df.to_excel(writer, merge_cells=False, sheet_name='日峰值')
    # flow_df.to_excel(writer, sheet_name='绘图参考')
    writer.save()