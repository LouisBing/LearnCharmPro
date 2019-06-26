#-*-coding:utf-8-*-

from pandas import Series, DataFrame, np, ExcelWriter
import pandas as pd
import os, time
import TxtOperator, FileOperator
from io import StringIO

# ------------------------------------------------------------------------------------------
# Txt输入读取
txtFile = u'Inputs\PandasTemplate.txt'
inputsList = TxtOperator.readTxt2List(txtFile,False)
print(inputsList)

folder = inputsList[0]
preFile = inputsList[1]
newFile = inputsList[2]

print(folder)
# 相关输出文件设置
outfile_xls = folder + '\\' + folder[folder.rfind('\\')+1:] + '_PANDAS汇总_' + '.xlsx'
# 如果汇总文件已存在，直接删除
isx = os.path.exists(outfile_xls)
if(isx):
    print('DelExistFile:', outfile_xls)
    os.remove(outfile_xls)

# 相关输入：目录下所有文件
fileList = FileOperator.getAllFiles(folder,notDeeep=False)
print(len(fileList))

# # ------------------------------------------------------------------------------------------
# # 数据导入
# exlist = []
# headerlist = []
# headerrows = 3
# oldexlist = []
# for file in fileList:
#     if ('.xls' in file) and ('~$' not in file):
#         print(file)
#         sf = pd.read_excel(file, sheet_name=0, header=None, skiprows=range(headerrows))
#         sfH = pd.read_excel(file, sheet_name=0, header=None, nrows=headerrows)
#         # sf = pd.read_excel(file, sheet_name=0, header=[0,1,2])
#         # sf.columns = sidf_header.columns[0:len(sf.columns)]
#         # sf.drop([0,1,2], inplace=True)
#         # # 为防止合并后列的重排，将列名重置为数字
#         # sf.columns = range(len(sf.columns))
#         #
#         # sf[sf == ' '] = np.nan
#         # sf.dropna(subset=sf.columns[1:2],how='all',inplace=True)
#         # sf[1] = sf[1].map(str.strip)
#         #
#         # # 新增更新时间列
#         # t = os.path.getmtime(file)
#         # mt = time.strftime("%Y%m%d%H%M%S", time.localtime(t))
#         # sf['更新时间'] = mt
#         # # exdic[file] = sf
#         exlist.append(sf)
#         headerlist.append(sfH)
#
# # 数据汇总
# sfall = pd.concat(exlist,sort=False)
# sf_Header = pd.concat(headerlist,sort=False)

# # ------------------------------------------------------------------------------------------
# 数据导入
newDf = pd.read_excel(newFile, sheet_name=0, header=[0,])
newDf[newDf=='?']=np.nan
newDf.dropna(subset=newDf.columns[-4:],how='all',inplace=True)
newDf['月份'] = 'NEW'

preDf = pd.read_excel(preFile, sheet_name=0, header=[0,])
preDf[preDf=='?']=np.nan
preDf.dropna(subset=preDf.columns[-3:],how='all',inplace=True)
dupSet = preDf.columns.drop(['签约主体','客户名称','签署地市名称'])
preDf['月份'] = 'PRE'

sfall = pd.concat([newDf,preDf],sort=False)

# ------------------------------------------------------------------------------------------
# fileR = r'Inputs\Test.xlsx'
# 数据导入
# xlsx = pd.ExcelFile(preFile)
# sidf_header = pd.read_excel(xlsx, sheet_name=0, header=[0,])
# sidf_header[sidf_header =='?'] = np.nan
# sidf_header.dropna(subset=sidf_header.columns[-3:],how='all',inplace=True)

sidf_name = pd.read_excel(preFile, sheet_name=3, header=[0,])
sidf_name.drop_duplicates(['key_desc','key_type_desc'],inplace=True)
sfall = pd.merge(sfall,sidf_name[['key_desc','key_type_desc']],how='left',left_on='签约主体',right_on='key_desc')

# # dupSet = sfall.columns[1:1+6]
# dupSet = sfall.columns.drop(['签约主体','key_desc'])
dupSet = dupSet.append(sfall.columns[[-1,]])
print(dupSet)
sfall['DUP'] = sfall.duplicated(subset=dupSet,keep=False)

# # ------------------------------------------------------------------------------------------
# # 数据检查
# print(sidf_header.shape)
# print(sidf_header.info())
# print(sidf_header.dtypes)
# # print(sidf_header)
#
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
# # 单文件单表输出
# sfall.to_excel(outfile_xls, sheet_name='all')

# # 单文件多表输出
# writer = ExcelWriter(outfile_xls,engine='xlsxwriter')
# sfall.to_excel(writer,sheet_name='数据汇总')
# # sf_Header.to_excel(writer,sheet_name='表头汇总')
# writer.save()


# 数据输出
fileR = newFile
tNow = time.strftime("%H%M%S", time.localtime())
fileW = fileR[:fileR.rfind('.')]+'-PANDAS-' + tNow + '.xlsx'
# 单表输出
sfall.to_excel(fileW)
