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
    # ==================================================================== mpl 한글 설정  
    font_path_ = "data/NanumGothic.ttf" 
    font_name = fm.FontProperties(fname=font_path_).get_name() 

    mpl.rcParams['axes.unicode_minus'] = False 
    mpl.rcParams['font.family'] = font_name 

    plt.style.use('ggplot') 

    mpl.rc('font', size=18)
    mpl.rc('axes', titlesize=18)
    mpl.rc('axes', labelsize=18) 
    mpl.rc('xtick', labelsize=18)
    mpl.rc('ytick', labelsize=18)
    mpl.rc('legend', fontsize=18)
    mpl.rc('figure', titlesize=12)
    # ==================================================================== layout 
    t1_head0, t1_head1, t1_head2 = st.columns( [0.001, 0.998, 0.001] )
    
    t1_body0, t1_body1, t1_body2, t1_body3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t1_body4, t1_body5, t1_body6 = st.columns( [0.001, 0.998, 0.001] )

    t1_tail0, t1_tail1, t1_tail2 = st.columns( [0.001, 0.998, 0.001] )
    
    t1_body1.markdown(""" <style> table {background-color:#f0f0f0;} </style>""", unsafe_allow_html=True) 


    # ==================================================================== content  

    t1_head1.markdown("###### 공지사항") 
    t1_head1.markdown(r"""
	1. 광주지사 민원은 증가추세에 있다고 할 수 있습니다.
    """)

    # -----------------------------------------------------------------------  
    t1_body1.markdown("###### 2024년 이슈 (민원 유형별)") 
    t1_body1_df = pd.read_csv("data/민원처리현황.csv")
    t1_body1_df = t1_body1_df.query("organ=='광주지사'" )
    t1_body1_df_gby_kind = t1_body1_df.groupby(by='서비스유형(대)').count().sort_values(by='서비스유형(대)', ascending=False)
    t1_body1_df_gby_kind = t1_body1_df_gby_kind.iloc[:5,:1]
    t1_body1_df_gby_kind.columns = ['건수']
    t1_body1_df_gby_kind['비율(%)'] = ( t1_body1_df_gby_kind['건수']/(t1_body1_df_gby_kind['건수'].sum())*100).astype(int)
    t1_body1_df_gby_kind = t1_body1_df_gby_kind.sort_values(by='건수', ascending=False)  
    t1_body1.table(t1_body1_df_gby_kind.style.background_gradient(cmap='Blues')) 

    # -----------------------------------------------------------------------  
    t1_body2.markdown("###### 주요 키워드 클라우드") 
    t = Okt() 

    text_raw = '한국어 분석을 시작합니다... 재미있어요!!!~~~한국어 분석 고속도로 포장 포장 광주 광주지사 시어요!!!~~~한국어 합니다... 재미있어요!!!~~~'
    text_nouns = t.nouns(text_raw) 
    stopwords =['시어']
    text_nouns = [n for n in text_nouns if n not in stopwords]
    text_str = ' '.join(text_nouns) 
    # t1_body2.write(text_raw)

    # text_data = '한국, 한국, korea, korea, usa, england, highway, service, highway'
    wc = WordCloud(background_color='white', font_path=r"data/NanumGothic.ttf", max_words=50).generate(text_str) 
    # wc = WordCloud(background_color='white', max_words=50).generate(text_str) 

    fig, ax = plt.subplots(figsize=(10,4)) 
    ax.axis('off')
    ax.imshow(wc)
    t1_body2.pyplot(fig) 

    # ------------------------------------------------------------------------
    data_x = t1_body1_df_gby_kind.index.values
    data_y = t1_body1_df_gby_kind['건수']

    fig1, ax1 = plt.subplots(figsize=(10,4)) 
    ax1.tick_params(
        # axis=x or axis=y,
        # labelsize=20,
        # colors = 'gray',
        rotation=20, 
        bottom = True, labelbottom=True,                # tick 수정
        top = False, labeltop=False,
        left = False, labelleft=False,
        right= False, labelright=False
        )
    ax1.figure(facecolor='white')                       # figure 배경색 
    ax1.bar(data_x, data_y, color='pink')               # plot 표시
    for i in range(len(data_x)):                        # text 표시
        height = data_y[i]-0.5 
        ax1.text(data_x[i], height, data_y[i], ha='center', va='bottom') 
    # sns.barplot(x=data_x, y=data_y, ax=ax1, dodge=False)

    t1_body5.pyplot(fig1) 
    
    # -----------------------------------------------------------------------

    t1_body5.markdown("###### 노선별 민원 발생현황") 
    t1_body5_df = pd.read_csv("data/민원처리현황.csv")
    t1_body5_df = t1_body5_df.query("organ=='광주지사'" )
    t1_body5_df_gby_kind = t1_body5_df.groupby(by='서비스유형(대)').count().sort_values(by='서비스유형(대)', ascending=False)
    t1_body5_df_gby_kind = t1_body5_df_gby_kind.iloc[:5,:1]
    t1_body5_df_gby_kind.columns = ['건수']
    t1_body5_df_gby_kind = t1_body5_df_gby_kind.sort_values(by='건수', ascending=False)  
    t1_body5.table(t1_body5_df_gby_kind.style.background_gradient(cmap='Blues')) 


    # -----------------------------------------------------------------------  
    # map 
    # base_position = [35.18668601, 126.87954220] 
    # map_data = pd.DataFrame(np.random.randn(5,1)/[20,20] + base_position,
    #     columns=['lat','lon'] 
    #     ) 
    # #print(map_data) 
    # t1_tail1.code('con11.map(map_data)')
    # t1_tail1.map(map_data) 

    # map data
    t1_gpf_point = gpd.read_file("data/ex_point_KWANGJU.geojson")
    t1_gpf_point = t1_gpf_point[ ['노선번호','X좌표값', 'Y좌표값'] ]
    t1_gpf_point.columns = ['노선번호','latitude','longitude'] 

    t1_gpf_point = t1_gpf_point.iloc[:5, :]
    base_position = [35.18668601, 126.87954220] 

    # map layout ---------------------------------------------------------
    t1_map = folium.Map( location=base_position, zoom_start=9 ) #, tiles='Stamentoner') 

    t1_gpf_line = gpd.read_file("data/ex_line_KWANGJU.shp") 
    folium.GeoJson(t1_gpf_line,
                   style_function=lambda feature: {
                       'fillColor': 'blue' , #feature['properties']['color'],
                       'color': '#F5F6CE',
                       'weight': 3,
                       'dashArray': '5, 5',
                       'fillOpacity': 0.3, 
                       }
                    ).add_to(t1_map)


    for index, row in t1_gpf_point.iterrows():
        folium.CircleMarker( location=[ row['latitude'], row['longitude'] ],  # 원 중심
                            radius=1,            # 원 반지름
                            color='blue',        # 원 테두리 색상
                            fill=True,           # 원 채움
                            fill_opacity=1.0     # 원 채움 투명도
                            ).add_to(t1_map) 
        
        folium.Marker( location=[ row['latitude'], row['longitude'] ],  # 값 중심 
                      popup=row['노선번호'],
                      tooltip=row['latitude'],
                      icon=folium.Icon(color='red', icon='star'), 
                    #   icon=folium.DivIcon(                              # 값 표시방식
                    #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
                      ).add_to(t1_map) 

    folium_map = t1_map._repr_html_() 
    st.components.v1.html(folium_map, height=500) #, width=800, height=600)
    # folium_static(t1_map) #, width=600, height=400)
    # t1_tail1.map(data=t1_gpf, latitude='latitude', longitude='longitude')  

