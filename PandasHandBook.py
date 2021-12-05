#%%
import os, time
from math import ceil
import numpy as np
import pandas as pd
import seaborn as sns

from functools import partial
from pandas.tseries.frequencies import to_offset

import TxtOperator, FileOperator
#%%


class PandasHandBook:
    inputFolder = os.path.abspath(r'..\..')
    inputFolder = os.path.join(inputFolder, 'Inputs', 'LearnCharmPro')
    input_file = os.path.join(inputFolder, 'PandasHandBook.xlsx')
    map_input_df = sidf_header = 0

    def __init__(self) -> None:
        self.loading()

    def loading(self):
        self.map_input_df = pd.read_excel(self.input_file, sheet_name=None, index_col=0, engine='openpyxl')
        # 全局表头文件，用于替换表头。如果哪个场景需要替换表头，可以使用此表数据
        self.sidf_header = self.map_input_df['表头列表']

    def getInputsList(self, sheet_name='ComMon'):
        input_df = self.map_input_df[sheet_name]
        inputsList = input_df.iloc[:, 0]
        print(inputsList)
        return inputsList

    # 场景:读取单个Excel下所有Sheet进行连接合并
    def singlefile_multi_sheets_concat(self, multi_sheets_file, headerrows=1, new_colname=False):
        print(multi_sheets_file)

        sheets_map_dfheader = pd.read_excel(multi_sheets_file, sheet_name=None, header=None, nrows=headerrows)
        sheets_map_df = pd.read_excel(multi_sheets_file, sheet_name=None, header=None, skiprows=range(headerrows))

        sheets_df_all = sheets_dfheader_all = pd.DataFrame()
        for sheet_key in sheets_map_dfheader.keys():
            # 个性化需求：新增一列，将表名记录此列中。根据需要选择是否保留
            if (new_colname):
                sheets_map_dfheader[sheet_key][new_colname] = sheet_key
                sheets_map_df[sheet_key][new_colname] = sheet_key

            sheets_dfheader_all = sheets_dfheader_all.append(sheets_map_dfheader[sheet_key], ignore_index=True)
            sheets_df_all = sheets_df_all.append(sheets_map_df[sheet_key], ignore_index=True)

        return sheets_dfheader_all, sheets_df_all

    # 场景:读取文件夹下所有Excel文件进行连接合并
    def folder_multi_file_concat(self, folder, headerrows=1, new_colname=False):
        print(folder)
        # 根据输入文件夹生成输出文件
        outfile_xls = folder + '\\' + folder[folder.rfind('\\') + 1:] + '_PANDAS汇总_' + '.xlsx'
        # 如果汇总文件已存在，直接删除
        is_outfile_exist = os.path.exists(outfile_xls)
        if (is_outfile_exist):
            print('DelExistFile:', outfile_xls)
            os.remove(outfile_xls)

        # 获取目录下所有文件名
        fileList = FileOperator.getAllFiles(folder, notDeeep=True)
        print(len(fileList))

        sheets_df_all = sheets_dfheader_all = pd.DataFrame()
        # 数据导入-依次读取每个Excel文件并进行连接
        for file in fileList:
            if ('.xls' in file) and ('~$' not in file):
                print(file)
                df_header = pd.read_excel(file, sheet_name=0, header=None, nrows=headerrows)
                df_content = pd.read_excel(file, sheet_name=0, header=None, skiprows=range(headerrows))

                # 个性化需求：新增一列，将表名记录此列中。根据需要选择是否保留
                if (new_colname):
                    df_header[new_colname] = file
                    df_content[new_colname] = file

                sheets_dfheader_all = sheets_dfheader_all.append(df_header, ignore_index=True)
                sheets_df_all = sheets_df_all.append(df_content, ignore_index=True)

        return sheets_dfheader_all, sheets_df_all, outfile_xls

    # 根据指定列是否为na，将一个DF分成两个DF
    def divide_with_na_col(self, sheets_df_all, subset_col):
        sheets_df_contend = sheets_df_all.dropna(subset=subset_col)
        drop_index = sheets_df_all.index.drop(sheets_df_contend.index)
        sheets_df_drop = sheets_df_all.loc[drop_index, :]
        return sheets_df_drop, sheets_df_contend

    # 替换表头
    def rename_title(self, df_to_retitle, title_index):
        title = self.sidf_header.loc[title_index, :]
        title.dropna(inplace=True)
        df_to_retitle.rename(columns=title, inplace=True)
        return df_to_retitle

    def to_excel_dflist(self, file_without_time, dflist, need_add_time=True):
        fileW = file_without_time
        if need_add_time:
            tNow = time.strftime("%H%M%S", time.localtime())
            fileW = fileW[:fileW.rfind('.')] + '_PANDAS_' + tNow + '.xlsx'

        writer = pd.ExcelWriter(fileW, engine='xlsxwriter')

        # 单文件多表输出
        for i, df in enumerate(dflist):
            df.to_excel(writer, sheet_name='Sheet' + str(i + 1))

        writer.save()


