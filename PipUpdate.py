# import pip
# from subprocess import call
# from pip._internal.utils.misc import get_installed_distributions
# n = 1
# s = len(get_installed_distributions())

# for dist in get_installed_distributions():
#     print(dist.project_name)
#     call("pip install --upgrade " + dist.project_name, shell=True)

import os

#%% 功能测试
# 执行DOS命令
upcm = 'python -m pip install --upgrade pip'
# upcm = 'ping www.baidu.com'
print(upcm)

result = os.popen(upcm)
result = result.read()
print(result)

# 从pip list --outdated命令结果中提取库名
# packinfo = 'pandas     0.25.0  0.25.1 wheel'
# packinfo = packinfo[0:packinfo.find(' ')]
# print(packinfo)
#%%
# ERROR: Could not install packages due to an EnvironmentError
# https://blog.csdn.net/a781751136/article/details/80231406
# 使用--user参数将导致安装变为用户目录非系统目录，不建议使用。建议直接使用最原始的更新版本，也不加版本号
cmd = 'pip list --outdated'
result = os.popen(cmd)
lines = result.readlines()
for resline_i in lines:
    print(resline_i)

size_l = len(lines)
for packi in range(2, size_l):
    print('%s/%s' % (packi - 1, size_l - 1))
    packinfo = lines[packi]
    packinfo = packinfo.split()
    # print(packinfo)
    # pipupc = 'pip install --upgrade %s==%s' % (packinfo[0], packinfo[2])
    pipupc = 'pip install --upgrade %s' % (packinfo[0], )
    if(packinfo[0]=='xlrd'):
        continue
    print(pipupc)
    os.system(pipupc)

os.system(cmd)