import asyncio
import hcskr
import json
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

async def main():
    n=0
    st=''
    with open('index.json',encoding='utf-8') as f:
        data=json.load(f)
    for i in data:
        d=data[i]
        res = await hcskr.asyncSelfCheck(i,d['birthday'],d['area'],d['org'],d['level'],d['password'])
        if res['error']==False:
            print(i+'의 자가진단을 완료했습니다.')
            n+=1
        else:
            st+=i+'의'+res['message']+'\n'
    if st=='':
        sendGmail(str(n)+'명의 자가진단을 완료했습니다','success')
    else:
        print(st)
        sendGmail(st, 'error')
        
        
asyncio.get_event_loop().run_until_complete(main())