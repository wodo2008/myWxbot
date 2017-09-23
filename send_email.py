#coding: utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

class Send_msg(object):
    def __init__(self):
        self.HOST = "smtp.163.com"
        self.SUBJECT = u"微信登陆二维码"
        self.TO = "1157715152@qq.com"
        self.FROM = "liujun4719@163.com"

    def addimg(self,src,imgid):
        print src
        while not os.path.exists(src):
            continue
        fp = open(src, 'rb')
        msgImage = MIMEImage(fp.read(),_subtype='octet-stream')
        fp.close()
        msgImage.add_header('Content-Disposition', 'attachment', filename=('gbk', '', imgid))
        #msgImage.add_header('Content-ID', imgid)
        return msgImage

    def send(self):
        msg = MIMEMultipart('related')
        msgtext = MIMEText("<font color=red>微信登陆二维码:</font>","html","utf-8")
        msg.attach(msgtext)
        msg.attach(self.addimg("/home/myWxbot/wxqr_fold/wxqr.png","wxqr.png"))

        #attach = MIMEText(open("doc/week_report.xlsx", "rb").read(), "base64", "utf-8")
        #attach["Content-Type"] = "application/octet-stream"
        #attach["Content-Disposition"] = "attachment; filename=\"业务服务质量周报(12周).xlsx\"".decode("utf-8").encode("gb18030")
        #msg.attach(attach)

        msg['Subject'] = self.SUBJECT
        msg['From']=self.FROM
        msg['To']=self.TO
        try:
            server = smtplib.SMTP()
            server.connect(self.HOST,"25")
            server.starttls()
            server.login("liujun4719@163.com","jason./1234")
            server.sendmail(self.FROM, self.TO, msg.as_string())
            server.quit()
            print "邮件发送成功！"
        except Exception, e:
            print "失败："+str(e)

if __name__ == '__main__':
    send_msg = Send_msg()
    send_msg.send()
