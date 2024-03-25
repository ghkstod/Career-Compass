import pandas as pd
import streamlit as st

class EduMatcher:
    def __init__(self, path='./db_data/'):
        self.path = path
        self.load_data()
        self.prepare_data()

    def load_data(self):
        self.edu_program_df = pd.read_csv(self.path + 'edu_program.csv')
        self.jobs_df = pd.read_csv(self.path + 'jobs.csv')
        self.ncs_to_jobs_df = pd.read_csv(self.path + 'ncs_to_jobs.csv')
        self.edu_company_df = pd.read_csv(self.path + 'edu_company.csv')

    def prepare_data(self):
        self.edu_company_df['simplified_address'] = self.edu_company_df['address'].apply(
            lambda x: x.split()[0] if pd.notnull(x) else x)
        self.unique_regions = sorted(self.edu_company_df['simplified_address'].unique())

        unique_ncs_codes = self.edu_program_df['ncs_code'].unique()
        related_job_ids = self.ncs_to_jobs_df[self.ncs_to_jobs_df['ncs_code'].isin(unique_ncs_codes)]['id_jobs'].unique()
        self.related_jobs = self.jobs_df[self.jobs_df['id_jobs'].isin(related_job_ids)]

    def app_interface(self):
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
