import time
import re

# 输入路径
File_Path = 'text/199801_sent.txt'
Dic_Path = 'text/dic.txt'

# 输出路径
Result_Path = 'text/TimeCost.txt'
FMM_Path_2 = 'text/Seg_FMM_2.txt'


# Trie节点
class TrieNode:
    # 构造函数
    def __init__(self, char: str):
        self.char = char
        self.childlist = []

    def __str__(self):
        return "%s" % self.char

    def getList(self):
        return self.childlist

    def inList(self, char):
        List = self.getList()
        for i in range(len(List)):
            if List[i].__str__ == char:
                return True
        return False


# 向Trie中插入新词中剩余部分
def insert(current, rest):
    p = current.getList()
    if rest == "":
        # 词尾
        if not current.inList('#'):
            p.append('#')
            return
        # Trie中已有
        else:
            return
    # 遍历当前节点所有子节点
    for node in p:
        if node.__str__() == rest[0]:
            insert(node, rest[1:])
            return
    new = TrieNode(rest[0])
    current.getList().append(new)
    insert(new, rest[1:])
    return


# 向Trie中插入新词
def wordInsert(root, word):
    current = root
    for w in range(len(word)):
        l = current.getList()
        for p in range(len(l)):
            if word[w] == l[p].__str__():
                current = l[p]
            else:
                break
        insert(current, word[w:])
        break


# 从Trie中搜索
def search(word, root):
    # 初始化当前节点
    current = root
    # 遍历词中每个字
    for w in word:
        l = current.getList()
        # 遍历当前节点的所有儿子
        flag = True
        for p in l:
            if w == p.__str__():
                current = p
                flag = False
                break
        if flag:
            return False
    # 检查当前节点的儿子节点中是否有'#'，如果有，则有以此字结尾的词，否则没有
    for k in current.getList():
        if k.__str__() == '#':
            return True
    return False


# 构建正向最大匹配Trie
def set_fmm_trie():
    file = open(Dic_Path, 'r', encoding='utf-8')
    try:
        b = file.read()  # 读取词典
    finally:
        file.close()
    # 将词典转化为list
    dic = b.split('\n')
    trie = TrieNode("")
    for word in dic:
        wordInsert(trie, word)
    return trie


# 从Trie中搜索
def search_fmm_trie(trie):
    MaxLen = 11

    readfile = open(File_Path, 'r', encoding='gbk')
    try:
        lines = readfile.readlines()  # 读取Sent.txt
    finally:
        readfile.close()
    writefile = open(FMM_Path_2, 'w', encoding='utf-8')
    try:
        for line in lines:
            segList = []
            # 正则表达式
            t = re.search(r'\d{8}-\d{2}-\d{3}-\d{3}', line)
            if not t == None:
                temp = t.span()
                segList.append(line[temp[0]:temp[1]] + "/  ")
                line = line[temp[1]:len(line)]

            line = line[:-1]
            while len(line) > 0:
                tryWord = line if len(line) < MaxLen else line[:MaxLen]
                p = search(tryWord, trie)
                while not p:
                    if len(tryWord) == 1:
                        break
                    tryWord = tryWord[:-1]
                    p = search(tryWord, trie)
                line = line[len(tryWord):]
                segList.append(tryWord + '/ ')
            segList.append('\n')
            print(segList)
            writefile.write(''.join(segList))
    finally:
        # writefile.close()
        a = 1




trie = set_fmm_trie()
print("词典")
startTime = time.time()
search_fmm_trie(trie)
endTime = time.time()
print('运行时间' + str(endTime - startTime))