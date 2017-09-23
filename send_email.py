#coding: utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

HOST = "smtp.163.com"
SUBJECT = u"微信登陆二维码"
TO = "1157715152@qq.com"
FROM = "liujun4719@163.com"

def addimg(src,imgid):
    while not os.path.exists(src):
        continue
    fp = open(src, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', imgid)
    return msgImage

msg = MIMEMultipart('related')
msgtext = MIMEText("<font color=red>微信登陆二维码:</font>","html","utf-8")
msg.attach(msgtext)
msg.attach(addimg("../wxqr_fold/wxqr.png","wxqr"))

#attach = MIMEText(open("doc/week_report.xlsx", "rb").read(), "base64", "utf-8")
#attach["Content-Type"] = "application/octet-stream"
#attach["Content-Disposition"] = "attachment; filename=\"业务服务质量周报(12周).xlsx\"".decode("utf-8").encode("gb18030")
#msg.attach(attach)

msg['Subject'] = SUBJECT
msg['From']=FROM
msg['To']=TO
try:
    server = smtplib.SMTP()
    server.connect(HOST,"25")
    server.starttls()
    server.login("liujun4719@163.com","jason./1234")
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()
    print "邮件发送成功！"
except Exception, e:
    print "失败："+str(e)