import pandas as pd
import streamlit as st

def edu():
    # Load CSV files
    path = './db_data/'
    edu_program_df = pd.read_csv(path + 'edu_program.csv')
    jobs_df = pd.read_csv(path + 'jobs.csv')
    ncs_to_jobs_df = pd.read_csv(path + 'ncs_to_jobs.csv')
    edu_company_df = pd.read_csv(path + 'edu_company.csv')

    # Simplify region names and sort them alphabetically
    edu_company_df['simplified_address'] = edu_company_df['address'].apply(lambda x: x.split()[0] if pd.notnull(x) else x)
    unique_regions = sorted(edu_company_df['simplified_address'].unique())
    

    # Filter related jobs
    unique_ncs_codes = edu_program_df['ncs_code'].unique()
    related_job_ids = ncs_to_jobs_df[ncs_to_jobs_df['ncs_code'].isin(unique_ncs_codes)]['id_jobs'].unique()
    related_jobs = jobs_df[jobs_df['id_jobs'].isin(related_job_ids)]

    # Streamlit UI setup
    st.title("직업연계 교육추천")

    selected_job = st.selectbox("직업을 선택하세요", related_jobs["name_jobs"].unique())
    selected_region = st.selectbox("지역을 선택하세요", ['All'] + list(unique_regions))
    selected_mode = st.selectbox("온라인 여부를 선택하세요", ['All', 'Online', 'Offline'])

    def get_programs_for_job(job_title, region, mode):
        job_id = related_jobs[related_jobs['name_jobs'] == job_title]['id_jobs'].iloc[0]
        ncs_codes = ncs_to_jobs_df[ncs_to_jobs_df['id_jobs'] == job_id]['ncs_code']
        recommended_programs = edu_program_df[edu_program_df['ncs_code'].isin(ncs_codes)]
        recommended_programs = recommended_programs.merge(edu_company_df, on='id_edu_company', how='left')

        if mode != 'All':
            mode_filter = '온라인' if mode == 'Online' else '오프라인'
            recommended_programs = recommended_programs[recommended_programs['online_status'] == mode_filter]

        if region != 'All':
            recommended_programs = recommended_programs[recommended_programs['simplified_address'] == region]

        return recommended_programs
    

    if st.button("교육추천"):
        recommended_programs = get_programs_for_job(selected_job, selected_region, selected_mode)
        
        if not recommended_programs.empty:
            for i in range(0, len(recommended_programs), 3):
                cols = st.columns(3)
                for col_num, index in enumerate(range(i, min(i + 3, len(recommended_programs)))):
                    program = recommended_programs.iloc[index]
                    with cols[col_num]:
                        # 카드 형식으로 교육 프로그램 정보를 표시
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
        else:
            st.write("조건에 맞는 교육 프로그램을 찾을 수 없습니다.")
