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