#-*-coding:utf-8-*-
#%%
import os
import time

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ------------------------------------------------------------------------------------------
# # 官方事例
# # fig = plt.figure()  # an empty figure with no axes
# # fig.suptitle('No axes on this figure')  # Add a title so we know which it is
#
# # fig, ax_lst = plt.subplots(2, 2)  # a figure with a 2x2 grid of Axes
#
# x = np.linspace(0, 10, 10)
#
# plt.plot(x, x, label='linear')
# plt.plot(x, x**2, label='quadratic')
# plt.plot(x, x**3, label='cubic')
#
# plt.xlabel('x label')
# plt.ylabel('y label')
#
# plt.title("Simple Plot")
# plt.legend()
# plt.show()
#
#
# def my_plotter(ax, data1, data2, param_dict):
#     """
#     A helper function to make a graph
#
#     Parameters
#     ----------
#     ax : Axes
#         The axes to draw to
#
#     data1 : array
#        The x data
#
#     data2 : array
#        The y data
#
#     param_dict : dict
#        Dictionary of kwargs to pass to ax.plot
#
#     Returns
#     -------
#     out : list
#         list of artists added
#     """
#     out = ax.plot(data1, data2, **param_dict)
#     return out
#
# data1, data2, data3, data4 = np.random.randn(4, 100)
# fig, ax = plt.subplots(1, 1)
# my_plotter(ax, data1, data2, {'marker': 'x'})
# plt.show()
#
#
# fig, (ax1, ax2) = plt.subplots(1, 2)
# my_plotter(ax1, data1, data2, {'marker': 'x'})
# my_plotter(ax2, data3, data4, {'marker': 'o'})
# plt.show()
# ------------------------------------------------------------------------------------------
# # Matplotlib可视化最有价值的50个图表
# # https://www.jiqizhixin.com/articles/2019-01-15-11
#
# large = 22; med = 16; small = 12
# params = {'axes.titlesize': large,
#           'legend.fontsize': med,
#           'figure.figsize': (16, 10),
#           'axes.labelsize': med,
#           'axes.titlesize': med,
#           'xtick.labelsize': med,
#           'ytick.labelsize': med,
#           'figure.titlesize': large}
#
# plt.rcParams.update(params)
# plt.style.use('seaborn-whitegrid')
# sns.set_style("white")
#
# # %matplotlib inline
# # Version
# print(mpl.__version__)  #> 3.0.0
# print(sns.__version__)  #> 0.9.0
#
#
# midwest = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/midwest_filter.csv")
#
#
#
# # Prepare Data
#
# # Create as many colors as there are unique midwest['category']
#
# categories = np.unique(midwest['category'])
#
# colors = [plt.cm.tab10(i/float(len(categories)-1)) for i in range(len(categories))]
#
#
#
# # Draw Plot for Each Category
#
# plt.figure(figsize=(16, 10), dpi= 80, facecolor='w', edgecolor='k')
#
#
#
# for i, category in enumerate(categories):
#
#     plt.scatter('area', 'poptotal',
#
#                 data=midwest.loc[midwest.category==category, :],
#
#                 s=20, cmap=colors[i], label=str(category))
#
#     # "c=" 修改为 "cmap="，Python数据之道 备注
#
#
#
# # Decorations
#
# plt.gca().set(xlim=(0.0, 0.1), ylim=(0, 90000),
#
#               xlabel='Area', ylabel='Population')
#
#
#
# plt.xticks(fontsize=12); plt.yticks(fontsize=12)
#
# plt.title("Scatterplot of Midwest Area vs Population", fontsize=22)
#
# plt.legend(fontsize=12)
#
# plt.show()


# Import Data

# df = pd.read_csv('https://github.com/selva86/datasets/raw/master/AirPassengers.csv')
#
#
#
# # Draw Plot
#
# plt.figure(figsize=(16,10), dpi= 80)
#
# plt.plot('date', 'value', data=df, color='tab:red')
#
#
#
# # Decoration
#
# plt.ylim(50, 750)
#
# xtick_location = df.index.tolist()[::12]
#
# xtick_labels = [x[:4] for x in df.date.tolist()[::12]]
#
# plt.xticks(ticks=xtick_location, labels=xtick_labels, rotation=0, fontsize=12, horizontalalignment='center', alpha=.7)
#
# plt.yticks(fontsize=12, alpha=.7)
#
# plt.title("Air Passengers Traffic (1949 - 1969)", fontsize=22)
#
# plt.grid(axis='both', alpha=.3)
#
#
#
# # Remove borders
#
# plt.gca().spines["top"].set_alpha(0.0)
#
# plt.gca().spines["bottom"].set_alpha(0.3)
#
# plt.gca().spines["right"].set_alpha(0.0)
#
# plt.gca().spines["left"].set_alpha(0.3)
#
# plt.show()

# ------------------------------------------------------------------------------------------
# xlsx = r'Inputs\CDN详单数据20190101-20190124.xls'
# sf_CDN = pd.read_excel(xlsx)
#
# plt.plot('带宽', data=sf_CDN )
# plt.plot('通信费(元) ', data=sf_CDN )
# # plt.gca().set(xlim=(20190101000000, 20190201000000), ylim=(0, 90000000),
# #
# #               xlabel='Area', ylabel='Population')
# plt.show()
# ------------------------------------------------------------------------------------------
#%%
inputFolder = os.path.abspath(r'..\..')
inputFolder = os.path.join(inputFolder, 'Inputs', 'LearnCharmPro')
xlsx = os.path.join(inputFolder, 'MX960-95计费(2015-02).xlsx')

