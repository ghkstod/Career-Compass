import streamlit as st
import pandas as pd

class JobMatcher:
    def __init__(self, path='./db_data/'):
        self.path = path
        self.jobs, self.jobs_to_worknet, self.worknet_positions, self.worknet_company = self.read_data()
        self.final_matched_data = self.match_data()

    def read_data(self):
        jobs = pd.read_csv(self.path+'jobs.csv')
        jobs_to_worknet = pd.read_csv(self.path+'jobs_to_worknet.csv')
        worknet_positions = pd.read_csv(self.path+'worknet_positions.csv')
        worknet_company = pd.read_csv(self.path+'worknet_company.csv')
        return jobs, jobs_to_worknet, worknet_positions, worknet_company

    def match_data(self):
        matched_jobs = pd.merge(self.jobs, self.jobs_to_worknet, on='id_jobs')
        matched_positions = pd.merge(matched_jobs, self.worknet_positions, on='work_code')
        final_matched_data = pd.merge(matched_positions, self.worknet_company, on='id_work_company')
        return final_matched_data

    def app_interface(self):
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
