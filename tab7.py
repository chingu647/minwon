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
    global t7_map  # ----------------------------------------------------------------------- 
    global t7_organ
    global t7_kind1 
    global t7_kind2 
    global t7_team 
    global t7_road 
    global t7_mapchoice 
    global t7_base_position 
    global t7_keyword 
    t7_organ = "남원지사"   # ALL 광주전남본부 광주지사 담양지사 순천지사 함평지사 구례지사 보성지사 남원지사 
    # choice 종류
    t7_kind1 = 'KIND1' # ----------------------------------------------------------------------
    t7_kind2 = 'KIND2' # ----------------------------------------------------------------------
    t7_team  = 'TEAM'  # ----------------------------------------------------------------------
    t7_road  = 'ROAD'  # ---------------------------------------------------------------------- 
    t7_mapchoice = 'KIND1' 
    t7_base_position = [35.18668601, 126.87954220] 
    # word cloud 
    t7_keyword = 'KEYWORD'
    # 
    st.markdown(""" 
                <style> 
                    table{background-color:#f0f0f0;} 
                    img {max-width: 1000px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
                
                </style> """, 
                unsafe_allow_html=True
                )     
    # 
    t7_cont0 = st.container(border=False)

    tabs = st.tabs(['📈월별 추이', '📚유형별', '🚔부서별', '🚌노선별', '💾데이터']) 
    with tabs[0]: # 월별

         
        t7_fig0_0, t7_df0_0, t7_df0_1, t7_df0_2, t7_wc0 = mf.create_px_bar_month(t7_organ, t7_kind1) 
        t7_df0_0_temp = t7_df0_0.sort_values(by='NUMBER', ascending=False) 

        tabs[0].write(f"📢 민원 건수는 <strong>총 { t7_df0_0_temp[ 'NUMBER' ].sum() } 건</strong> 이며, " +
                      f"최다 발생 기간은 <strong>{ t7_df0_0_temp.iloc[0][ 'DATE' ].strftime('%Y') }년 " +
                      f"{ t7_df0_0_temp.iloc[0][ 'DATE' ].strftime('%m') }월</strong> <strong>( { t7_df0_0_temp.iloc[0][ 'NUMBER' ] } 건 )</strong> 입니다. ", unsafe_allow_html=True) 
        tabs[0].plotly_chart(t7_fig0_0, use_container_width=True) 


    with tabs[1]: # 유형별 
        t7_fig1_0, t7_df1_0, t7_df1_1, t7_df1_2, t7_wc1 = mf.create_px_pie_kind1(t7_organ, t7_kind1) 
        t7_df1_2_temp = t7_df1_2.sort_values(by='NUMBER', ascending=False) 
        tabs[1].write(f"📚 최다 유형은 <strong>{ t7_df1_2_temp.iloc[0][ f'{t7_kind1}' ] }</strong> 관련으로, " +
                      f"<strong>총 { t7_df1_2_temp.iloc[0][ 'NUMBER' ] } 건 ({ t7_df1_2_temp.iloc[0][ f'NUMBER_pct' ] } %)</strong> 입니다. ", unsafe_allow_html=True) 
        tabs[1].plotly_chart(t7_fig1_0, use_container_width=True) 


    with tabs[2]: # 팀별
        t7_fig2_0, t7_df2_0, t7_df2_1, t7_df2_2, t7_wc2 = mf.create_px_bar_team(t7_organ, t7_team) 
        t7_df2_2_temp = t7_df2_2.sort_values(by='NUMBER', ascending=False) 
        tabs[2].write(f"📚 최다 처리 팀은 <strong>{ t7_df2_2_temp.iloc[0][ f'{t7_team}' ] }</strong> 으로, " +
                      f"<strong>총 { t7_df2_2_temp.iloc[0][ 'NUMBER' ] } 건 ({ t7_df2_2_temp.iloc[0][ f'NUMBER_pct' ] } %)</strong> 입니다. ", unsafe_allow_html=True) 
        tabs[2].plotly_chart(t7_fig2_0, use_container_width=True) 


    with tabs[3]: # 노선별
        t7_fig3_0, t7_df3_0, t7_df3_1, t7_df3_2, t7_wc3 = mf.create_px_scatter_road(t7_organ, t7_road) 
        t7_df3_2_temp = t7_df3_2.sort_values(by='NUMBER', ascending=False) 
        tabs[3].write(f"📢 최다 노선은 <strong>{ t7_df3_2_temp.iloc[0][ f'{t7_road}' ] }</strong> 으로, " + 
                      f"<strong>총 { t7_df3_2_temp.iloc[0][ 'NUMBER' ] } 건 ({t7_df3_2_temp.iloc[0][ f'NUMBER_pct' ] } %)</strong> 입니다. ", unsafe_allow_html=True) 
        tabs[3].plotly_chart(t7_fig3_0, use_container_width=True) 


    with tabs[4]: # 데이터
        t7_df4_0, t7_df4_1, t7_df4_2, t7_wc4 = mf.load_df(t7_organ, t7_road)  
        t7_df4_2_temp = t7_df4_2.sort_values(by='NUMBER', ascending=False) 
        tabs[4].dataframe(t7_df4_2_temp.style.background_gradient(cmap='Blues'), use_container_width=True) 


    # 
    t7_cont9 = st.container(border=False)
    t7_cont9.markdown(f"##### 😎 {t7_organ} 민원 :rainbow[노선별로 한눈에 보기] 👀") 

    tabs = st.tabs(['🌍 지 도', '🔎키워드', '💾데이터']) 
    with tabs[0]: 
        mf.load_map(t7_base_position, t7_organ, t7_mapchoice) 

    with tabs[1]: 
        t7_fig9_0, t7_df9_0, t7_df9_1, t7_df9_2, t7_wc9 = mf.load_wc(t7_organ, t7_keyword) 
        tabs[1].pyplot(t7_fig9_0, use_container_width=True) 

    with tabs[2]: 
        tabs[2].dataframe(t7_df9_1, use_container_width=True) 
  
