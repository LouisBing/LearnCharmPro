#-*-coding:utf-8-*-

from pandas import Series, DataFrame, np, ExcelWriter
import pandas as pd
import os, time
import TxtOperator, FileOperator
from io import StringIO

# 数据加载
# ------------------------------------------------------------------------------------------
# ############################################
# ####Txt读取输入变量值####
txtFile = u'Inputs\PandasTemplate.txt'
inputsList = TxtOperator.readTxt2List(txtFile,False)
print(inputsList)
# # #############################################
# # 输入为单个文件
# fileR = inputsList[0]
# xlsx = pd.ExcelFile(fileR)
# sidf = pd.read_excel(xlsx, sheet_name=2, header=[1,])
# ############################################
# 输入为文件夹
folder = inputsList[0]
print(folder)
# 根据输入设置输出文件的名称
outfile_xls = folder + '\\' + folder[folder.rfind('\\')+1:] + '_PANDAS汇总_' + '.xlsx'
# 如果汇总文件已存在，直接删除
isx = os.path.exists(outfile_xls)
if(isx):
    os.remove(outfile_xls)

# 目录下面所有文件中的指定表
fileList = FileOperator.getAllFiles(folder,notDeeep=False)
print(len(fileList))

fileR = r'F:\互联网解决方案部\销售支撑费\2018年\各省邮件反馈\最终确认无问题\！各省确认文件@晓桐\附件七：2018年XX省公司TOP55客户统谈出账收入统计模板-表头.xls'
xlsx = pd.ExcelFile(fileR)
sidf_header = pd.read_excel(xlsx, sheet_name=0, header=[0,])

exdic = {}
exlist = []
oldexlist = []
for file in fileList:
    if '.xls' in file:
        print(file)
        sf = pd.read_excel(file, sheet_name=0, header=None, skiprows=[0, 1, 2])
        sf = pd.read_excel(file, sheet_name=0, header=None)
        sf.columns = sidf_header.columns[0:len(sf.columns)]
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

# 所有表汇总
sfall = pd.concat(exlist,sort=False)
# ############################################
# 单个文件多个表
# sidl = []
# for name in xlsx.sheet_names[:-2]:
#     print(name)
#     id = pd.read_excel(xlsx, sheet_name=name, header=[1,2])
#     # id.columns = range(id.columns.size)
#     sidl.append(id)
# ############################################
# 特殊格式文件读取
# 测试代码
# # sf = pd.read_csv(r'D:\网络下载专区\BaiduNetdiskDownload\阿里腾讯巨人金山20180524\20180608\ali\阿里巴巴金融',encoding='UTF-8')
# # print(open(r'D:\网络下载专区\BaiduNetdiskDownload\阿里腾讯巨人金山20180524\20180608\ali\阿里巴巴金融').read())
#
# f= open(r'D:\网络下载专区\BaiduNetdiskDownload\阿里腾讯巨人金山20180524\20180608\ali\阿里巴巴金融','r', encoding='UTF-8')
# sf = pd.read_csv(StringIO(f.read()))

# for file in fileList:
#     print(file)
#     f = open(file, 'r', encoding='UTF-8')
#     # print(f)
#     sf = pd.read_csv(StringIO(f.read()), header=None)
#     # exdic[file] = sf
#     exlist.append(sf)

# 数据预处理：检查、规整
# ------------------------------------------------------------------------------------------
# print(excelFile.columns)
# ############################################
# 规整表头
# fileR = r'F:\互联网解决方案部\销售支撑费\2018年\2018年支撑费收取表-分省拆分\调研表-整理 - 备份20181127-仅用于拆分-表头.xlsx'
# xlsx = pd.ExcelFile(fileR)
# sidf_header = pd.read_excel(xlsx, sheet_name=1, header=[0,1])
# sidf_header.reset_index(col_level=1,col_fill='序号')
# 规整列名
# sal.rename(columns={'应收收入\n（万元，\n税前）':'应收收入\n（万元，税前）'},level=1,inplace=True)
# 规整列序
# sfa.reindex(columns=sf.columns)

# 数据清洗和准备
# ------------------------------------------------------------------------------------------
# 样例
# sfa.dropna(subset=sfa.columns[1:2],how='all',thresh=3,inplace=True)

# 因为要删除数据一定要慎之又慎，一定要对删除的数据特征进行充分的总结再删除：
# 能否统一删除前几行，能否根据某一列的特征删除行（湖南上报时删除了第1列，导致列错位）
sfall.replace({'1810账期':{'1810账期':np.nan}}, inplace=True)
sfall.dropna(subset=['1810账期',],how='any',inplace=True)

# sfa.loc[sfa[0].str.contains('注：') == True, 0] = np.nan
# sfa[sfa == ' '] = np.nan
# sfa.str.strip()
# name.drop_duplicates(['key_desc','key_type_desc'],inplace=True)


