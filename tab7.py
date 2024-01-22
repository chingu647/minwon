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
                    img {max-width: 900px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
                
                </style> """, 
                unsafe_allow_html=True
                ) 
    
    ###################################################################### layout 
    t7h0, t7h1, t7h2 = st.columns( [0.001, 0.998, 0.001] ) 
    
    t1b0, t1b1, t1b2, t1b3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t1b4, t1b5, t1b6, t1b7 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t1b8, t1b9, t1b10,t1b11= st.columns( [0.001, 0.499, 0.499, 0.001] )

    t7t0, t7t1, t7t2 = st.columns( [0.001, 0.998, 0.001] ) 



    ###################################################################### head 1  
    t7h1.markdown(f"##### {organ_t7} : 공지사항")
    t7h1.markdown(f"""
	1. {organ_t7} 민원은 증가추세에 있습니다.
    """)



    ###################################################################### body 1  
    t1b1.markdown("##### 2024년 이슈")

    t1b1_kind1_df, _, _ = mf.load_df(organ_t7, kind1_t7) 

    t1b1.table(t1b1_kind1_df.style.background_gradient(cmap='Blues')) 



    ###################################################################### body 2 
    t1b2.markdown("##### 주요 키워드 클라우드") 

    t1b2_fig = mf.load_wc(organ_t7, kind1_t7)
    t1b2.pyplot(t1b2_fig) 



    ###################################################################### body 5 
    t1b5.markdown("##### 유형별 민원") 

    # pie 그래프 
    t1b5_pie = mf.create_pie(organ_t7, kind1_t7)
    t1b5.pyplot(t1b5_pie) 


    ###################################################################### body 6 
    t1b6.markdown("##### 유형별 민원") 

    # 가로 sns bar 그래프 
    t1b6_sns_hbar = mf.create_sns_hbar(organ_t7, kind1_t7)
    t1b6.pyplot(t1b6_sns_hbar)    
        

    ###################################################################### body 9



    ###################################################################### body 10



    ###################################################################### tail 1
    t7t1.markdown("##### 노선별 민원") 

    # 테이블 데이터
    _, t7t1_point_df, _ = mf.load_df(organ_t7, kind1_t7) 
    t7t1.dataframe(t7t1_point_df) 

    # map data  
    map_t7 = mf.load_map(organ_t7, kind1_t7, base_position_t7) 

