#!/usr/bin/python
# coding=utf-8

from __future__ import print_function
import websocket
import sys


def get_web_content(read_name, write_name):
    # websocket.enableTrace(True)
    ws = websocket.create_connection("ws://hlt-la.suda.edu.cn/")
    sentence_count = 0
    try:
        fr = open(read_name, 'r')
        fw = open(write_name, 'a+')
        for sentence in fr.readlines():
            # line = '我是中国人'
            # print("Sending '%s'" %sentence)
            sentence = sentence.strip()
            ws.send(sentence)
            # print("Sent")
            # print("Receiving...")
            result = ws.recv()
            if result:
                # print("Received '%s'" % result)
                fw.write(result + '\n')
                sentence_count += 1
                if sentence_count % 100 == 0:
                    # print sentence_count, ' ',
                    print(str(sentence_count) + ' ', end="")
                    sys.stdout.flush()
            else:
                fw.write("no result received" + '\n')
        fr.close()
        fw.close()
        print('数据处理完全！！！')
    except IOError:
        print('please check the filename')
    ws.close()


if __name__ == "__main__":
    read_name = 'nlpcc2015_seg.txt'    # 输入待处理数据
    write_name = 'nlpcc2015_sentence_seg.conll'   # 保存处理结果
    get_web_content(read_name, write_name)


# from __future__ import print_function
# import websocket
#
# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.create_connection("ws://hlt-la.suda.edu.cn/")
#     print("Sending 'Hello, World'...")
#     ws.send("Hello, World")
#     print("Sent")
#     print("Receiving...")
#     result = ws.recv()
#     print("Received '%s'" % result)
#     ws.close()