sf_CDN = pd.read_excel(xlsx,header=2,sheet_name=1)
n95 = int(sf_CDN.shape[0]*0.05)+1
sf_CDN.sort_values('Traffic_In(Mbps)',ascending=False,inplace=True)
#%%
mx = pd.read_excel(xlsx,header=[1,2],sheet_name=0)
mx.replace([r'^[\D]+.*'],np.nan,regex=True,inplace=True)
#%%
# 真实数据本身含有全为空的情况，此操作会导致真实数据被删除，导致后面concat操作失败
# mx.dropna(how='all', axis=1, inplace=True)
#%%
idx = pd.IndexSlice
midmx = mx.loc[:,idx[:,['时间', 'Traffic_In(Mbps)', 'Traffic_Out 流量(Mbps)']]]
#%%
col_len = midmx.columns.size
sf_all = pd.DataFrame()
# sf_all = midmx.iloc[:,[0,1]]
# sf_all.set_index(keys=sf_all.columns[0],inplace=True)
# sf_all.dropna(how='all',inplace=True)
# ValueError: Shape of passed values is (7781, 8), indices imply (7778, 8)
for coli in range(0,col_len,2):
    colj= coli+1
    a=midmx.iloc[:,[coli,colj]]
    a.set_index(keys=a.columns[0],inplace=True)
    a.dropna(how='all',inplace=True)
    # print(coli,colj)
    sf_all = pd.concat([sf_all,a], axis=1)
    # print(sf_all.head())
#%% 代码测试
# a = midmx.iloc[:,[0,1]].head(5)
# b = midmx.iloc[:,[2,3]].head(7)
# a.set_index(keys=a.columns[0],inplace=True)
# b.set_index(keys=b.columns[0],inplace=True)
# a.dropna(how='all',inplace=True)
# b.dropna(how='all',inplace=True)
# c = pd.concat([a,b], axis=1)
#%%
sf_CDN = sf_all.groupby(level=1,axis=1).sum()

n95 = int(sf_CDN.shape[0]*0.05)+1
sf_CDN.sort_values('Traffic_In(Mbps)',ascending=False,inplace=True)
sf_CDN['日期']=sf_CDN.index.map(lambda x:x.split()[0])
sf_CDN['95']='IN'
sf_CDN.iloc[:n95,-1]='OUT'
sf_CDN.iloc[n95,-1]='OK'

sf_CDN.sort_index(inplace=True)
#%% matplotlib不使用data参数
# X轴为时间点，字符串类型，plot不会自动排序，除非字符串相同，否则向后插入
step = 12
plot_data = sf_CDN.iloc[::step,:]
out_data = plot_data[plot_data['95']=='OUT']
xloc_date = plot_data.loc[:,'日期']
xloc_date.drop_duplicates(inplace=True)

plt.plot(plot_data.index, plot_data['Traffic_In(Mbps)'],color="blue",label="L-OK")
plt.scatter(out_data.index, out_data['Traffic_In(Mbps)'],color="red",label="S-OUT",linewidths=0.0001)
plt.xticks(ticks=xloc_date.index,labels=xloc_date,rotation=30)

x = [plot_data.index[0],plot_data.index[-1]]
y = sf_CDN.loc[sf_CDN['95']=='OK','Traffic_In(Mbps)']
y = [y.iloc[0],y.iloc[0]]
plt.plot(x,y,label='95',color="red")

plt.legend()
plt.show()
#%% matplotlib使用data参数
# X轴使用数值类型，plot会自动排序
step = 12
sf_CDN.index.name='时间点'
sf_CDN.reset_index(inplace=True)
sf_CDN.index.name='NO'
sf_CDN.reset_index(inplace=True)

plt.scatter('NO', 'Traffic_In(Mbps)', data=sf_CDN[sf_CDN['95']=='OUT'][::step],color="red",label="S-OUT",linewidths=0.0001)
plt.scatter('NO', 'Traffic_In(Mbps)', data=sf_CDN[sf_CDN['95']=='OK'][::step],color="blue",label="S-OK",linewidths=0.0001)
plt.plot('NO', 'Traffic_In(Mbps)', data=sf_CDN[::step],color="blue",label="L-OK")
x = [sf_CDN.iloc[0,0],sf_CDN.iloc[-1,0]]
y = sf_CDN.loc[sf_CDN['95']=='OK','Traffic_In(Mbps)']
y = [y.iloc[0],y.iloc[0]]
plt.plot(x,y,label='95',color="red")

xloc_date:pd.DataFrame = sf_CDN.loc[:,['NO', '日期']]
xloc_date.drop_duplicates(subset='日期', inplace=True)
plt.xticks(ticks=xloc_date['NO'],labels=xloc_date['日期'],rotation=30)

plt.legend()
plt.show()
#%%
# 场景:数据导出
# 根据输入文件名自动生成输出文件名
fileR = xlsx
tNow = time.strftime("%H%M%S", time.localtime())
fileW = fileR[:fileR.rfind('.')]+'_PANDAS_' + tNow + '.xlsx'

# 单文件多表输出
writer = pd.ExcelWriter(fileW,engine='xlsxwriter')
midmx.to_excel(writer,sheet_name='全量端口数据')
sf_all.to_excel(writer,sheet_name='有效数据')
sf_CDN.to_excel(writer,sheet_name='汇总统计数据')
writer.save()
