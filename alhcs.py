from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
import json
from pyvirtualdisplay import Display 
display = Display(visible=0, size=(1920, 1080)) 
display.start() 
path='/home/ss2468456/chromedriver' 
driver = webdriver.Chrome(path)
driver.implicitly_wait(10)



url = 'https://hcs.eduro.go.kr/'


def hcs (name, birthday, area, org, level, password):
    u=0
    if u==0:
        driver.get(url)
        u=1
    else:
        driver.execute_script('window.open("https://hcs.eduro.go.kr/","", "_blank")')
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element_by_xpath('/html/body/app-root/div/div[1]/div/button').click()
        driver.switch_to_alert().accept()
        
    driver.implicitly_wait(10)
    driver.find_elements_by_css_selector('button#btnConfirm2')[0].click()
    driver.implicitly_wait(10)
    time.sleep(1)
    driver.implicitly_wait(10)
    driver.find_elements_by_css_selector('button.searchBtn')[0].click()
    driver.implicitly_wait(10)
    time.sleep(1)
    driver.implicitly_wait(10)
    select = Select(driver.find_element_by_id('sidolabel'))
    select.select_by_value(value=area)  
    select = Select(driver.find_element_by_id('crseScCode'))
    select.select_by_value(value=level)
    school = driver.find_element_by_id('orgname')
    school.send_keys(orgname)
    driver.find_elements_by_css_selector('button.searchBtn')[0].click()
    driver.implicitly_wait(10)
    time.sleep(2)
    driver.find_elements_by_css_selector('a')[0].click()
    driver.find_elements_by_css_selector('input.layerFullBtn')[0].click()
    driver.implicitly_wait(10)
    name = driver.find_element_by_id('user_name_input')
    name.send_keys(name)
    name = driver.find_element_by_id('birthday_input')
    name.send_keys(birthday)
    driver.implicitly_wait(10)
    driver.find_elements_by_css_selector('input#btnConfirm')[0].click()
    driver.implicitly_wait(10)
    time.sleep(1)
    driver.implicitly_wait(10)
    
    pas=driver.find_element_by_xpath('//*[@id="WriteInfoForm"]/table/tbody/tr/td/input').click()
    driver.implicitly_wait(10)
    time.sleep(1)
    
    for i in range(4):
        driver.find_element_by_xpath("//a[@aria-label="+'"'+password[i]+'"'+"]").click()
    
    driver.find_elements_by_id('btnConfirm')[0].click()
    
    driver.implicitly_wait(10)
    time.sleep(2)
    driver.implicitly_wait(10)
    elem = driver.find_element_by_xpath("//*[@id='container']/div[1]/section[2]/div[2]/ul/li[1]/a/span[1]")  
    elem.click()

    driver.implicitly_wait(10)
    try:
        driver.switch_to_alert().accept()
    except:
        time.sleep(1)
        driver.implicitly_wait(10)
        for j in range(1,4):
            driver.find_elements_by_id('survey_q'+str(j)+'a1')[0].click()
            time.sleep(0.2)
        driver.find_elements_by_id('btnConfirm')[0].click()
        driver.implicitly_wait(10)
        try: 
            for j in range(1,4):
                driver.find_elements_by_id('survey_q'+str(j)+'a1')[0].click()
                time.sleep(0.2)
        except:
            None
        time.sleep(1)
    driver.implicitly_wait(10)
    if u==1:
        u=2
    else:
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])



    driver.quit()
with open('index.json',encoding='utf-8') as f:
    data=json.load(f)
for i in data:
    d=data[i]
    hcs(i,d['birthday'],d['area'],d['org'],d['level'],d['password'])
