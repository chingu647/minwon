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
    # 
    global t6_map  # ----------------------------------------------------------------------- 
    global t6_organ
    global t6_kind1 
    global t6_kind2 
    global t6_team 
    global t6_road 
    global t6_mapchoice  
    global t6_base_position 
    global t6_keyword 
    t6_organ = "보성지사"   # ALL 광주전남본부 광주지사 담양지사 순천지사 함평지사 구례지사 보성지사 남원지사 
    # choice 종류
    t6_kind1 = 'KIND1' # ----------------------------------------------------------------------
    t6_kind2 = 'KIND2' # ----------------------------------------------------------------------
    t6_team  = 'TEAM'  # ----------------------------------------------------------------------
    t6_road  = 'ROAD'  # ---------------------------------------------------------------------- 
    t6_mapchoice = 'KIND1'
    t6_base_position = [35.18668601, 126.87954220] 
    # word cloud 
    t6_keyword = 'KEYWORD'
    # 
    st.markdown(""" 
                <style> 
                    table{background-color:#f0f0f0;} 
                    img {max-width: 1000px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
                
                </style> """, 
                unsafe_allow_html=True
                )     
    # 
    t6_cont0 = st.container(border=False)

    tabs = st.tabs(['📈월별 추이', '📚유형별', '🚔부서별', '🚌노선별', '💾데이터']) 
    with tabs[0]: # 월별

         
        t6_fig0_0, t6_df0_0, t6_df0_1, t6_df0_2, t6_wc0 = mf.create_px_bar_month(t6_organ, t6_kind1) 
        t6_df0_0_temp = t6_df0_0.sort_values(by='NUMBER', ascending=False) 

        tabs[0].write(f"📢 민원 건수는 <strong>총 { t6_df0_0_temp[ 'NUMBER' ].sum() } 건</strong> 이며, " +
                      f"최다 발생 기간은 <strong>{ t6_df0_0_temp.iloc[0][ 'DATE' ].strftime('%Y') }년 " +
                      f"{ t6_df0_0_temp.iloc[0][ 'DATE' ].strftime('%m') }월</strong> <strong>( { t6_df0_0_temp.iloc[0][ 'NUMBER' ] } 건 )</strong> 입니다. ", unsafe_allow_html=True) 
        tabs[0].plotly_chart(t6_fig0_0, use_container_width=True) 


    with tabs[1]: # 유형별 
        t6_fig1_0, t6_df1_0, t6_df1_1, t6_df1_2, t6_wc1 = mf.create_px_pie_kind1(t6_organ, t6_kind1) 
        t6_df1_2_temp = t6_df1_2.sort_values(by='NUMBER', ascending=False) 
        tabs[1].write(f"📚 최다 유형은 <strong>{ t6_df1_2_temp.iloc[0][ f'{t6_kind1}' ] }</strong> 관련으로, " +
                      f"<strong>총 { t6_df1_2_temp.iloc[0][ 'NUMBER' ] } 건 ({ t6_df1_2_temp.iloc[0][ f'NUMBER_pct' ] } %)</strong> 입니다. ", unsafe_allow_html=True) 
        tabs[1].plotly_chart(t6_fig1_0, use_container_width=True) 


    with tabs[2]: # 팀별
        t6_fig2_0, t6_df2_0, t6_df2_1, t6_df2_2, t6_wc2 = mf.create_px_bar_team(t6_organ, t6_team) 
        t6_df2_2_temp = t6_df2_2.sort_values(by='NUMBER', ascending=False) 
        tabs[2].write(f"📚 최다 처리 팀은 <strong>{ t6_df2_2_temp.iloc[0][ f'{t6_team}' ] }</strong> 으로, " +
                      f"<strong>총 { t6_df2_2_temp.iloc[0][ 'NUMBER' ] } 건 ({ t6_df2_2_temp.iloc[0][ f'NUMBER_pct' ] } %)</strong> 입니다. ", unsafe_allow_html=True) 
        tabs[2].plotly_chart(t6_fig2_0, use_container_width=True) 


    with tabs[3]: # 노선별
        t6_fig3_0, t6_df3_0, t6_df3_1, t6_df3_2, t6_wc3 = mf.create_px_scatter_road(t6_organ, t6_road) 
        t6_df3_2_temp = t6_df3_2.sort_values(by='NUMBER', ascending=False) 
        tabs[3].write(f"📢 최다 노선은 <strong>{ t6_df3_2_temp.iloc[0][ f'{t6_road}' ] }</strong> 으로, " + 
                      f"<strong>총 { t6_df3_2_temp.iloc[0][ 'NUMBER' ] } 건 ({ t6_df3_2_temp.iloc[0][ f'NUMBER_pct' ] } %)</strong> 입니다. ", unsafe_allow_html=True) 
        tabs[3].plotly_chart(t6_fig3_0, use_container_width=True) 


    with tabs[4]: # 데이터
        t6_df4_0, t6_df4_1, t6_df4_2, t6_wc4 = mf.load_df(t6_organ, t6_road)  
        t6_df4_2_temp = t6_df4_2.sort_values(by='NUMBER', ascending=False) 
        tabs[4].dataframe(t6_df4_2_temp.style.background_gradient(cmap='Blues'), use_container_width=True) 


    # 
    t6_cont9 = st.container(border=False)
    t6_cont9.markdown(f"##### 😎 {t6_organ} 민원 :rainbow[노선별로 한눈에 보기] 👀") 

    tabs = st.tabs(['🌍 지 도', '🔎키워드', '💾데이터']) 
    with tabs[0]: 
        mf.load_map(t6_base_position, t6_organ, t6_mapchoice) 

    with tabs[1]: 
        t6_fig9_0, t6_df9_0, t6_df9_1, t6_df9_2, t6_wc9 = mf.load_wc(t6_organ, t6_keyword) 
        tabs[1].pyplot(t6_fig9_0, use_container_width=True) 

    with tabs[2]: 
        tabs[2].dataframe(t6_df9_1, use_container_width=True) 
  
