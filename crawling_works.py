import selenium
import pandas as pd
import numpy as np
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 환경변수 파일 업로드
from dotenv import load_dotenv
import os
load_dotenv()

# 텍스트에서 첫 번째 줄만 추출
def remove_after_newline(text):
    """
    주어진 텍스트에서 첫 번째 줄만을 반환합니다.

    매개변수:
        text (str): 처리할 전체 텍스트.

    반환값:
        str: 첫 번째 줄에 해당하는 텍스트.
    """
    return text.split('\n')[0]

# 웹페이지에서 데이터를 수집
def crawling(driver):
    """
    Selenium WebDriver를 사용하여 현재 웹 페이지에서 채용 공고 정보를 수집합니다.

    매개변수:
        driver (webdriver.Chrome): 채용 공고 정보를 수집할 웹 페이지에 접근하는 데 사용되는 WebDriver 객체.

    반환값:
        DataFrame: 수집된 채용 공고 정보가 담긴 Pandas DataFrame.
    """

    # 데이터를 저장할 리스트 생성
    company_list = []
    recruit_list = []
    jd_1_list = []
    jd_2_list = []
    condition_list = []
    date_list = []
    link_list = []

    # 중분류당 수집할 채용공고의 개수
    how_many = 10
    
    for i in range(1, how_many + 1):

        # 수집할 선택자 요소
        company_xpath_1 = f'//*[@id="list{i}"]/td[2]/a'
        company_xpath_2 = f'//*[@id="list{i}"]/td[2]'
        recruit_css_path = f'#list{i} > td:nth-child(3) > div > div > a'
        jd_1_path = f'#jobContLine{i}'
        jd_2_path = f'#list{i} > td:nth-child(3) > div > p:nth-child(3)'
        condition_css_path = f'#list{i} > td:nth-child(4) > div'
        date_css_path = f'#list{i} > td:nth-child(5) > div > p:nth-child(2)'
        link_path = f'#list{i} > td:nth-child(3) > div > div > a'

        # 선택자 요소 찾기
        company_elements = driver.find_elements(By.XPATH, company_xpath_1)
        if not company_elements:
            company_elements = driver.find_elements(By.XPATH, company_xpath_2)
        
        recruit_elements = driver.find_elements(By.CSS_SELECTOR, recruit_css_path)
        jd_1_elements = driver.find_elements(By.CSS_SELECTOR, jd_1_path)
        jd_2_elements = driver.find_elements(By.CSS_SELECTOR, jd_2_path)
        condition_elements = driver.find_elements(By.CSS_SELECTOR, condition_css_path)
        date_elements = driver.find_elements(By.CSS_SELECTOR, date_css_path)
        link_elements = driver.find_elements(By.CSS_SELECTOR, link_path)

        # 찾은 데이터를 리스트에 추가
        for company_element in company_elements:
            company_list.append(company_element.text)
        for recruit_element in recruit_elements:
            recruit_list.append(recruit_element.text)
        for jd_1_element in jd_1_elements:
            jd_1_list.append(jd_1_element.text)
        for jd_2_element in jd_2_elements:
            jd_2_list.append(jd_2_element.text)
        for condition_element in condition_elements:
            condition_list.append(condition_element.text)
        for date_element in date_elements:
            date_list.append(date_element.text)
        for link_element in link_elements:
            link_list.append(link_element.get_attribute('href'))
    
    # work_company 데이터에서 첫 번째 줄만 추출
    company_list = [remove_after_newline(text) for text in company_list]

    # 데이터프레임 생성
    df = pd.DataFrame({
        'work_company' : company_list,
        'recruit' :recruit_list,
        'job_describ_1': jd_1_list,
        'job_describ_2' : jd_2_list,
        'condition' : condition_list,
        'date' : date_list,
        'link' : link_list})
    return df

