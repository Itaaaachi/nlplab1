from math import log
import part3  # part3是评价正确率模块，如果使用pycharm划红色波浪线，选择打开nlplab1文件夹作为项目或无视错误直接运行皆可

# 输入路径
Sent_Path = 'text/test.txt'
# 训练集路径
Train_Path = 'text/train.txt'
# 输出路径
Dic_Path = 'text/bi-gram_dic.txt'
LM_Path = 'text/seg_LM.txt'

pre_dict = {}  # 以前缀词典保存单词-词频
words_number = 0  # 总词频数，用于计算
bi_words = {}  # 二元分词字典
word_set = set()
Min_Float = -3.14e+100
Pi = {}  # 初始状态集pi
A = {}  # 状态转移概率
B = {}  # 符号发射概率
States = ['B', 'M', 'E', 'S']  # 状态列表
State_Count = {}  # 状态出现次数
isHMM = True  # 是否使用HMM识别未登录词 True为使用 False为不使用


class Bi_gram:
    @staticmethod  # 生成参数
    def pre_dictionary():
        global pre_dict
        global words_number
        global word_set
        readfile = open(Train_Path, 'r', encoding='utf-8')
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
        word_set = set(words)
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
        readfile = open(Train_Path, 'r', encoding='utf-8')
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
        global isHMM
        readfile = open(Sent_Path, 'r', encoding='utf-8')
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
            if isHMM:
                seglines = HMM.OOV(seglines) if seglines else ''  # 使用HMM对未登录词进行处理
            writefile.write(seglines + '\n')  # 写入分词文件中

    @staticmethod  # 由part3生成最终正确率评估结果
    def score():
        global isHMM
        if isHMM:
            part3.score(5)
        else:
            part3.score(4)


class HMM:

    @staticmethod  # 初始化参数
    def init():
        global States, Pi, A, B, State_Count
        for state in States:
            Pi[state] = 0.0
            State_Count[state] = 0
            B[state], A[state] = {}, {}
            for next_state in States:
                A[state][next_state] = 0.0  # 初始化转换状态概率

    @staticmethod  # 通过训练文本训练参数π,A,B
    def train_args():
        global words_number, States, Pi, A, B, State_Count
        HMM.init()  # 初始化参数
        readfile = open(Train_Path, 'r', encoding='utf-8')
        lines = readfile.readlines()
        for line in lines:  # 对一行文本进行标注
            if line == '\n':
                continue
            line_word, line_state = [], []  # 保存每一行的所有单字和状态
            for word in line.split():
                if word[0] == '[':
                    word = word[1:word.index('/')]
                else:
                    word = word[0:word.index('/')]
                line_word.extend(list(word))  # 将词的每个字加到该行的单字list
                if len(word) == 1:
                    line_state.append('S')
                    Pi['S'] += 1
                else:
                    line_state.append('B')
                    line_state.extend(['M'] * (len(word) - 2))
                    line_state.append('E')
                    Pi['B'] += 1
            for i in range(len(line_state)):
                State_Count[line_state[i]] += 1
                B[line_state[i]][line_word[i]] = B[line_state[i]].get(line_word[i], 0) + 1
                if i > 0:
                    A[line_state[i - 1]][line_state[i]] += 1
        for state in States:  # 计算A/B/Pi
            Pi[state] = Min_Float if Pi[state] == 0 else log(Pi[state] / words_number)
            for next_state in States:
                A[state][next_state] = Min_Float if A[state][next_state] == 0 else log(
                    A[state][next_state] / State_Count[state])
            for word in B[state].keys():
                B[state][word] = log(B[state][word] / State_Count[state])

    @staticmethod
    def viterbi(obs):  # 维特比算法
        Pre_State = {'B': 'ES', 'M': 'MB', 'S': 'SE', 'E': 'BM'}
        v = [{}]
        path = {}
        # t=0 此时为初始状态
        for state in States:
            v[0][state] = Pi[state] + B[state].get(obs[0], Min_Float)
            path[state] = [state]
        # 时刻t = 1,...,len(obs) - 1
        for t in range(1, len(obs)):
            v.append({})
            new_path = {}
            # 当前时刻所处的各种可能的状态
            for y in States:
                # 获取发射概率对数
                emit_p = B[y].get(obs[t], Min_Float)
                # 分别获取上一时刻的状态的概率对数，该状态到本时刻的状态的转移概率对数，本时刻的状态的发射概率对数
                # Pre_State[y]是当前时刻的状态所对应上一时刻可能的状态
                (prob, state) = max([(v[t - 1][y0] + A[y0].get(y, Min_Float) + emit_p, y0) for y0 in
                                     Pre_State[y]])
                v[t][y] = prob
                # 新路径状态 = 上一时刻最优状态 + 此时状态
                new_path[y] = path[state] + [y]
            path = new_path
        # 最后时刻
        (prob, state) = max((v[len(obs) - 1][y], y) for y in 'ES')
        # 返回最大概率对数和最优路径
        return prob, path[state]

    @staticmethod
    def decode(obs):  # 对连续单字进行解码获取分词结果
        if len(obs) == 1:
            return obs + '/ '
        best_path = HMM.viterbi(obs)[1]  # 获取根据viterbi算法得出的最优路径
        word = ''
        begin, next_i = 0, 0

        for i, char in enumerate(obs):
            state = best_path[i]
            if state == 'S':  # 单字成词
                word += char + '/ '
                next_i = i + 1
            elif state == 'B':  # 对于BM...ME的情况下，B为开始，E为结束
                begin = i
            elif state == 'E':
                word += obs[begin:i + 1] + '/ '
                next_i = i + 1

        if next_i < len(obs):
            word += obs[next_i:] + '/ '
        return word

    @staticmethod
    def OOV(sentence):  # 将每行的分词文本进行未登录词识别处理
        global word_set
        word_list = sentence[:len(sentence) - 2].split('/ ')
        sentence = ''
        word = ''
        for i in range(len(word_list)):
            if len(word_list[i]) == 1:  # 单字成词有在字典或不在字典两种情况
                if word_list[i] in word_set:
                    if word:
                        sentence += HMM.decode(word)
                        word = ''
                    sentence += word_list[i] + '/ '
                else:
                    word += word_list[i]
                    if i + 1 == len(word_list):  # 整行都是单字形式的未登录词时直接处理整个句子
                        sentence += HMM.decode(word)
            else:  # 非单字情况的词肯定在字典中
                if word:
                    sentence += HMM.decode(word)
                    word = ''
                sentence += word_list[i] + '/ '
        return sentence


Bi_gram.pre_dictionary()
HMM.train_args()
Bi_gram.generate_dictionary()
Bi_gram.Bi_Seg()
Bi_gram.score()
