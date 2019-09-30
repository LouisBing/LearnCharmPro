#-*-coding:utf-8-*-

import os
import shutil
import time
from io import StringIO

import pandas as pd
from pandas import DataFrame, ExcelWriter, Series, np

import FileOperator
import TxtOperator

# ------------------------------------------------------------------------------------------
# 场景：从TXT文件中输入变量
txtFile = r'Inputs\PandasTemplate.txt'
inputsList = TxtOperator.readTxt2List(txtFile,False)
print(inputsList)

SCENE = 1
if SCENE == 0:  
    # ------------------------------------------------------------------------------------------
    # 场景:读取文件夹下所有Excel文件进行连接合并
    # 1.1：根据输入文件夹生成输出文件
    folder = inputsList[0]
    outfile_xls = folder + '\\' + folder[folder.rfind('\\')+1:] + '_PANDAS汇总_' + '.xlsx'
    # 如果汇总文件已存在，直接删除
    isx = os.path.exists(outfile_xls)
    if(isx):
        print('DelExistFile:', outfile_xls)
        os.remove(outfile_xls)

    # 1.2：获取目录下所有文件名
    fileList = FileOperator.getAllFiles(folder,notDeeep=True)
    print(len(fileList))

    # ------------------------------------------------------------------------------------------
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
            # 数据清洗-删除列
            # sf.drop([0,1,2], inplace=True)
            # 数据清洗-重命名列
            # sf.columns = range(len(sf.columns))

            # 数据规整-新增列
            t = os.path.getmtime(file)
            mt = time.strftime("%Y%m%d%H%M%S", time.localtime(t))
            sf['更新时间'] = mt
            sf['文件名'] = file
            exlist.append(sf)
            headerlist.append(sfH)

    # 数据规整-连接
    sfall = pd.concat(exlist,sort=False,ignore_index=True)
    sf_Header = pd.concat(headerlist,sort=False,ignore_index=True)

    # 数据清洗
    # sfall.loc[sfall[0].str.contains('注：') == True, 0] = np.nan
    # sfall[sfall.isin([' ','\t','\\'])] = np.nan
    # sfall.replace([' ','\t','\\'],np.nan,inplace=True)
    # sfall.replace([r'^[\s\\]+$',r'^注：.*'],np.nan,regex=True,inplace=True)
    # 数据清洗-替换
    sfall.replace([r'^[\W]+$',r'^注：.*'],np.nan,regex=True,inplace=True)
    print(sfall.columns[:20])
    # 数据清洗-删除空行
    sfall.dropna(subset=sfall.columns[:20] ,how='all',inplace=True)
    # 数据清洗-填充空值
    sfall[1].fillna(method='pad',inplace=True)
    # 数据清洗-单元格处理，删除单元格空格
    sfall.loc[:,1]  = sfall.loc[:,1].map(str.strip,na_action='ignore')
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

    # 细分场景:文件分类
    # def fileMove(df,dir):
    #     moveFile = df['文件名']
    #     dir = folder
    #     shutil.move(moveFile, dir)
    #
    # strNow = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # sf_filemove = midsf[midsf['历史数据']==False]
    # dir = folder + r'\最新文件' + strNow
    # os.makedirs(dir)
    # 数据规整：函数级应用
    # sf_filemove.apply(fileMove, axis=1,  args=(dir,))
    #
    # sf_filemove = midsf[midsf['历史数据']==True]
    # dir = folder + r'\历史文件' + strNow
    # os.makedirs(dir)
    # 数据规整：函数级应用
    # sf_filemove.apply(fileMove, axis=1,  args=(dir,))
    #
    # sf_filemove = midsf[midsf['异常文件']==True]
    # sf_filemove.drop_duplicates(subset='文件名', inplace=True)
    # dir = folder + r'\异常文件' + strNow
    # os.makedirs(dir)
    # 数据规整：函数级应用
    # sf_filemove.apply(fileMove, axis=1,  args=(dir,))

    sf_pivtable = sf_new.pivot_table(values=19, index=[9, 12, 11, 13, 1, 2, 7], aggfunc=np.count_nonzero)
    # print(sf_new.iloc[:,10])
    sf_sort = sf_new.loc[sf_new.iloc[:,10]=='是',:]
    sf_sort.sort_values(by=[9,12,11,13,1,2,7],ascending=True,inplace=True)
    sf_sort = sf_sort[sf_sort.columns.drop([3,4,5,6,8])]

    # # 删除一些行不如筛选一些行更方便直观
    # midsf.drop(midsf[midsf['历史数据']==True].index,inplace=True)
    # midsf = midsf[midsf['历史数据']==False]

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
elif SCENE == 1:
    # ------------------------------------------------------------------------------------------
    # 场景:重复数据比对
    # 新数据导入,新增标签列
    preFile = inputsList[1]
    newFile = inputsList[2]
    newDf = pd.read_excel(newFile, sheet_name=0, header=[0,])
    # 数据清洗-值替换
    newDf[newDf=='?']=np.nan
    # 数据清洗-删除空行
    newDf.dropna(subset=newDf.columns[-4:],how='all',inplace=True)
    # 数据规整-新增列
    newDf['月份'] = 'NEW'
    
    # 老数据导入,新增标签列
    preDf = pd.read_excel(preFile, sheet_name=0, header=[0,])
    # 数据清洗-值替换
    preDf[preDf=='?']=np.nan
    # 数据清洗-删除空行
    preDf.dropna(subset=preDf.columns[-3:],how='all',inplace=True)
    # 重复行比对依据列
    dupSet = preDf.columns.drop(['签约主体','客户名称','签署地市名称'])
    # 数据规整-新增列
    preDf['月份'] = 'PRE'
    
    # 数据规整-连接：新老数据连接
    sfall = pd.concat([newDf,preDf],sort=False)
    
    # 读取中间表，用于表格合并
    sidf_name = pd.read_excel(preFile, sheet_name=3, header=[0,])
    # 数据清洗-删除重复行
    sidf_name.drop_duplicates(['key_desc','key_type_desc'],inplace=True)
    # 数据清洗-列名重命名
    sidf_name.rename(columns={'key_desc':'签约主体','key_type_desc':'客户简称'},inplace=True)
    # 数据规整-合并
    # sfall = pd.merge(sfall,sidf_name[['key_desc','key_type_desc']],how='left',left_on='签约主体',right_on='key_desc')
    sfall = pd.merge(sfall,sidf_name[['签约主体','客户简称']],how='left',on='签约主体')
    
    # 更新重复行比对依据列
    # dupSet = sfall.columns[1:1+6]
    # dupSet = sfall.columns.drop(['签约主体','key_desc'])
    dupSet = dupSet.append(sfall.columns[[-1,]])
    print(dupSet)
    # 数据预处理-判断重复行：根据列名生成重复标签列
    sfall['DUP'] = sfall.duplicated(subset=dupSet,keep=False)
    
    # 根据文件名自动生成输出文件名
    fileR = newFile
    tNow = time.strftime("%H%M%S", time.localtime())
    fileW = fileR[:fileR.rfind('.')]+'-PANDAS-' + tNow + '.xlsx'
    # 单表输出
    sfall.to_excel(fileW)
