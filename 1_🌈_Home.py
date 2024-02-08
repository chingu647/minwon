import streamlit as st 
import plotly.express as px
import plotly.graph_objects as go 
import plotly.figure_factory as ff 
from plotly.subplots import make_subplots 
import pandas as pd
import numpy as np 
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import matplotlib.font_manager as fm 
# import seaborn as sns
import geopandas as gpd 
import folium 
from streamlit_folium import folium_static 
import nltk 
from konlpy.tag import Kkma, Hannanum, Twitter, Okt
from wordcloud import WordCloud, STOPWORDS 
from PIL import Image 
from streamlit_option_menu import option_menu 
from time import localtime, strftime 
import os 
import mf 
import tab_all
import tab0 
import tab1 
import tab2
import tab3 
import tab4 
import tab5 
import tab6 
import tab7 
st.set_page_config(layout="wide",
                   page_title="한눈에 민원 보기", 
                   page_icon="🌈", 
                   ) 
#   
font_path_ = "data/NanumGothic.ttf" 
font_name = fm.FontProperties(fname=font_path_).get_name() 
mpl.rcParams['axes.unicode_minus'] = False 
mpl.rcParams['font.family'] = font_name 
# plt.style.use('ggplot') 
mpl.rc('font', size=18)
mpl.rc('axes', titlesize=18)
mpl.rc('axes', labelsize=18) 
mpl.rc('xtick', labelsize=18)
mpl.rc('ytick', labelsize=18)
mpl.rc('legend', fontsize=18)
mpl.rc('figure', titlesize=12) 
# 
st.markdown(""" 
            <style> 
                table{background-color:#f0f0f0;} 
            </style> """, 
            unsafe_allow_html=True
            ) 
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    # padding-bottom: 1rem;
                    # padding-left: 1rem;
                    # padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True) 
# 
user_name = None
user_pass = None
my_name = " "
my_pass = " "
placeholder = st.empty() 
if (user_name != my_name ) and (user_pass != my_pass): 
    with placeholder.form(key="form"): 
        col1, col2 = st.columns(2)
        with col1:
            user_name = st.text_input("아이디를 입력하세요 ! : ") 
        with col2: 
            user_pass = st.text_input("암호를 입력하세요 ! : ")
        submit = st.form_submit_button("login") 
    if user_name != my_name:
        st.error("이름을 정확히 입력하세요 !!!") 
    elif user_pass != my_pass:
        st.error("암호를 정확히 입력하세요 !!!") 
    else: 
        placeholder.empty() 
        global file_name 
        menu = ['2023','2024', '2025']
        op1 = st.sidebar.selectbox('Source Data', menu) 
        if menu[0] == op1: 
            if os.path.exists('data/2023.csv') :
                file_name =  "data/2023.csv" 
        elif menu[1] == op1: 
            if os.path.exists('data/2024.csv') :
                file_name =  "data/2024.csv" 
        elif menu[2] == op1: 
            if os.path.exists('data/2025.csv') :
                file_name =  "data/2025.csv" 
        else:
            file_name = "data/2023.csv" 
        st.image('data/th.jpg', width=30 ) 
        ################################################################################# 
        st.subheader('한눈에 보는 :blue[광주전남] 민원 지도', divider='rainbow') 
        ################################################################################# 
        selected = option_menu(menu_title=None,
                                options=[ "ALL", "본부","광주","담양","순천","함평","구례","보성","남원"],
                                icons=[None,None,None,None,None,None,None,None,],  
                                menu_icon="cast",
                                default_index=0,
                                orientation='horizontal', 
                                styles={"container": {"padding": "0px", # {"padding": "0!important", 
                                                    "margin" : "0px",
                                                    "background-color": "#fafafa"},
                                        "icon": {"color": "orange",  
                                                "margin":"0px", 
                                                "padding":"0px",
                                                "font-size": "0px"}, 
                                        "nav-link": {"font-size": "13px", 
                                                    "text-align": "center", 
                                                    "margin":"0px", 
                                                    "padding":"0px",
                                                    "--hover-color": "#eee"},
                                        "nav-link-selected": {"background-color": "green"}, 
                                        } 
        )
        if selected == "ALL": 
            tab_all.run_tab() 
        elif selected == "본부": 
            tab0.run_tab() 
        elif selected == "광주": 
            tab1.run_tab() 
        elif selected == "담양":
            tab2.run_tab()
        elif selected == "순천":
            tab3.run_tab()
        elif selected == "함평":
            tab4.run_tab()
        elif selected == "구례":
            tab5.run_tab()
        elif selected == "보성":
            tab6.run_tab()
        elif selected == "남원":
            tab7.run_tab() 