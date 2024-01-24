import streamlit as st 
import plotly.express as px
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


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-1) ST CACHE 사용
import mf 


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ global 변수 설정
global map_t50  # ----------------------------------------------------------------------- 
global organ_t50
global kind1_t50 
global base_position_t50 

organ_t50 = "본부" 
kind1_t50 = '서비스유형(대)'
base_position_t50 = [35.18668601, 126.87954220] 


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
st.markdown(""" 
            <style> 
                table{background-color:#f0f0f0;} 
                img {max-width: 1000px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
            
            </style> """, 
            unsafe_allow_html=True
            ) 


st.title('Project') 


###################################################################### tail 1 
st.markdown(f"##### 😎 :rainbow[광주전남{organ_t50} 민원 한눈에 보기] 👀 ") 

# 테이블 데이터
t50t1_kind1_df, t50t1_point_df, _ = mf.load_df(organ_t50, kind1_t50) 
    
st.markdown(f"""
<center>2024년도 주요 민원 유형은 <font color='red'><b>{t50t1_kind1_df.index[0]}</b> > {t50t1_kind1_df.index[1]} > {t50t1_kind1_df.index[2]} > {t50t1_kind1_df.index[3]} > {t50t1_kind1_df.index[4]}</font> 순 입니다.</center>
""", unsafe_allow_html=True) 


# map data  
# map_t1 = mf.load_map_kind1(organ_t0, kind1_t0, base_position_t0) 

mf.load_map_kind1(organ_t50, kind1_t50, base_position_t50) 