#%%
import os, time
from math import ceil
import numpy as np
import pandas as pd

from functools import partial
from pandas.tseries.frequencies import to_offset

import TxtOperator, FileOperator
#%%
inputFolder = os.path.abspath(r'..\..')
inputFolder = os.path.join(inputFolder, 'Inputs', 'LearnCharmPro')
input_file = os.path.join(inputFolder, 'PandasHandBook.xlsx')

map_input_df = pd.read_excel(input_file, sheet_name=None, index_col=0, engine='openpyxl')
# 全局表头文件，用于替换表头。如果哪个场景需要替换表头，可以使用此表数据
sidf_header = map_input_df['表头列表']

#%%
# 场景:读取单个Excel下所有Sheet进行连接合并
input_df = map_input_df['多表合并']
inputsList = input_df.iloc[:, 0]
print(inputsList)
multi_sheets_file = inputsList[0]
headerrows = 5

sheets_map_dfheader = pd.read_excel(multi_sheets_file, sheet_name=None, header=None, nrows=headerrows)
sheets_map_df = pd.read_excel(multi_sheets_file, sheet_name=None, header=None, skiprows=range(headerrows))

sheets_df_all = sheets_dfheader_all = pd.DataFrame()
for sheet_key in sheets_map_dfheader.keys():
    sheets_dfheader_all = sheets_dfheader_all.append(sheets_map_dfheader[sheet_key], ignore_index=True)
    # 个性化需求：新增一列，将表名记录此列中。根据需要选择是否保留
    sheets_map_df[sheet_key]['结算省'] = sheet_key
    sheets_df_all = sheets_df_all.append(sheets_map_df[sheet_key], ignore_index=True)

#%%
# 替换表头
headerindex = 6
title = sidf_header.loc[headerindex, :]
title.dropna(inplace=True)
# print(title.values)
sheets_df_all.rename(columns=title, inplace=True)
# print(sheets_df_all.info())

#%%
sheets_df = sheets_df_all.dropna(subset=['集团客户'])
drop_index = sheets_df_all.index.drop(sheets_df.index)
sheets_drop_df = sheets_df_all.loc[drop_index, :]

#%%
fileR = multi_sheets_file
tNow = time.strftime("%H%M%S", time.localtime())
fileW = fileR[:fileR.rfind('.')] + '_PANDAS_' + tNow + '.xlsx'

# 单文件多表输出
writer = pd.ExcelWriter(fileW, engine='xlsxwriter')

sheets_df.to_excel(writer, sheet_name='总表')
sheets_dfheader_all.to_excel(writer, sheet_name='表头')
sheets_drop_df.to_excel(writer, sheet_name='删除')

writer.save()
#%%
# 场景:读取文件夹下所有Excel文件进行连接合并
input_df = map_input_df['多表合并']
inputsList = input_df.iloc[:, 0]
print(inputsList)
folder = inputsList[2]
#%%
# 根据输入文件夹生成输出文件
outfile_xls = folder + '\\' + folder[folder.rfind('\\') + 1:] + '_PANDAS汇总_' + '.xlsx'
# 如果汇总文件已存在，直接删除
isx = os.path.exists(outfile_xls)
if (isx):
    print('DelExistFile:', outfile_xls)
    os.remove(outfile_xls)
#%%
# 获取目录下所有文件名
fileList = FileOperator.getAllFiles(folder, notDeeep=True)
print(len(fileList))

sheets_df_all = sheets_dfheader_all = pd.DataFrame()
headerrows = 4
# 数据导入-依次读取每个Excel文件并进行连接
for file in fileList:
    if ('.xls' in file) and ('~$' not in file):
        print(file)
        df_header = pd.read_excel(file, sheet_name=0, header=None, nrows=headerrows)
        df_content = pd.read_excel(file, sheet_name=0, header=None, skiprows=range(headerrows))

        sheets_dfheader_all = sheets_dfheader_all.append(df_header, ignore_index=True)
        sheets_df_all = sheets_df_all.append(df_content, ignore_index=True)

# %%
fileW = outfile_xls
# 单文件多表输出
writer = pd.ExcelWriter(fileW, engine='xlsxwriter')

sheets_df_all.to_excel(writer, sheet_name='总表')
sheets_dfheader_all.to_excel(writer, sheet_name='表头')

writer.save()
# %%
# 场景:时间序列
input_df = map_input_df['DateTimes']
inputsList = input_df.iloc[:, 0]
print(inputsList)
sheet_file = inputsList[2]

df_content = pd.read_csv(sheet_file, index_col=0, parse_dates=True)

# df_content.index = pd.to_datetime(df_content.index)
# df_content.sort_values()
# df_content.sort_values('求和项:流量(KB)',ascending=False,inplace=True)
# df_content.iloc[447,:]

t5 = df_content.resample('5T')[['流量(KB)']].sum()
t5['数量'] = df_content.resample('5T')[['流量(KB)']].count()
t5['带宽（Mbps）'] = t5['流量(KB)'] * 8 / 300 / 1024
t5.sort_values('流量(KB)', ascending=False, inplace=True)
n95 = ceil(t5.shape[0] * 0.05)
t5['95计费点'] = np.nan
t5.iloc[n95, -1] = '是'
t5.loc[t5['流量(KB)'] > 31, :]

# day_df = df_content.resample('D').count()
# day_df.sort_values('流量(KB)')

# "稀疏"时间序列
# def round(t, freq):
#     freq = to_offset(freq)
#     return pd.Timestamp((t.value // freq.delta.value) * freq.delta.value)

# T5_Sparset =df_content.groupby(partial(round, freq='5T')).count()
#%%
fileR = sheet_file
tNow = time.strftime("%H%M%S", time.localtime())
fileW = fileR[:fileR.rfind('.')] + '_PANDAS_' + tNow + '.xlsx'

# 单文件多表输出
writer = pd.ExcelWriter(fileW, engine='xlsxwriter')

t5.to_excel(writer, sheet_name='T5')
# day_df.to_excel(writer, sheet_name='D')
# T5_Sparset.to_excel(writer,sheet_name='T5_Sparset')

writer.save()
# %%
