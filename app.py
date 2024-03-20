# -*- codin:utf-8 -*-

import streamlit as st 
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px 
from board import board
from home import home
from survey import survey

def main():
    with st.sidebar:
        choice = option_menu("Menu", ["Main", "설문조사", "교육추천","공고추천","커뮤니티"],
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
        
    if choice=='설문조사':
        survey()
        
    if choice=='교육추천':
        st.write('mmmm')
        
    if choice=='공고추천':

        # 각 버튼에 대한 내용 정의
        button_options = {
            "Button 1": "This is the content for Button 1",
            "Button 2": "This is the content for Button 2",
            "Button 3": "This is the content for Button 3",
        }

        # 각 버튼을 생성하고 클릭 여부를 확인
        button_clicked = {}
        for option in button_options.keys():
            button_clicked[option] = st.button(option)

        # 클릭한 버튼에 대해 내용을 표시하는 창 생성
        for option, clicked in button_clicked.items():
            if clicked:
                st.subheader(option)
                content = st.text_area("Write something:")
                st.write(f"You wrote: {content}")
                
            
    if choice=='커뮤니티':
        board()
        
    
    
        
if __name__=='__main__':
    main()
    