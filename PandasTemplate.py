#-*-coding:utf-8-*-

from pandas import Series, DataFrame, np, ExcelWriter
import pandas as pd
import os, time
# import TxtOperator, FileOperator
from io import StringIO

# ------------------------------------------------------------------------------------------
# 数据导入
fileR = r'Inputs\TOP55客户统谈出账收入统计-汇总.xlsx'
xlsx = pd.ExcelFile(fileR)
sidf_header = pd.read_excel(xlsx, sheet_name=1, header=[0,])

# ------------------------------------------------------------------------------------------
# 数据检查
print(sidf_header.shape)
print(sidf_header.info())
print(sidf_header.dtypes)
# print(sidf_header)

# ------------------------------------------------------------------------------------------
# 数据统计
idf1 = sidf_header.groupby('省份')['10月汇总'].agg([np.sum,np.mean])
idf2 = sidf_header.pivot_table(index=['省份'],values=['10月汇总'],aggfunc=['sum','count'])
print(idf1)