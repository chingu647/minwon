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
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ global 변수 설정
    global t6t1_map  # ----------------------------------------------------------------------- 
    global organ_t6
    global kind1_t6
    organ_t6 = "보성지사" 
    kind1_t6 = '서비스유형(대)'  

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
    
    # global t6t1_map  # ----------------------------- #    map이 다르므로 함수명도 다르게 설정함    
    @st.cache_resource
    def create_map_t6(point_df): 
        for index, row in point_df.iterrows(): 
            if not pd.isna(row['latitude']) and not pd.isna(row['longitude']):
                folium.CircleMarker( location=[ row['latitude'], row['longitude'] ],  # 원 중심
                                    radius=1,            # 원 반지름
                                    color='blue',        # 원 테두리 색상
                                    fill=True,           # 원 채움
                                    fill_opacity=0.5,     # 원 채움 투명도
                                    ).add_to(t6t1_map) 
                
                folium.Marker( location=[ row['latitude'], row['longitude'] ],  # 값 중심 
                            popup=f"{row['서비스유형(소)']} ( {row['고객유형']} ) ", 
                            tooltip=row['latitude'], 
                            icon=folium.Icon(color='red', icon='star'), 
                            #   icon=folium.DivIcon(                              # 값 표시방식
                            #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
                            ).add_to(t6t1_map) 

        folium_map_t6 = t6t1_map._repr_html_() 
        st.components.v1.html(folium_map_t6, height=900) #, width=800, height=600)
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

    ###################################################################### layout 
    t6h0, t6h1, t6h2 = st.columns( [0.001, 0.998, 0.001] ) 
    
    t6b0, t6b1, t6b2, t6b3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t6b4, t6b5, t6b6, t6b7 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t6b8, t6b9, t6b10,t6b11= st.columns( [0.001, 0.499, 0.499, 0.001] )

    t1t0, t6t1, t1t2 = st.columns( [0.001, 0.998, 0.001] ) 

    ###################################################################### head 1  
    t6h1.markdown(f"##### {organ_t6} : 공지사항")
    t6h1.markdown(r"""
	1. 보성지사 민원은 증가추세에 있습니다.
    """)

    ###################################################################### body 1  
    t6b1.markdown("##### 2024년 이슈")

    t6b1_kind1_df, _ = load_df(organ_t6, kind1_t6) 

    t6b1.table(t6b1_kind1_df.style.background_gradient(cmap='Blues')) 

    ###################################################################### body 2 
    t6b2.markdown("##### 주요 키워드 클라우드") 

    text_raw = '한국어 분석을 시작합니다... 재미있어요!!!~~~한국어 분석 고속도로 포장 포장 광주 광주지사 시어요!!!~~~한국어 합니다... 재미있어요!!!~~~'
    t6b2_wc = load_wc(text_raw)
  

    t6b2_fig, t6b2_ax = plt.subplots(figsize=(10,4)) 
    t6b2_ax.axis('off')
    t6b2_ax.imshow(t6b2_wc)
    t6b2.pyplot(t6b2_fig) 

    ###################################################################### body 5 
    t6b5.markdown("##### 유형별 민원") 

    # -------------------------------------------------------- pie 그래프 
    # data  
    t6b5_kind1_df, _ = load_df(organ_t6, kind1_t6) 

    t6b5_x = t6b5_kind1_df.index.values
    t6b5_y = t6b5_kind1_df['건수'] 

    # preprocessing
    t6b5_fig, t6b5_ax = plt.subplots(figsize=(10,4)) 
    t6b5_ax.tick_params(
        # axis=x or axis=y,
        # labelsize=20,
        direction='inout',
        color = 'red',
        colors = 'blue',
        # rotation=20, 
        bottom = True, labelbottom=True,        # tick 수정
        top = False, labeltop=False,
        left = True, labelleft=True,
        right= False, labelright=False
        )
    t6b5_ax.set_facecolor('white')                  # figure 배경색 

    # paint 
    explode = [0.05 for i in t6b5_x]
    wedgeprops={'width': 0.5, 'edgecolor': 'w', 'linewidth': 3}
    t6b5_ax.pie(t6b5_y, labels=t6b5_x, 
            startangle=260,
            counterclock=False, 
            autopct="%.1f%%", 
            # explode=explode,
            # shadow=True,
            wedgeprops=wedgeprops, 
            textprops={'size':9}) 
    t6b5_cx = 0
    t6b5_cy = 0
    t6b5_val= '총' + str(t6b5_kind1_df['건수'].sum()) + '건'
    t6b5_ax.text(t6b5_cx, t6b5_cy, t6b5_val, 
                ha='center', va='center', 
                color='red',
                fontsize=23)                           # bar text 폰크 

    t6b5.pyplot(t6b5_fig) 

    ###################################################################### body 6 
    t6b6.markdown("##### 유형별 민원") 

    # -------------------------------------------------------- 세로 bar 그래프 
    # data  
    t6b6_kind1_df, _ = load_df(organ_t6, kind1_t6) 

    t6b6_x = t6b6_kind1_df.index.values
    t6b6_y = t6b6_kind1_df['건수'] 

    # preprocessing 
    t6b6_fig, t6b6_ax = plt.subplots(figsize=(10,4)) 
    t6b6_ax.tick_params(
        # axis=x or axis=y,
        labelsize=20,
        direction='inout',
        color = 'red',
        colors = 'blue',
        # rotation=20, 
        bottom = True, labelbottom=True,        # tick 수정
        top = False, labeltop=False,
        left = False, labelleft=False,
        right= False, labelright=False
        )
    t6b6_ax.set_facecolor('white')                  # figure 배경색 

    # paint 
    t6b6_ax.bar(t6b6_x, t6b6_y, color='#E0ECF8')            # bar plot 표시
    for i in range(len(t6b6_x)):                        # bar text 표시
        height = t6b6_y[i]+0.5 
        height_str = str(t6b6_y[i])+'건'
        t6b6_ax.text(t6b6_x[i], height, height_str, 
                 ha='center', va='bottom', 
                 color='green',
                 fontsize=20)                           # bar text 폰크 

    t6b6.pyplot(t6b6_fig) 

    ###################################################################### body 9
    t6b9.markdown("##### 노선별 민원") 
    
    # -------------------------------------------------------- 가로 sns bar 그래프 
    # data  
    t6b9_kind1_df, _ = load_df(organ_t6, kind1_t6) 
    t6b9_x = t6b9_kind1_df.index.values
    t6b9_y = t6b9_kind1_df['건수'] 

    # preprocessing ---------------------------
    t6b9_fig,  t6b9_ax = plt.subplots(figsize=(10,6)) 
    t6b9_ax.tick_params(
        # axis=x or axis=y,
        labelsize=20,
        direction='inout',
        color = 'red',
        colors = 'blue',
        # rotation=20, 
        bottom = False, labelbottom=False,        # tick 수정
        top = False, labeltop=False,
        left = True, labelleft=True,
        right= False, labelright=False
        )
    t6b9_ax.set_facecolor('white')                  # figure 배경색 

    # paint 
    sns.barplot(x=t6b9_y, y=t6b9_x, 
                hue=t6b9_x, 
                dodge=False,
                ax=t6b9_ax) 
    for i in range(len(t6b9_x)):               # bar text 표시
        width = t6b9_y[i]+1.5 
        width_str = str(t6b9_y[i])+'건'
        t6b9_ax.text(width, i, width_str, 
                #  ha='center', va='bottom', 
                 color='green',
                 fontsize=20)                   # bar text 폰크

    t6b9.pyplot(t6b9_fig)  

    ###################################################################### body 10
    t6b10.markdown("##### 노선별 민원") 

    t6b10_kind1_df, _ = load_df(organ_t6, kind1_t6) 

    t6b10.table(t6b10_kind1_df.style.background_gradient(cmap='winter')) 



    ###################################################################### tail 1
    t6t1.markdown("##### 노선별 민원") 
    
    # -------------------------------------------------------- 가로 sns bar 그래프 
    # map data  

    t6t1_kind1_df, t6t1_point_df = load_df(organ_t6, kind1_t6)   
    t6t1_point_df_temp = t6t1_point_df.copy()  
    t6t1.dataframe(t6t1_point_df_temp)

    base_position = [35.18668601, 126.87954220] 

    t6t1_map = load_map(base_position) 
    # create_map(t6t1_map, t6t1_point_df) 


    create_map_t6(t6t1_point_df) 

