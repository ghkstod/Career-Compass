import pandas as pd
import streamlit as st

def edu():
    # CSV 파일 로드
    path = './db_data/'
    edu_program_df = pd.read_csv(path + 'edu_program.csv')
    jobs_df = pd.read_csv(path + 'jobs.csv')
    ncs_to_jobs_df = pd.read_csv(path + 'ncs_to_jobs.csv')
    edu_company_df = pd.read_csv(path + 'edu_company.csv')

    # 지역 이름 단순화 및 알파벳 순으로 정렬
    edu_company_df['simplified_address'] = edu_company_df['address'].apply(lambda x: x.split()[0] if pd.notnull(x) else x)
    unique_regions = sorted(edu_company_df['simplified_address'].unique())
    
    # 관련 직업 필터링
    unique_ncs_codes = edu_program_df['ncs_code'].unique()
    related_job_ids = ncs_to_jobs_df[ncs_to_jobs_df['ncs_code'].isin(unique_ncs_codes)]['id_jobs'].unique()
    related_jobs = jobs_df[jobs_df['id_jobs'].isin(related_job_ids)]

    # Streamlit UI 설정
    st.markdown('<h1 style = "color : #2ec4b6; font-size : 50px; text-align : left;">교육매칭</h1>', unsafe_allow_html=True)

    selected_job = st.selectbox("찾을 직업을 선택해!", related_jobs["name_jobs"].unique())
    
    # 멀티 셀렉트박스로 변경
    selected_regions = st.multiselect("교육을 들을 지역을 골라줘", options=['All'] + list(unique_regions), default='All')
    
    selected_mode = st.selectbox("온라인 강의만 들을거야?", ['상관없어', '응', '아니'])

    def get_programs_for_job(job_title, regions, mode):
        # 선택된 직업 제목에 해당하는 job_id 가져오기
        job_id = related_jobs[related_jobs['name_jobs'] == job_title]['id_jobs'].iloc[0]
        # 해당 job_id와 관련된 ncs 코드 가져오기
        ncs_codes = ncs_to_jobs_df[ncs_to_jobs_df['id_jobs'] == job_id]['ncs_code']
        # 추천 교육 프로그램 찾기
        recommended_programs = edu_program_df[edu_program_df['ncs_code'].isin(ncs_codes)]
        # 교육 회사 정보와 결합
        recommended_programs = recommended_programs.merge(edu_company_df, on='id_edu_company', how='left')

        # 온라인/오프라인 모드 필터
        if mode == '응':
            recommended_programs = recommended_programs[recommended_programs['online_status'] == '온라인']
        elif mode == '아니':
            recommended_programs = recommended_programs[recommended_programs['online_status'] == '오프라인']

        # 지역 필터, 'All' 선택 시 모든 지역 표시
        if 'All' not in regions:
            recommended_programs = recommended_programs[recommended_programs['simplified_address'].isin(regions)]

        return recommended_programs
    
    if st.button("교육추천"):
        recommended_programs = get_programs_for_job(selected_job, selected_regions, selected_mode)
        
        if not recommended_programs.empty:
            for i in range(0, len(recommended_programs), 2):
                cols = st.columns(2)
                for col_num, index in enumerate(range(i, min(i + 2, len(recommended_programs)))):
                    program = recommended_programs.iloc[index]
                    with cols[col_num]:
                        # 카드 형식으로 교육 프로그램 정보 표시
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
            st.write("아쉽지만 조건에 맞는 교육 프로그램이 없어...")