def main():
    """
    메인 함수에서는 Selenium을 설정하여 특정 채용 공고 웹페이지로부터 데이터를 크롤링하고,
    결과를 처리하여 최종적으로 두 개의 CSV 파일(`worknet_company.csv`와 `worknet_positions.csv`)로 저장합니다.
    
    이 과정에서 직업 코드 리스트를 순회하며 각 코드에 해당하는 웹 페이지에서 채용 정보를 수집하고,
    수집된 데이터에서 필요한 변환 작업을 수행한 후, 데이터 저장 형식에 맞게 CSV 파일로 저장합니다.
    """

    # Chrome WebDriver 설정
    CHROME_DRIVER_PATH = './chromedriver.exe'
    service = Service(executable_path=CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=service, options=options)
    
    # 데이터를 저장할 데이터 프레임 생성
    df = pd.DataFrame()

    # 직업 코드 리스트
    list_1 = ['084', '086', '081', '082', '085', '083']
    list_2 = ['014', '017', '012', '01C', '019', '013', '01A', '016', '01B', '011', '015', '018']
    list_3 = ['039', '031', '032', '036', '038', '037', '034', '035', '033']
    list_4 = ['132', '135', '134', '133', '131']
    list_5 = ['06A', '062', '067', '066', '068', '061', '065', '063', '064', '069']
    list_6 = ['044', '042', '043', '041']
    list_7 = ['096', '093', '095', '091', '094', '099', '09A', '098', '092', '097']
    list_8 = ['123', '124', '122', '125', '121', '126']
    list_9 = ['103', '107', '102', '104', '105', '101', '106', '112', '111', '114', '11A', '119', '116', '118', '117', '115', '113']
    list_10 = ['027', '028', '025', '02B', '024', '021', '029', '026', '02C', '023', '022', '02A']
    list_11 = ['076', '07A', '071', '074', '079', '072', '07B', '073', '075', '077', '078']
    list_12 = ['058', '052', '055', '056', '059', '057', '051', '054', '053']
    
    # 직업 코드를 합친 work_code 리스트 생성
    worknet_job_list = [item for sublist in [list_1, list_2, list_3, list_4, list_5, list_6, list_7, list_8, list_9, list_10, list_11, list_12] for item in sublist]
    df2 = pd.DataFrame({'work_code_original': worknet_job_list})

    # index 순서로 work_code 생성
    df2['work_code'] = df2.index
    df2.index.name = 'work_code'

    # 환경변수에서 url 호출
    url_1 = os.getenv('URL_WORK_1')
    url_2 = os.getenv('URL_WORK_2')

    for i in worknet_job_list:

        # url 조합 후 chrome.driver 실행
        url = f'{url_1}{i}{url_2}'
        driver.get(url=url)

        # 데이터 수집 실행
        result_crawl = crawling(driver) 
        result_crawl['work_code_original'] = str(i)
        
        # 수집한 데이터 저장
        df = pd.concat([df, result_crawl], ignore_index=True)
        time.sleep(random.uniform(2,20))

    # worknet_company 데이터프레임 생성 
    df3 = df[['work_company']].copy()
    df3 = df3.drop_duplicates()
    df3 = df3.reset_index(drop=True).rename_axis('id_work_company').reset_index()

    # 수집된 데이터의 work_code_original을 work_code로 변경
    work_code_mapping = df2.set_index('work_code_original')['work_code'].to_dict()
    df['work_code']=df['work_code_original'].map(work_code_mapping)
    df = df.drop(columns=['work_code_original'])

    # worknet_company의 회사id와 worknet_position의 회사id 매핑
    company_id_mapping = df3.set_index('work_company')['id_work_company'].to_dict()
    df['id_work_company']=df['work_company'].map(company_id_mapping)
    df = df.drop(columns=['work_company'])
    
    # 컬럼 순서 변경
    priority_columns = ['id_work_company', 'work_code']
    remaining_columns = [col for col in df.columns if col not in priority_columns]
    new_column_order = priority_columns + remaining_columns
    df = df[new_column_order]
    
    # 채용공고id를 index번호로 변경
    df = df.reset_index(drop=True).rename_axis('id_work_positions').reset_index()

    # csv 파일로 저장
    df3.to_csv('db_data/worknet_company.csv', index=False)
    df.to_csv('db_data/worknet_positions.csv', index=False)
    
    driver.quit()

if __name__ == '__main__':
    main()