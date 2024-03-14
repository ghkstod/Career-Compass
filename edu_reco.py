import streamlit as st
import csv
import pandas as pd
from datetime import datetime
def edu():
    def load_job_info(job_name):
        job_info = None
        df = pd.read_csv('./data/job_info.csv', encoding = 'utf-8')
        filterd_df = df[df['직무'] == job_name]
        filterd_df = filterd_df.drop_duplicates(subset='직무')
        if not filterd_df.empty:
            job_info = filterd_df.iloc[0].to_dict()
    
        return job_info

    def load_job_list():
        df = pd.read_csv('./data/job_info.csv', encoding = 'utf-8')
        df = df.drop_duplicates(subset='직무')
        return df['직무'].tolist()

    def load_education_info(start_date,ncs_code, online_only=False, without_fee=False):
        education_info = None
        df = pd.read_csv('./data/it_edu.csv', encoding = 'utf-8')

        df['훈련시작일자'] = pd.to_datetime(df['훈련시작일자'], format = '%Y%m%d').dt.date
        df['훈련종료일자'] = pd.to_datetime(df['훈련종료일자'], format = '%Y%m%d').dt.date
        filtered_df = df[df['NCS 직무분류_코드'] == ncs_code]

        if online_only:
            filtered_df=filtered_df[filtered_df['온라인 여부'] == '온라인']
        
        if without_fee:
            filtered_df = filtered_df[filtered_df['자비부담금'] == 0]
        
        # 날짜 필터링
        if start_date :
            mask = (filtered_df['훈련시작일자']>= start_date)
            filtered_df = filtered_df.loc[mask]

        if not filtered_df.empty:
            education_info=filtered_df.to_dict(orient='records')

        return education_info

    # 교육 과정 추천 페이지
    job_list = load_job_list()
    selected_job = st.selectbox('',['희망 직무를 선택하세요'] + job_list)

    if selected_job != '희망 직무를 선택하세요': # 희망 직무가 선택된 경우에만 칼럼 표시
        job_info = load_job_info(selected_job)
        if job_info:
            # st.write(f'선택된 직무: {selected_job}')

            ncs_code = job_info['NCS 직무분류코드']
                
            online_only = st.checkbox('온라인 교육 과정만 보기')
            without_fee = st.checkbox('자비 부담금 없는 교육 과정만 보기')
            start_date = st.date_input('교육 시작 날짜 선택', None)
            education_info = load_education_info(start_date,ncs_code, online_only, without_fee)

            if education_info :
                num_cols = 2
                total_info_count = len(education_info)
                num_rows = total_info_count // num_cols + (1 if total_info_count % num_cols != 0 else 0)

                cols = st.columns(num_cols)

                for row_idx in range(num_rows):
                    for col_idx in range(num_cols):
                        info_idx = row_idx * num_cols + col_idx
                        if info_idx < total_info_count:
                            with cols[col_idx]:
                                info = education_info[info_idx]
                                formatted_fee = '{:,.0f}'.format(info['훈련비'])
                                formatted_c_fee = '{:,.0f}'.format(info['자비부담금'])
                                link = info['링크']
                                if link.startswith('http'):
                                    link_text =f'<a href = "{link}">신청하러가기</a>'
                                else:
                                    link_text = '링크 없음'
                                st.markdown(f'''
                                    <div style ="background-color :#cbf3f0; padding : 10px; border-radius : 5px;">
                                        <h2 style = "color : #494D46; "font-size : 18px;">{info["훈련과정명"]}</h2>
                                        <p style = "color : #494D46; "font-size : 15px;">훈련일정: {info["훈련시작일자"]} ~ {info["훈련종료일자"]}</p>
                                        <p style = "color : #494D46; "font-size : 15px;">훈련비 : {formatted_fee}원</p>
                                        <p style = "color : #494D46; "font-size : 15px;">자비부담금 : {formatted_c_fee}원</p>
                                        <p style = "color : #494D46; "font-size : 15px;">수강 방식: {info['온라인 여부']}</p>
                                        <p style = "color : #494D46; "font-size : 15px;">{link_text}</p>
                                    </div>
                                    ''', unsafe_allow_html = True)

                            if col_idx == num_cols -1:
                                st.write('')
                        else : 
                            with cols[col_idx]:
                                pass


        