import selenium
import pandas as pd
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 환경변수 파일 업로드
from dotenv import load_dotenv
import os
load_dotenv()

# 웹페이지에서 데이터를 수집
def crawling(driver):
    """
    주어진 웹 드라이버 인스턴스를 사용하여 웹 페이지에서 직업명과 NCS 분류 코드를 크롤링합니다.

    페이지 내에 특정 CSS 선택자를 사용하여 직업명과 NCS 코드가 담긴 요소를 찾고,
    이를 딕셔너리 형태로 변환하여 리스트에 저장합니다. 최종적으로, 이 리스트를 바탕으로
    Pandas DataFrame을 생성하여 반환합니다.

    매개변수:
        driver (selenium.webdriver.Chrome): Selenium WebDriver 인스턴스.

    반환값:
        pandas.DataFrame: 수집된 데이터를 포함하는 DataFrame.
    """

    # 데이터를 저장할 리스트 생성
    job_data = []

    for i in range(0, 11):
        jobs_css_path = f'#list_{i} > td.pl_50 > button'
        ncs_css_path = f'#list_{i} > td:nth-child(4) > div > div > ul > li > a'
        
        # 수집할 선택자 요소
        job_elements = driver.find_elements(By.CSS_SELECTOR, jobs_css_path)
        ncs_elements = driver.find_elements(By.CSS_SELECTOR, ncs_css_path)

        # 찾은 데이터를 딕셔너리 형태로 저장
        for job_index, job_element in enumerate(job_elements):
            job_title = job_element.text
            ncs_codes = []
            for ncs_element in ncs_elements:
                href = ncs_element.get_attribute('href')
                start = href.find("'") + 1
                code = href[start:start+8]
                ncs_codes.append(code)
           
           # 딕셔너리를 리스트에 추가
            for code in ncs_codes:
                job_data.append({'직업명': job_title, 'NCS분류': code})

    # 데이터 프레임 생성
    return pd.DataFrame(job_data)

def main():
    """
    메인 함수에서는 Selenium WebDriver를 설정하고, 환경변수에서 URL을 로드하여
    지정된 페이지 범위에 대해 크롤링을 수행합니다. 각 페이지에서 수집된 데이터는
    하나의 DataFrame으로 합쳐지며, 최종적으로 CSV 파일로 저장됩니다.
    """
    # Chrome WebDriver 설정
    options = Options()
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu')  
    options.add_argument("user-agent=Yeti") 
    driver = webdriver.Chrome(options=options)

    # 데이터를 저장할 데이터 프레임 생성
    df = None

    # 데이터 수집 범위
    last_page = 31

    # 환경변수에서 url 호출
    url = os.getenv('URL_JOB')

    for i in range(0, last_page + 1):
        # url 조합 후 chrome.driver 실행
        url = f'{url}'+str(i)
        driver.get(url=url)

        # 데이터 수집 실행
        result_crawl = crawling(driver)

        # 수집한 데이터 저장
        df = pd.concat([df, result_crawl], ignore_index=True)
        
        time.sleep(random.uniform(2,5))
        
    # csv 파일로 저장
    df.to_csv('db_data/jobs.csv', index=False)
    driver.quit()

if __name__ == '__main__':
    main()