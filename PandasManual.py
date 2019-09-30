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
# # 数据清洗-填充空值
# sidf_header.fillna(value=0,inplace=True)
# # 数据清洗-删除列
# sf.drop([0,1,2], inplace=True)
# # 数据清洗-重命名列
# sf.columns = range(len(sf.columns))

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