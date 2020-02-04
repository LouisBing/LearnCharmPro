#%%
import os
import time
from math import ceil

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import FileOperator
import TxtOperator


#%%
def mark_95(flow_df, sort_col, out_col):
    n95 = ceil(flow_df.shape[0] * 0.05)
    flow_df.sort_values(sort_col, ascending=False, inplace=True)
    flow_df.iloc[:n95, :][out_col] = 'OUT'
    flow_df.iloc[n95:n95 + 1, :][out_col] = 'OK'
    flow_df.iloc[n95:n95 + 1, -1] = 4

    # print(flow_df)
    return flow_df


#%%
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

outfile_xls = folder + '\\' + folder[folder.rfind('\\') + 1:] + '_PANDAS汇总_' + '.xlsx'
isx = os.path.exists(outfile_xls)
# 测试期间可选择每次都删除汇总文件
# if (isx):
#     print('删除历史汇总文件:', outfile_xls)
#     os.remove(outfile_xls)
# isx = False

# 全局表头文件，用于替换表头。如果哪个场景需要替换表头，可以使用此表数据
sidf_header = pd.read_excel(header_file, sheet_name=3, header=0, index_col=0)
#%%
# 获取目录下所有文件名，并汇总xls文件
xlslist = []
fileList = FileOperator.getAllFiles(folder, notDeeep=True)
# print(len(fileList))
isxlsx = True
if isxlsx:
    for file in fileList:
        if ('.xls' in file) and ('~$' not in file):
            print(file)
            xlslist.append(file)
else:
    xlslist = fileList
iscon = len(xlslist)

# 全局变量初始化
boss_df = sf_Header = pivotable_df = pivProvince_df = maxDateFlow_df = pivFlow_df = pd.DataFrame()
if (isx == False or iscon > 1):
    print('需要合并和重新生成')
    # 数据保量相关变量
    exlist = []
    # 设置表头行数
    headerrows = 1
    headerlist = []

    # 数据导入-依次读取每个Excel文件并进行连接
    if isxlsx:
        for file in xlslist:
            pd_xls = pd.ExcelFile(file)
            sheet_list = pd_xls.sheet_names[:]
            sf = pd.read_excel(file, sheet_name=sheet_list, header=None, skiprows=range(headerrows), dtype={2: str})
            sfH = pd.read_excel(file, sheet_name=sheet_list, header=None, nrows=headerrows)
            for si in sheet_list:
                print('si=', si)
                exlist.append(sf[si])
                headerlist.append(sfH[si])
    else:
        for file in xlslist:
            sf = pd.read_csv(file,
                             skiprows=1,
                             header=None,
                             skipfooter=1,
                             skipinitialspace=True,
                             engine='python',
                             dtype={2: str})
            # sfH = pd.read_excel(file, sheet_name=0, header=None, nrows=headerrows)
            exlist.append(sf)
            # headerlist.append(sfH)
    # 数据规整-连接
    boss_df = pd.concat(exlist, sort=False, ignore_index=True)
    if isxlsx:
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
    pivotable_df['95'] = 'IN'

    pivotable_df.reset_index(inplace=True)
    pivotable_df['date'] = pivotable_df['begin_time'].str.slice(0, 8)
    pivotable_df['time'] = pivotable_df['begin_time'].str.slice(8, )

    # 时间刻度间隔，单位：小时
    timestep = 6
    step = int(timestep * 60 / 5)
    # 流量图中时间点间隔，单位：分钟
    chartStep = 60
    chartStep = int(chartStep / 5)

    code_time = pd.read_excel(code_file, sheet_name=0, dtype={'time': str})
    code_province = pd.read_excel(code_file, sheet_name=1)
    code_time.loc[::chartStep, 'xtick'] = 2
    code_time.loc[::step, 'xtick'] = 1
    code_time.loc[code_time['time'] == '000000', 'xtick'] = 0

    pivotable_df = pd.merge(pivotable_df, code_time, how='left', on='time')
    # pivotable_df.set_index(['product_id', 'begin_time'],inplace=True)

    pivProvince_df = boss_df.pivot_table(index=['product_id', 'province'], values=['flow'], aggfunc='sum')
    pivProvince_df.reset_index(inplace=True)
    pivProvince_df = pd.merge(pivProvince_df, code_province, how='inner', on='province')
    pivProvince_df.sort_values(['product_id', 'flow'], ascending=False, inplace=True)
    pivProvince_df.index = range(len(pivProvince_df))
    #%%
    group_id = pivotable_df.groupby(['product_id'], group_keys=False)
    pivotable_df = group_id.apply(mark_95, 'flow', '95')
    pivotable_df.sort_index(inplace=True)
    # print(pivotable_df)

    pivFlow_df = boss_df.pivot_table(index=['product_id'], values=['flow'], aggfunc='sum')
    pivProvince_df = pd.merge(pivProvince_df,
                              pivFlow_df,
                              how='left',
                              left_on='product_id',
                              right_index=True,
                              suffixes=('', '-pidsum'))
    pivProvince_df['占比'] = pivProvince_df['flow'] / pivProvince_df['flow-pidsum']

    group_df = pivotable_df.groupby(['product_id', 'date'])
    maxDateFlow_df = group_df.apply(lambda x: x.nlargest(1, 'bandwidth-cm'))
    print('合并和重新生成完成')

elif (isx == True and iscon == 1):
    print('直接读取汇总透视')
    # pivotable_df = pd.read_excel(outfile_xls, sheet_name='汇总透视', header=[0,1],index_col=[0,1])
    pivotable_df = pd.read_excel(outfile_xls, sheet_name='汇总透视', header=[0], index_col=[0], dtype={'begin_time': str})
    pivProvince_df = pd.read_excel(outfile_xls, sheet_name='省份透视', header=[0], index_col=[0])
    pivFlow_df = pd.read_excel(outfile_xls, sheet_name='总流量透视', header=[0], index_col=[0])
    print('直接读取完成')

