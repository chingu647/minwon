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
import seaborn as sns

import geopandas as gpd 

import folium 
from streamlit_folium import folium_static 
from folium.plugins import GroupedLayerControl

import nltk 
from konlpy.tag import Kkma, Hannanum, Twitter, Okt
from wordcloud import WordCloud, STOPWORDS 

from time import localtime, strftime 

import mf 

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ global 변수 설정
global map_t0  # ----------------------------------------------------------------------- 
global organ
global kind1 
global base_position 
global keyword 

organ = "ALL"   # ALL 광주전남본부 광주지사 담양지사 순천지사 함평지사 구례지사 보성지사 남원지사 
# choice 종류
kind1 = 'KIND1' # ----------------------------------------------------------------------
kind2 = 'KIND2' # ----------------------------------------------------------------------
team  = 'TEAM'  # ----------------------------------------------------------------------
road  = 'ROAD'  # ---------------------------------------------------------------------- 

base_position = [35.18668601, 126.87954220] 
# word cloud 
keyword = 'KEYWORD'

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
st.markdown(""" 
            <style> 
                table{background-color:#f0f0f0;} 
                img {max-width: 1000px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
            
            </style> """, 
            unsafe_allow_html=True
            )     

# ################################################# 민원 지도 보기 
cont9 = st.container(border=False)
cont9.markdown(f"##### 😎 {organ} 민원 :rainbow[노선별로 한눈에 보기] 👀") 

tabs = st.tabs(['🌍 지 도', '🔎키워드', '💾데이터']) 
with tabs[0]: 
    pass 
    # 테이블 데이터
    df8_0, df8_1, df8_2, wc8  = mf.load_df(organ, kind1) 

    # map data  
    map_t1 = mf.load_map(base_position, organ, kind1) 
    # mf.load_map_kind1(organ, kind1, base_position) 

with tabs[1]: 
    fig9_0, df9_0, df9_1, df9_2, wc9 = mf.load_wc(organ, keyword) 
    tabs[1].pyplot(fig9_0, use_container_width=True) 

with tabs[2]: 
    tabs[2].dataframe(df9_1, use_container_width=True) 