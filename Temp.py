import streamlit as st 
import plotly.express as px
import plotly.graph_objects as go 
import plotly.figure_factory as ff 
from plotly.subplots import make_subplots

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

from time import localtime, strftime 

import mf 

def run_tab(): 
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ global 변수 설정
    global map_t0  # ----------------------------------------------------------------------- 
    global organ
    global kind1 
    global base_position 

    organ = "ALL"   # ALL 광주전남본부 광주지사 담양지사 순천지사 함평지사 구례지사 보성지사 남원지사 
    kind1 = 'KIND1' # ----------------------------------------------------------------------
    team  = 'TEAM'  # ----------------------------------------------------------------------
    road  = 'ROAD'  # ----------------------------------------------------------------------
    base_position = [35.18668601, 126.87954220] 

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
    st.markdown(""" 
                <style> 
                    table{background-color:#f0f0f0;} 
                    img {max-width: 1000px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
                
                </style> """, 
                unsafe_allow_html=True
                )     

    # # ################################################# 민원 건수 현황 
    cont0 = st.container(border=False)
    # cont0.markdown(f"##### 📢 :rainbow[{organ}  민원 분석]") 

    tabs = st.tabs(['📈월별 추이', '📚유형별', '🚔부서별', '🚌노선별', '💾데이터']) 
    with tabs[0]: # 월별
        # 
        # tabs[0].dataframe(df0_0)
        # tabs[0].dataframe(df0_1)
        # tabs[0].dataframe(df0_2)
        # tabs[0].dataframe(df0_2_temp)
        # tabs[0].write(df0_3) 
        # cont0.markdown(f"##### 📢 :rainbow[{organ}  민원 분석]")        
         
        fig0_0, df0_0, df0_1, df0_2, df0_3 = mf.create_px_bar_month(organ, kind1) 
        df0_0_temp = df0_0.sort_values(by='NUMBER', ascending=False) 

        tabs[0].write(f"📢 민원 건수는 <strong>총 { df0_0_temp[ 'NUMBER' ].sum() } 건</strong> 이며, 최다 발생 기간은 <strong>{ df0_0_temp.iloc[0][ 'DATE' ].strftime('%Y') }년  { df0_0_temp.iloc[0][ 'DATE' ].strftime('%m') }월</strong> <strong>( { df0_0_temp.iloc[0][ 'NUMBER' ] } 건 )</strong> 입니다.       , ", unsafe_allow_html=True) 
        tabs[0].plotly_chart(fig0_0, use_container_width=True) 


    with tabs[1]: # 유형별 
        fig1_0, df1_0, df1_1, df1_2, df1_3 = mf.create_px_pie_kind1(organ, kind1) 
        df1_2_temp = df1_2.sort_values(by='NUMBER', ascending=False) 
        tabs[1].write(f"📚 최다 유형은 <strong>{ df1_2_temp.iloc[0][ f'{kind1}' ] }</strong> 관련으로, " +
                      f"<strong>총 { df1_2_temp.iloc[0][ 'NUMBER' ] } 건 ({ df1_2_temp.iloc[0][ f'NUMBER_pct' ] } %)</strong> 입니다.       , ", unsafe_allow_html=True) 
        # tabs[1].write(f"최다 민원은 <strong>{ df1_2.iloc[0][ f'{kind1}' ] }</strong> 관련으로, <strong>총 { df1_2.iloc[0][ 'NUMBER' ] } 건 ({ df1_2.iloc[0][ f'NUMBER_pct' ] } %)</strong> 입니다.       , ", unsafe_allow_html=True) 
        tabs[1].plotly_chart(fig1_0, use_container_width=True) 

        # fig0_1, _, _, _, _ = mf.create_px_bar(organ, kind1) 
        # tabs[1].plotly_chart(fig0_1, use_container_width=True) 


    with tabs[2]: # 팀별
        fig2_0, df2_0, df2_1, df2_2, df2_3 = mf.create_px_bar_kind1(organ, team) 
        df2_2_temp = df2_2.sort_values(by='NUMBER', ascending=False) 
        tabs[2].write(f"📚 최다 처리 팀은 <strong>{ df2_2_temp.iloc[0][ f'{team}' ] }</strong> 으로, " +
                      f"<strong>총 { df2_2_temp.iloc[0][ 'NUMBER' ] } 건 ({ df2_2_temp.iloc[0][ f'NUMBER_pct' ] } %)</strong> 입니다.       , ", unsafe_allow_html=True) 
        tabs[2].plotly_chart(fig2_0, use_container_width=True) 


    with tabs[3]: # 노선별
        fig3_0, df3_0, df3_1, df3_2, df3_3 = mf.create_px_scatter_kind1(organ, road) 
        df3_2_temp = df3_2.sort_values(by='NUMBER', ascending=False) 
        tabs[3].write(f"📢 최다 노선은 <strong>{ df3_2_temp.iloc[0][ f'{road}' ] }</strong> 으로, " + 
                      f"<strong>총 { df3_2_temp.iloc[0][ 'NUMBER' ] } 건 ({ df3_2_temp.iloc[0][ f'NUMBER_pct' ] } %)</strong> 입니다.       , ", unsafe_allow_html=True) 
        tabs[3].plotly_chart(fig3_0, use_container_width=True) 



    with tabs[4]: # 데이터
        df4_0, df4_1, df4_2, df4_3 = mf.load_df(organ, kind1)  
        df4_2_temp = df3_2.sort_values(by='NUMBER', ascending=False) 
        tabs[4].dataframe(df4_2_temp.style.background_gradient(cmap='Blues'), use_container_width=True) 


    # ################################################# 민원 지도 보기 
    cont9 = st.container(border=False)
    cont9.markdown(f"##### 😎 {organ} 민원 :rainbow[노선별로 한눈에 보기] 👀") 

    tabs = st.tabs(['🌍 지 도', '🔎키워드', '💾데이터']) 
    with tabs[0]: 
        pass 
        # 테이블 데이터
        df9_0, df9_1, df9_2, df9_3  = mf.load_df(organ, kind1) 

        # map data  
        map_t1 = mf.load_map(organ, kind1, base_position) 
        # mf.load_map_kind1(organ, kind1, base_position) 

    with tabs[1]: 
        fig9_0, df9_0, df9_1, df9_2, df9_3 = mf.load_wc(organ, road) 
        # df9_2_temp = df9_2.sort_values(by='NUMBER', ascending=False) 
        # tabs[1].write(f"📢 최다 노선은 <strong>{ df3_2_temp.iloc[0][ f'{road}' ] }</strong> 으로, " + 
        #               f"<strong>총 { df3_2_temp.iloc[0][ 'NUMBER' ] } 건 ({ df3_2_temp.iloc[0][ f'NUMBER_pct' ] } %)</strong> 입니다.       , ", unsafe_allow_html=True) 
        tabs[1].pyplot(fig9_0, use_container_width=True)  

    with tabs[2]: 
    #     # df1_0.columns = ['민원 유형', '발생 건수', '백분율 (%)']         
    #     # cont9.dataframe(df9_1) 
        tabs[2].dataframe(df9_1, use_container_width=True) 
        # tabs[1].dataframe(df9_0) #.style.background_gradient(cmap='Blues'), use_container_width=True) 
  





    # tabs = st.tabs(['📊 차트', '📈 그래프', ' 🚩🌍데이터'])     
    # with tabs[0]: 
    #     fig1, df1  = mf.create_px_pie(organ, kind1)
    #     tabs[0].plotly_chart(fig1, use_container_width=True) 
