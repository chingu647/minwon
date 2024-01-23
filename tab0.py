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
    global map_t0  # ----------------------------------------------------------------------- 
    global organ_t0
    global kind1_t0 
    global base_position_t0 

    organ_t0 = "광주지사" 
    kind1_t0 = '서비스유형(대)'
    base_position_t0 = [35.18668601, 126.87954220] 

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
    # st.markdown(""" 
    #             <style> 
    #                 table{background-color:#f0f0f0;} 
    #                 img {max-width: 900px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
                
    #             </style> """, 
    #             unsafe_allow_html=True
    #             ) 
    


    # ###################################################################### layout 
    t0h0, t0h1, t0h2 = st.columns( [0.001, 0.998, 0.001] ) 
    
    t0b0, t0b1, t0b2, t0b3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t0b4, t0b5, t0b6, t0b7 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t0b8, t0b9, t0b10,t0b11= st.columns( [0.001, 0.499, 0.499, 0.001] )

    t0t0, t0t1, t0t2 = st.columns( [0.001, 0.998, 0.001] ) 



    # ###################################################################### head 1  
    t0h1.markdown("##### 공지사항")
    t0h1.markdown(r"""
	1. 오늘의 이슈. 
    """) 


    # ###################################################################### body 1  
    t0b1.markdown("##### 2024년 이달의 이슈")
    t0b1.markdown(r"""
	1. 오늘의 이슈.
    """) 


    # ###################################################################### body 2 

    t0b2.markdown("##### 주요 키워드 클라우드") 

    t0b2_fig = mf.load_wc(organ_t0, kind1_t0)
    t0b2.pyplot(t0b2_fig)


    # ###################################################################### body 5 
    t0b5.markdown("##### 지사별 민원") 

    # pie 그래프 
    t0b5_pie = mf.create_pie(organ_t0, kind1_t0) 
    t0b5.pyplot(t0b5_pie)


    # ###################################################################### body 6
    t0b6.markdown("##### 유형별 민원") 
    
    # 가로 sns bar 그래프 
    t0b6_sns_hbar = mf.create_sns_hbar(organ_t0, kind1_t0) 
    t0b6.pyplot(t0b6_sns_hbar)
