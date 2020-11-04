MaxLen = 0
Words = []
Test_Path = 'text/199801_sent.txt'
Dic_Path = 'text/dic.txt'
FMM_Path = 'text/seg_FMM.txt'
BMM_Path = 'text/seg_BMM.txt'


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
