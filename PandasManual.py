#%%
import pandas as pd
#%%
xlsx = r'F:\个人文件夹\ProJects\LearnCharmPro\Inputs\【PandasTest】变量导入.xlsx'
adf:pd.DataFrame = pd.read_excel(xlsx, header=0, sheet_name=0, index_col=0)
bdf:pd.DataFrame = pd.read_excel(xlsx, header=0, sheet_name=1, index_col=0)
cdf = pd.concat([adf, bdf], axis=1)
#%%
# # 数据导入
# sf = pd.read_excel(file, sheet_name=0, header=None, skiprows=range(headerrows))
# sfH = pd.read_excel(file, sheet_name=0, header=None, nrows=headerrows)

# # ------------------------------------------------------------------------------------------
# # 数据检查
# print(sidf_header.shape)
# print(sidf_header.info())
# print(sidf_header.dtypes)
# print(sidf_header)

# # ------------------------------------------------------------------------------------------
# # 数据清洗
#%% 增
# # 数据清洗-填充空值
# sidf_header.fillna(value=0,inplace=True)
# sfall[1].fillna(method='pad',inplace=True)
# 数据清洗-删除重复行
# sidf_name.drop_duplicates(['key_desc','key_type_desc'],inplace=True)
#%% 删
# # 数据清洗-删除列
# sf.drop([0,1,2], inplace=True)
# # 数据清洗-删除空行
# sfall.dropna(subset=sfall.columns[:20] ,how='all',inplace=True)
# # 数据清洗-筛选:删除一些行不如筛选一些行更方便直观
# midsf.drop(midsf[midsf['历史数据']==True].index,inplace=True)
# midsf = midsf[midsf['历史数据']==False]
#%% 改
# # 数据清洗-列名重命名
# sf.columns = range(len(sf.columns))
# sidf_name.rename(columns={'key_desc':'签约主体','key_type_desc':'客户简称'},inplace=True)
# # 数据清洗-值替换
# sfall.replace([r'^[\W]+$',r'^注：.*'],np.nan,regex=True,inplace=True)
# newDf[newDf=='?']=np.nan
# # 数据清洗-函数级应用:单元格处理，删除单元格空格
# sfall.loc[:,1]  = sfall.loc[:,1].map(str.strip,na_action='ignore')
#%%
# # ------------------------------------------------------------------------------------------
# # 数据规整-新增列
# sf['更新时间'] = mt
# # 数据规整-连接
# sfall = pd.concat(exlist,sort=False,ignore_index=True)
# # 数据规整：函数级应用
# sf_filemove.apply(fileMove, axis=1,  args=(dir,))
# # 数据规整-合并
# sfall = pd.merge(sfall,sidf_name[['签约主体','客户简称']],how='left',on='签约主体')
# # 数据规整-判断重复行：根据列名生成重复标签列
# sfall['DUP'] = sfall.duplicated(subset=dupSet,keep=False)
# # ------------------------------------------------------------------------------------------
# 场景：数据统计
# 数据透视表
# pivotable_df = read_df.pivot_table(index=['省份','客户名称'], values=['10月汇总'], aggfunc=['sum', 'count'])
# # 数据分组
# group_df = read_df.groupby(['省份','客户名称'],sort=True)['10月汇总'].agg([np.sum, np.mean])
# # 数据排序
# sort_df = read_df.sort_values(['省份','客户名称','10月汇总'], ascending=False)
# group_df.sort_values(group_df.columns[0], ascending=False, inplace=True)
# # 数据筛选
# filtra_df = read_df.loc[((read_df['客户名称'].isin(['腾讯','爱奇艺'])) & (read_df['10月汇总']>6000000)),['省份','客户名称','10月汇总']]
# # ------------------------------------------------------------------------------------------
# # 场景:数据导出
# # 根据输入文件名自动生成输出文件名
# fileR = header_file
# tNow = time.strftime("%H%M%S", time.localtime())
# fileW = fileR[:fileR.rfind('.')]+'-PANDAS-' + tNow + '.xlsx'

# # 单文件单表输出
# sidf_header.to_excel(fileW, sheet_name='all')

# # 单文件多表输出
# writer = ExcelWriter(fileW,engine='xlsxwriter')
# sf_new.to_excel(writer,sheet_name='最新数据')
# sf_history.to_excel(writer,sheet_name='历史数据')
# sf_Header.to_excel(writer,sheet_name='表头汇总')
# sf_error.to_excel(writer,sheet_name='异常文件')
# midsf.to_excel(writer,sheet_name='中间表')
# sf_pivtable.to_excel(writer, sheet_name='透视')
# sf_sort.to_excel(writer, sheet_name='排序')
# writer.save()