# coding=utf-8
import os
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


class Mailer(object):
    def __init__(self, **kwargs):
        self.mail_list = kwargs["mail_list"]
        self.mail_title = kwargs["mail_title"]
        self.mail_content = kwargs["mail_content"]
        self.file_path = kwargs["file_path"]

        self.mail_host = "smtp.163.com"
        self.mail_user = "chenghao961012@163.com"
        self.mail_pass = "{0.873A976S081!?"
        self.mail_postfix = "163.com"

    def send_mail(self):

        me = self.mail_user + "<" + self.mail_user + "@" + self.mail_postfix + ">"
        msg = MIMEMultipart()
        msg['Subject'] = u'自动化测试结果输出'
        msg['From'] = self.format_addr(u'自动化测试 <%s>' % me)
        msg['To'] = self.format_addr(u'管理员 <%s>' % ";".join(self.mail_list))

        # puretext = MIMEText('<h1>你好，<br/>'+self.mail_content+'</h1>','html','utf-8')
        puretext = MIMEText(u'Dear All:\n'
                            u'    如下是公牛智联APP自动测试结果输出，请各位审阅，谢谢。\n', 'plain', 'utf-8')
        msg.attach(puretext)

        # 文本类型的附件
        for i in self.file_path:
            name = os.path.basename(i)
            jpgpart = MIMEApplication(open(r'%s' % i, 'rb').read())
            jpgpart.add_header('Content-Disposition', 'attachment', filename=name)
            msg.attach(jpgpart)

        # jpg类型的附件
        # jpgpart = MIMEApplication(open('D:/test.log', 'rb').read())
        # jpgpart.add_header('Content-Disposition', 'attachment', filename='test.log')
        # msg.attach(jpgpart)

        # xlsx类型的附件
        # xlsxpart = MIMEApplication(open('test.xlsx', 'rb').read())
        # xlsxpart.add_header('Content-Disposition', 'attachment', filename='test.xlsx')
        # msg.attach(xlsxpart)

        # mp3类型的附件
        # mp3part = MIMEApplication(open('kenny.mp3', 'rb').read())
        # mp3part.add_header('Content-Disposition', 'attachment', filename='benny.mp3')
        # msg.attach(mp3part)

        # pdf类型附件
        # part = MIMEApplication(open('foo.pdf', 'rb').read())
        # part.add_header('Content-Disposition', 'attachment', filename="foo.pdf")
        # msg.attach(part)

        try:
            s = smtplib.SMTP()  # 创建邮件服务器对象
            s.connect(self.mail_host)  # 连接到指定的smtp服务器。参数分别表示smpt主机和端口
            s.login(self.mail_user, self.mail_pass)  # 登录到你邮箱
            s.sendmail(me, self.mail_list, msg.as_string())  # 发送内容
            s.close()
            return True
        except Exception, e:
            print str(e)
            return False

    def format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr(
            (Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))
