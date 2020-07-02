from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication  #附件

import smtplib #发送邮件
import argparse
parser = argparse.ArgumentParser()

input("pls input ")
#像linux命令一样的东西
#准备发送邮件的参数
'''
1. sender: -s --sender qq,126,163, 
2. to_list: -t --to_list d多个
3. cc_list: -c --cc_list 
4. subject -sub --subject
5.auth_pwd: -auth --auth_pwd
6.smtp_server: -server --smtpserver 可选

'''
parser.add_argument("-s", "--sender", dest="sender", required=True)
parser.add_argument("-t", "--to_list", dest="to_list", nargs="+", required=True)
parser.add_argument("-c", "--cc_list", dest="cc_list", default=[],nargs="+", required=False)
parser.add_argument("-sub", "--subject", dest="subject", required=True)
parser.add_argument("-p", "--auth_pwd", dest="auth_pwd", required=True)
parser.add_argument("-server", "--ssmtp_server", dest="smtp_server", required=False)


result = parser.parse_args()
# sender = "838750084@qq.com"
sender = result.sender

#收件人
#to_list = ["838750084@qq.com",
          # "ryan_zhang310@163.com"
# ]

to_list = result.to_list
#抄送人
# cc_list = [
#     "838750084@qq.com",
#     "ryan_zhang310@163.com"
# ]
cc_list = result.cc_list

# subject = "This is a test today "
subject = result.subject

#授权密码，链接邮箱smtp
#auth_pwd = ' '
auth_pwd = result.auth_pwd


dic = {
    "126":'smtp.126.com',
    "qq":'smtp.qq.com',
    "163":'smtp.163.com'
}
if not result.smtp_server:
    #计算smtp服务器
    k = sender.split("@")[1].split(".")[0]
    v = dic.get(k)

    if v:
        smtp_server = v
    else:
        raise Exception("对不起，您输入的邮箱，对应的服务器不存在，请联系管理员！")

#写邮件
#创建邮件
em = MIMEMultipart() #em 其实是message.Message 的子类的对象
em['Subject'] = subject
em['From'] = sender
em['To'] = ",".join(to_list)
em['Cc'] = ','.join(cc_list)

#邮件内容
'''
content = MIMEText("This is a test for python send email!")
em.attach(content)
 '''
#发送html 代码

content = MIMEText("<a href='http://www.baidu.com'><img src='cid:Python'/></a>", _subtype="html")
em.attach(content)

#发送图片
img = MIMEImage(open("OIP.jpg",mode="rb").read())
img.add_header("Content-ID","Python") # 给图片设置id值
em.attach(img)

#发送附件
app = MIMEApplication(open("OIP.jpg", mode='rb').read())
app.add_header('content-disposition', 'attachment', filename='test.jpg')
em.attach(app)
# 发送邮件
#1.链接smtp 服务器

smtp = smtplib.SMTP()
smtp.connect("smtp.qq.com")
#2.登录
smtp.login(sender,auth_pwd)
#3.发送邮件
smtp.send_message(em) #msg 必须是message.Message 的对象，fromaddr 和 to_addr 都不用提供，smtp.send_message(em,from_addr=None, to_addrs=None)
# smtp.sendmail() #必须是字符串

#4.关闭链接
smtp.close()