# Import necessary libraries
import streamlit as st
import pandas as pd

def work():
    # Read the CSV files
    path = './db_data/'
    def read_data():
        jobs = pd.read_csv(path+'jobs.csv')
        jobs_to_worknet = pd.read_csv(path+'jobs_to_worknet.csv')
        worknet_positions = pd.read_csv(path+'worknet_positions.csv')
        worknet_company = pd.read_csv(path+'worknet_company.csv')
        return jobs, jobs_to_worknet, worknet_positions, worknet_company

    # Process and match the data
    def match_data(jobs, jobs_to_worknet, worknet_positions, worknet_company):
        # First match: jobs to jobs_to_worknet
        matched_jobs = pd.merge(jobs, jobs_to_worknet, on='id_jobs')
        # Second match: matched_jobs to worknet_positions
        matched_positions = pd.merge(matched_jobs, worknet_positions, on='work_code')
        # Final match: matched_positions to worknet_company
        final_matched_data = pd.merge(matched_positions, worknet_company, on='id_work_company')
        return final_matched_data

    # Streamlit app interface
    def app_interface(final_matched_data):
        st.title("공고매칭")
        
        # Let users select a job title to view postings
        job_titles = final_matched_data['name_jobs'].unique()
        # Add an empty option at the beginning of the job titles list
        job_titles = [''] + list(job_titles)  # Empty option added
        selected_job_title = st.selectbox("직업을 선택하세요:", job_titles)
        
        # Only proceed if a job title is selected
        if selected_job_title:
            # Filter data based on selected job title
            filtered_data = final_matched_data[final_matched_data['name_jobs'] == selected_job_title]
            
            # Display job postings and company names in card format, one per line
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

    jobs, jobs_to_worknet, worknet_positions, worknet_company = read_data()
    final_matched_data = match_data(jobs, jobs_to_worknet, worknet_positions, worknet_company)
    app_interface(final_matched_data)
