import streamlit as st
import pandas as pd
import sqlite3

class JobMatcher:
    '''
    사용자의 직업 선택에 기반하여 적합한 채용 공고를 매칭하고 표시하는 애플리케이션.

    이 클래스는 사용자에게 직업 선택을 위한 인터페이스를 제공하고, 선택된 직업에 대한 채용 공고를 데이터베이스에서 조회하여 표시합니다.
    데이터는 pandas DataFrame을 통해 처리되며, Streamlit을 사용하여 웹 기반 인터페이스를 구현합니다.
    
    속성:
        path (str): 데이터 파일이 위치한 디렉토리의 경로.
        
    메서드:
        read_data(): 채용 관련 데이터 파일들을 로드합니다.
        match_data(): 로드된 데이터를 기반으로 직업과 채용 공고를 매칭합니다.
        app_interface(): 사용자에게 직업 선택 인터페이스를 제공하고 매칭된 채용 공고를 표시합니다.
    '''
    def __init__(self, db_path='./db/data.db'):
        '''
        JobMatcher 클래스의 인스턴스를 초기화합니다.
        
        매개변수 : 
            db_path(str) : SQLite DB 파일 경로
        '''
        self.db_path = db_path
        self.jobs, self.jobs_to_worknet, self.worknet_positions, self.worknet_company = self.load_data()
        self.final_matched_data = self.match_data()


    def load_data(self):
        '''
        SQLite 데이터베이스에서 채용 관련 데이터를 로드합니다.
        '''
        conn = sqlite3.connect(self.db_path)
        jobs = pd.read_sql_query('SELECT * FROM jobs', conn)
        jobs_to_worknet = pd.read_sql_query('SELECT * FROM jobs_to_worknet', conn)
        worknet_positions = pd.read_sql_query('SELECT * FROM worknet_positions', conn)
        worknet_company = pd.read_sql_query('SELECT * FROM worknet_company', conn)
        conn.close()
        return jobs, jobs_to_worknet, worknet_positions, worknet_company

    def match_data(self):
        '''
        로드된 데이터를 기반으로 직업과 채용 공고를 매칭합니다.
        '''
        matched_jobs = pd.merge(self.jobs, self.jobs_to_worknet, on='id_jobs')
        matched_positions = pd.merge(matched_jobs, self.worknet_positions, on='work_code')
        final_matched_data = pd.merge(matched_positions, self.worknet_company, on='id_work_company')
        return final_matched_data

    def app_interface(self):
        '''
        사용자에게 직업 선택 인터페이스를 제공하고 매칭된 채용 공고를 표시합니다.
        '''
        st.markdown('<h1 style = "color : #2ec4b6; font-size : 50px; text-align : left;">공고매칭</h1>', unsafe_allow_html=True)
        job_titles = self.final_matched_data['name_jobs'].unique()
        job_titles = [''] + list(job_titles)
        selected_job_title = st.selectbox("찾을 직업을 선택해!", job_titles)

        # 지역 정보 변환을 위한 내부 함수
        def convert_region(region):
            region_mapping = {
                '경기': '경기도', '경남': '경상남도', '경북': '경상북도',
                '광주': '광주광역시', '대구': '대구광역시', '대전': '대전광역시',
                '부산': '부산광역시', '서울': '서울특별시', '인천': '인천광역시',
                '전북': '전라북도', '충남': '충청남도', '전북특별자치도':'전라북도',
                '강원특별자치도':'강원도', '세종특별자치시':'서울특별시',
            }
            return region_mapping.get(region, region)
        
        # 지역 정보 추출 및 변환
        self.final_matched_data['region'] = self.final_matched_data['job_describ_2'].apply(
            lambda x: convert_region(x.split(' ')[4]) if len(x.split(' ')) > 4 and x.split(' ')[2] == '~' else convert_region(x.split(' ')[2]) if len(x.split(' ')) > 2 else 'Unknown'
        )
        regions = self.final_matched_data['region'].unique()
        regions = list(sorted(regions))
        selected_regions = st.multiselect("지역을 선택해!", options=regions)

        # 멀티셀렉트를 통해 선택된 지역들에 대한 필터링 적용
        filtered_data = self.final_matched_data[self.final_matched_data['name_jobs'] == selected_job_title]
        if selected_regions:
            filtered_data = filtered_data[filtered_data['region'].isin(selected_regions)]

        if selected_job_title and not filtered_data.empty:
            for _, row in filtered_data.iterrows():
                st.markdown(f"""
                <div style="background-color:#cbf3f0;padding:20px;border-radius:10px;margin-bottom:10px;">
                    <h4 style="color:#333;">{row['recruit']}</h4>
                    <p>회사명: <strong>{row['work_company']}</strong></p>
                    <p>{row['job_describ_1']}</p>
                    <p>{row['job_describ_2']}</p>
                    <p>{row['condition']}</p>
                    <p>{row['date']}</p>
                    <a href="{row['link']}" target="_blank">More Info</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("아쉽지만 알맞은 공고가 없어..")





if __name__ == '__main__':
    job_matcher = JobMatcher()
    job_matcher.app_interface()
