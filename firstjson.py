import pandas as pd
import json

location ='C:/Users/RYZEN5/Documents/hcs'
file='hcslist.xlsx'
data_pd=pd.read_excel('{}/{}'.format(location, file), header=None, index_col=None, names=None)
data=pd.DataFrame.to_numpy(data_pd)

json_data = {}

for i in data:
    if i[4] <100000 :
        i[4]='0'+str(i[4])
    else:
        i[4]=str(i[4])
    
    if i[5] < 10:
        i[5]='000'+str(i[5])
    elif i[5] < 100:
        i[5]='00'+str(i[5])
    elif i[5] < 1000:
        i[5]='0'+str(i[5])
    else :
        i[5]=str(i[5])

    json_data[i[3]]={'area' : i[0], 'level' : i[1], 'org' : i[2], 'birthday' : i[4], 'password' : i[5]}
    
    
with open('index.json', 'w', encoding="utf-8") as make_file:
    json.dump(json_data, make_file, indent="\t")