# 输入路径
File_Path = 'text/199801_sent.txt'
Dic_Path = 'text/dic.txt'

# 输出路径
Result_Path = 'text/TimeCost.txt'
FMM_Path_2='text/Seg_FMM_2.txt'

#Trie节点
class TrieNode:
    # 构造函数
    def __init__(self, char):
        self.char = char
        self.childlist = []

    def getchar(self):
        return '%s' % self.char

    def getList(self):
        return self.childlist

    def inList(self, char):
        List = self.getList()
        for i in range(len(List)):
            if(List[i].getchar == char):
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
        if p.getchar == rest[0]:
            insert(node, rest[1:])
            return
    new = TrieNode(rest[0])
    current.getList().append(new)
    insert(new, rest[1:])
    return

#向Trie中插入新词
def wordInsert(root,word):
    current = root
    for w in range(len(word)):
        l = current.getList()
        for p in l:
            if word[w] == p.getchar():
                current = p
                break
    insert(current,word[w:])

# 从Trie中搜索
def search(word, root):
    # 初始化当前节点
    current = root
    # 遍历词中每个字
    for w in word:
        l = current.getList()
        # 遍历当前节点的所有儿子
        for p in l:
            if w == p.getchar():
                current = p
                break
        return False
    # 检查当前节点的儿子节点中是否有'#'，如果有，则有以此字结尾的词，否则没有
    for k in current.getList():
        if k.getchar() == '#':
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
    trie=TrieNode("")
    for word in dic:
        wordInsert(trie,word)
    return trie

#从Trie中搜索
def search_fmm_trie(trie):
    MaxLen=11
    segList = []
    readfile = open(File_Path, 'r', encoding='gbk')
    try:
        lines = readfile.readlines()  # 读取Sent.txt
    finally:
        readfile.close()
    writefile = open(FMM_Path_2, 'w', encoding='utf-8')
    try:
        for line in lines:
            line = line[:len(line) - 1]  # 去掉每行最后的\n
            while len(line) > 0:
                if len(line) < MaxLen:
                    tryWord = line[0:len(line)]
                else:
                    tryWord = line[0:MaxLen]
                p=search(tryWord,trie)
                while not p:
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

trie=set_fmm_trie()
search_fmm_trie(trie)