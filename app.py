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
from job_search import job_search
from edu_reco import edu

def main():
    with st.sidebar:
        choice = option_menu("Menu", ["Main", "직업검색", "교육추천","공고추천","커뮤니티"],
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
        
    if choice=='직업검색':
        job_search()
        
    if choice=='교육추천':
        edu()
            
    if choice=='커뮤니티':
        board()
        
    
    
        
if __name__=='__main__':
    main()
    