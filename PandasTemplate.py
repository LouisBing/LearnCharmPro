#-*-coding:utf-8-*-

from pandas import Series, DataFrame, np, ExcelWriter
import pandas as pd
import os, time
# import TxtOperator, FileOperator
from io import StringIO

# ------------------------------------------------------------------------------------------
# 数据导入
fileR = r'Inputs\Test.xlsx'
xlsx = pd.ExcelFile(fileR)
sidf_header = pd.read_excel(xlsx, sheet_name=1, header=[0,])

# ------------------------------------------------------------------------------------------
# 数据检查
print(sidf_header.shape)
print(sidf_header.info())
print(sidf_header.dtypes)
# print(sidf_header)

# ------------------------------------------------------------------------------------------
# 数据清洗
sidf_header.fillna(value=0,inplace=True)

# ------------------------------------------------------------------------------------------
# 数据筛选
bz = sidf_header.loc[sidf_header['客户名称']=='B站']

# ------------------------------------------------------------------------------------------
# 数据统计
idf1 = sidf_header.groupby('省份')['10月汇总'].agg([np.sum,np.mean])
idf2 = sidf_header.pivot_table(index=['省份'],values=['10月汇总'],aggfunc=['sum','count'])
print(idf1)

# ------------------------------------------------------------------------------------------
# 数据提取
idf1.loc[['上海市','江苏','浙江'],'sum']
idf1.sort_values('sum')


