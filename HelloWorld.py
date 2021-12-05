#-*-coding:utf-8-*-
#%% Hello World
print('Hello World !')
#%% Hello for
sum = 0
for i in range(1, 11):
    print('this is =', i)
    sum += i
print('SUM=%s' % sum)
print(sum * sum)


#%% hello try with func
# 定义函数
def testExcept(level):
    if level < 5:
        # 触发异常后，后面的代码就不会再执行
        # raise Exception("Invalid level=%s" % level)
        raise Exception('ERR_ARGS')
    print(level)


try:
    testExcept(5)  # 触发异常
except Exception as err:
    print('触发异常', err)
    print(err.args)
else:
    print('未触发异常')
#%% Hello try
a = 9
b = 0
try:
    c = a / b
    # raise Exception()
except ZeroDivisionError:
    print('b=0')
    # print(zo)
except:
    # print("Unexpected error:", sys.exc_info()[0])
    print("Unexpected error")
    # raise
else:
    print('c=%s' % c)

# %%
import PandasHandBook

pdhand = PandasHandBook.PandasHandBook()
inpl = pdhand.getInputsList('多表合并')

# 单文件多表合并
multi_sheets_file = inpl[1]
he, pda = pdhand.singlefile_multi_sheets_concat(multi_sheets_file)
print(he, pda)
pdhand.to_excel_dflist(multi_sheets_file, [he, pda])

# 文件夹多文件合并
folder = inpl[5]
he, pda, outfile_xls = pdhand.folder_multi_file_concat(folder, headerrows=2, new_colname='wenjian')
# pdhand.rename_title(pda, title_index=9)
drop, con = pdhand.divide_with_na_col(pda, subset_col=[2])
he = he.append(drop)
pdhand.to_excel_dflist(outfile_xls, [con, he], need_add_time=False)