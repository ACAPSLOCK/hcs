import smtplib
from email.mime.text import MIMEText
import pytz
import datetime as dt

def sendGmail(text, code):
    date=dt.datetime.now(pytz.timezone('Asia/Seoul'))
    da=date.strftime("%m월 %d일")
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('ss2468456@gmail.com', 'xazsvuikvgkqdydt')
    msg = MIMEText(da+' '+text)
    msg['Subject'] = da+' '+code
    s.sendmail("ss2468456@gmail.com", "h_s_posan21_1405@dge.go.kr", msg.as_string())
    s.quit()

sendGmail('test1','test2')
