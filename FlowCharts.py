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
    flow_df.iloc[0:1, :][out_col] = 'MAX'
    flow_df.iloc[1:n95, :][out_col] = 'OUT'
    flow_df.iloc[n95:n95 + 1, :][out_col] = 'OK'
    # print(flow_df)
    return flow_df


#%%
inputFolder = os.path.abspath(r'..\..')
inputFolder = os.path.join(inputFolder, 'Inputs', 'LearnCharmPro')
input_file = os.path.join(inputFolder, 'PandasHandBook.xlsx')

map_input_df = pd.read_excel(input_file, sheet_name=None, index_col=0, engine='openpyxl')
# 全局表头文件，用于替换表头。如果哪个场景需要替换表头，可以使用此表数据
sidf_header = map_input_df['表头列表']

input_df = map_input_df['FlowCharts']
inputsList = input_df.iloc[:, 0]
print(inputsList)

# header_file = inputsList[0]
code_file = inputsList[1]
read_file = inputsList[2]

# folder = inputsList[9]
# isxlsx = True

folder = inputsList[5]
isxlsx = False

outfile_xls = folder + '\\' + folder[folder.rfind('\\') + 1:] + '_PANDAS汇总_' + '.xlsx'
# 汇总文件读取前是否已存在标识
is_outfile_exist = os.path.exists(outfile_xls)
# 测试期间可选择每次都删除汇总文件
# if (is_outfile_exist):
#     print('删除历史汇总文件:', outfile_xls)
#     os.remove(outfile_xls)
# is_outfile_exist = False

#%%
# 获取目录下所有文件名，并生成待读取文件列表
read_file_list = []
fileList = FileOperator.getAllFiles(folder, notDeeep=True)
# print(len(fileList))

if isxlsx:
    for file in fileList:
        if ('.xls' in file) and ('~$' not in file):
            print(file)
            read_file_list.append(file)
else:
    read_file_list = fileList
len_toread_file = len(read_file_list)

# 全局变量初始化
boss_df = sheets_dfheader_all = pivotable_df = pivProvince_df = maxDateFlow_df = pivFlow_df = pd.DataFrame()

# 用于测试-强赋值变量
# len_toread_file = 1

if (is_outfile_exist == False or len_toread_file > 1):
    print('需要合并和重新生成')
    # 数据保量相关变量
    sheets_df_list = []
    # 设置表头行数
    headerrows = 1
    sheets_dfheader_list = []

    # 数据导入-依次读取每个文件并进行连接
    # Excel文件
    if isxlsx:
        # 用于测试：文件过多时，只读前3个进行测试
        # for file in read_file_list[:3]:
        for file in read_file_list:
            sheet_list = [0]
            # sf = pd.read_excel(file, sheet_name=sheet_list, header=None, skiprows=range(headerrows), dtype={2: str})
            df_content = pd.read_excel(file,
                                       sheet_name=sheet_list,
                                       header=None,
                                       skiprows=range(headerrows),
                                       parse_dates=[2])
            df_header = pd.read_excel(file, sheet_name=sheet_list, header=None, nrows=headerrows)
            for sheet_i in sheet_list:
                print('si=', sheet_i)
                sheets_df_list.append(df_content[sheet_i])
                sheets_dfheader_list.append(df_header[sheet_i])
    # 非Excel文件
    else:
        for file in read_file_list:
            df_content = pd.read_csv(file,
                                     skiprows=1,
                                     header=None,
                                     skipfooter=1,
                                     skipinitialspace=True,
                                     engine='python',
                                     parse_dates=[2])
            sheets_df_list.append(df_content)
    # 数据规整-连接
    boss_df = pd.concat(sheets_df_list, sort=False, ignore_index=True)
    # 表头规整-连接
    if isxlsx:
        sheets_dfheader_all = pd.concat(sheets_dfheader_list, sort=False, ignore_index=True)

    # 替换表头
    headerindex = 5
    title = sidf_header.loc[headerindex, :]
    title.dropna(inplace=True)
    print(title.values)
    boss_df.rename(columns=title, inplace=True)
    print(boss_df.info())

    # 根据product_id分类，5分钟数据汇总统计
    # pivotable_df = boss_df.pivot_table(index=['product_id', 'begin_time'], values=['flow'], aggfunc=['sum', 'count'])
    group_pivot = boss_df.groupby(['product_id']).resample('5T', on='begin_time')
    pivotable_df = group_pivot['flow'].apply(['sum', 'count'])
    # 将Multi-Index变为Single-Index
    pivotable_df.columns = ['flow', 'count-flow']

    # 添加新列
    pivotable_df['bandwidth-icp'] = pivotable_df['flow'] * 8 * 1024 / 300 / 1000 / 1000
    pivotable_df['bandwidth-cm'] = pivotable_df['flow'] * 8 / 300 / 1024
    pivotable_df['bandwidth-cm'] = pivotable_df['bandwidth-cm'].map(ceil)
    pivotable_df['95'] = 'IN'

    pivotable_df.reset_index(inplace=True)
    # pivotable_df['date'] = pivotable_df['begin_time'].str.slice(0, 8)
    # pivotable_df['time'] = pivotable_df['begin_time'].str.slice(8, )

    # 通过apply为95列打标签
    group_id = pivotable_df.groupby(['product_id'], group_keys=False)
    pivotable_df = group_id.apply(mark_95, 'flow', '95')
    pivotable_df.sort_index(inplace=True)
    # print(pivotable_df)

    # 读取时间密码，设置时间刻度间隔，单位小时
    # 非DateTime解决办法
    timestep = 6
    step = int(timestep * 60 / 5)
    code_time = pd.read_excel(code_file, sheet_name=0, dtype={'time': str})
    code_time.loc[::step, 'xtick'] = 1
    code_time.loc[code_time['time'] == '000000', 'xtick'] = 0

    # 与时间密码进行合并
    # pivotable_df = pd.merge(pivotable_df, code_time, how='left', on='time')
    # pivotable_df.set_index(['product_id', 'begin_time'],inplace=True)

    pivProvince_df = boss_df.pivot_table(index=['product_id', 'province'], values=['flow'], aggfunc='sum')
    pivProvince_df.reset_index(inplace=True)

    # 与省份密码进行合并
    code_province = pd.read_excel(code_file, sheet_name=1)
    pivProvince_df = pd.merge(pivProvince_df, code_province, how='inner', on='province')
    pivProvince_df.sort_values(['product_id', 'flow'], ascending=False, inplace=True)
    pivProvince_df.index = range(len(pivProvince_df))

    # 总流量-根据product_id透视
    pivFlow_df = boss_df.pivot_table(index=['product_id'], values=['flow'], aggfunc='sum')

    # 省份合并总流量并求得流量占比
    pivProvince_df = pd.merge(pivProvince_df,
                              pivFlow_df,
                              how='left',
                              left_on='product_id',
                              right_index=True,
                              suffixes=('', '-pidsum'))
    pivProvince_df['占比'] = pivProvince_df['flow'] / pivProvince_df['flow-pidsum']

    # group_df = pivotable_df.groupby(['product_id', 'date'])
    # maxDateFlow_df = group_df.apply(lambda x: x.nlargest(2, 'bandwidth-cm'))
    maxDateFlow_df = pivotable_df.loc[pivotable_df['95'] == 'MAX', :]
    print('合并和重新生成完成')

