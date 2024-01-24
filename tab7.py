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

import nltk 
from konlpy.tag import Kkma, Hannanum, Twitter, Okt
from wordcloud import WordCloud, STOPWORDS 

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-1) ST CACHE 사용
import mf 

def run_tab(): 
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ global 변수 설정
    global map_t7  # ----------------------------------------------------------------------- 
    global organ_t7
    global kind1_t7 
    global base_position_t7

    organ_t7 = "남원지사" 
    kind1_t7 = '서비스유형(대)'
    base_position_t7 = [35.18668601, 126.87954220] 

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
    st.markdown(""" 
                <style> 
                    table{background-color:#f0f0f0;} 
                    img {max-width: 1000px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
                
                </style> """, 
                unsafe_allow_html=True
                ) 
        
    ###################################################################### layout 
    # t7h0, t7h1, t7h2 = st.columns( [0.001, 0.998, 0.001] ) 
    
    t7b0, t7b1, t7b2, t7b3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t7b4, t7b5, t7b6, t7b7 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t7b8, t7b9, t7b10,t7b11= st.columns( [0.001, 0.499, 0.499, 0.001] )

    t7t0, t7t1, t7t2 = st.columns( [0.001, 0.998, 0.001] ) 


    ###################################################################### head 1  


    ###################################################################### body 1  
    t7b1.markdown(f"##### 📢 :rainbow[2024년 주요 이슈] ") 

    t7b1.markdown(f"""
	<center>최근 이슈</font>는 <font color='red'>{organ_t7}</font> 입니다.</center>
    """, unsafe_allow_html=True)

    t1b1_kind1_df, _, _ = mf.load_df(organ_t7, kind1_t7) 

    t7b1.table(t1b1_kind1_df.style.background_gradient(cmap='Blues')) 



    ###################################################################### body 2     # wc 그래프  
    t7b2.markdown("##### 🔎 :rainbow[주요 키워드 클라우드] ") 

    t7b2.markdown(f"""
	<center>주요 키워드</font>는 <font color='red'>{organ_t7}</font> 입니다.</center>
    """, unsafe_allow_html=True)

    t7b2_fig = mf.load_wc(organ_t7, kind1_t7)
    t7b2.pyplot(t7b2_fig, use_container_width=True)    


    ###################################################################### body 5     # pie 그래프 
    t7b5.markdown("##### 📚 :rainbow[유형별 민원] ") 

    t7b5.markdown(f"""
	<center>주요 민원유형</font>은 <font color='red'>{organ_t7}</font> 입니다.</center>
    """, unsafe_allow_html=True)

    t7b5_pie = mf.create_pie(organ_t7, kind1_t7)
    t7b5.pyplot(t7b5_pie, use_container_width=True)    


    ###################################################################### body 6     # 가로 sns bar 그래프 
    t7b6.markdown("##### 🚌 :rainbow[노선별 민원] ") 

    t7b6.markdown(f"""
	<center>최다 민원노선</font>은 <font color='red'>{organ_t7}</font> 입니다.</center>
    """, unsafe_allow_html=True) 

    t7b6_sns_hbar = mf.create_sns_hbar(organ_t7, kind1_t7)
    t7b6.pyplot(t7b6_sns_hbar, use_container_width=True)    
        

    ###################################################################### body 9



    ###################################################################### body 10



    ###################################################################### tail 1
    t7t1.markdown("##### 😎 :rainbow[민원 위치 한눈에 보기] 👀 ") 

    # 테이블 데이터
    _, t7t1_point_df, _ = mf.load_df(organ_t7, kind1_t7) 
    t7t1.dataframe(t7t1_point_df) 

    # map data  
    mf.load_map_kind1(organ_t7, kind1_t7, base_position_t7) 

