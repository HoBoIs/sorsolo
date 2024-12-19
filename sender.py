#sender.py
import smtplib
from email.mime.text import MIMEText

def send_mails(sender:str,pwd:str,tos:list[str],subject,messages:list[str]):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(sender,pwd)
    for to, body in zip(tos,messages):
        msg=MIMEText(body)
        msg['Subject']=subject
        msg['To']=to
        msg['From']=sender
        server.sendmail(sender,to,msg.as_string())
    server.close()