elif SCENE == 2:
    # ------------------------------------------------------------------------------------------
    # 场景：表头处理
    header_file = inputsList[3]
    xlsx = pd.ExcelFile(header_file)
    sidf_header1 = pd.read_excel(xlsx, sheet_name=1, header=[0,1])
    # sidf_header1.columns.name='列名'
    sidf_header1.columns.names=('表头1级','表头2级')
    
    sidf_header2 = pd.read_excel(xlsx, sheet_name=2, header=[0])
    sidf_header2.columns.name='表头2'
    
    sidf_header3 = pd.read_excel(xlsx, sheet_name=2, header=None)
    sidf_header3.columns.name='表头3'
    
    # header与skiprows：跳过这些行，下面的行从0编号开始读取。如skiprows=0，即跳过第1行，然后header=0，则原表中第2行为表头。
    # 如果直接header=1，则默认跳过第1行
    
    # 根据输入文件名自动生成输出文件名
    tNow = time.strftime("%H%M%S", time.localtime())
    fileW = header_file[:header_file.rfind('.')]+'-PANDAS-' + tNow + '.xlsx'
    # 单文件多表输出
    writer = ExcelWriter(fileW,engine='xlsxwriter')
    sidf_header1.to_excel(writer,sheet_name='表头1')
    sidf_header2.to_excel(writer,sheet_name='表头2')
    sidf_header3.to_excel(writer,sheet_name='表头3')
    writer.save()
elif SCENE == 3:
    # ------------------------------------------------------------------------------------------
    # 场景：数据统计
    fileR = inputsList[4]
    xlsx = pd.ExcelFile(fileR)
    read_df = pd.read_excel(xlsx, sheet_name=1)

    # 数据透视表
    pivotable_df = read_df.pivot_table(index=['省份','客户名称'], values=['10月汇总'], aggfunc=['sum', 'count'])
    # pivotable_df.sort_values(pivotable_df.columns[0], ascending=False, inplace=True)
    # 数据分组
    group_df = read_df.groupby(['省份','客户名称'],sort=True)['10月汇总'].agg([np.sum, np.mean])
    # group_df.sort_values(group_df.columns[0], ascending=False, inplace=True)
    # 数据排序
    sort_df = read_df.sort_values(['省份','客户名称','10月汇总'], ascending=False)
    # 数据筛选
    filtra_df = read_df.loc[((read_df['客户名称'].isin(['腾讯','爱奇艺'])) & (read_df['10月汇总']>6000000)),['省份','客户名称','10月汇总']]

    # 根据输入文件名自动生成输出文件名
    tNow = time.strftime("%H%M%S", time.localtime())
    fileW = fileR[:fileR.rfind('.')]+'-PANDAS-' + tNow + '.xlsx'

    # 单文件多表输出
    writer = ExcelWriter(fileW,engine='xlsxwriter')
    pivotable_df.to_excel(writer,sheet_name='数据透视')
    group_df.to_excel(writer,sheet_name='数据分组')
    sort_df.to_excel(writer,sheet_name='数据排序')
    filtra_df.to_excel(writer,sheet_name='数据筛选')
    writer.save()