elif (is_outfile_exist == True and len_toread_file == 1):
    print('直接读取汇总透视')
    # pivotable_df = pd.read_excel(outfile_xls, sheet_name='汇总透视', header=[0,1],index_col=[0,1])
    # pivotable_df = pd.read_excel(outfile_xls, sheet_name='汇总透视', header=[0], index_col=[0], dtype={'begin_time': str})

    pivotable_df = pd.read_excel(outfile_xls, sheet_name='汇总透视', header=[0], index_col=[0], parse_dates=['begin_time'])
    # gyf = pivotable_df.groupby(['product_id'])
    # gyf.resample('D',on='begin_time').max()
    # gyf.resample('M',on='begin_time').sum()
    # dm = gyf.resample('D',on='begin_time',kind='period').max()

    pivProvince_df = pd.read_excel(outfile_xls, sheet_name='省份透视', header=[0], index_col=[0])
    pivFlow_df = pd.read_excel(outfile_xls, sheet_name='总流量透视', header=[0], index_col=[0])
    print('直接读取完成')

#%%
product_ids = pivotable_df['product_id'].drop_duplicates()
axlen = len(product_ids)
pivProvince_df = pivProvince_df[pivProvince_df['flow'] > 0]
pivProvince_df.index = range(len(pivProvince_df))

fig, axs = plt.subplots(2, 1)

for id, product_id in enumerate(product_ids):
    # idx = pd.IndexSlice
    # plot_data = pivotable_df.loc[idx[9001035304],idx['sum']]
    flow_df = pivotable_df.loc[pivotable_df['product_id'] == product_id]
    charge_95 = flow_df.loc[flow_df['95'] == 'OK', 'bandwidth-cm'].iloc[0]

    # 流量图中时间点间隔，单位：分钟
    chartStep = 5
    chartStep = int(chartStep / 5)
    flow_df = flow_df.iloc[::chartStep, :]

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

# xmajor_tick = pivotable_df[pivotable_df['xtick'] == 0]
# axs[0].set_xticks(ticks=xmajor_tick['begin_time'])
# axs[0].set_xticklabels(labels=xmajor_tick['begin_time'].str[4:8])
# # 使用isin，相当于==
# xminor_tick = pivotable_df[pivotable_df['xtick'].isin([1])]
# axs[0].set_xticks(ticks=xminor_tick['begin_time'], minor=True)
# axs[0].set_xticklabels(labels=xminor_tick['begin_time'].str[8:10], minor=True)

axs[1].set_xticks(pivProvince_df.index)
axs[1].set_xticklabels(pivProvince_df['省份'])

# axs[0].legend()
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
# 解决Seaborn中文显示问题
sns.set(font='SimHei')

# 测试-order参数使用
# orde = pivProvince_df.loc[pivProvince_df['product_id'] == 9001035304, '省份']
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
# fileW = fileR[:fileR.rfind('.')]+'_PANDAS_' + tNow + '.xlsx'

if (is_outfile_exist and len_toread_file > 1):
    print('删除历史汇总文件:', outfile_xls)
    os.remove(outfile_xls)

if (is_outfile_exist and len_toread_file == 1):
    print('不需要重新写入')
else:
    print('重新写入中···')
    # 单文件多表输出
    writer = pd.ExcelWriter(outfile_xls, engine='xlsxwriter')
    # boss_df.to_excel(writer, index=False, sheet_name='汇总数据')
    sheets_dfheader_all.to_excel(writer, sheet_name='表头汇总')

    pivotable_df.to_excel(writer, merge_cells=False, sheet_name='汇总透视')
    pivProvince_df.to_excel(writer, merge_cells=False, sheet_name='省份透视')
    pivFlow_df.to_excel(writer, merge_cells=False, sheet_name='总流量透视')
    maxDateFlow_df.to_excel(writer, merge_cells=False, sheet_name='日峰值')
    # flow_df.to_excel(writer, sheet_name='绘图参考')
    writer.save()
