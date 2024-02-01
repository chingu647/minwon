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
    global ta_map  # ----------------------------------------------------------------------- 
    global ta_organ 
    global ta_kind1  
    global ta_kind2  
    global ta_team  
    global ta_road 
    global ta_mapchoice 
    global ta_base_position 
    global ta_keyword 

    ta_organ = "ALL"   # ALL 광주전남본부 광주지사 담양지사 순천지사 함평지사 구례지사 보성지사 남원지사 
    # choice 종류
    ta_kind1 = 'KIND1' # ----------------------------------------------------------------------
    ta_kind2 = 'KIND2' # ----------------------------------------------------------------------
    ta_team  = 'TEAM'  # ----------------------------------------------------------------------
    ta_road  = 'ROAD'  # ---------------------------------------------------------------------- 
    ta_mapchoice  = 'KIND1'  # ---------------------------------------------------------------- 
    ta_base_position = [35.18668601, 126.87954220] 
    ta_keyword = 'KEYWORD' 

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
    st.markdown(""" 
                <style> 
                    table{background-color:#f0f0f0;} 
                    img {max-width: 1000px; max-height: 600px; }       
                </style> 
                """, unsafe_allow_html=True )     

    # # ################################################# 민원 건수 현황 
    ta_cont0 = st.container(border=False)
    # ta_cont0.markdown(f"##### 📢 :rainbow[{ta_organ}  민원 분석]") 

    tabs = st.tabs(['📈월별 추이', '📚유형별', '🚔부서별', '🚌노선별', '💾데이터']) 
    with tabs[0]: # 월별
        # 
        # tabs[0].dataframe(df0_0)
        # tabs[0].dataframe(df0_1)
        # tabs[0].dataframe(df0_2)
        # tabs[0].dataframe(df0_2_temp)
        # tabs[0].write(df0_3) 
        # cont0.markdown(f"##### 📢 :rainbow[{ta_organ}  민원 분석]")        
         
        ta_fig0_0, ta_df0_0, ta_df0_1, ta_df0_2, ta_wc0 = mf.create_px_bar_month(ta_organ, ta_kind1) 
        ta_df0_0_temp = ta_df0_0.sort_values(by='NUMBER', ascending=False) 

        tabs[0].write(f"📢 민원 건수는 <strong>총 { ta_df0_0_temp[ 'NUMBER' ].sum() } 건</strong> 이며, " +
                      f"최다 발생 기간은 <strong>{ ta_df0_0_temp.iloc[0][ 'DATE' ].strftime('%Y') }년 " +
                      f"{ ta_df0_0_temp.iloc[0][ 'DATE' ].strftime('%m') }월</strong> <strong>( { ta_df0_0_temp.iloc[0][ 'NUMBER' ] } 건 )</strong> 입니다.", unsafe_allow_html=True) 
        tabs[0].plotly_chart(ta_fig0_0, use_container_width=True) 


    with tabs[1]: # 유형별 
        ta_fig1_0, ta_df1_0, ta_df1_1, ta_df1_2, ta_wc1 = mf.create_px_pie_kind1(ta_organ, ta_kind1) 
        ta_df1_2_temp = ta_df1_2.sort_values(by='NUMBER', ascending=False) 
        tabs[1].write(f"📚 최다 유형은 <strong>{ ta_df1_2_temp.iloc[0][ f'{ta_kind1}' ] }</strong> 관련으로, " +
                      f"<strong>총 { ta_df1_2_temp.iloc[0][ 'NUMBER' ] } 건 ({ ta_df1_2_temp.iloc[0][ f'NUMBER_pct' ] } %)</strong> 입니다. ", unsafe_allow_html=True) 
        tabs[1].plotly_chart(ta_fig1_0, use_container_width=True) 


    with tabs[2]: # 팀별
        ta_fig2_0, ta_df2_0, ta_df2_1,ta_df2_2, ta_wc2 = mf.create_px_bar_team(ta_organ, ta_team) 
        ta_df2_2_temp = ta_df2_2.sort_values(by='NUMBER', ascending=False) 
        tabs[2].write(f"📚 최다 처리 팀은 <strong>{ ta_df2_2_temp.iloc[0][ f'{ta_team}' ] }</strong> 으로, " +
                      f"<strong>총 { ta_df2_2_temp.iloc[0][ 'NUMBER' ] } 건 ({ ta_df2_2_temp.iloc[0][ f'NUMBER_pct' ] } %)</strong> 입니다.", unsafe_allow_html=True) 
        tabs[2].plotly_chart(ta_fig2_0, use_container_width=True) 


    with tabs[3]: # 노선별
        ta_fig3_0, ta_df3_0, ta_df3_1, ta_df3_2, ta_wc3 = mf.create_px_scatter_road(ta_organ, ta_road) 
        ta_df3_2_temp = ta_df3_2.sort_values(by='NUMBER', ascending=False) 
        tabs[3].write(f"📢 최다 노선은 <strong>{ ta_df3_2_temp.iloc[0][ f'{ta_road}' ] }</strong> 으로, " + 
                      f"<strong>총 { ta_df3_2_temp.iloc[0][ 'NUMBER' ] } 건 ({ ta_df3_2_temp.iloc[0][ f'NUMBER_pct' ] } %)</strong> 입니다. ", unsafe_allow_html=True) 
        tabs[3].plotly_chart(ta_fig3_0, use_container_width=True) 


    with tabs[4]: # 데이터
        ta_df4_0, ta_df4_1, ta_df4_2, ta_wc4 = mf.load_df(ta_organ, ta_road)  
        ta_df4_2_temp = ta_df4_2.sort_values(by='NUMBER', ascending=False) 
        tabs[4].dataframe(ta_df4_2_temp.style.background_gradient(cmap='Blues'), use_container_width=True) 


    # ################################################# 민원 지도 보기 
    ta_cont9 = st.container(border=False)
    ta_cont9.markdown(f"##### 😎 {ta_organ} 민원 :rainbow[노선별로 한눈에 보기] 👀") 

    tabs = st.tabs(['🌍 지 도', '🔎키워드', '💾데이터']) 
    with tabs[0]: 
        mf.load_map_choice(ta_base_position, ta_organ, ta_mapchoice) 

    with tabs[1]: 
        ta_fig9_0, ta_df9_0, ta_df9_1, ta_df9_2, ta_wc9 = mf.load_wc(ta_organ, ta_keyword) 
        tabs[1].pyplot(ta_fig9_0, use_container_width=True) 

    with tabs[2]: 
        tabs[2].dataframe(ta_df9_1, use_container_width=True) 
  
