import streamlit as st
import pandas as pd
import plotly.graph_objs as go

def insight():
    # 데이터 불러오기
    file_path = '연도별 직종별 신규구인인원.csv'
    data = pd.read_csv(file_path, index_col=0, encoding='CP949')

    # Streamlit 앱 시작
    st.title('연도별 구인인원수 변화')

    # 직종 선택 드롭다운
    selected_job = st.selectbox('직종을 선택하세요', data.index)

    # 선택한 직종에 대한 그래프 표시
    if selected_job:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=data.columns.astype(str), 
                            y=data.loc[selected_job], 
                            name=selected_job))  
        fig.update_layout(title='연도별 구인인원수 변화 - {}'.format(selected_job))
        fig.update_xaxes(tickvals=data.columns, ticktext=[f'{year}년' for year in data.columns])
        st.plotly_chart(fig)

    # 데이터프레임 출력 (옵션)
    if st.checkbox('데이터 보기'):
        st.write(data)