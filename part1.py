#输入路径
Train_Path = 'text/199801_seg&pos.txt'

#输出路径
Dic_Path = 'text/dic.txt'


def generate_dic():
    # 根据分词数据生成词典
    maxLen = 0  # 最大词长
    word_list = list()  # 所有词表
    dic = list()  # 词典
    readfile = open(Train_Path, 'r', encoding='gbk')
    try:
        lines = readfile.readlines()  # 读取seg＆pos.txt
    finally:
        readfile.close()
    writefile = open(Dic_Path, 'w', encoding='utf-8')  # 写入dic.txt 生成词典
    try:
        for line in lines:
            for word in line.split():
                if '/m' in word:  # 量词过多，不计入词典
                    continue
                if word[0] == '[':  # []中为专有名词，不拆开
                    index = word.index('/')
                    word = word[1:index]
                else:
                    index = word.index('/')
                    word = word[0:index]
                word_list.append(word)
                if len(word) > maxLen:  # 更新最长词列表
                    maxLen = len(word)
        for word in word_list:
            if word not in dic:  # 去重
                dic.append(word)
        dic.sort()  # 按照拼音排序
        writefile.write('\n'.join(dic))
    finally:
        writefile.close()
    return dic, maxLen


generate_dic()
