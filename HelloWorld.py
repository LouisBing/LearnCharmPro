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
