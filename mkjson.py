import json

with open('index.json','r',encoding='utf-8') as f:
    data=json.load(f)


name=input('이름:')
code=input('지역코드(대구):')
level=input('학교등급코드(초,중,고):')
org=input('학교이름:')
birthday=input('생년월일(6자리):')
password=input('자가진단비밀번호(4자리)')

data[name]={'area' : code, 'level' : level, 'org' : org, 'birthday' : birthday, 'password' : password}



with open('index.json', 'w', encoding="utf-8") as make_file:
    json.dump(data, make_file, indent="\t")