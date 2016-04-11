# -*- coding: UTF-8 -*-
import zerorpc

if __name__ == '__main__':
  c = zerorpc.Client(timeout=3600, heartbeat=3600)
  c.connect("tcp://127.0.0.1:4243")
  for i in  c.ExtractWeiboKeywords("黄晓明"):
    print i[0], i[1]
