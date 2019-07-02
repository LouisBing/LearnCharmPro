#-*-coding:utf-8-*-

from pandas import Series, DataFrame, np, ExcelWriter
import pandas as pd
import os, time
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
        #
        # sf[sf == ' '] = np.nan
        # sf.dropna(subset=sf.columns[1:2],how='all',inplace=True)
        # sf[1] = sf[1].map(str.strip)
        #
        # # 新增更新时间列
        # t = os.path.getmtime(file)
        # mt = time.strftime("%Y%m%d%H%M%S", time.localtime(t))
        # sf['更新时间'] = mt
        # # exdic[file] = sf
        exlist.append(sf)
        headerlist.append(sfH)

# 数据连接
sfall = pd.concat(exlist,sort=False)
sf_Header = pd.concat(headerlist,sort=False)

# 数据清洗
sfall.loc[sfall[0].str.contains('注：') == True, 0] = np.nan
sfall[sfall.isin([' ','\t','\\'])] = np.nan
sfall.dropna(how='all',inplace=True)
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
# fileR = r'Inputs\Test.xlsx'
# 数据导入
# xlsx = pd.ExcelFile(preFile)
# sidf_header = pd.read_excel(xlsx, sheet_name=0, header=[0,])
# sidf_header[sidf_header =='?'] = np.nan
# sidf_header.dropna(subset=sidf_header.columns[-3:],how='all',inplace=True)

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
# # 场景:数据导出
# # 根据文件名自动生成输出文件名
# fileR = newFile
# tNow = time.strftime("%H%M%S", time.localtime())
# fileW = fileR[:fileR.rfind('.')]+'-PANDAS-' + tNow + '.xlsx'
# # 单表输出
# sfall.to_excel(fileW)

# # 已知导出文件名,单文件单表输出
# sfall.to_excel(outfile_xls, sheet_name='all')

# 已知导出文件名,单文件多表输出
writer = ExcelWriter(outfile_xls,engine='xlsxwriter')
sfall.to_excel(writer,sheet_name='数据汇总')
sf_Header.to_excel(writer,sheet_name='表头汇总')
writer.save()
