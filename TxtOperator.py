# -*- coding: utf-8 -*-

import re, sys, datetime
# from FileOperator import getAllFiles
# reload(sys)
# print sys.getdefaultencoding()
# sys.setdefaultencoding(u'utf-8')
# print sys.getdefaultencoding()

diubao = re.compile(r'= (\d+) \(')
shiyan = re.compile(r'=.*=.*= (\d+)ms')
inputSplit = re.compile(r',')
# print(datetime.datetime.now())


def readTxt2List(txtFile, allList=True):
    cmds = open(txtFile, u'rb')
    inputsList = []
    inputsLines = cmds.readlines()
    if allList:
        for line in inputsLines:
            line = line.decode(u'utf-8')
            if line[0] != u'#':
                line = line.strip()
                if line == u'':
                    line = []
                else:
                    line = inputSplit.split(line)
                inputsList.append(line)
    else:
        for line in inputsLines:
            line = line.decode(u'utf-8')
            if line[0] != u'#':
                line = line.strip()
                inputsList.append(line)
    cmds.close()
    return inputsList


def writeList2Txt(txtFile, valueList, op=u'w'):
    cmd_tracert_result = open(txtFile, op, encoding='utf-8')
    for value in valueList:
        cmd_tracert_result.write(value)
        cmd_tracert_result.write('\n')
    cmd_tracert_result.close()


# readTxt2List测试
if __name__ == '__main__':
    # txtFile = u'TxtOperator.txt'
    txtFile = u'Inputs\TxtOperator.txt'
    inputsList = readTxt2List(txtFile, True)
    for dirItr in inputsList:
        print(dirItr)
        # for d in dirItr:
        #     print(d)
    # writeFile = 'txtWrite.txt'
    # writeList2Txt(writeFile,inputsList)
    # print('\\\n\\')
    # print('\r\n')
    # print(r'\\\n\\')
