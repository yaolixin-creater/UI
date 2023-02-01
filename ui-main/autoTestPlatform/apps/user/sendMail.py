from .nameMap import account, mail_list
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from addict import Dict
import logging

logger = logging.getLogger("user")


class Sender:
    def __init__(self, response=None, person=None):
        self.account = Dict(account)
        self.smtpserver = self.account.smtpserver
        self.response = Dict(response)
        self.tname = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.subject = "Email code for registring DSP TEST PLATFORM {}".format(self.tname)
        self.msg = MIMEMultipart("mixed")
        self.msg["Subject"] = self.subject
        self.msg["From"] = "DSP TEST PLATFORM <hh18837292725@163.com>"
        if person is None:
            self.receiver = mail_list
        else:
            # mail_list.clear()
            if person not in mail_list:
                mail_list.append(person)
            self.receiver = mail_list
            self.email_code = ""
        self.msg["To"] = ";".join(self.receiver)

    def create_email_code(self):
        def generate_email_code(randomlength=6):
            import random

            base_str = "ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz01234567890123456789"
            length = len(base_str) - 1
            for times in range(randomlength):
                self.email_code += base_str[random.randint(0, length)]
            return self.email_code

        message = "您好！\n如下为您用于注册的验证码，请查收，\n" + "\n\n\n\n{}".format(
            generate_email_code()
        )
        message = MIMEText(message, "plain", "utf-8")
        self.msg.attach(message)

    def send_message_through_qq(self):
        connect = False
        try:
            smtp = smtplib.SMTP()
            smtp.connect("smtp.qq.com")
            connect = True
            # set_debuglevel(1) info for debug
            smtp.login(self.account.username, self.account.password.decode())
            smtp.sendmail(self.account.sender, self.receiver, self.msg.as_string())
            logger.debug("send mail PASS...\n\n")
        except smtplib.SMTPException:
            logger.error("send mail FAIL...\n\n")
        finally:
            if connect:
                smtp.quit()

    def send_message_from_163(self):
        connect = False
        try:
            server = smtplib.SMTP_SSL(self.account.host, self.account.port)
            # server.set_debuglevel(1)
            connect = True
            server.login(self.account.username, self.account.password.decode())
            server.sendmail(self.account.sender, self.receiver, self.msg.as_string())
            logger.debug("send mail PASS...\n\n")
        except Exception as e:
            if connect:
                server.quit()
            logger.error("send mail FAIL...\n\n")
            raise Exception(str(e))

    def main(self):
        self.create_email_code()
        self.send_message_from_163()
        return self.email_code


if __name__ == "__main__":

    Sender(person="hh18837292725@163.com").main()

