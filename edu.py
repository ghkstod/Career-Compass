import pandas as pd
import streamlit as st

class EduMatcher:
    '''
    사용자의 직업 선호와 지역 기반으로 적합한 교육 프로그램을 추천하는 애플리케이션.
    
    이 클래스는 교육 프로그램 데이터를 로드하고, 사용자의 선호에 따라 맞춤형 교육 프로그램을 추천합니다.
    Streamlit을 사용하여 웹 기반 인터페이스를 제공하며, 사용자는 직업과 원하는 교육의 지역, 온라인 여부를 선택할 수 있습니다.
    
    속성 :
        path (str): 교육 프로그램 및 관련 데이터 파일이 위치한 디렉토리의 경로.
        
    메서드 :
        load_data() : 교육 프로그램, 직업, NCS 코드, 교육 기관 데이터를 로드합니다.
        prepare_data() : 로드된 데이터를 처리하고, 사용자 인터페이스에 필요한 형태로 준비합니다.
        app_interface() : Streamlit을 통해 사용자 인터페이스를 구성하고 사용자 입력을 처리합니다.
        get_programs_for_job(job_title, regions, mode) : 사용자의 선택에 따라 적합한 교육 프로그램을 조회합니다.
        display_programs(programs) : 추천된 교육 프로그램을 사용자에게 표시합니다.
        display_program_card(program) : 개별 교육 프로그램 정보를 카드 형식으로 표시합니다.
    '''
    def __init__(self, path='./db_data/'):
        '''
        EduMatcher 클래스의 인스턴스를 초기화합니다.
        
        매개변수 : 
            path(str) : 데이터 파일이 위치한 디렉토리의 경로.
        '''
        self.path = path
        self.load_data()
        self.prepare_data()

    def load_data(self):
        '''
        교육 프로그램, 직업, NCS코드, 교육기관 데이터 파일을 로드합니다.
        '''
        self.edu_program_df = pd.read_csv(self.path + 'edu_program.csv')
        self.jobs_df = pd.read_csv(self.path + 'jobs.csv')
        self.ncs_to_jobs_df = pd.read_csv(self.path + 'ncs_to_jobs.csv')
        self.edu_company_df = pd.read_csv(self.path + 'edu_company.csv')

    def prepare_data(self):
        '''
        로드된 데이터를 처리하고, 사용자 인터페이스에 필요한 형태로 준비합니다.
        '''
        self.edu_company_df['simplified_address'] = self.edu_company_df['address'].apply(
            lambda x: x.split()[0] if pd.notnull(x) else x)
        self.unique_regions = sorted(self.edu_company_df['simplified_address'].unique())

        unique_ncs_codes = self.edu_program_df['ncs_code'].unique()
        related_job_ids = self.ncs_to_jobs_df[self.ncs_to_jobs_df['ncs_code'].isin(unique_ncs_codes)]['id_jobs'].unique()
        self.related_jobs = self.jobs_df[self.jobs_df['id_jobs'].isin(related_job_ids)]

    def app_interface(self):
        '''
        Streamlit을 통해 사용자 인터페이스를 구성하고 사용자 입력을 처리합니다.
        '''
        st.markdown('<h1 style = "color : #2ec4b6; font-size : 50px; text-align : left;">교육매칭</h1>',
                    unsafe_allow_html=True)

        selected_job = st.selectbox("찾을 직업을 선택해!", self.related_jobs["name_jobs"].unique())
        selected_regions = st.multiselect("교육을 들을 지역을 골라줘",
                                          options=['All'] + list(self.unique_regions), default='All')
        selected_mode = st.selectbox("온라인 강의만 들을거야?", ['상관없어', '응', '아니'])

        if st.button("교육추천"):
            recommended_programs = self.get_programs_for_job(selected_job, selected_regions, selected_mode)
            self.display_programs(recommended_programs)

    def get_programs_for_job(self, job_title, regions, mode):
        '''
        사용자의 선택에 따라 적합한 교육 프로그램을 조회합니다.
        사용자는 직업, 지역, 온라인 여부들에 대해 선택하여 필터링 할 수 있습니다.
        
        매개변수 : 
            job_title(str) : 사용자가 선택한 직업
            regions(list) : 사용자가 선택한 지역 리스트
            mode(str) : 사용자가 선택한 온라인 여부
            
        반환값 :
            recomended_programs(DataFrame) : 추천된 교육 프로그램 목록
        '''
        job_id = self.related_jobs[self.related_jobs['name_jobs'] == job_title]['id_jobs'].iloc[0]
        ncs_codes = self.ncs_to_jobs_df[self.ncs_to_jobs_df['id_jobs'] == job_id]['ncs_code']
        recommended_programs = self.edu_program_df[self.edu_program_df['ncs_code'].isin(ncs_codes)]
        recommended_programs = recommended_programs.merge(self.edu_company_df, on='id_edu_company', how='left')

        if mode == '응':
            recommended_programs = recommended_programs[recommended_programs['online_status'] == '온라인']
        elif mode == '아니':
            recommended_programs = recommended_programs[recommended_programs['online_status'] == '오프라인']

        if 'All' not in regions:
            recommended_programs = recommended_programs[recommended_programs['simplified_address'].isin(regions)]

        return recommended_programs

    def display_programs(self, programs):
        '''
        추천된 교육 프로그램을 사용자에게 표시합니다.
        
        매개변수 :
            programs(DataFrame) : 추천된 교육 프로그램 데이터'''
        if not programs.empty:
            for i in range(0, len(programs), 2):
                cols = st.columns(2)
                for col_num, index in enumerate(range(i, min(i + 2, len(programs)))):
                    program = programs.iloc[index]
                    with cols[col_num]:
                        self.display_program_card(program)
        else:
            st.write("아쉽지만 조건에 맞는 교육 프로그램이 없어...")

    @staticmethod
    def display_program_card(program):
        '''
        개별 교육 프로그램 정보를 카드 형식으로 표시합니다.
        
        매개변수 :
            program(DataFrame) : 추천된 교육 프로그램 데이터
        '''
        st.markdown(
            f"""
            <div style="background-color: #cbf3f0; padding: 20px; border-radius: 10px; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,.1);">
                <h4 style="color: #333;">{program['name_edu_program']}</h4>
                <p style="color: #666;"><b>{program['name_edu_company']}</b></p>
                <p style="color: #666;">시작일: {program['date_start']} | 종료일: {program['date_end']}</p>
                <p style="color: #666;">자가부담금: {program['oopc']}</p>
                <p style="color: #666;">온라인 여부: {program['online_status']}</p>
                <p style="color: #666;">지역: {program['simplified_address']}</p>
                <a href="{program['link']}" target="_blank">More Info</a>
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == '__main__':
    edu_matcher = EduMatcher()
    edu_matcher.app_interface()
