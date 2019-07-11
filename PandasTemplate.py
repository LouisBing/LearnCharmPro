#-*-coding:utf-8-*-

from pandas import Series, DataFrame, np, ExcelWriter
import pandas as pd
import os, time, shutil
import TxtOperator, FileOperator
from io import StringIO

# ------------------------------------------------------------------------------------------
# 输入变量-Txt
txtFile = u'Inputs\PandasTemplate.txt'
inputsList = TxtOperator.readTxt2List(txtFile,False)
print(inputsList)

folder = inputsList[0]
print(folder)
preFile = inputsList[1]
newFile = inputsList[2]
# ------------------------------------------------------------------------------------------
# 场景:读取文件夹下所有Excel文件进行连接合并

# 根据输入文件夹生成输出文件
outfile_xls = folder + '\\' + folder[folder.rfind('\\')+1:] + '_PANDAS汇总_' + '.xlsx'
# 如果汇总文件已存在，直接删除
isx = os.path.exists(outfile_xls)
if(isx):
    print('DelExistFile:', outfile_xls)
    os.remove(outfile_xls)

# 获取目录下所有文件名
fileList = FileOperator.getAllFiles(folder,notDeeep=False)
print(len(fileList))

# 数据保量相关变量
exlist = []
# 设置表头行数
headerrows = 1
headerlist = []
oldexlist = []

# 数据导入-依次读取每个Excel文件并进行连接
for file in fileList:
    if ('.xls' in file) and ('~$' not in file):
        print(file)
        sf = pd.read_excel(file, sheet_name=0, header=None, skiprows=range(headerrows))
        sfH = pd.read_excel(file, sheet_name=0, header=None, nrows=headerrows)
        # sf = pd.read_excel(file, sheet_name=0, header=[0,1,2])
        # sf.columns = sidf_header.columns[0:len(sf.columns)]
        # sf.drop([0,1,2], inplace=True)
        # # 为防止合并后列的重排，将列名重置为数字
        # sf.columns = range(len(sf.columns))

        # 新增更新时间列
        t = os.path.getmtime(file)
        mt = time.strftime("%Y%m%d%H%M%S", time.localtime(t))
        sf['更新时间'] = mt
        sf['文件名'] = file
        # # exdic[file] = sf
        exlist.append(sf)
        headerlist.append(sfH)

# 数据连接
sfall = pd.concat(exlist,sort=False,ignore_index=True)
sf_Header = pd.concat(headerlist,sort=False,ignore_index=True)

# 数据清洗
# sfall.loc[sfall[0].str.contains('注：') == True, 0] = np.nan
# sfall[sfall.isin([' ','\t','\\'])] = np.nan
# sfall.replace([' ','\t','\\'],np.nan,inplace=True)
# sfall.replace([r'^[\s\\]+$',r'^注：.*'],np.nan,regex=True,inplace=True)
sfall.replace([r'^[\W]+$',r'^注：.*'],np.nan,regex=True,inplace=True)
print(sfall.columns[:20])
sfall.dropna(subset=sfall.columns[:20] ,how='all',inplace=True)
sfall[1].fillna(method='pad',inplace=True)
# sfall.sort_values(by=['更新时间',0],inplace=True,ascending=False)


midsf = sfall[[1,'更新时间','文件名']]
midsf.drop_duplicates(inplace=True)
midsf.sort_values(by='更新时间',ascending=False,inplace=True)
midsf['异常文件']=midsf.duplicated(subset='文件名',keep=False)
midsf2=midsf[midsf['异常文件']==False]
midsf['历史数据']=midsf2.duplicated(subset=1)

sfall = pd.merge(sfall,midsf,how='left')

sf_new = sfall[sfall['历史数据']==False]
sf_history = sfall[sfall['历史数据']==True]
sf_error = sfall[sfall['异常文件']==True]

# 场景:文件分类
# def fileMove(df,dir):
#     moveFile = df['文件名']
#     dir = folder
#     shutil.move(moveFile, dir)
#
# strNow = time.strftime("%Y%m%d%H%M%S", time.localtime())
# sf_filemove = midsf[midsf['历史数据']==False]
# dir = folder + r'\最新文件' + strNow
# os.makedirs(dir)
# sf_filemove.apply(fileMove, axis=1,  args=(dir,))
#
# sf_filemove = midsf[midsf['历史数据']==True]
# dir = folder + r'\历史文件' + strNow
# os.makedirs(dir)
# sf_filemove.apply(fileMove, axis=1,  args=(dir,))
#
# sf_filemove = midsf[midsf['异常文件']==True]
# sf_filemove.drop_duplicates(subset='文件名', inplace=True)
# dir = folder + r'\异常文件' + strNow
# os.makedirs(dir)
# sf_filemove.apply(fileMove, axis=1,  args=(dir,))

