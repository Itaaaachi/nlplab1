Score_Path = 'text/score.txt'
Original_Path = 'text/199801_seg&pos.txt'
Fmm_Path = 'text/seg_FMM.txt'
Bmm_Path = 'text/seg_BMM.txt'


def unified(para):
    if para == 1:
        path = 'text/199801_seg&pos.txt'
        encoding = 'gbk'
    elif para == 2:
        path = 'text/seg_FMM.txt'
        encoding = 'utf-8'
    elif para == 3:
        path = 'text/seg_BMM.txt'
        encoding = 'utf-8'
    elif para == 4:
        path = 'text/seg_LM.txt'
        encoding = 'utf-8'
    readfile = open(path, 'r', encoding=encoding)
    result = []
    for line in readfile:
        if line == '\n':  # 去掉空行
            continue
        new = ''
        for letter in line.split():
            if letter[0] == '[':
                new += letter[1:letter.index('/')] + '/ '
            else:
                new += letter[0:letter.index('/')] + '/ '
        result.append(new)
    return result


def score(para):
    standard, right, mm, index, i, j = 0, 0, 0, 0, 0, 0
    standard_lines = unified(1)
    mm_lines = unified(para)

    for line in standard_lines:
        standard_words = line.split('/ ')
        mm_words = mm_lines[index].split('/ ')
        index += 1
        standard_size = len(standard_words) - 1  # 去掉每行句尾的空格
        mm_size = len(mm_words) - 1
        standard += standard_size
        mm += mm_size
        standard_length = len(standard_words[0])
        mm_length = len(mm_words[0])
        while (i < standard_size) and (j < mm_size):

            if standard_length == mm_length:
                right += 1
                if i == standard_size - 1:
                    break
                i += 1
                j += 1
                standard_length += len(standard_words[i])
                mm_length += len(mm_words[j])

            else:
                while True:
                    if standard_length < mm_length:
                        i += 1
                        standard_length += len(standard_words[i])

                    elif standard_length > mm_length:
                        j += 1
                        mm_length += len(mm_words[j])
                    else:
                        if i < standard_size - 1:
                            standard_length += len(standard_words[i + 1])
                            mm_length += len(mm_words[j + 1])
                        i += 1
                        j += 1
                        break
        i = j = 0
    p = right / standard
    r = right / mm
    f = p * r * 2 / (p + r)
    print("标准词库词数：" + str(standard))
    if para == 2:
        print("FMM结果为：")
        print("FMM词数：" + str(mm))
    elif para == 3:
        print("BMM结果为：")
        print("BMM词数：" + str(mm))
    elif para == 4:
        print("二元分词结果为：")
        print("LM词数：" + str(mm))
    print("正确词数：" + str(right))
    print("准确率：" + str(p * 100) + "%")
    print("召回率：" + str(r * 100) + "%")
    print("F值：" + str(f * 100) + "%")
    writefile = open(Score_Path, 'a+', encoding='UTF-8')

    if para == 2:
        writefile.write("FMM结果为：\n")
        writefile.write("FMM词数：" + str(mm) + "\n")
    elif para == 3:
        writefile.write("BMM结果为：\n")
        writefile.write("BMM词数：" + str(mm) + "\n")
    elif para == 4:
        writefile.write("二元分词结果为：\n")
        writefile.write("LM词数：" + str(mm) + "\n")
    writefile.write("标准词库词数：" + str(standard) + "\n")
    writefile.write("正确词数：" + str(right) + "\n")
    writefile.write("准确率：" + str(p * 100) + "%\n")
    writefile.write("召回率：" + str(r * 100) + "%\n")
    writefile.write("F值：" + str(f * 100) + "%\n\n")
