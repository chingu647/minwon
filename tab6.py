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
    global map_t6  # ----------------------------------------------------------------------- 
    global organ_t6
    global kind1_t6 
    global base_position_t6

    organ_t6 = "보성지사" 
    kind1_t6 = '서비스유형(대)'
    base_position_t6 = [35.18668601, 126.87954220] 

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
    st.markdown(""" 
                <style> 
                    table{background-color:#f0f0f0;} 
                    img {max-width: 900px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
                
                </style> """, 
                unsafe_allow_html=True
                ) 
    
    ###################################################################### layout 
    t6h0, t6h1, t6h2 = st.columns( [0.001, 0.998, 0.001] ) 
    
    t6b0, t6b1, t6b2, t6b3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t6b4, t6b5, t6b6, t6b7 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t6b8, t6b9, t6b10,t6b11= st.columns( [0.001, 0.499, 0.499, 0.001] )

    t6t0, t6t1, t6t2 = st.columns( [0.001, 0.998, 0.001] ) 



    ###################################################################### head 1  
    t6h1.markdown(f"##### {organ_t6} : 공지사항")
    t6h1.markdown(f"""
	1. {organ_t6} 민원은 증가추세에 있습니다.
    """)



    ###################################################################### body 1  
    t6b1.markdown("##### 2024년 이슈")

    t6b1_kind1_df, _, _ = mf.load_df(organ_t6, kind1_t6) 

    t6b1.table(t6b1_kind1_df.style.background_gradient(cmap='Blues')) 



    ###################################################################### body 2 
    t6b2.markdown("##### 주요 키워드 클라우드") 

    t6b2_fig = mf.load_wc(organ_t6, kind1_t6) 
    t6b2.pyplot(t6b2_fig) 



    ###################################################################### body 5 
    t6b5.markdown("##### 유형별 민원") 

    # pie 그래프 
    t6b5_pie = mf.create_pie(organ_t6, kind1_t6)
    t6b5.pyplot(t6b5_pie) 


    ###################################################################### body 6 
    t6b6.markdown("##### 유형별 민원") 

    # 가로 sns bar 그래프 
    t6b6_sns_hbar = mf.create_sns_hbar(organ_t6, kind1_t6)
    t6b6.pyplot(t6b6_sns_hbar)    
        

    ###################################################################### body 9



    ###################################################################### body 10



    ###################################################################### tail 1
    t6t1.markdown("##### 노선별 민원") 

    # 테이블 데이터
    _, t6t1_point_df, _ = mf.load_df(organ_t6, kind1_t6) 
    t6t1.dataframe(t6t1_point_df) 

    # map data  
    map_t6 = mf.load_map(organ_t6, kind1_t6, base_position_t6) 

