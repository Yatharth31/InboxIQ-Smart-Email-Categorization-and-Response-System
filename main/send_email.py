from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os

cwd = os.getcwd()
f1 = open(os.path.join(cwd,"emailID.txt"))
emailID = f1.read().rstrip('\n')
f1.close()

f2 = open(os.path.join(cwd,"password.txt"))
emailPassword = f2.read().rstrip('\n')
f2.close()

def message(subject="Send_email test Subject", 
            text="This is the Body for send_email program to test the send_email functionality for sedning emails through python script", img=None,
            attachment=None):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    return msg


def send_mail(to,sub,body,emailID = emailID,emailPassword=emailPassword):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(emailID, emailPassword)
    msg = message(subject=sub, text=body)
    to = to
    smtp.sendmail(from_addr=emailID,
              to_addrs=to, msg=msg.as_string())
    smtp.quit()

