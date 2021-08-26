from base64 import b64decode, b64encode
from Cryptodome.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Cryptodome.PublicKey import RSA
import json
import requests
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


pubkey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA81dCnCKt0NVH7j5Oh2+SGgEU0aqi5u6sYXemouJWXOlZO3jqDsHYM1qfEjVvCOmeoMNFXYSXdNhflU7mjWP8jWUmkYIQ8o3FGqMzsMTNxr+bAp0cULWu9eYmycjJwWIxxB7vUwvpEUNicgW7v5nCwmF5HS33Hmn7yDzcfjfBs99K5xJEppHG0qc+q3YXxxPpwZNIRFn0Wtxt0Muh1U8avvWyw03uQ/wMBnzhwUC8T4G5NclLEWzOQExbQ4oDlZBv8BM/WxxuOyu0I8bDUDdutJOfREYRZBlazFHvRKNNQQD2qDfjRz484uFs7b5nykjaMB9k/EJAuHjJzGs9MMMWtQIDAQAB=="

def send_hcsreq(headers: dict, endpoint: str, school: str, json: dict):
    resp=requests.post(headers=headers, url=f"https://{school}hcs.eduro.go.kr{endpoint}", json=json) 
    return resp
def search_school(code: str, level: str, org: str):
    resp=requests.get(url=f"https://hcs.eduro.go.kr/v2/searchSchool?lctnScCode={code}&schulCrseScCode={level}&orgName={org}&loginType=school")
    return resp.json()
        



def enc(n):
    rsa_public_key = b64decode(pubkey)
    pub_key = RSA.importKey(rsa_public_key)
    cipher = Cipher_pkcs1_v1_5.new(pub_key)
    msg = n.encode("utf-8")
    length = 245

    msg_list = [msg[i : i + length] for i in list(range(0, len(msg), length))]

    encrypt_msg_list = [
        b64encode(cipher.encrypt(message=msg_str)) for msg_str in msg_list
    ]

    return encrypt_msg_list[0].decode("utf-8")        



def survey():
    st=''
    n=0
    with open('index.json',encoding='utf-8') as f:
        data=json.load(f)
    for i in data:
        d=data[i]
    
        orgcode=search_school(code=d['code'], level=d['level'], org=d['org'])['schulList'][0]['orgCode']
        res = send_hcsreq(headers={"Content-Type": "application/json"}, endpoint="/v2/findUser",school='dge',json={"orgCode": orgcode, "name": enc(i), "birthday": enc(d['birthday']), "loginType": "school","stdntPNo": None})
        try:
            token=res.json()['token']
        except:
            st+=i+'의 정보가 잘못되었습니다.\n'
            continue
    
        res = send_hcsreq(headers={"Content-Type": "application/json", "Authorization": token}, endpoint="/v2/validatePassword", school='dge', json={"password": enc(d['password']), "deviceUuid": ""})
        try:
            token=res.json()
        except:
            st+=i+'의 비밀번호가 잘못되었습니다.\n'
            continue
        
        res = send_hcsreq(headers={'Content-Type': 'application/json', 'Authorization': token}, endpoint="/v2/selectUserGroup", school='dge', json={})
        try:
            token=res.json()[0]['token']
        except:
            st+=i+'의 자가진단에 실패했습니다.(selectUserGroup error)\n'
            continue
        
        res = send_hcsreq(headers={'Authorization': token, 'Content-Type': 'application/json'}, endpoint= "/registerServey", school='dge', json={'deviceUuid': '', 'rspns00': 'Y', 'rspns01': '1', 'rspns02': '1', 'rspns03': None, 'rspns04': None, 'rspns05': None, 'rspns06': None, 'rspns07': '0', 'rspns08': '0', 'rspns09': '0', 'rspns10': None, 'rspns11': None, 'rspns12': None, 'rspns13': None, 'rspns14': None, 'rspns15': None, 'upperToken': token, 'upperUserNameEncpt': i})
        if res.status_code != 200:
            st+=i+'의 자가진단에 실패했습니다.(registerServey error)\n'
        n+=1
    if st=='':
        return sendGmail(str(n)+'명의 자가진단을 완료했습니다','success')
    else:
        return sendGmail(st, 'error')
    
survey() 
   
