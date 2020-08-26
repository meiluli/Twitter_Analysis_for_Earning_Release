
import smtplib
from glob import glob
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

today = str(date.today())
msg = MIMEMultipart()
dir = '/Users/limeilu/PycharmProjects/Twitter_Analysis_for_Earning_Release'

class SendEmail:
    def __init__(self,toaddr, ccaddr):

        self.fromaddr = "ml6684@nyu.edu"
        self.pswd = pd.read_csv(dir+'/utils/token/TOKEN.txt').columns[0]
        # send to which email address
        self.toaddr = toaddr
        self.ccaddr = ccaddr
    def send_preopen_email(self):
        
        fileaddr= f'{dir}/utils/data/preopen/{today}/*'

        msg['From'] = self.fromaddr
        msg['To'] = ", ".join(self.toaddr)
        msg['Subject'] = "Twitter sentiment pre-open analysis results"
        msg['Cc'] = self.ccaddr
        body = "Hi there, \n This is pre-open analysis result for today. \n\n  - Sent by Python"
        msg.attach(MIMEText(body, 'plain'))

        names = glob(fileaddr)
        for filename in names:
            attachment = open(f"{filename}", "rb")

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {filename.split('$')[-1]}" )

            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.fromaddr, self.pswd)
        text = msg.as_string()
        server.sendmail(self.fromaddr, self.toaddr, text)
        server.quit()
        print(f'Email successfully sent to {self.toaddr}')

    def send_regular_email(self):
        
        fileaddr= f'{dir}/utils/data/senti_graph/{today}/*'
        msg['From'] = self.fromaddr
        msg['To'] = ", ".join(self.toaddr)
        msg['Subject'] = "Twitter sentiment analysis results"
        msg['Cc'] = self.ccaddr
        body = "Hi there, \n This is twitter analysis result for today. \n\n  - Sent by Python"
        msg.attach(MIMEText(body, 'plain'))

        names = glob(fileaddr)
        for filename in names:
            attachment = open(f"{filename}", "rb")

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {filename.split('$')[-1]}" )

            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.fromaddr,self.pswd)
        text = msg.as_string()
        server.sendmail(self.fromaddr, self.toaddr, text)
        server.quit()
        print(f'Email successfully sent to {self.toaddr}')


    def send_realtime_email(self,body_):
        msg['From'] = "ml6684@nyu.edu"
        msg['To'] = ", ".join(self.toaddr)
        msg['Subject'] = "[Test] Twitter real time (half) hourly trending alert"
        body = body_
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.fromaddr,self.pswd)
        text = msg.as_string()
        server.sendmail(self.fromaddr, self.toaddr, text)
        server.quit()
        print(f'Email successfully sent to {self.toaddr}')