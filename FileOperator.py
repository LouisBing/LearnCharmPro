# -*- coding: utf-8 -*-
import os
import glob
import shutil
import re


#获得目录下的所有文件夹和文件列表
#返回文件列表
def getAllFiles(rootDir, notDeeep=False):
    filelist = []
    dirlist = []
    rwalk = os.walk(rootDir)
    # print(len(rwalk))
    for dirpath, dirnames, filenames in rwalk:
        dirlist.append(dirpath)
        for fileItr in filenames:
            filenameAbs = os.path.join(dirpath, fileItr)
            filelist.append(filenameAbs)
        if notDeeep:
            break
    # print u'dirlist'
    # for dirItr in dirlist:
    #     print dirItr, os.path.isdir(dirItr)
    # print u'filelist'
    # for fileItr in filelist:
    #     print fileItr, os.path.isfile(fileItr)
    return filelist


def getNewstFile(forder, fileMath='None'):
    fileList = getAllFiles(forder)
    mt = 0
    reFile = u''
    for fi in fileList:
        if fileMath != u'None' and fi.find(fileMath) == -1:
            continue
        mtfi = os.path.getmtime(fi)
        if mtfi > mt:
            mt = mtfi
            reFile = fi

    return reFile


def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)), reverse=True)
        # print(dir_list)
        return dir_list


def rename():
    i = 0
    path = "F:\test"
    filelist = os.listdir(path)  # 该文件夹下所有的文件（包括文件夹）
    for files in filelist:  # 遍历所有文件
        i = i + 1
        Olddir = os.path.join(path, files)
        # 原来的文件路径
        if os.path.isdir(Olddir):  # 如果是文件夹则跳过
            continue
        filename = os.path.splitext(files)[0]
        # 文件名
        filetype = os.path.splitext(files)[1]
        # 文件扩展名
        Newdir = os.path.join(path,
                              str(i) + filetype)
        # 新的文件路径
        os.rename(Olddir, Newdir)  # 重命名


if __name__ == '__main__':
    # ------------------------------------------------------------------------------------------
    ###系统函数功能测试###
    folder = r'Inputs'
    # 只能列出当前目录下的文件和文件夹，文件夹下面的文件无法遍历
    for file in os.listdir(folder):
        print(file)

    for file in glob.glob(folder + r'/*.xlsx'):
        print(file)

    # print r'os.path.walk'
    # def processDirectory ( args, dirname, filenames ):
    #     print 'Directory',dirname
    #     for filename in filenames:
    #         print ' File',filename
    # os.path.walk(rootFolder, processDirectory, None)

    print('os.walk')
    for dirpath, dirnames, filenames in os.walk(folder):
        print('Directory', dirpath)
        for filename in filenames:
            print(' File', filename)
# ------------------------------------------------------------------------------------------
# 测试getAllFiles
    rootFolder = r'Inputs'
    l = getAllFiles(rootFolder)
    print(u'getAllFiles')
    for dirItr in l:
        print(dirItr, os.path.isfile(dirItr))

    # 测试
    forlderMatch = re.compile(r'附件一', re.M)
    rootFolder = r'Inputs'
    forldList = os.listdir(rootFolder)
    for folder in forldList:
        # forlderMatch = re.compile(r'数据中心', re.M)
        isF_Match = forlderMatch.search(folder)
        if isF_Match:
            folder = os.path.join(rootFolder, folder)
            fileNst = getNewstFile(folder)
            print(u'Match:', fileNst)
        else:
            folder = os.path.join(rootFolder, folder)
            fileNst = getNewstFile(folder)
            print(u'NotMatch:', fileNst)