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


import mf 

def run_tab(): 
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ global 변수 설정
    global map_t0  # ----------------------------------------------------------------------- 
    global organ
    global kind1 
    global base_position 

    organ = "본부" 
    kind1 = 'KIND1'
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
    cont0.markdown(f"##### 📢 {organ} :rainbow[민원 건 수] 현황") 

    tabs = st.tabs(['차 트', '그래프', '데이터']) 
    with tabs[0]: 
        # 
        fig0_0, df0_0, df0_1, df0_2, df0_3 = mf.create_px_scatter(organ, kind1) 
        df0_2_temp = df0_2.copy()
        df0_2_temp.sort_values(by=f'{kind1}', ascending=True)  # 오름차순으로 ...

        tabs[0].dataframe(df0_0)
        tabs[0].dataframe(df0_1)
        tabs[0].table(df0_2)
        tabs[0].write(df0_3) 
        tabs[0].write(f"최다 민원은 <strong>{ df0_2_temp.iloc[-1][ f'{kind1}' ] }</strong> 관련으로, <strong>총 { df0_2_temp.iloc[-1][ 'NUMBER' ] } 건 ({ df0_2_temp.iloc[-1][ f'NUMBER_pct' ] } %)</strong> 입니다.       , ", unsafe_allow_html=True) 

        tabs[0].plotly_chart(fig0_0, use_container_width=True) 

    with tabs[1]: 
        tabs[1].write(f"최다 민원은 <strong>{ df0_2_temp.iloc[-1][ f'{kind1}' ] }</strong> 관련으로, <strong>총 { df0_2_temp.iloc[-1][ 'NUMBER' ] } 건 ({ df0_2_temp.iloc[-1][ f'NUMBER_pct' ] } %)</strong> 입니다.       , ", unsafe_allow_html=True) 

        # fig0_1, _, _, _, _ = mf.create_px_bar(organ, kind1) 
        # tabs[1].plotly_chart(fig0_1, use_container_width=True) 

    with tabs[2]: 
        tabs[2].write(f"최다 민원은 <strong>{ df0_2_temp.iloc[-1][ f'{kind1}' ] }</strong> 관련으로, <strong>총 { df0_2_temp.iloc[-1][ 'NUMBER' ] } 건 ({ df0_2_temp.iloc[-1][ f'NUMBER_pct' ] } %)</strong> 입니다.       , ", unsafe_allow_html=True) 

        # df0_2_tmp = df0_2.copy() 
        # # df0_2_tmp.columns = ['민원 유형', '발생 건수', '백분율 (%)'] 
        # tabs[2].dataframe(df0_2_tmp.style.background_gradient(cmap='Blues'), use_container_width=True)

    # # # ################################################# 유형별 민원 현황 
    # cont1 = st.container(border=False)
    # cont1.markdown(f"##### 📚 {organ} :rainbow[유형별 민원] 현황") 

    # tabs = st.tabs(['차 트', '그래프', '데이터']) 
    # with tabs[0]: 
    #     # df0, df1 
    #     fig1_0, df1_0, df1_1, df1_2, df1_3 = mf.create_px_pie(organ, kind1) 
    #     df1_2_1 = df1_2.sort_values(by=f'{kind1}', ascending=True)  # 오름차순으로 ...

    #     tabs[0].write(f"최다 민원은 <strong>{ df1_2_1.iloc[-1][ f'{kind1}' ] }</strong> 관련으로, <strong>총 { df1_2_1.iloc[-1][ 'NUMBER' ] } 건 ({ df1_2_1.iloc[-1][ f'NUMBER_pct' ] } %)</strong> 입니다.       , ", unsafe_allow_html=True) 

    #     tabs[0].plotly_chart(fig1_0, use_container_width=True) 

    # with tabs[1]: 
    #     fig1_1, _, _, _, _ = mf.create_px_bar(organ, kind1) 
    #     tabs[1].plotly_chart(fig1_1, use_container_width=True) 

    # with tabs[2]: 
    #     df1_2_tmp = df1_2.copy() 
    #     # df1_2_tmp.df1_2.columns = ['민원 유형', '발생 건수', '백분율 (%)'] 
    #     tabs[2].dataframe(df1_2_tmp.style.background_gradient(cmap='Blues'), use_container_width=True) 

    # # # ################################################# 지사별 민원 현황 
    # cont2 = st.container(border=False)
    # cont2.markdown(f"##### 🚔 {organ} :rainbow[지사별 민원] 현황") 

    # tabs = st.tabs(['차 트', '그래프', '데이터']) 
    # with tabs[0]: 
    #     # df0, df1 
    #     fig2_0, df2_0, df2_1, df2_2, df2_3 = mf.create_px_scatter(organ, kind1) 
    #     df2_2_1 = df2_2.sort_values(by=f'{kind1}', ascending=True)  # 오름차순으로 ...

    #     tabs[0].write(f"최다 민원은 <strong>{ df2_2_1.iloc[-1][ f'{kind1}' ] }</strong> 관련으로, <strong>총 { df2_2_1.iloc[-1][ 'NUMBER' ] } 건 ({ df2_2_1.iloc[-1][ f'NUMBER_pct' ] } %)</strong> 입니다.       , ", unsafe_allow_html=True) 

    #     tabs[0].plotly_chart(fig2_0, use_container_width=True) 

    # with tabs[1]: 
    #     fig2_1, _, _, _, _ = mf.create_px_bar(organ, kind1) 
    #     tabs[1].plotly_chart(fig2_1, use_container_width=True) 

    # with tabs[2]: 
    #     df2_2_tmp = df2_2.copy() 
    #     # df2_2_tmp.columns = ['민원 유형', '발생 건수', '백분율 (%)'] 
    #     tabs[2].dataframe(df2_2_tmp.style.background_gradient(cmap='Blues'), use_container_width=True) 

    # ################################################# 민원 지도 보기 
    cont9 = st.container(border=False)
    cont9.markdown(f"##### 😎 {organ} :rainbow[민원 한눈에 보기] 👀") 

    tabs = st.tabs(['지 도', '데이터']) 
    with tabs[0]: 
        # 테이블 데이터
        df9_0, df9_1, df9_2, df9_3  = mf.load_df(organ, kind1) 

        # map data  
        # map_t1 = mf.load_map_kind1(organ0, kind1, base_position) 
        mf.load_map(organ, kind1, base_position) 

    with tabs[1]:
        # df1_0.columns = ['민원 유형', '발생 건수', '백분율 (%)']         
        # cont9.dataframe(df9_1) 
        tabs[1].dataframe(df9_1) #.style.background_gradient(cmap='Blues'), use_container_width=True) 


    





    # tabs = st.tabs(['📊 차트', '📈 그래프', '💾 데이터'])     
    # with tabs[0]: 
    #     fig1, df1  = mf.create_px_pie(organ, kind1)
    #     tabs[0].plotly_chart(fig1, use_container_width=True) 


    # with tabs[1]: 
    #     fig1, df1  = mf.create_go_Scatter(organ, kind1)
    #     tabs[1].plotly_chart(fig1, use_container_width=True) 

    #     col1, col2, col3 = st.columns(3) 
    #     with col1: 
    #         col1.write( 'tabs[1] > col1 ') 

    #     with col2:  
    #         col2.write( 'tabs[1] > col2 ') 


    # with tabs[2]: 
    #     fig1, df1  = mf.create_go_Bar(organ, kind1)
    #     tabs[2].plotly_chart(fig1, use_container_width=True) 

    #     col1, col2, col3 = st.columns(3) 
    #     with col1: 
    #         col1.write( 'tabs[2] > col1 ') 

    #     with col2:  
    #         col2.write( 'tabs[2] > col2 ') 
            

    # with tabs[2]:
    #     col1, col2, col3 = st.columns(3) 
    #     fig1, df1  = mf.create_px_pie(organ, kind1)
    #     st.dataframe(df1.iloc.style.background_gradient(cmap='Blues'), use_container_width=True) 





      



    # organ_t0_container_1.markdown(f"##### 📢 {organ_t0} :rainbow[민원 건 수] 현황") 
    # organ_t0_fig1, organ_t0_df1  = mf.create_px_pie(organ_t0, kind1_t0)
    # organ_t0_container_1.plotly_chart(organ_t0_fig1, use_container_width=True) 
    # organ_t0_container_1.dataframe(organ_t0_df1.iloc[:5,:].style.background_gradient(cmap='Blues'), use_container_width=True) 



    # t0b2_container = st.container(border=True)
    # t0b2_container.markdown(f"##### 📢 {organ_t0} :rainbow[유형별] 민원") 
    # t0b1_fig2 = mf.create_px_pie(organ_t0, kind1_t0)
    # t0b2_container.plotly_chart(t0b1_fig2, use_container_width=True) 
    # t0b2_container.dataframe(t0b1_kind1_df.style.background_gradient(cmap='Blues'), use_container_width=True) 

    # t0b5_container = st.container(border=True)
    # t0b5_container.markdown(f"##### 📢 {organ_t0} :rainbow[유형별] 민원") 
    # t0b1_fig3 = mf.create_go_Scatter(organ_t0, kind1_t0)
    # t0b5_container.plotly_chart(t0b1_fig3, use_container_width=True) 

    # t0b1.markdown(f"""
	# <center>최근 이슈는 <b>{t0b1_kind1_df.index[0]}</b> > {t0b1_kind1_df.index[1]} > {t0b1_kind1_df.index[2]} 순 입니다.</center>
    # """, unsafe_allow_html=True) 

    # t0b1.table(t0b1_kind1_df.style.background_gradient(cmap='Blues')) 




    # # # ###################################################################### body 1  
    # t0b1.markdown(f"##### 📢 {organ_t0} :rainbow[민원 건 수] 현황") 
    
    # _, _, t0b1_kind1_df, _ = mf.load_df(organ_t0, kind1_t0) 

    # t0b1.markdown(f"""
	# <center>최근 이슈는 <b>{t0b1_kind1_df.index[0]}</b> > {t0b1_kind1_df.index[1]} > {t0b1_kind1_df.index[2]} 순 입니다.</center>
    # """, unsafe_allow_html=True) 

    # t0b1.table(t0b1_kind1_df.style.background_gradient(cmap='Blues')) 





    # # # ###################################################################### body 2     # wc 그래프  
    # t0b2.markdown("##### 🔎 :rainbow[2024년 주요 키워드] ") 
    # t0b2_fig, _, _, _, _ = mf.load_wc(organ_t0, kind1_t0) 

    # t0b2.markdown(f"""
	# <center>주요 키워드는 <b>{organ_t0}</b> 입니다.</center>
    # """, unsafe_allow_html=True)

    # t0b2.pyplot(t0b2_fig, use_container_width=True)   


    # ###################################################################### body 5     # pie 그래프 
    # t0b5.markdown("##### 📚 :rainbow[2024년 유형별] ") 

    # t0b5.markdown(f"""
	# <center>주요 민원유형은 <b>{organ_t0}</b> 입니다.</center>
    # """, unsafe_allow_html=True)

    # t0b5_pie, _, _, _, _  = mf.create_pie(organ_t0, kind1_t0)
    # t0b5.pyplot(t0b5_pie, use_container_width=True)  


    # # # ###################################################################### body 6 
    # t0b6.markdown("##### 🚔 :rainbow[2024년 지사별] ") 

    # # # pie 그래프 
    # # t0b6_pie = mf.create_pie(organ_t0, kind1_t0) 
    # # t0b6.pyplot(t0b6_pie)


    # # # ###################################################################### body 9
    # t0b9.markdown("##### 🚌 :rainbow[2024년 노선별] ") 

    # t0b9.markdown(f"""
	# <center>최다 민원노선은 <b>{organ_t0}</b> 입니다.</center>
    # """, unsafe_allow_html=True)
    
    # # 가로 sns bar 그래프 
    # t0b9_sns_hbar, _, _, _, _  = mf.create_sns_hbar(organ_t0, kind1_t0) 
    # t0b9.pyplot(t0b9_sns_hbar)


    # ###################################################################### body 10



    # ###################################################################### tail 1 
    # t0t1.markdown(f"##### 😎 :rainbow[{organ_t0} 민원 한눈에 보기] 👀 ") 

    # # 테이블 데이터
    # t0t1_point_df, _, _, _ = mf.load_df(organ_t0, kind1_t0) 
    # t0t1.dataframe(t0t1_point_df) 

    # # map data  
    # # map_t1 = mf.load_map_kind1(organ_t0, kind1_t0, base_position_t0) 

    # mf.load_map_kind1(organ_t0, kind1_t0, base_position_t0) 

