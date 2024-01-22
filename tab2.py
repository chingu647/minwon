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
    global map_t2  # ----------------------------------------------------------------------- 
    global organ_t2
    global kind1_t2 
    global base_position_t2

    organ_t2 = "담양지사" 
    kind1_t2 = '서비스유형(대)'
    base_position_t2 = [35.18668601, 126.87954220] 

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
    st.markdown(""" 
                <style> 
                    table{background-color:#f0f0f0;} 
                    # div{border:1px solid #00ff00;}
                    img {max-width: 900px; max-height: 600px;}    # 이미지 파일 최대크기 제한  
                
                </style> """, 
                unsafe_allow_html=True
                ) 
    
    ###################################################################### layout 
    t2h0, t2h1, t2h2 = st.columns( [0.001, 0.998, 0.001] ) 
    
    t2b0, t2b1, t2b2, t2b3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t2b4, t2b5, t2b6, t2b7 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t2b8, t2b9, t2b10,t2b11= st.columns( [0.001, 0.499, 0.499, 0.001] )

    t2t0, t2t1, t2t2 = st.columns( [0.001, 0.998, 0.001] ) 



    ###################################################################### head 1  
    t2h1.markdown(f"##### {organ_t2} : 공지사항")
    t2h1.markdown(f"""
	1. {organ_t2} 민원은 증가추세에 있습니다.
    """)



    ###################################################################### body 1  
    t2b1.markdown("##### 2024년 이슈")

    t2b1_kind1_df, _, _ = mf.load_df(organ_t2, kind1_t2) 

    t2b1.table(t2b1_kind1_df.style.background_gradient(cmap='Blues')) 



    ###################################################################### body 2 
    t2b2.markdown("##### 주요 키워드 클라우드") 

    t2b2_fig = mf.load_wc(organ_t2, kind1_t2)
    t2b2.pyplot(t2b2_fig) 



    ###################################################################### body 5 
    t2b5.markdown("##### 유형별 민원") 

    # pie 그래프 
    t2b5_pie = mf.create_pie(organ_t2, kind1_t2)
    t2b5.pyplot(t2b5_pie) 


    ###################################################################### body 6 
    t2b6.markdown("##### 유형별 민원") 

    # 가로 sns bar 그래프 
    t2b6_sns_hbar = mf.create_sns_hbar(organ_t2, kind1_t2)
    t2b6.pyplot(t2b6_sns_hbar)    
        

    ###################################################################### body 9



    ###################################################################### body 10



    ###################################################################### tail 1
    t2t1.markdown("##### 노선별 민원") 

    # 테이블 데이터
    _, t2t1_point_df, _ = mf.load_df(organ_t2, kind1_t2) 
    t2t1.dataframe(t2t1_point_df) 

    # map data  
    map_t2 = mf.load_map(organ_t2, kind1_t2, base_position_t2) 

