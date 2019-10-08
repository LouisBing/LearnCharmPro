#-*-coding:utf-8-*-
#%%
import os
pin = 'ping www.baidu.com'

cmd = 'pip list --outdated'
result = os.popen(cmd)
# res = result.read()
# print(res)

# ERROR: Could not install packages due to an EnvironmentError
# https://blog.csdn.net/a781751136/article/details/80231406
lines = result.readlines()
for paki in range(2,len(lines)):
    pa = lines[paki]
    pa = pa[0:pa.find(' ')]
    # print(pa)
    pipupc = 'pip install --upgrade %s' % pa
    print(pipupc)
    os.system(pipupc)

# pa = lines[2]
# pa.find(' ')

# upcm = 'pip install --upgrade openpyxl'
# result = os.popen(upcm)
# res = result.read()
# print(res)

# result = os.popen(cmd)
# res = result.read()
# print(res)
# #%%
# print('Hello World !')
# #%%
# sum = 0
# for i in range(1,11):
#     print('this is =', i)
#     sum += i
# print('SUM=%s' % sum)
# #%%
# print(sum*sum)

# #%%