#%%
# le0 = pivotable_df.index.get_level_values(0)
# le0 = le0.drop_duplicates()
# product_ids = pivotable_df.index.levels[0]
product_ids = pivotable_df['product_id'].drop_duplicates()
axlen = len(product_ids)
pivProvince_df = pivProvince_df[pivProvince_df['flow'] > 0]
pivProvince_df.index = range(len(pivProvince_df))

fig, axs = plt.subplots(2, 1)

for id, product_id in enumerate(product_ids):
    # idx = pd.IndexSlice
    # plot_data = pivotable_df.loc[idx[9001035304],idx['sum']]
    flow_df = pivotable_df.loc[pivotable_df['product_id'] == product_id]
    flow_df = flow_df.loc[flow_df['xtick'].notna()]
    charge_95 = flow_df.loc[flow_df['95'] == 'OK', 'bandwidth-cm'].iloc[0]

    # ax = plt.subplot(axlen,1,id+1)
    # ax.plot('datetime', 'flow', data=flow_df, color="red",label="S-OUT")
    axs[0].set_title('CDN业务流量图')
    axs[0].set_xlabel('时间')
    axs[0].set_ylabel('流量(Mbps)')
    axs[0].plot(flow_df['begin_time'], flow_df['bandwidth-cm'], label=product_id, marker='1')

    x_95 = [flow_df['begin_time'].iloc[0], flow_df['begin_time'].iloc[-1]]
    y_95 = [charge_95, charge_95]
    print(x_95, y_95)
    axs[0].plot(x_95, y_95, color="red", marker='.', linestyle='--')

    # province_df = pivProvince_df[(pivProvince_df['product_id'] == product_id) & (pivProvince_df['flow'] > 0)]
    # axs[1].bar(province_df['省份'], province_df['flow'], label=product_id)
    # axs[1].plot(province_df['省份'], province_df['flow'], label=str(product_id) + 'line')

    province_df = pivProvince_df[pivProvince_df['product_id'] == product_id]
    axs[1].bar(province_df.index, province_df['占比'], label=product_id)

    # axs[1].plot(province_df['省份'], province_df['flow'], label=str(product_id) + 'line')

    # ax1=plt.subplot(411)
    # ax2=plt.subplot(412)
    # ax3=plt.subplot(413)
    # ax4=plt.subplot(414)

    # ax1.plot(pivotable_df.loc[idx[le0[0],:],idx['sum','flow']].values, color="red", label=le0[0])
    # ax1.plot('flow', data=flow_df, color="red", label=product_ids[0])
    # ax2.plot('begin_time', 'flow', data=flow_df, color='blue', label='OK', linestyle='--')
    # ax3.scatter(flow_df.index, flow_df['flow'], color="red",label="S-OUT")
    # ax4.scatter('datetime', 'flow', data=flow_df, color="red",label="S-OUT")

# xloc_date = pivotable_df.index.levels[1].astype(str)
# xloc_date = pivotable_df['begin_time'].drop_duplicates()
# xloc_date = xloc_date[::step]
# plt.xticks(ticks=xloc_date['datetime'],rotation=45)
# plt.xticks(ticks=xloc_date, rotation=40)

xmajor_tick = pivotable_df[pivotable_df['xtick'] == 0]
axs[0].set_xticks(ticks=xmajor_tick['begin_time'])
axs[0].set_xticklabels(labels=xmajor_tick['begin_time'].str[4:8])
# 使用isin，相当于==
xminor_tick = pivotable_df[pivotable_df['xtick'].isin([1])]
axs[0].set_xticks(ticks=xminor_tick['begin_time'], minor=True)
axs[0].set_xticklabels(labels=xminor_tick['begin_time'].str[8:10], minor=True)

axs[1].set_xticks(pivProvince_df.index)
axs[1].set_xticklabels(pivProvince_df['省份'])

axs[0].legend()
# axs[1].legend()

# 解决无法显示中文问题
# 步骤一（替换sans-serif字体）
plt.rcParams['font.sans-serif'] = ['SimHei']
# 步骤二（解决坐标轴负数的负号显示问题）
plt.rcParams['axes.unicode_minus'] = False

# plt.legend()
plt.show()
#%%
sns.set(style="whitegrid")
sns.set(font='SimHei')  # 解决Seaborn中文显示问题

orde = pivProvince_df.loc[pivProvince_df['product_id'] == 9001035304, '省份']
# gp = sns.catplot(x='省份',
#                  y='占比',
#                  hue='product_id',
#                  data=pivProvince_df,
#                  kind='bar',
#                  palette="muted",
#                  height=6,
#                  order=orde)
gp = sns.catplot(
    x='省份',
    y='占比',
    hue='product_id',
    data=pivProvince_df,
    kind='bar',
    #  palette="muted",
    height=6)
# gp.despine(left=True)
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
    # boss_df.to_excel(writer, index=False, sheet_name='汇总数据')
    sf_Header.to_excel(writer, sheet_name='表头汇总')

    pivotable_df.to_excel(writer, merge_cells=False, sheet_name='汇总透视')
    pivProvince_df.to_excel(writer, merge_cells=False, sheet_name='省份透视')
    pivFlow_df.to_excel(writer, merge_cells=False, sheet_name='总流量透视')
    maxDateFlow_df.to_excel(writer, merge_cells=False, sheet_name='日峰值')
    # flow_df.to_excel(writer, sheet_name='绘图参考')
    writer.save()
