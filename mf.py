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


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-1) ST CACHE 사용

##################################################################################### load_df 
# arg1 : global organ_ t?? ---------- 탭 페이지에서 입력
# arg2 : global kind1_ t?? ---------- 탭 페이지에서 입력
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

    # wc data
    wc_sr = df.loc[:, '본문 요약']
    wc_data = ' '.join( map(str,wc_sr) )

    return kind1_df, point_df, wc_data  
    # kind1_df --------- 
    # point_df --------- 



##################################################################################### load wc 
# arg1 : text_raw 
@st.cache_resource 
def load_wc(organ, kind1): # target_layout 에러 발생 
    # data  
    _, _, wc_data = load_df(organ, kind1)  #   <================================================== 
    t = Okt()
    text_nouns = t.nouns(wc_data) 
    stopwords =['시어','및','조치','예정','민원','처리','해당','통해','대한','방향','후','검토','확인','완료','내','노력','등','위해','지사',
                '대하','도록','말씀','수','음','귀하','주신','답변','향','중','향','사항','아래','다음','문의사항','내용','요청',]
    text_nouns = [n for n in text_nouns if n not in stopwords]
    text_str = ' '.join(text_nouns)
    wc = WordCloud(background_color='#ECF8E0', font_path=r"data/NanumGothic.ttf", max_words=20).generate(text_str) 
    
    fig, ax = plt.subplots(figsize=(10,4)) 
    ax.axis('off')
    ax.imshow(wc) 
    # target_layout.pyplot(fig) 
    return fig 



##################################################################################### load map
# arg1 : organ_ t?? ---------- 탭 페이지에서 입력
# arg2 : kind1_ t?? ---------- 탭 페이지에서 입력
# base_position_ t?? --------- 탭 페이지에서 입력

@st.cache_resource 
def load_map(organ, kind1, base_position): 
    # data  
    kind1_df, point_df, _ = load_df(organ, kind1)  #   <==================================================

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



##################################################################################### create pie
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
def create_pie(organ, kind1): 
    # data  
    kind1_df, _, _ = load_df(organ, kind1)  #   <==================================================

    data_x = kind1_df.index.values
    data_y = kind1_df['건수'] 

    # preprocessing
    fig, ax = plt.subplots(figsize=(10,4)) 
    ax.tick_params(
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
    ax.set_facecolor('white')                  # figure 배경색 

    # paint 
    explode = [0.05 for i in data_x]
    wedgeprops={'width': 0.5, 'edgecolor': 'w', 'linewidth': 3}
    ax.pie(data_y, labels=data_x, 
           startangle=260,
           counterclock=False, 
           autopct="%.1f%%", 
           # explode=explode,
           # shadow=True,
           wedgeprops=wedgeprops, 
           textprops={'size':9}) 
    data_cx = 0
    data_cy = 0
    data_val= '총' + str(kind1_df['건수'].sum()) + '건'
    ax.text(data_cx, data_cy, data_val, 
            ha='center', va='center', 
            color='red',
            fontsize=23)                           # bar text 폰크 
    
    return fig  



##################################################################################### 세로 막대 create vbar 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_vbar(organ, kind1): 
    # data  
    kind1_df, _, _ = load_df(organ, kind1)  #   <==================================================

    data_x = kind1_df.index.values
    data_y = kind1_df['건수'] 

    # preprocessing 
    fig, ax = plt.subplots(figsize=(10,4)) 
    ax.tick_params(
        # axis=x or axis=y,
        labelsize=20,
        direction='inout',
        color = 'red',
        colors = 'blue',
        # rotation=20, 
        bottom = True, labelbottom=True,        # tick 수정
        top = False, labeltop=False,
        left = False, labelleft=False,
        right= False, labelright=False,  
        )
    ax.set_facecolor('white')                  # figure 배경색 

    # paint 
    ax.bar(data_x, data_y, color='#E0ECF8')            # bar plot 표시
    for i in range(len(data_x)):                        # bar text 표시
        height = data_y[i]+0.5 
        height_str = str(data_y[i])+'건'
        ax.text(data_x[i], height, height_str, 
                ha='center', va='bottom', 
                color='green',
                fontsize=20)                           # bar text 폰크 
    
    return fig  



##################################################################################### 가로 막대 create sns hbar 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_sns_hbar(organ, kind1): 
    # data  
    kind1_df, _, _ = load_df(organ, kind1)  #   <==================================================

    data_x = kind1_df.index.values
    data_y = kind1_df['건수'] 

    # preprocessing ---------------------------
    fig,  ax = plt.subplots(figsize=(10,6)) 
    ax.tick_params(
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
    ax.set_facecolor('white')                  # figure 배경색 

    # paint 
    sns.barplot(x=data_y, y=data_x, 
                hue=data_x, 
                dodge=False,
                ax=ax) 

    for i in range(len(data_x)):               # bar text 표시
        width = data_y[i]+1.5 
        width_str = str(data_y[i])+'건'
        ax.text(width, i, width_str,
                # ha='center', va='bottom', 
                color='green',
                fontsize=20)                   # bar text 폰크

    return fig   

