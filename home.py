import streamlit as st 
import bcrypt
import sqlite3

def home():
    '''
    Streamlit 애플리케이션의 메인화면의 내용을 꾸미는 함수
    '''
    
    st.markdown('<h1 style = "color : #2ec4b6; font-size : 36px; text-align : right;">CareerCompass</h1>', unsafe_allow_html=True)
    st.markdown('<h6 style = "color :#2ec4b6; text-align : right;"> 사용자의 성향을 기반으로 한 직업 추천 및 교육 프로그램 매칭 서비스</h6>', unsafe_allow_html=True)
    st.write('')
    st.write('이 서비스의 목표는 사용자에게 적합한 직업을 찾아주고 해당 직업을 달성하기 위한 맞춤형 국비 교육 과정 정보를 제공하는 것으로 이를 통해 취업이나 경력 개발에 대한 부담감을 줄이고 성공적인 진로를 찾을 수 있을 것으로 기대됩니다.')
    st.write('')
    st.write('')

    st.markdown('<h4 style = "color : #2ec4b6; "> 🧭 개발자의 말</h4>', unsafe_allow_html = True)
    st.write('주요 기능 알파 테스트 단계입니다.')
    st.write('향후 기능을 추가할 예정이고 더 좋은 서비스를 제공하고자 테스터분들의 피드백을 받고 있습니다.')
    st.write('불편한 사항 및 문의사항이 있으시면 아래 구글폼을 통해서 전달해주시면 감사드리겠습니다. 알파 테스터 어려분 모두에게 감사의 말씀을 드립니다.')
    st.write('')
    
    # 변경된 부분: 버튼 대신 하이퍼링크를 사용
    st.markdown('[설문조사 하러 가기](https://docs.google.com/forms/d/e/1FAIpQLScmomvXZ1mDu4Brg7tASW9yOwjw7qxtsx34Ias9LoIKZTpfDw/viewform)', unsafe_allow_html=True)

    # 사이트 주요 기능
    st.markdown('<h4 style = "color : #2ec4b6; "> 🧭 사이트 주요 기능</h4>', unsafe_allow_html = True)
    st.markdown('<h5> - 직업 추천 서비스</h5>', unsafe_allow_html=True)
    st.write(': 자신의 해시태그를 선택하는 설문조사를 기반으로 개인의 성향을 분석하고, 가장 적합한 직업을 추천')
    st.markdown('<h5> - 교육 매칭 서비스</h5>', unsafe_allow_html=True)
    st.write(': 선택 직무의 역량을 키우기 위한 국비 교육 프로그램 추천')
    st.markdown('<h5> - 채용 공고 매칭 서비스</h5>', unsafe_allow_html=True)
    st.write(': 사용자의 선호 직무 관련 채용 공고 매칭')
    
    st.write('')
    st.write('')

    # 향후 계획
    st.markdown('<h4 style = "color : #2ec4b6; "> 🧭 향후 계획</h4>', unsafe_allow_html = True)
    st.write('- 교육과정, 채용공고 추천에서 더 나아가 관련 자격증과 그에 따른 교육과정 정보까지 추천하여 경력 개발에 도움을 준다.')
    st.write('- Open API를 통해 데이터를 수집해 대상 산업군과 직업군을 확대할 수 있고 더욱 더 개인화된 맞춤 정보를 제공한다.')
    st.write('- 머신러닝, MBTI 등을 이용해 사용자의 특성과 유형을 자세하게 이해하고 보다 사용자 맞춤형 콘텐츠를 제공한다.')