sf_pivtable = sf_new.pivot_table(values=19, index=[9, 12, 11, 13, 1, 2, 7], aggfunc=np.count_nonzero)
# print(sf_new.iloc[:,10])
sf_sort = sf_new.loc[sf_new.iloc[:,10]=='是',:]
sf_sort.sort_values(by=[9,12,11,13,1,2,7],ascending=True,inplace=True)
sf_sort = sf_sort[sf_sort.columns.drop([3,4,5,6,8])]

# # ------------------------------------------------------------------------------------------
# # 场景:重复数据比对
# # 新数据导入,新增标签列
# newDf = pd.read_excel(newFile, sheet_name=0, header=[0,])
# newDf[newDf=='?']=np.nan
# newDf.dropna(subset=newDf.columns[-4:],how='all',inplace=True)
# newDf['月份'] = 'NEW'
# # 老数据导入,新增标签列
# preDf = pd.read_excel(preFile, sheet_name=0, header=[0,])
# preDf[preDf=='?']=np.nan
# preDf.dropna(subset=preDf.columns[-3:],how='all',inplace=True)
# dupSet = preDf.columns.drop(['签约主体','客户名称','签署地市名称'])
# preDf['月份'] = 'PRE'
# # 新老数据连接
# sfall = pd.concat([newDf,preDf],sort=False)
#
# # 数据合并
# sidf_name = pd.read_excel(preFile, sheet_name=3, header=[0,])
# sidf_name.drop_duplicates(['key_desc','key_type_desc'],inplace=True)
# sidf_name.rename(columns={'key_desc':'签约主体','key_type_desc':'客户简称'},inplace=True)
# # sfall = pd.merge(sfall,sidf_name[['key_desc','key_type_desc']],how='left',left_on='签约主体',right_on='key_desc')
# sfall = pd.merge(sfall,sidf_name[['签约主体','客户简称']],how='left',on='签约主体')
#
# # 选择要对比相关列名
# # dupSet = sfall.columns[1:1+6]
# # dupSet = sfall.columns.drop(['签约主体','key_desc'])
# dupSet = dupSet.append(sfall.columns[[-1,]])
# print(dupSet)
# # 根据列名生成重复标签列
# sfall['DUP'] = sfall.duplicated(subset=dupSet,keep=False)
# ------------------------------------------------------------------------------------------
# # 场景：表头专门处理
# # 数据导入
# header_file = inputsList[3]
# xlsx = pd.ExcelFile(header_file)
# sidf_header = pd.read_excel(xlsx, sheet_name=1, header=[0])
# sidf_header.columns.name='列名'
# # sidf_header.columns.names=('a','b')
# # sidf_header[sidf_header =='?'] = np.nan
# # sidf_header.dropna(subset=sidf_header.columns[-3:],how='all',inplace=True)
#
# # header_file = inputsList[3]
# # xlsx = pd.ExcelFile(header_file)
# # sidf_header = pd.read_excel(xlsx, sheet_name=1, nrows=2, header=None)
# # sidf_header.columns.name='列名'

# # ------------------------------------------------------------------------------------------
# # 数据检查
# print(sidf_header.shape)
# print(sidf_header.info())
# print(sidf_header.dtypes)
# print(sidf_header)

# # ------------------------------------------------------------------------------------------
# # 数据清洗
# sidf_header.fillna(value=0,inplace=True)
#
# # ------------------------------------------------------------------------------------------
# # 数据筛选
# bz = sidf_header.loc[sidf_header['客户名称']=='B站']
#
# # ------------------------------------------------------------------------------------------
# # 数据统计
# idf1 = sidf_header.groupby('省份')['10月汇总'].agg([np.sum,np.mean])
# idf2 = sidf_header.pivot_table(index=['省份'],values=['10月汇总'],aggfunc=['sum','count'])
# print(idf1)
#
# # ------------------------------------------------------------------------------------------
# # 数据提取
# idf1.loc[['上海市','江苏','浙江'],'sum']
# idf1.sort_values('sum')

# ------------------------------------------------------------------------------------------
# 场景:数据导出
# 根据文件名自动生成输出文件名
# fileR = header_file
# tNow = time.strftime("%H%M%S", time.localtime())
# fileW = fileR[:fileR.rfind('.')]+'-PANDAS-' + tNow + '.xlsx'
# # 单表输出
# sidf_header.to_excel(fileW)

# # 已知导出文件名,单文件单表输出
# sfall.to_excel(outfile_xls, sheet_name='all')

# 已知导出文件名,单文件多表输出
writer = ExcelWriter(outfile_xls,engine='xlsxwriter')
sf_new.to_excel(writer,sheet_name='最新数据')
sf_history.to_excel(writer,sheet_name='历史数据')
sf_Header.to_excel(writer,sheet_name='表头汇总')
sf_error.to_excel(writer,sheet_name='异常文件')
midsf.to_excel(writer,sheet_name='中间表')
sf_pivtable.to_excel(writer, sheet_name='透视')
sf_sort.to_excel(writer, sheet_name='排序')
writer.save()
