# -*- codin:utf-8 -*-

import streamlit as st 
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px 
from home import home
from survey import SurveyMatcher
from edu import EduMatcher
from work import JobMatcher
from board import BoardApp


def main():
    '''
    CareerCompass 웹 애플리케이션의 메인 함수
    
    사용자에게 다음 옵션을 제공하는 사이드바 메뉴를 생성합니다.
    - Main : 애플리케이션의 메인 화면을 보여줍니다.
    - 직업추천 : 몇가지 질문과 답변을 통해 사용자의 선호와 능력에 맞는 직업을 추천합니다.
    - 교육매칭 : 앞서 추천한 직업 또는 사용자가 이미 결정한 직업에 맞는 교육과정을 매칭합니다.
    - 공고매칭 : 사용자가 희망하는 직업에 맞는 공고를 매칭합니다.
    - 커뮤니티 : 사용자가 게시판에서 소통할 수 있는 공간을 제공합니다.
    
    선택된 메뉴에 따라 해당하는 기능을 실행합니다.
    '''
    
    with st.sidebar:
        choice = option_menu("Menu", ["Main", "직업추천", "교육매칭","공고매칭","커뮤니티"],
                            icons=['house', 'bi bi-search','bi bi-stack-overflow' ,'bi bi-person-badge-fill','bi bi-people-fill'],
                            menu_icon="app-indicator", default_index=0,
                            styles={
            "container": {"padding": "4!important", "background-color": "#fafafa"},
            "icon": {"color": "black", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
            "nav-link-selected": {"background-color": "#cbf3f0"},
        }                  
        )
    
    if choice=='Main':
        home()
        
    if choice=='직업추천':
        survey=SurveyMatcher()
        survey.run_survey()
        
    if choice=='교육매칭':
        edu=EduMatcher()
        edu.app_interface()
        
    if choice=='공고매칭':
        work=JobMatcher()
        work.app_interface()
        
                      
    if choice=='커뮤니티':
        board=BoardApp()
        board.run()
        
    
    
        
if __name__=='__main__':
    main()
    