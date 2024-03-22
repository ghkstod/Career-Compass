import streamlit as st
import pandas as pd

def work():
    # CSV 파일 읽기
    path = './db_data/'
    def read_data():
        jobs = pd.read_csv(path+'jobs.csv')
        jobs_to_worknet = pd.read_csv(path+'jobs_to_worknet.csv')
        worknet_positions = pd.read_csv(path+'worknet_positions.csv')
        worknet_company = pd.read_csv(path+'worknet_company.csv')
        return jobs, jobs_to_worknet, worknet_positions, worknet_company

    # 데이터 처리 및 매칭
    def match_data(jobs, jobs_to_worknet, worknet_positions, worknet_company):
        # 첫번째 매칭: jobs와 jobs_to_worknet 매칭
        matched_jobs = pd.merge(jobs, jobs_to_worknet, on='id_jobs')
        # 두번째 매칭: matched_jobs와 worknet_positions 매칭
        matched_positions = pd.merge(matched_jobs, worknet_positions, on='work_code')
        # 최종 매칭: matched_positions와 worknet_company 매칭
        final_matched_data = pd.merge(matched_positions, worknet_company, on='id_work_company')
        return final_matched_data

    # Streamlit 앱 인터페이스
    def app_interface(final_matched_data):
        st.markdown('<h1 style = "color : #2ec4b6; font-size : 50px; text-align : left;">공고매칭</h1>', unsafe_allow_html=True)
        
        # 사용자가 직무 제목을 선택하여 게시물 보기
        job_titles = final_matched_data['name_jobs'].unique()
        # 직무 제목 리스트의 시작 부분에 빈 옵션 추가
        job_titles = [''] + list(job_titles)  # 빈 옵션 추가
        selected_job_title = st.selectbox("찾을 직업을 선택해!", job_titles)
        
        # 직무 제목이 선택된 경우에만 진행
        if selected_job_title:
            # 선택된 직무 제목에 기반한 데이터 필터링
            filtered_data = final_matched_data[final_matched_data['name_jobs'] == selected_job_title]
            
            # 게시물과 회사 이름을 카드 형식으로 한 줄씩 표시
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