# 数据处理:提取、筛选、排序、聚合、合并和重塑
# ------------------------------------------------------------------------------------------
# ############################################
# sidf['重复行'] = sidf.duplicated(['实例ID'])
# sidf['重复行2'] = sidf.loc[sidf['来源']=='支撑费',:].duplicated(['实例ID'])
# id = sidf.loc[sidf['来源']=='支撑费','实例ID']
# id1 = sidf.loc[sidf['来源']=='一经','实例ID']
# sidf['重复行3']=id1.isin(id)
# ############################################
# em = pd.merge(er5000,es,how='left',on='目的IP')
# ############################################
# 多层索引
# sf.xs('本省IDC服务全网总解析次数',level=1,axis=1)
# idx = pd.IndexSlice
# sf.loc[idx[:],idx[:,'本省IDC服务全网总解析次数']].max()
# sidc = sf.loc[idx[:],idx[:,'本省IDC服务全网总解析次数']]
# sidc = sf.loc[:,(slice(None),'本省IDC服务全网总解析次数')]
# sidc = sf.loc(axis=1)[:,'本省IDC服务全网总解析次数']
# # sidc.iloc[0]=sidc.iloc[0]/sidc.iloc[0]['全国','本省IDC服务全网总解析次数']
# for i in range(len(sidc.index)):
#     name = str(sidc.index[i])
#     print(i,name)
#     # sidc.iloc[i].sort_values(ascending=False).to_excel('分析.xlsx', sheet_name=name)
#     t0 = sidc.iloc[i]
#     t0 = t0.reset_index(level=0)
#     rc = pd.MultiIndex.from_arrays([[t0.columns[1], t0.columns[1]], ['全国排行', '解释次数']])
#     t0.columns = rc
#     t0[(rc[0][0], '百分比')]=t0[(rc[0][0], '解释次数')] / t0[(rc[0][0])].iloc[0, 1]
#     t0.sort_values(by=(rc[0][0], '解释次数'), ascending=False, inplace=True)
#     r = pd.concat([r, t0], axis=1)

# ############################################
# a = excelFile.ix[excelFile['HIT总次数']>1000,:3]
# a = excelFile[excelFile['HIT总次数']>1000]
# add = excelFile[excelFile['C']==1]
# add.loc[:,'D'] = add.loc[:,'A']+add.loc[:,'B']
# excelFile.loc[excelFile['C']==1,'D'] = excelFile.loc[excelFile['C']==1,'A']+excelFile.loc[excelFile['C']==1,'B']
# a.sort_values(by='HIT总次数',ascending=False)
# us = excelFile.unstack(0)
# ############################################
# for exsf in exlist[1:]:
#     provinceList = sfa[1].unique()
#     addpro = exsf[1].unique()[0]
#     if addpro in provinceList:
#         nt = exsf['更新时间'].unique()[0]
#         ot = sfa.loc[sfa[1]==addpro,'更新时间'].unique()[0]
#         if nt>ot:
#             oldexlist.append(sfa[sfa[1].isin([addpro])])
#             sfa = sfa[~sfa[1].isin([addpro])]
#         else:
#             oldexlist.append(exsf)
#             continue
#
#     sfa = pd.concat([sfa,exsf])
# ############################################
# le=10
# s=len(sidf)
# for n in range(int(s/le)):
#     for l in range(le):
#         si = n*le
#         ei = si+le
#         a = sidf.iloc[si,0:6]
#         b = sidf.iloc[si:ei,6:11]
#         b.set_index('账期',inplace=True)
#         c=b.T
#         a=a.append(c.loc['实际出账（含税，元）',:])
#     sidf_new=sidf_new.append(a,ignore_index=True)

# 数据聚合:分组、汇总和统计
# ------------------------------------------------------------------------------------------
# suma = excelFile.groupby('C').max()
# pio = excelFile.pivot('C','A')
# gSum = excelFile.groupby([excelFile['目的IP'],excelFile['运营商'],excelFile['目的IP所属省份']]).sum()
# gSum.to_excel('gSum.xlsx', sheet_name='gSum')
# pSum = excelFile.pivot_table(index=['目的IP', '运营商', '目的IP所属省份'],values=['解析次数'],aggfunc=np.sum)
# pSum.to_excel('pSum.xlsx', sheet_name='pSum')
# provGroup = sidf.groupby(['省份','运营商'])
# eidf = provGroup.apply(ipAdd)
# eidf = provGroup['IP起始地址段','IP终止地址段'].agg([('a',ipAdd)])

# 数据导出
# ------------------------------------------------------------------------------------------
# # 输出文件名中新增时间字段，便于不断生成新的文件
# tNow = time.strftime("%H%M%S", time.localtime())
# outfile_xls = fileR[:fileR.rfind('.')]+'_PANDAS(XXX)_' + tNow + '.xlsx'

# 单文件单表输出
sfall.to_excel(outfile_xls, sheet_name='all')

# 单文件多表输出
# writer = ExcelWriter(outfile_xls,engine='xlsxwriter')
# sfa.to_excel(writer,sheet_name='只保留最新')
# sfa_old.to_excel(writer,sheet_name='之前版本')
# sfall.to_excel(writer,sheet_name='所有汇总（供参考）')
# writer.save()

# fileR2 = fileR[:fileR.rfind('.')]+'-数据合并.xlsx'
# # em2.to_excel(fileR2,sheet_name='原始数据与ICP合并')
# with ExcelWriter(fileR2,engine='xlsxwriter') as writer:
#     er5000.to_excel(writer, sheet_name='ICP数据')
#     em2.to_excel(writer, sheet_name='原始数据与ICP合并')

# 多文件输出
# for file in fileList:
#     print(file)
#     excelFile = pd.read_excel(file,sheet_name=0)
#     # print(f)
#     er5000 = excelFile[excelFile['解析次数'] >= 5000]
#     fileR = file[:file.rfind('.')]+'筛选.xlsx'
#     print(fileR)
#     er5000.to_excel(fileR)
