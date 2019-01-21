#!/usr/bin/python
# encoding: utf-8

import sys


if __name__ == "__main__":
    filename = sys.argv[1]
    file = open(filename, 'r')
    write_file = open("file.out", 'w')
    sentence_count, assignment = 0, 0
    words = {}
    flag = 1
    for line in file:
        lines = line.split('\t')
        lines_length = len(lines)
        if lines_length != 4:
            print "error"
            print lines
            exit()
        sentence = lines[0]
        probability = lines[2].split(' ')
        probability = [float(p) for p in probability]
        sorted_probability = sorted(probability)
        sentence_length = len(sentence.split(' '))
        if sentence_length >= 5:
            sentence_words = sentence.split(' ')
            hard_words_count = int(sentence_length * 0.1 // 1 + 1)
            flag = 1
            p_indexes = []
            for i in xrange(hard_words_count):  # 总共有多少个需要标注的任务
                p = sorted_probability[i]
                p_index = probability.index(p)
                if p <= 0.7:
                    # 相邻的任务只需要一个
                    p_flag = 0
                    for p_i in p_indexes:
                        if p_i - 1 <= p_index <= p_i + 1:
                            p_flag = 1
                            break
                    if p_flag == 1:
                        continue
                    # 相邻的任务只需要一个END
                    p_indexes.append(p_index)
                    if flag == 1:
                        sentence_count += 1
                        write_file.write(sentence + '\t')
                        flag = 0
                    assignment += 1  # 任务的数量 + 1
                    hard_word = sentence_words[p_index]
                    if hard_word in words:
                        words[hard_word] += 1
                    else:
                        words[hard_word] = 1
                    write_file.write(str(p_index + 1) + '_' + str(p) + ' ')  # word 从1开始
            if flag == 0:
                write_file.write('\n')
    write_file.write("句子数量：" + str(sentence_count) + '\n')
    write_file.write("任务数量：" + str(assignment) + '\n')
    file.close()
    write_file.close()
    word_frequence_file = open('word_frequence_file.txt', 'w')
    for word in words:
        word_frequence_file.write(word + ' ' + str(words[word]) + '\n')
    word_frequence_file.close()
