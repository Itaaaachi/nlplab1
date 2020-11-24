# 输入路径
FilePath = 'text/199801_sent.txt'

# 输出路径
ResultPath = 'text/TimeCost.txt'


class Trie:
    #构造函数
    def _init_(self, character, terminal, children):
        self.character = character
        self.terminal = terminal
        self.children = children
    
    #返回当前节点的terminal
    def in_terminal(self):
        return self.terminal
    
    #设置当前节点terminal
    def set_terminal(self,terminal):
        self.terminal=terminal

    #返回当前节点字符
    def get_character(self):
        return self.character

    #设置当前节点terminal
    def set_character(self,character):
        self.character=character

    