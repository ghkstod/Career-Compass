import streamlit as st
import pandas as pd

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
    def __init__(self, path='./db_data/'):
        '''
        JobMatcher 클래스의 인스턴스를 초기화합니다.
        
        매개변수 : 
            path(str) : 채용 관련 데이터 파일이 위치한 디렉토리의 경로
        '''
        self.path = path
        self.jobs, self.jobs_to_worknet, self.worknet_positions, self.worknet_company = self.load_data()
        self.final_matched_data = self.match_data()

    def load_data(self):
        '''
        채용 관련 데이터 파일들을 로드합니다.
        직업, 직업과 워크넷 코드와의 매핑, 워크넷 채용 공고, 회사 정보 데이터를 불러옵니다.
        
        반환값 : 
            jobs(DataFrame) : 직업에 대한 테이블
            jobs_to_worknet(DataFrame) : 직업과 워크넷 코드 매핑에 대한 테이블
            worknet_positions(DataFrame) : 워크넷 공고에 대한 테이블
            worknet_company(DataFrame) : 회사에 대한 테이블
        '''
        jobs = pd.read_csv(self.path+'jobs.csv')
        jobs_to_worknet = pd.read_csv(self.path+'jobs_to_worknet.csv')
        worknet_positions = pd.read_csv(self.path+'worknet_positions.csv')
        worknet_company = pd.read_csv(self.path+'worknet_company.csv')
        return jobs, jobs_to_worknet, worknet_positions, worknet_company

    def match_data(self):
        '''
        로드된 데이터를 기반으로 직업과 채용 공고를 매칭합니다.
        
        반환값 :
            final_matched_data(DataFrame) : 매칭된 채용 공고 정보를 포함하는 데이터 프레임
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

        if selected_job_title:
            filtered_data = self.final_matched_data[self.final_matched_data['name_jobs'] == selected_job_title]
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

if __name__ == '__main__':
    job_matcher = JobMatcher()
    job_matcher.app_interface()
