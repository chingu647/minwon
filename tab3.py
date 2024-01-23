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
    global map_t3  # ----------------------------------------------------------------------- 
    global organ_t3
    global kind1_t3 
    global base_position_t3

    organ_t3 = "순천지사" 
    kind1_t3 = '서비스유형(대)'
    base_position_t3 = [35.18668601, 126.87954220] 

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
    st.markdown(""" 
                <style> 
                    table{background-color:#f0f0f0;} 
                    img {max-width: 1000px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
                
                </style> """, 
                unsafe_allow_html=True
                ) 
    

    ###################################################################### layout 
    t3h0, t3h1, t3h2 = st.columns( [0.001, 0.998, 0.001] ) 
    
    t3b0, t3b1, t3b2, t3b3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t3b4, t3b5, t3b6, t3b7 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t3b8, t3b9, t3b10,t3b11= st.columns( [0.001, 0.499, 0.499, 0.001] )

    t3t0, t3t1, t3t2 = st.columns( [0.001, 0.998, 0.001] ) 



    ###################################################################### head 1  
    t3h1.markdown(f"##### {organ_t3} : 공지사항")
    t3h1.markdown(f"""
	1. {organ_t3} 민원은 증가추세에 있습니다.
    """)



    ###################################################################### body 1  
    t3b1.markdown("##### 2024년 이슈")

    t3b1_kind1_df, _, _ = mf.load_df(organ_t3, kind1_t3) 

    t3b1.table(t3b1_kind1_df.style.background_gradient(cmap='Blues')) 



    ###################################################################### body 2     # wc 그래프  
    t3b2.markdown("##### 주요 키워드 클라우드") 

    t3b2_fig = mf.load_wc(organ_t3, kind1_t3)
    t3b2.pyplot(t3b2_fig, use_container_width=True)     



    ###################################################################### body 5     # pie 그래프 
    t3b5.markdown("##### 유형별 민원") 


    t3b5_pie = mf.create_pie(organ_t3, kind1_t3)
    t3b5.pyplot(t3b5_pie, use_container_width=True)    


    ###################################################################### body 6     # 가로 sns bar 그래프 
    t3b6.markdown("##### 유형별 민원") 


    t3b6_sns_hbar = mf.create_sns_hbar(organ_t3, kind1_t3)
    t3b6.pyplot(t3b6_sns_hbar, use_container_width=True)      
        

    ###################################################################### body 9



    ###################################################################### body 10



    ###################################################################### tail 1

    t3t1.markdown("##### 노선별 민원") 

    # 테이블 데이터
    _, t3t1_point_df, _ = mf.load_df(organ_t3, kind1_t3) 
    t3t1.dataframe(t3t1_point_df) 

    # map data  
    map_t3 = mf.load_map(organ_t3, kind1_t3, base_position_t3) 

