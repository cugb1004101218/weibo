# -*- coding: UTF-8 -*-
import zerorpc
import jieba.analyse
import jieba
import sys

class AnalysisWeiboRPC(object):
  def __init__(self):
    jieba.set_dictionary('../dict/dict.txt.big')
    jieba.analyse.set_stop_words('../dict/stop_words.txt')
    jieba.initialize()
  def ExtractWeiboKeywords(self, content):
    return jieba.analyse.extract_tags(content, topK=50, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
  def ceshi(self):
    return "test"

if __name__ == '__main__':
  s = zerorpc.Server(AnalysisWeiboRPC())
  s.bind("tcp://0.0.0.0:4243")
  s.run()
