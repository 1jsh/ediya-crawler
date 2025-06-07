from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import warnings

#모든 경고 메시지 무시
warnings.filterwarnings(action='ignore')

#chrome 드라이버 등록 및 홈페이지 URL 지정
#접속
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.ediya.com/contents/find_store.html")
time.sleep(2)

# 주소 버튼 클릭
xpath = '//*[@id="contentWrap"]/div[3]/div/div[1]/ul/li[2]/a'
addr_btn = driver.find_element(By.XPATH, xpath)
ActionChains(driver).move_to_element(addr_btn).perform()
addr_btn.click()
time.sleep(0.5)

driver.find_element(By.CSS_SELECTOR, "#contentWrap > div.contents > div > div.store_search_pop > ul > li:nth-child(2) > a").click()

city_list = ['종로구', '서울 중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구' , '마포구', '양천구', '서울 강서구', '구로구', '금천구', '영등포구', '동작구', '관악구', '서초구', '강남구', '송파구', '강동구']

# 매장 정보 저장할 초기 변수 선언
ediya_list = []   

for i in range(len(city_list)):
    
    #구 이름 집어넣고 검색 버튼 클릭하는 동작
    kw = driver.find_element(By.CSS_SELECTOR, "#keyword")
    kw.clear()
    kw.send_keys(city_list[i])
    btn = driver.find_element(By.CSS_SELECTOR, "#keyword_div > form > button")
    ActionChains(driver).move_to_element(btn).perform()
    btn.click()
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    ediya_store_list = soup.select('#placesList > li > a')
    time.sleep(2) 

    for store in range(len(ediya_store_list)):
               
        store_name = ediya_store_list[store].select_one("dt").text
        store_addr = ediya_store_list[store].select_one("dd").text
        ediya_list.append([store_name,store_addr])

columns = ['매장이름','매장주소']
ediya_df = pd.DataFrame(ediya_list, columns = columns)
ediya_df.to_csv('Ediya_stores_seoul.csv', index=False, encoding='utf-8')

driver.close()