def FunctionName(args):
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
    input_df = map_input_df['数据可视化']
    inputsList = input_df.iloc[:, 0]
    print(inputsList)
    sheet_file = inputsList[0]

    df_content = pd.read_excel(sheet_file, parse_dates=['账期'])
    tpc = df_content.pivot_table('账期出账', aggfunc='sum', columns='客户', index='账期')

    from pyecharts.globals import CurrentConfig, NotebookType

    CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_NOTEBOOK
    # CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB

    from pyecharts import options as opts
    from pyecharts.charts import Bar, Line, Pie
    from pyecharts.charts import Scatter
    from pyecharts.globals import ChartType, SymbolType, ThemeType

    bar_pro = Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    bar_pro.add_xaxis(tpc.index.tolist())
    for tp in tpc.columns:
        bar_pro.add_yaxis(tp, tpc[tp].tolist())

    tpc.columns
    bar_pro.set_global_opts(
        brush_opts=opts.BrushOpts(),
        datazoom_opts=opts.DataZoomOpts(type_='inside'),
        toolbox_opts=opts.ToolboxOpts(),
        tooltip_opts=opts.TooltipOpts(is_show=True, trigger="axis", axis_pointer_type="cross"),
    )
    bar_pro.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    bar_pro.render_notebook()

    bar_pro = Scatter(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    bar_pro.add_xaxis(tpc.index.tolist())
    for tp in tpc.columns:
        bar_pro.add_yaxis(tp, tpc[tp].tolist())

    tpc.columns
    bar_pro.set_global_opts(
        brush_opts=opts.BrushOpts(),
        datazoom_opts=opts.DataZoomOpts(type_='inside'),
        toolbox_opts=opts.ToolboxOpts(),
        tooltip_opts=opts.TooltipOpts(is_show=True, trigger="axis", axis_pointer_type="cross"),
    )
    bar_pro.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    #%%
    bar_pro.set_global_opts(visualmap_opts=[
        opts.VisualMapOpts(
            type_="size",
            max_=15000000,
            min_=20000,
            range_size=[20, 100],
            # range_text=['High', 'Low'],
            pos_left='left'
            # range_color=['blue','red'],
        ),
        opts.VisualMapOpts(
            type_="color",
            max_=15000000,
            min_=20000,
            # range_size=[20, 100],
            # range_text=['High', 'Low'],
            pos_left='right',
            range_color=['blue', 'red'],
            is_calculable=False,
        )
    ])

    # bar_pro.set_global_opts(visualmap_opts=opts.VisualMapOpts(
    #     type_="color",
    #     max_=15000000,
    #     min_=20000,
    #     # range_size=[20, 100],
    #     # range_text=['High', 'Low'],
    #     pos_left='right',
    #     range_color=['blue', 'red'],
    # ))
    bar_pro.render_notebook()
    # %%
