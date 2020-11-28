from math import log
import part3

# 输入路径
Sent_Path = 'text/199801_sent.txt'
# 训练集路径
Train_Path = 'text/199801_seg&pos.txt'
# 输出路径
Dic_Path = 'text/bi-gram_dic.txt'
LM_Path = 'text/seg_LM.txt'

pre_dict = {}  # 以前缀词典保存单词-词频
words_number = 0  # 总词频数，用于计算
bi_words = {}  # 二元分词字典


class Bi_gram:
    @staticmethod  # 生成参数
    def pre_dictionary():
        global pre_dict
        global words_number
        readfile = open(Train_Path, 'r', encoding='gbk')
        lines = readfile.readlines()
        readfile.close()
        for line in lines:
            for word in line.split():
                if word[0] == '[':
                    word = word[1:word.index('/')]
                else:
                    word = word[0:word.index('/')]
                pre_dict[word] = pre_dict.get(word, 0) + 1
        words = list(pre_dict.keys())
        counts = list(pre_dict.values())
        pre_dict = dict(sorted(zip(words, counts)))  # 对字典进行排序
        for ele in range(0, len(counts)):
            words_number = words_number + counts[ele]  # 获取总词频数
        for word in words:
            for count in range(1, len(word)):  # 获取每个词的前缀词
                prefix = word[:count]
                if prefix not in pre_dict:
                    pre_dict[prefix] = 0  # 若词典中无该前缀词，就将其存入，设置单词频数=0
        pre_dict = dict(sorted(zip(list(pre_dict.keys()), list(pre_dict.values()))))  # 对字典重新排序

    @staticmethod  # 构建二元分词词典
    def generate_dictionary():
        global bi_words
        readfile = open(Train_Path, 'r', encoding='gbk')
        lines = readfile.readlines()
        readfile.close()
        for line in lines:
            if line == '\n':
                continue
            words = line.split()
            words.insert(0, 'BOS')  # 每行开头加入BOS代表开头位置
            words.append('EOS/ ')  # 每行结尾加入EOS代表结尾位置

            for i in range(1, len(words)):
                if words[i][0] == '[':
                    words[i] = words[i][1:words[i].index('/')]
                else:
                    words[i] = words[i][0:words[i].index('/')]
                if words[i] not in bi_words.keys():
                    bi_words[words[i]] = {}
                if words[i - 1] not in bi_words[words[i]].keys():
                    bi_words[words[i]][words[i - 1]] = 0
                bi_words[words[i]][words[i - 1]] += 1  # 更新词频

        bi_word = list(bi_words.keys())
        bi_count = list(bi_words.values())
        bi_words = dict(sorted(zip(bi_word, bi_count)))  # 对字典排序
        writefile = open(Dic_Path, 'w', encoding='utf-8')
        for key in bi_words:
            word = list(bi_words[key].keys())
            count = list(bi_words[key].values())
            bi_words[key] = dict(sorted(zip(word, count)))
            for pre in bi_words[key]:
                writefile.write(key + ' ' + pre + ' ' + str(bi_words[key][pre]) + '\n')
        writefile.close()

    @staticmethod  # 构建有向无环图DAG
    def DAG(sentence):
        graph = {}
        for k in range(len(sentence)):  # 遍历每行的每个位置并对位置k形成一个片段
            i = k
            graph[k] = []
            frag = sentence[k]
            while i < len(sentence) and frag in pre_dict:  # 判断该片段是否在前缀词典中
                if pre_dict[frag] > 0:
                    graph[k].append(i)
                i += 1
                frag = sentence[k:i + 1]
            if not graph[k]:
                graph[k].append(k)
            # graph[k].append(k) if not graph[k] else graph[k]
        return graph

    @staticmethod  # 计算上一个词的对数概率
    def p_log(pre, word):
        return log(bi_words.get(word, {}).get(pre, 0) + 1) - log(pre_dict.get(pre, 0) + words_number)

    @staticmethod  # 对构建的DAG进行计算
    def calc_graph(sentence, graph):
        start = 3  # 跳过开头位置的BOS
        pre_graph = {'BOS': {}}  # {前词:{词:对数概率,...}}
        for x in graph[3]:  # 初始化dag
            pre_graph['BOS'][(3, x + 1)] = Bi_gram.p_log('BOS', sentence[3:x + 1])
        while start < len(sentence) - 3:  # EOS长度=3
            for i in graph[start]:
                pre = sentence[start:i + 1]
                temp = {}
                for end in graph[i + 1]:
                    last = sentence[i + 1:end + 1]
                    if sentence[i + 1:end + 3] == 'EOS':  # 到达该行结尾，即EOS处
                        temp['EOS'] = Bi_gram.p_log(pre, 'EOS')
                    else:
                        temp[(i + 1, end + 1)] = Bi_gram.p_log(pre, last)
                pre_graph[(start, i + 1)] = temp
            start += 1
        return pre_graph

    @staticmethod  # 得到最大概率路径
    def route(sentence, graph):
        word_graph = {}  # {word:[前词list]}
        route = {}  # 待构建的最大概率路径
        pre_graph = Bi_gram.calc_graph(sentence, graph)  # 由calc函数得到的{前词:{词:对数概率}}构成的图
        words = list(pre_graph.keys())
        for pre in words:
            for word in pre_graph[pre].keys():
                word_graph[word] = word_graph.get(word, list())
                word_graph[word].append(pre)
        words.append('EOS')
        for word in words:
            if word == 'BOS':  # 前词为BOS
                route[word] = (0.0, 'BOS')
            else:
                pre_list = word_graph.get(word, list())
                route[word] = (-10000, 'BOS') if not pre_list else max(  # 若pre_list非空，计算得到最短路径
                    (pre_graph[pre][word] + route[pre][0], pre) for pre in pre_list)
        return route

    @staticmethod  # 获得分词结果
    def Bi_Seg():
        readfile = open(Sent_Path, 'r', encoding='gbk')
        lines = readfile.readlines()
        writefile = open(LM_Path, 'w', encoding='utf-8')
        for sentence in lines:
            seglines = ''
            position = 'EOS'
            sentence = 'BOS' + sentence[:len(sentence) - 1] + 'EOS'
            graph = Bi_gram.DAG(sentence)
            route = Bi_gram.route(sentence, graph)
            while True:
                position = route[position][1]
                if position == 'BOS':
                    break
                seglines = sentence[position[0]:position[1]] + '/ ' + seglines
            writefile.write(seglines + '\n')  # 写入分词文件中


Bi_gram.pre_dictionary()
Bi_gram.generate_dictionary()
Bi_gram.Bi_Seg()
part3.score(4)
