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
    global map_t1  # ----------------------------------------------------------------------- 
    global organ_t1
    global kind1_t1 
    global base_position_t1

    organ_t1 = "광주지사" 
    kind1_t1 = '서비스유형(대)'
    base_position_t1 = [35.18668601, 126.87954220] 

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
    st.markdown(""" 
                <style> 
                    table{background-color:#f0f0f0;} 
                    img {max-width: 1000px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
                
                </style> """, 
                unsafe_allow_html=True
                ) 
    
    
    ###################################################################### layout 
    t1h0, t1h1, t1h2 = st.columns( [0.001, 0.998, 0.001] ) 
    
    t1b0, t1b1, t1b2, t1b3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t1b4, t1b5, t1b6, t1b7 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t1b8, t1b9, t1b10,t1b11= st.columns( [0.001, 0.499, 0.499, 0.001] )

    t1t0, t1t1, t1t2 = st.columns( [0.001, 0.998, 0.001] ) 



    ###################################################################### head 1  
    t1h1.markdown(f"##### {organ_t1} : 공지사항")
    t1h1.markdown(r"""
	1. 광주지사 민원은 증가추세에 있습니다.
    """)



    ###################################################################### body 1  
    t1b1.markdown("##### 2024년 이슈")

    t1b1_kind1_df, _, _ = mf.load_df(organ_t1, kind1_t1) 

    t1b1.table(t1b1_kind1_df.style.background_gradient(cmap='Blues')) 



    ###################################################################### body 2     # wc 그래프  
    t1b2.markdown("##### 주요 키워드 클라우드") 

    t1b2_fig = mf.load_wc(organ_t1, kind1_t1)
    t1b2.pyplot(t1b2_fig, use_container_width=True)    



    ###################################################################### body 5     # pie 그래프 
    t1b5.markdown("##### 유형별 민원") 


    t1b5_pie = mf.create_pie(organ_t1, kind1_t1)
    t1b5.pyplot(t1b5_pie, use_container_width=True)    


    ###################################################################### body 6     # 가로 sns bar 그래프 
    t1b6.markdown("##### 유형별 민원") 


    t1b6_sns_hbar = mf.create_sns_hbar(organ_t1, kind1_t1)
    t1b6.pyplot(t1b6_sns_hbar, use_container_width=True)     
        

    ###################################################################### body 9



    ###################################################################### body 10



    ###################################################################### tail 1
    t1t1.markdown("##### 노선별 민원") 

    # 테이블 데이터
    _, t1t1_point_df, _ = mf.load_df(organ_t1, kind1_t1) 
    t1t1.dataframe(t1t1_point_df) 

    # map data  
    map_t1 = mf.load_map(organ_t1, kind1_t1, base_position_t1) 

