def home():
    import streamlit as st 
    import bcrypt
    import sqlite3
    
    st.title('Career Compass')
    st.write('Career Compass는 사용자의 성향을 기반으로 한 직업, 교육 프로그램 및 채용 공고 추천 서비스입니다.')
    st.write('')
    st.write('이 서비스의 목표는 사용자에게 적합한 직업을 찾아주고 해당 직업을 달성하기 위한 맞춤형 국비 교육 과정 정보를 제공하는 것으로 이를 통해 취업이나 경력 개발에 대한 부담감을 줄이고 성공적인 진로를 찾을 수 있을 것으로 기대됩니다.')
    st.write('')
        
    with st.expander('방식1'):
        st.write('설명')