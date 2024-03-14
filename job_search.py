import streamlit as st
import pandas as pd
def job_search():
    job_tag=pd.read_csv('./data/job_info.csv',encoding='utf-8')
    job_int=pd.read_csv('./data/job_int.csv',encoding='utf-8')
    job_info=pd.read_csv('./data/job_tag.csv',encoding='utf-8')

    merged_df = pd.merge(job_tag, job_info, on='직무', how='inner')
    merged_df = pd.merge(merged_df, job_int, left_on='직무', right_on='NCS 기준', how='inner')
    merged_df=merged_df.drop(labels='NCS 직무분류코드',axis=1)
    merged_df=merged_df.drop_duplicates()

    st.subheader('직업검색')
    tab1,tab2,tab3=st.tabs(['정보기술','통신기술','방송기술'])

    def display_jobs(select_df):
        # 몇 줄이 필요한지 계산합니다 (한 줄에 3개의 직무 카드가 있습니다).
        num_of_rows = len(select_df) // 3 + (len(select_df) % 3 > 0)
        for i in range(num_of_rows):
            cols = st.columns(3)  # 3개의 칼럼을 생성합니다.
            for j in range(3):
                idx = i * 3 + j  # 현재 데이터프레임에서 카드에 해당하는 데이터의 인덱스입니다.
                if idx < len(select_df):
                    with cols[j]:
                        st.markdown(f'''
                                <div style ="background-color :#cbf3f0; padding : 10px; border-radius : 5px;">
                                    <p style = "font-size : 13px;">{'직무:'}{select_df.iloc[idx]["직무"]}</p>
                                </div>
                                ''', unsafe_allow_html = True)
                        st.write("-----")  # 카드 구분선입니다.

    with tab1:
        select_df=merged_df.loc[merged_df['중분류_1']=='정보기술']
        display_jobs(select_df)
        
    with tab2:
        select_df=merged_df.loc[merged_df['중분류_1']=='통신기술']
        display_jobs(select_df)
        
    with tab3:
        select_df=merged_df.loc[merged_df['중분류_1']=='방송기술']
        display_jobs(select_df)
        
        
        


