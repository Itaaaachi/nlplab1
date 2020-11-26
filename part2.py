import time

#输入路径
Sent_Path = 'text/199801_sent.txt'
Dic_Path = 'text/dic.txt'

#输出路径
FMM_Path = 'text/seg_FMM.txt'
BMM_Path = 'text/seg_BMM.txt'

MaxLen = 0
Words = []
dic = []

def init_dic():
    global MaxLen
    file = open(Dic_Path, 'r', encoding='utf-8')
    try:
        b = file.read()  # 读取词典
    finally:
        file.close()
    # 将词典转化为list
    dic = b.split('\n')
    # 计算词典中最长词的长度
    for word in dic:
        Words.append(word[0:len(word) - 1])  # 将该词加入词典列表中
        if len(word) - 1 > MaxLen:  # 更新最大词长
            MaxLen = len(word) - 1
        if len(word) > 11:
            print(word)
    print(MaxLen)


init_dic()

# 处理每行信息前面的日期序号，连接


def pre_line(line):
    punctuation = '-./'
    buffer, result = '', ''
    word_list = line.split('/ ')
    word_list = word_list[:len(word_list) - 1]
    for idx, word in enumerate(word_list):
        if word.isascii() or word in punctuation:  # 若是字母、数字或者英文标点
            buffer += word
            if idx + 1 == len(word_list):
                result += buffer + '/ '
        else:
            if buffer:
                result += buffer + '/ '
                buffer = ''
            result += word + '/ '
    return result


class String_Match:
    @staticmethod
    # 正向最大匹配
    def fmm():
        init_dic()
        segList = []
        readfile = open(Sent_Path, 'r', encoding='gbk')
        try:
            lines = readfile.readlines()  # 读取Sent.txt
        finally:
            readfile.close()
        writefile = open(FMM_Path, 'w', encoding='utf-8')
        try:
            for line in lines:
                line = line[:len(line) - 1]  # 去掉每行最后的\n
                while len(line) > 0:
                    if len(line) < MaxLen:
                        tryWord = line[0:len(line)]
                    else:
                        tryWord = line[0:MaxLen]
                    while tryWord not in Words:
                        # 若字串长度为1，跳出循环
                        if len(tryWord) == 1:
                            break
                        # 截掉子串尾部一个字，用剩余部分到字典中匹配
                        tryWord = tryWord[0:len(tryWord) - 1]
                    # 将匹配成功的词加入到分词列表中
                    segList.append(tryWord + '/ ')
                    # 将匹配成功的词从待分词字符串中去除，继续循环，直到分词完成
                    line = line[len(tryWord):]
                segList.append('\n')
            writefile.write(pre_line(''.join(segList)))
        finally:
            writefile.close()

    @staticmethod
    # 反向最大匹配
    def bmm():
        init_dic()
        segList = []
        readfile = open(Sent_Path, 'r', encoding='gbk')
        try:
            lines = readfile.readlines()  # 读取Sent.txt
        finally:
            readfile.close()
        writefile = open(BMM_Path, 'w', encoding='utf-8')
        try:
            for line in lines:
                line = line[:len(line) - 1]  # 去掉每行最后的\n
                segList.append('\n')
                while len(line) > 0:
                    if len(line) < MaxLen:
                        tryWord = line
                    else:
                        tryWord = line[len(line) - MaxLen:]
                    while tryWord not in Words:
                        # 若字串长度为1，跳出循环
                        if len(tryWord) == 1:
                            break
                        # 截掉子串尾部一个字，用剩余部分到字典中匹配
                        tryWord = tryWord[1:]
                    # 将匹配成功的词加入到分词列表中
                    segList.insert(0, tryWord + '/ ')
                    # 将匹配成功的词从待分词字符串中去除，继续循环，直到分词完成
                    line = line[:len(line) - len(tryWord)]

                writefile.write(pre_line(''.join(segList)) + '\n')
                segList.clear()
        finally:
            writefile.close()


startTime=time.time()
String_Match.fmm()
endTime=time.time()
print ('运行时间'+str(endTime-startTime))

# String_Match.bmm()
