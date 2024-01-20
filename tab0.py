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


def run_tab(): 
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-2) ST CACHE 사용
    @st.cache_resource 
    def load_df(organ, kind1):
        df = pd.read_csv("data/민원처리현황.csv")
        df = df.query( f"organ=='{organ}'" )
        kind1_df = df.groupby(by=f'{kind1}').count() #.sort_values(by=f'{kind1}', ascending=False)
        kind1_df = kind1_df.iloc[:5,:1]
        kind1_df.columns = ['건수']
        kind1_df['비율(%)'] = ( kind1_df['건수']/(kind1_df['건수'].sum())*100).astype(int)
        kind1_df = kind1_df.sort_values(by='건수', ascending=False) 

        # map data
        # point_df = df[ (df['latitude'].str.strip() != '') and (df['longitude'].str.strip() != '') ] 
        point_df = df[ ~( (df['latitude'].isna()) | (df['longitude'].isna()) ) ] 

        return kind1_df, point_df  


    @st.cache_resource 
    def load_wc(text_raw):
        t = Okt()
        text_nouns = t.nouns(text_raw) 
        stopwords =['시어']
        text_nouns = [n for n in text_nouns if n not in stopwords]
        text_str = ' '.join(text_nouns)
        wc = WordCloud(background_color='#ECF8E0', font_path=r"data/NanumGothic.ttf", max_words=50).generate(text_str) 
        
        return wc 

    @st.cache_resource 
    def load_map(base_position): 
        map = folium.Map( location=base_position, zoom_start=9 ) #, tiles='Stamentoner') 
        gpf_line = gpd.read_file("data/ex_line_KWANGJU.shp") 
        folium.GeoJson(gpf_line, 
                        style_function=lambda feature: {
                            'fillColor': 'blue' , #feature['properties']['color'],
                            'color': '#F5F6CE',
                            'weight': 3,
                            'dashArray': '5, 5',
                            'fillOpacity': 0.3, 
                        }
                    ).add_to(map) 
        return map

    # @st.cache_resource 
    def create_map(map, point_df): 
        for index, row in point_df.iterrows(): 
            if not pd.isna(row['latitude']) and not pd.isna(row['longitude']):
                folium.CircleMarker( location=[ row['latitude'], row['longitude'] ],  # 원 중심
                                    radius=1,            # 원 반지름
                                    color='blue',        # 원 테두리 색상
                                    fill=True,           # 원 채움
                                    fill_opacity=0.5,     # 원 채움 투명도
                                    ).add_to(map) 
                
                folium.Marker( location=[ row['latitude'], row['longitude'] ],  # 값 중심 
                            popup=f"{row['서비스유형(소)']} ( {row['고객유형']} ) ", 
                            tooltip=row['latitude'], 
                            icon=folium.Icon(color='red', icon='star'), 
                            #   icon=folium.DivIcon(                              # 값 표시방식
                            #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
                            ).add_to(map) 

        folium_map = map._repr_html_() 
        st.components.v1.html(folium_map, height=900) #, width=800, height=600)
        # folium_static(t1_map) #, width=600, height=400)
        # t1_tail1.map(data=t1_gpf, latitude='latitude', longitude='longitude')  


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
    st.markdown(""" 
                <style> 
                    table{background-color:#f0f0f0;} 
                    # div{border:1px solid #00ff00;}
                    img {max-width: 600px; max-height: 600px;}    # 이미지 파일 최대크기 제한 
                
                </style> """, 
                unsafe_allow_html=True
                ) 
    
    # ###################################################################### layout 
    t0h0, t0h1, t0h2 = st.columns( [0.001, 0.998, 0.001] ) 
    
    t0b0, t0b1, t0b2, t0b3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t0b4, t0b5, t0b6, t0b7 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t0b8, t0b9, t0b10,t0b11= st.columns( [0.001, 0.499, 0.499, 0.001] )

    t0t0, t0t1, t0t2 = st.columns( [0.001, 0.998, 0.001] ) 

    # ###################################################################### head 1  
    t0h1.markdown("##### 공지사항")
    t0h1.markdown(r"""
	1. 오늘의 이슈. 
    """) 

    # ###################################################################### body 1  
    t0b1.markdown("##### 2024년 이달의 이슈")
    t0b1.markdown(r"""
	1. 오늘의 이슈.
    """)

    # ###################################################################### body 2  
    t0b2.markdown("##### 지사별 현황")

    t0b2_kind1_df, _ = load_df('광주지사', '서비스유형(대)') 

    t0b2.table(t0b2_kind1_df.style.background_gradient(cmap='Blues')) 

    # ###################################################################### body 5 
    t0b5.markdown("##### 노선별 현황")

    t0b5_kind1_df, _ = load_df('광주지사', '서비스유형(대)') 

    t0b5.table(t0b5_kind1_df.style.background_gradient(cmap='Reds')) 

    # ###################################################################### body 6 

    t0b6.markdown("##### 주요 키워드 클라우드") 

    text_raw = '한국어 분석을 시작합니다... 재미있어요!!!~~~한국어 분석 고속도로 포장 포장 광주 광주지사 시어요!!!~~~한국어 합니다... 재미있어요!!!~~~'
    t0b6_wc = load_wc(text_raw)
  
    t0b6_fig, t0b6_ax = plt.subplots(figsize=(10,4)) 
    t0b6_ax.axis('off')
    t0b6_ax.imshow(t0b6_wc)
    t0b6.pyplot(t0b6_fig)  
