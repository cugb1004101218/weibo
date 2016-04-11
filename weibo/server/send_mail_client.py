import zerorpc

if __name__ == '__main__':
  c = zerorpc.Client(timeout=3600, heartbeat=3600)
  c.connect("tcp://127.0.0.1:4242")
  c.CrawlWeiboListAndSendMail("3541019981", "763687347@qq.com")
