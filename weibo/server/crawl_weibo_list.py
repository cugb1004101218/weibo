import commands

def GetWeiboList(user_id):
  cmd = "cd /home/cugbacm/weibo && scrapy crawl weibo_list -a user_id=" + str(user_id)
  status,output = commands.getstatusoutput(cmd)
  print output

if __name__ == '__main__':
  GetWeiboList("2814822392")
