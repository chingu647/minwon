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
kind1_t50 = 'KIND1'
base_position_t50 = [35.18668601, 126.87954220] 


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
st.markdown(""" 
            <style> 
                table{background-color:#f0f0f0;} 
                img {max-width: 1000px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
            
            </style> """, 
            unsafe_allow_html=True
            ) 


st.subheader('광주전남본부 민원 지도', divider='rainbow') 


###################################################################### tail 1 
st.markdown(f"##### 😎 :rainbow[{organ_t50} 민원 한눈에 보기] 👀 ") 

# 테이블 데이터
t50t1_month_df, t50t1_point_df, t50t1_kind1_df, _ = mf.load_df(organ_t50, kind1_t50) 
    
st.markdown(f"""
<center>2024년도 민원은 <b>{t50t1_kind1_df.index[0]}({t50t1_kind1_df.iloc[0,0]}건)</b> > {t50t1_kind1_df.index[1]}({t50t1_kind1_df.iloc[1,0]}건) > {t50t1_kind1_df.index[2]}({t50t1_kind1_df.iloc[2,0]}건) > {t50t1_kind1_df.index[3]}({t50t1_kind1_df.iloc[3,0]}건) > {t50t1_kind1_df.index[4]}({t50t1_kind1_df.iloc[4,0]}건) 순 입니다.</center>
""", unsafe_allow_html=True) 


t50t1_fig, _, _, _, _ = mf.create_plotly_vbar(organ_t50, kind1_t50) 
st.plotly_chart(t50t1_fig, use_container_width=True) 


# map data  
# map_t1 = mf.load_map_kind1(organ_t0, kind1_t0, base_position_t0) 

# mf.load_map_kind1(organ_t50, kind1_t50, base_position_t50) 
# st.balloons()