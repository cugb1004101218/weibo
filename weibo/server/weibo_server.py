# -*- coding: UTF-8 -*-
import sys
import zerorpc
import smtplib
import commands
from email.mime.text import MIMEText


class WeiboRPC(object):
  def SendMail(self, to, subject, body, attachment):
    cmd = "echo \"" + body + "\"" + " | mutt -s " + "\"" + subject + "\" "+ to + " -a " + attachment
    commands.getstatusoutput(cmd)
    return "Send to %s" % to

  def CrawlWeiboList(self, user_id):
    cmd = "cd /home/cugbacm/weibo && scrapy crawl weibo_list -a user_id=" + str(user_id) + " > /tmp/" + str(user_id) + ".txt"
    commands.getstatusoutput(cmd)
    status,output = commands.getstatusoutput("cat /tmp/" + str(user_id) + ".txt")
    return output

  def CrawlWeiboListAndSendMail(self, user_id, to):
    weibo_list = self.CrawlWeiboList(user_id)
    return self.SendMail(to, user_id + "的微博", "详情见附件", "/tmp/" + user_id + ".txt")

  def CrawlUserId(self, user_name):
    cmd = "cd /home/cugbacm/weibo && scrapy crawl search_user_id -a user_name=" + str(user_name) + " 2>/dev/null"
    status,output = commands.getstatusoutput(cmd)
    return output.strip()

  def CrawlWeiboListFromUserNameAndSendMail(self, user_name, to):
    user_id = self.CrawlUserId(user_name)
    return self.CrawlWeiboListAndSendMail(user_id, to)

if __name__ == '__main__':
  s = zerorpc.Server(WeiboRPC())
  s.bind("tcp://0.0.0.0:4242")
  s.run()
