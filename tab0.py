import streamlit as st 
import plotly.express as px
import pandas as pd
import numpy as np 

import matplotlib as mpl 
import matplotlib.pyplot as plt 
import matplotlib.font_manager as fm 
import seaborn as sns

from streamlit_echart import st_echarts

import geopandas as gpd 
import folium 
from streamlit_folium import folium_static 
from folium.plugins import GroupedLayerControl

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

    organ_t0 = "본부" 
    kind1_t0 = 'KIND1'
    base_position_t0 = [35.18668601, 126.87954220] 

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
    st.markdown(""" 
                <style> 
                    table{background-color:#f0f0f0;} 
                    img {max-width: 1000px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
                
                </style> """, 
                unsafe_allow_html=True
                ) 
    

    # ###################################################################### layout  
    t0h0, t0h1, t0h2 = st.columns( [0.001, 0.998, 0.001] ) 
    
    t0b0, t0b1, t0b2, t0b3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t0b4, t0b5, t0b6, t0b7 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t0b8, t0b9, t0b10,t0b11= st.columns( [0.001, 0.499, 0.499, 0.001] )

    t0t0, t0t1, t0t2 = st.columns( [0.001, 0.998, 0.001] ) 
    t0t3, t0t4, t0t5 = st.columns( [0.001, 0.998, 0.001] ) 



    # # ###################################################################### head 1  
    t0h1.markdown("##### 공지사항")
    # t0h1.markdown(r"""
	# 1. 오늘의 이슈. 
    # """) 
    # # ###################################################################### body 1  
    t0b1.markdown(f"##### 📢 {organ_t0} :rainbow[민원 건 수] 현황") 

    t0b1_kind1_df, _, _ = mf.load_df(organ_t0, kind1_t0) 

    t0b1.markdown(f"""
	<center>최근 이슈는 <b>{t0b1_kind1_df.index[0]}</b> > {t0b1_kind1_df.index[1]} > {t0b1_kind1_df.index[2]} 순 입니다.</center>
    """, unsafe_allow_html=True) 

    t0b1.table(t0b1_kind1_df.style.background_gradient(cmap='Blues')) 

    options = {
        "xAxis": {
            "type": "category",
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "yAxis": {"type": "value"},
        "series": [
            {"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}
        ],
    }
    t0b1.st_echarts(options=options)





    # # ###################################################################### body 2     # wc 그래프  
    t0b2.markdown("##### 🔎 :rainbow[2024년 주요 키워드] ") 
    t0b2_fig = mf.load_wc(organ_t0, kind1_t0) 

    t0b2.markdown(f"""
	<center>주요 키워드는 <b>{organ_t0}</b> 입니다.</center>
    """, unsafe_allow_html=True)

    t0b2.pyplot(t0b2_fig, use_container_width=True)   


    ###################################################################### body 5     # pie 그래프 
    t0b5.markdown("##### 📚 :rainbow[2024년 유형별] ") 

    t0b5.markdown(f"""
	<center>주요 민원유형은 <b>{organ_t0}</b> 입니다.</center>
    """, unsafe_allow_html=True)

    t0b5_pie = mf.create_pie(organ_t0, kind1_t0)
    t0b5.pyplot(t0b5_pie, use_container_width=True)  


    # # ###################################################################### body 6 
    t0b6.markdown("##### 🚔 :rainbow[2024년 지사별] ") 

    # # pie 그래프 
    # t0b6_pie = mf.create_pie(organ_t0, kind1_t0) 
    # t0b6.pyplot(t0b6_pie)


    # # ###################################################################### body 9
    t0b9.markdown("##### 🚌 :rainbow[2024년 노선별] ") 

    t0b9.markdown(f"""
	<center>최다 민원노선은 <b>{organ_t0}</b> 입니다.</center>
    """, unsafe_allow_html=True)
    
    # 가로 sns bar 그래프 
    t0b9_sns_hbar = mf.create_sns_hbar(organ_t0, kind1_t0) 
    t0b9.pyplot(t0b9_sns_hbar)


    ###################################################################### body 10



    ###################################################################### tail 1 
    t0t1.markdown(f"##### 😎 :rainbow[{organ_t0} 민원 한눈에 보기] 👀 ") 

    # 테이블 데이터
    t0t1_kind1_df, t0t1_point_df, _ = mf.load_df(organ_t0, kind1_t0) 
    t0t1.dataframe(t0t1_point_df) 

    # map data  
    # map_t1 = mf.load_map_kind1(organ_t0, kind1_t0, base_position_t0) 

    mf.load_map_kind1(organ_t0, kind1_t0, base_position_t0) 

