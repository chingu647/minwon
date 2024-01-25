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
    global map_t5  # ----------------------------------------------------------------------- 
    global organ_t5
    global kind1_t5 
    global base_position_t5

    organ_t5 = "구례지사" 
    kind1_t5 = '서비스유형(대)'
    base_position_t5 = [35.18668601, 126.87954220] 

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
    st.markdown(""" 
                <style> 
                    table{background-color:#f0f0f0;} 
                    img {max-width: 1000px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
                
                </style> """, 
                unsafe_allow_html=True
                ) 
        
    ###################################################################### layout 
    # t5h0, t5h1, t5h2 = st.columns( [0.001, 0.998, 0.001] ) 
    
    t5b0, t5b1, t5b2, t5b3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t5b4, t5b5, t5b6, t5b7 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t5b8, t5b9, t5b10,t5b11= st.columns( [0.001, 0.499, 0.499, 0.001] )

    t5t0, t5t1, t5t2 = st.columns( [0.001, 0.998, 0.001] ) 


    ###################################################################### head 1  
 

    ###################################################################### body 1  
    t5b1.markdown(f"##### 📢 :rainbow[2024년 {organ_t5} 이슈] ") 

    t5b1_kind1_df, _, _ = mf.load_df(organ_t5, kind1_t5) 

    t5b1.markdown(f"""
	<center>최근 이슈는 <b>{t5b1_kind1_df.index[0]}</b> > {t5b1_kind1_df.index[1]} > {t5b1_kind1_df.index[2]} 순 입니다.</center>
    """, unsafe_allow_html=True) 

    t5b1.table(t5b1_kind1_df.style.background_gradient(cmap='Blues')) 


    ###################################################################### body 2     # wc 그래프  
    t5b2.markdown("##### 🔎 :rainbow[주요 키워드 클라우드] ") 

    t5b2.markdown(f"""
	<center>주요 키워드는 {organ_t5} 입니다.</center>
    """, unsafe_allow_html=True)

    t5b2_fig = mf.load_wc(organ_t5, kind1_t5)
    t5b2.pyplot(t5b2_fig, use_container_width=True)    


    ###################################################################### body 5     # pie 그래프 
    t5b5.markdown("##### 📚 :rainbow[유형별 민원] ") 

    t5b5.markdown(f"""
	<center>주요 민원유형은 {organ_t5} 입니다.</center>
    """, unsafe_allow_html=True)

    t5b5_pie = mf.create_pie(organ_t5, kind1_t5)
    t5b5.pyplot(t5b5_pie, use_container_width=True)    


    ###################################################################### body 6     # 가로 sns bar 그래프 
    t5b6.markdown("##### 🚌 :rainbow[노선별 민원] ") 

    t5b6.markdown(f"""
	<center>최다 민원노선은 {organ_t5} 입니다.</center>
    """, unsafe_allow_html=True)

    t5b6_sns_hbar = mf.create_sns_hbar(organ_t5, kind1_t5)
    t5b6.pyplot(t5b6_sns_hbar, use_container_width=True)      
        

    ###################################################################### body 9



    ###################################################################### body 10



    ###################################################################### tail 1
    t5t1.markdown(f"##### 😎 :rainbow[{organ_t5} 민원 한눈에 보기] 👀 ") 

    # 테이블 데이터
    _, t5t1_point_df, _ = mf.load_df(organ_t5, kind1_t5) 
    t5t1.dataframe(t5t1_point_df) 

    # map data  
    mf.load_map_kind1(organ_t5, kind1_t5, base_position_t5) 

