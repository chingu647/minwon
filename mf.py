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

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ DATABASE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ load_df 
# arg1 : global organ_ t?? ---------- 탭 페이지에서 입력
# arg2 : global kind1_ t?? ---------- 탭 페이지에서 입력
# @st.cache_resource 
def load_df(organ, kind1):
    df = pd.read_csv("data/민원처리현황.csv") 

    # DATE 컬럼 DatetimeIndex로 변환 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    df['DATE'] = pd.to_datetime(df['DATE'])
    # st.write(df.dtypes )
    # st.write(df['DATE'].unique())

    # CSV 컬럼 변수 
    LATITUDE = 'LATITUDE'
    LONGITUDE = 'LONGITUDE'
    KEYWORD = 'KEYWORD' 

    if organ=='본부':
        df = df 
    else:
        df = df.query( f"organ=='{organ}'" ) 
    
    # 시계열 data
    month_df = df.groupby(pd.Grouper(key='DATE', freq='M'))['NUMBER'].count().reset_index() 
    month_df['NUMBER_pct_change'] = (   month_df['NUMBER'].pct_change(periods=1)*100   ).round(1)
    month_df['NUMBER_cumsum'] = month_df['NUMBER'].transform('cumsum') 
    # month_df = month_df.assign(NUMBER_DELTA=month_df.NUMBER_CUMSUM - month_df.NUMBER) 
    
    # map data : 위경도 없는 자료는 제외 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    point_df = df[ ~( (df[f'{LATITUDE}'].isna()) | (df[f'{LONGITUDE}'].isna()) ) ] 

    # kind1 data
    kind1_df = point_df.groupby(by=f'{kind1}')['NUMBER'].count().reset_index().sort_values(by=f'{kind1}', ascending=False) 
    kind1_df['NUMBER_pct'] = (   kind1_df['NUMBER'] / kind1_df['NUMBER'].sum()*100   ).astype(int) 
 
    # wc data
    wc_sr = df.loc[:, f'{KEYWORD}']
    wc_data = ' '.join( map(str,wc_sr) )

    return month_df, point_df, kind1_df, wc_data 



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ M A P @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ load wc 
# arg1 : text_raw 
@st.cache_resource 
def load_wc(organ, kind1): # target_layout 에러 발생 
    # data  
    month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <================================================== 
    t = Okt()
    text_nouns = t.nouns(wc_data) 
    stopwords =['시어','및','조치','예정','민원','처리','해당','통해','방향','후','검토','확인','완료','내','노력','등','위해','위하여','지사',
                '대하','대하여','대해','대한','도록','토록','하도록','되도록','말씀','수','음','귀하','주신','답변','향','중','향','사항','아래','다음',
                '문의사항','내용','요청','요지','안내','일부','부분','미완료','관내','박준혁','대리','박준혁 대리','관련','저희','것','함','구간','고객']
    text_nouns = [n for n in text_nouns if n not in stopwords]
    text_str = ' '.join(text_nouns)
    wc = WordCloud(background_color='#fdf0fd', font_path=r"data/NanumGothic.ttf", max_words=20).generate(text_str)   # '#ECF8E0'
    
    fig, ax = plt.subplots(figsize=(6,2)) 
    ax.axis('off')
    ax.imshow(wc) 
    
    return fig, month_df, point_df, kind1_df, wc_data  



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ load map
# arg1 : organ_ t?? ---------- 탭 페이지에서 입력
# arg2 : kind1_ t?? ---------- 탭 페이지에서 입력
# base_position_ t?? --------- 탭 페이지에서 입력

@st.cache_resource 
def load_map(organ, kind1, base_position): 

    # CSV 컬럼 변수
    LATITUDE = 'LATITUDE'
    LONGITUDE = 'LONGITUDE'
    KIND2 = 'KIND2'
    KEYWORD = 'KEYWORD'

    # data  
    month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

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
        if not pd.isna(row[f'{LATITUDE}']) and not pd.isna(row[f'{LONGITUDE}']):
            folium.CircleMarker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 원 중심
                                radius=1,            # 원 반지름
                                color='blue',        # 원 테두리 색상
                                fill=True,           # 원 채움
                                fill_opacity=0.5,     # 원 채움 투명도
                                ).add_to(map) 
                      
            folium.Marker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 값 중심 
                        popup=f"{row[f'{KIND2}']} ( {row[f'{KEYWORD}']} ) ", 
                        tooltip=row[f'{LATITUDE}'], 
                        icon=folium.Icon(color='red', icon='star'), 
                        #   icon=folium.DivIcon(                              # 값 표시방식
                        #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
                        ).add_to(map) 

    folium_map = map._repr_html_()
    st.components.v1.html(folium_map, height=900) #, width=800, height=600)
    # st_folium(map) #, width=600, height=400)



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ load map
# arg1 : organ_ t?? ---------- 탭 페이지에서 입력
# arg2 : kind1_ t?? ---------- 탭 페이지에서 입력
# base_position_ t?? --------- 탭 페이지에서 입력

@st.cache_resource 
def load_map_kind1(organ, kind1, base_position): 

    # CSV 컬럼 변수
    LATITUDE = 'LATITUDE'
    LONGITUDE = 'LONGITUDE'
    KIND2 = 'KIND2'
    KEYWORD = 'KEYWORD'

    # data  
    month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

    # kind1 상위 5개 : Grouped Layer Control 준비...
    
    # if kind1 in point_df.columns:
    #     result = folium.FeatureGroup(name=f'@kind1_df.index[0]')
    # else:
    #     result = "해당 열이 존재하지 않습니다." 
    kind1_df_indexes = list(kind1_df.index)  #   -------------------------------------------------- kind1 5개는 본부 전체로 고정하면?

    fg_k0_df = point_df.query(f' `{kind1}` == "{kind1_df_indexes[0]}" ')
    fg_k1_df = point_df.query(f' `{kind1}` == @kind1_df.index[1] ') 
    fg_k2_df = point_df.query(f' `{kind1}` == @kind1_df.index[2] ')
    fg_k3_df = point_df.query(f' `{kind1}` == @kind1_df.index[3] ')
    fg_k4_df = point_df.query(f' `{kind1}` == @kind1_df.index[4] ')

    fg_k0 = folium.FeatureGroup(name=f'{kind1_df.index[0]}') 
    fg_k1 = folium.FeatureGroup(name=f'{kind1_df.index[1]}') 
    fg_k2 = folium.FeatureGroup(name=f'{kind1_df.index[2]}') 
    fg_k3 = folium.FeatureGroup(name=f'{kind1_df.index[3]}') 
    fg_k4 = folium.FeatureGroup(name=f'{kind1_df.index[4]}') 

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
    
    # folium.Marker([, ]).add_to(fg_k0) -------------------------------
    for index, row in fg_k0_df.iterrows(): 
        if not pd.isna(row[f'{LATITUDE}']) and not pd.isna(row[f'{LONGITUDE}']):
            folium.CircleMarker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 원 중심
                                radius=1,            # 원 반지름
                                color='blue',        # 원 테두리 색상
                                fill=True,           # 원 채움
                                fill_opacity=0.5,     # 원 채움 투명도
                                ).add_to(fg_k0) 
                      
            folium.Marker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 값 중심 
                        popup=f"{row[f'{KIND2}']} ( {row[f'{KEYWORD}']} ) ", 
                        tooltip=row[f'{LATITUDE}'], 
                        icon=folium.Icon(color='red', icon='star'), 
                        #   icon=folium.DivIcon(                              # 값 표시방식
                        #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
                        ).add_to(fg_k0) 

    # folium.Marker([, ]).add_to(fg_k1) -------------------------------
    for index, row in fg_k1_df.iterrows(): 
        if not pd.isna(row[f'{LATITUDE}']) and not pd.isna(row[f'{LONGITUDE}']):
            folium.CircleMarker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 원 중심
                                radius=1,            # 원 반지름
                                color='blue',        # 원 테두리 색상
                                fill=True,           # 원 채움
                                fill_opacity=0.5,     # 원 채움 투명도
                                ).add_to(fg_k1) 
                      
            folium.Marker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 값 중심 
                        popup=f"{row[f'{KIND2}']} ( {row[f'{KEYWORD}']} ) ", 
                        tooltip=row[f'{LATITUDE}'], 
                        icon=folium.Icon(color='darkgreen', icon='star'), 
                        #   icon=folium.DivIcon(                              # 값 표시방식
                        #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
                        ).add_to(fg_k1) 

    # folium.Marker([, ]).add_to(fg_k2) -------------------------------
    for index, row in fg_k2_df.iterrows(): 
        if not pd.isna(row[f'{LATITUDE}']) and not pd.isna(row[f'{LONGITUDE}']):
            folium.CircleMarker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 원 중심
                                radius=1,            # 원 반지름
                                color='blue',        # 원 테두리 색상
                                fill=True,           # 원 채움
                                fill_opacity=0.5,     # 원 채움 투명도
                                ).add_to(fg_k2) 
                      
            folium.Marker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 값 중심 
                        popup=f"{row[f'{KIND2}']} ( {row[f'{KEYWORD}']} ) ", 
                        tooltip=row[f'{LATITUDE}'], 
                        icon=folium.Icon(color='orange', icon='star'), 
                        #   icon=folium.DivIcon(                              # 값 표시방식
                        #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
                        ).add_to(fg_k2) 

    # folium.Marker([, ]).add_to(fg_k3) -------------------------------
    for index, row in fg_k3_df.iterrows(): 
        if not pd.isna(row[f'{LATITUDE}']) and not pd.isna(row[f'{LONGITUDE}']):
            folium.CircleMarker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 원 중심
                                radius=1,            # 원 반지름
                                color='blue',        # 원 테두리 색상
                                fill=True,           # 원 채움
                                fill_opacity=0.5,     # 원 채움 투명도
                                ).add_to(fg_k3) 
                      
            folium.Marker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 값 중심 
                        popup=f"{row[f'{KIND2}']} ( {row[f'{KEYWORD}']} ) ", 
                        tooltip=row[f'{LATITUDE}'], 
                        icon=folium.Icon(color='blue', icon='star'), 
                        #   icon=folium.DivIcon(                              # 값 표시방식
                        #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
                        ).add_to(fg_k3) 

    # folium.Marker([, ]).add_to(fg_k4) -------------------------------
    for index, row in fg_k4_df.iterrows(): 
        if not pd.isna(row[f'{LATITUDE}']) and not pd.isna(row[f'{LONGITUDE}']):
            folium.CircleMarker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 원 중심
                                radius=1,            # 원 반지름
                                color='blue',        # 원 테두리 색상
                                fill=True,           # 원 채움
                                fill_opacity=0.5,     # 원 채움 투명도
                                ).add_to(fg_k4) 
                      
            folium.Marker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 값 중심 
                        popup=f"{row[f'{KIND2}']} ( {row[f'{KEYWORD}']} ) ", 
                        tooltip=row[f'{LATITUDE}'], 
                        icon=folium.Icon(color='yellow', icon='star'), 
                        #   icon=folium.DivIcon(                              # 값 표시방식
                        #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
                        ).add_to(fg_k4)  

    # map.add_child(fg_???) 
    map.add_child(fg_k0)
    map.add_child(fg_k1)
    map.add_child(fg_k2)
    map.add_child(fg_k3)
    map.add_child(fg_k4)

    # 
    # folium.LayerControl(collapsed=False).add_to(map)

    GroupedLayerControl(groups={  f'{kind1}': [fg_k0, fg_k1, fg_k2, fg_k3, fg_k4]  }, 
                        exclusive_groups=False, 
                        collapsed=True, 
                        ).add_to(map)

    folium_map = map._repr_html_()
    st.components.v1.html(folium_map, height=900) #, width=800, height=600) 






# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ p x @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px pie

# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_px_pie(organ, kind1): 
    # data  
    month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

    # colors = ['darkgray',] * 5

    fig = px.pie(kind1_df, values=kind1_df.NUMBER, names=kind1_df.KIND1,                   
                 
                #  title="pie chart test...", 
                 labels={'KIND1':'민원 유형', 'NUMBER':'발생 건수'}, 

                 hole=0.4,
                ) 
    
    fig.update_traces(marker=dict(colors=px.colors.qualitative.Dark24, # colors
                                  line=dict(color='black', width=2)), 

                                #   hoverinfo='label+percent',

                                  textinfo='value+percent',   # 'value' or 'value+percent'
                                  textfont_size=20, 
                                  textposition='inside',
                  )

    # fig.update_layout( ) 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 옵션 시작 @ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
   
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 타이틀  
    # add a title 옵션
    # fig.update_layout(title=dict(text='<b>     관련 불량 위치 수</b><br><sup>Check All Error Pin Point by Portion</sup>',        # <br> 태크와 <sup>태그 사용해서 서브 타이틀을 작성할 수 있음 
    #                              x=0.0, 
    #                              y=0.9, 
    #                              font=dict(family="Arial", size=25, color="#000000"), 
    #                             ),
    #                  )   
    
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 범례  
    # legend 감추기 ... 
    fig.update_layout(showlegend=True) 

    # add a legend 옵션 
    fig.update_layout(# 범례 위치
    #                   legend_x = 0.01,  # (0~1) 사이값
    #                   legend_y = 0.99,  # (0~1) 사이값
    #                   legend_xanchor = "left",  # (`auto","left","center","right")
    #                   legend_yanchor = "top",   # ("auto","top","middle","bottom")

    #                   # 범례 스타일 
    #                   legend_title_text='성별',                     # 타이틀명 text 입력       
    #                   legend_title_font_family = "Times New Roman", # 범례 타이틀 서체 (HTML font family)
    #                   legend_title_font_color="red",                # 범례 타이틀 색
    #                   legend_title_font_size= 20,                   # 범례 타이틀 글자 크기
    #                   legend_font_family="Courier",         # 범례 서체 (HTML font family)
                      legend_font_size=14,                  # 범례 글자 크기
    #                   legend_font_color="black",            # 범례 색
    #                   legend_bgcolor="LightSteelBlue",  # 범례 배경색
    #                   legend_bordercolor="Black",       # 범례 테두리 색
    #                   legend_borderwidth=2,             # 범례 테두리 두깨

    #                   margin = dict(l=10, r=10, b=10), 
                     ) 
    


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 옵션 종료 @ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



    return fig 




# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ CSS COLOR 
# aliceblue, antiquewhite, aqua, aquamarine, azure,
# beige, bisque, black, blanchedalmond, blue,
# blueviolet, brown, burlywood, cadetblue,
# chartreuse, chocolate, coral, cornflowerblue,
# cornsilk, crimson, cyan, darkblue, darkcyan,
# darkgoldenrod, darkgray, darkgrey, darkgreen,
# darkkhaki, darkmagenta, darkolivegreen, darkorange,
# darkorchid, darkred, darksalmon, darkseagreen,
# darkslateblue, darkslategray, darkslategrey,
# darkturquoise, darkviolet, deeppink, deepskyblue,
# dimgray, dimgrey, dodgerblue, firebrick,
# floralwhite, forestgreen, fuchsia, gainsboro,
# ghostwhite, gold, goldenrod, gray, grey, green,
# greenyellow, honeydew, hotpink, indianred, indigo,
# ivory, khaki, lavender, lavenderblush, lawngreen,
# lemonchiffon, lightblue, lightcoral, lightcyan,
# lightgoldenrodyellow, lightgray, lightgrey,
# lightgreen, lightpink, lightsalmon, lightseagreen,
# lightskyblue, lightslategray, lightslategrey,
# lightsteelblue, lightyellow, lime, limegreen,
# linen, magenta, maroon, mediumaquamarine,
# mediumblue, mediumorchid, mediumpurple,
# mediumseagreen, mediumslateblue, mediumspringgreen,
# mediumturquoise, mediumvioletred, midnightblue,
# mintcream, mistyrose, moccasin, navajowhite, navy,
# oldlace, olive, olivedrab, orange, orangered,
# orchid, palegoldenrod, palegreen, paleturquoise,
# palevioletred, papayawhip, peachpuff, peru, pink,
# plum, powderblue, purple, red, rosybrown,
# royalblue, rebeccapurple, saddlebrown, salmon,
# sandybrown, seagreen, seashell, sienna, silver,
# skyblue, slateblue, slategray, slategrey, snow,
# springgreen, steelblue, tan, teal, thistle, tomato,
# turquoise, violet, wheat, white, whitesmoke,
# yellow, yellowgreen


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ g o @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create go Scatter  
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_go_Scatter(organ, kind1): 
    # data  
    month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Create subplot grid
    fig = make_subplots(rows=1, cols=1,   specs= [  [  {"secondary_y": True}  ]  ]   )

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Add traces to the subplot grid : Scatter chart 
    fig.add_trace(go.Scatter(x=month_df.DATE, y=month_df.NUMBER, 
                             mode="lines+markers+text", fill='tozeroy',   # lines+markers+text 
                             line=dict(width=0.5, 
                                       color='skyblue'),
                             marker=dict(size=30, # month_df.NUMBER,
                                         color='antiquewhite', 
                                        #  color=np.random.randn(400).cumsum(), colorscale='YlOrRd', showscale=True
                                         ), 
                             text=month_df.NUMBER, # textposition="top center",  # "bottom center" 
                             hoverinfo="x+y", 
                             name="Markers A",
                             ), 
                  row=1, col=1, secondary_y=False, 
                  )  

    fig.update_traces( 
                      textfont_size=20, textfont_color='black', 
                     ) 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 옵션 시작 @ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 센터 
    # Bar mode 옵션 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ center 1
    # fig.update_layout(barmode='relative',          # barmode='stack' 음수값 에러 ~~ 
    #                   bargap=0.5,                  # barmode='group', bargroupgab=0.5, 
    #                  )

    # 가로 세로 마진 배경 옵션 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ center 2
    # fig.update_layout(autosize=False, width=400, height=400,
    #                   margin=dict(l=10, r=20, t=30, b=40, pad=4),

    #                   paper_bgcolor='skyblue', 
    #                  ) 
    
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 타이틀  
    # add a title 옵션
    # fig.update_layout(title=dict(text='<b>     관련 불량 위치 수</b><br><sup>Check All Error Pin Point by Portion</sup>',        # <br> 태크와 <sup>태그 사용해서 서브 타이틀을 작성할 수 있음 
    #                              x=0.0, 
    #                              y=0.9, 
    #                              font=dict(family="Arial", size=25, color="#000000"), 
    #                             ),
    #                  )   
    
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 범례  
    # legend 감추기 ... 
    # fig.update_layout(showlegend=True) 

    # add a legend 옵션 
    # fig.update_layout(# 범례 위치
    #                   legend_x = 0.01,  # (0~1) 사이값
    #                   legend_y = 0.99,  # (0~1) 사이값
    #                   legend_xanchor = "left",  # (`auto","left","center","right")
    #                   legend_yanchor = "top",   # ("auto","top","middle","bottom")

    #                   # 범례 스타일 
    #                   legend_title_text='성별',                     # 타이틀명 text 입력       
    #                   legend_title_font_family = "Times New Roman", # 범례 타이틀 서체 (HTML font family)
    #                   legend_title_font_color="red",                # 범례 타이틀 색
    #                   legend_title_font_size= 20,                   # 범례 타이틀 글자 크기
    #                   legend_font_family="Courier",         # 범례 서체 (HTML font family)
    #                   legend_font_size=12,                  # 범례 글자 크기
    #                   legend_font_color="black",            # 범례 색
    #                   legend_bgcolor="LightSteelBlue",  # 범례 배경색
    #                   legend_bordercolor="Black",       # 범례 테두리 색
    #                   legend_borderwidth=2,             # 범례 테두리 두깨

    #                   margin = dict(l=10, r=10, b=10), 
    #                  ) 
    

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ x축 
    # Set xaxis title
    # fig.update_xaxes(title_text="<b>xaxis</b> title") 
    # fig.update_xaxes(title_font=dict(size=38, family='Courier', color='orange')) 

    # xaxis tick 감추기 ... 
    # fig.update_xaxes(showticklabels=False) 

    # add a xaxis tick 옵션 
    # fig.update_xaxes(tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'
    # fig.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=18))
    # fig.update_xaxes(ticks='inside', tickwidth=4, tickcolor='orange', ticklen=5) 

    # fig.update_xaxes(range=[0, 5])

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ y축 
    # Set yaxis titles
    # fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False) 
    # fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True) 

    # fig.update_yaxes(title_font=dict(size=18, family='Courier', color='black')) 

    # yaxis tick 감추기 ... 
    # fig.update_yaxes(showticklabels=True)  

    # add a yaxis tick 옵션 
    # fig.update_yaxes(tickformat = '%') 
    # fig.update_yaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=18))
    # fig.update_yaxes(ticks='outside', tickwidth=2, tickcolor='purple', ticklen=10, col=1) 

    # fig.update_yaxes(range=[0, 10])

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 기타  
    # Set a grid and zeroline 감추기 ...
    # fig.update_xaxes(showgrid=False, zeroline=False)
    # fig.update_yaxes(showgrid=False, zeroline=False)

    # Set a grid 옵션  
    fig.update_xaxes(showgrid=False, linewidth=3, linecolor='red')  #, mirror=True)
    fig.update_yaxes(showgrid=True, linewidth=3, linecolor='red')   #, mirror=True)
   
    # Set a zeroline 옵션  
    fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='blue')
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='orange')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 옵션 종료 @ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    return fig 



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create go Bar  
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_go_Bar(organ, kind1): 
    # data  
    month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

    month_df = month_df.iloc[:5,:] 

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Create subplot grid
    fig = make_subplots(rows=1, cols=1,   specs= [  [  {"secondary_y": True}  ]  ]   )

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Add traces to the subplot grid : Bar chart 
    fig.add_trace(go.Bar(x=month_df.DATE, y=month_df.NUMBER, 

                         marker_color = px.colors.qualitative.Dark24,  # 'crimson'
                         text=month_df.NUMBER, textposition="inside",   # ['inside', 'outside', 'auto', 'none']
                         hoverinfo="x+y",                          
                         name="Bar A",
                         ), 
                  row=1, col=1, secondary_y=False, 
                  )  

    fig.update_traces(
                      textfont_size=20, textfont_color='black', 
                     )  
    
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 옵션 시작 @ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 센터 
    # Bar mode 옵션 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ center 1
    # fig.update_layout(barmode='relative',          # barmode='stack' 음수값 에러 ~~ 
    #                 #   bargap=0.5,                  # barmode='group', bargroupgab=0.5, 
    #                  )

    # 가로 세로 마진 배경 옵션 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ center 2
    # fig.update_layout(autosize=False, width=400, height=400,
    #                   margin=dict(l=10, r=20, t=30, b=40, pad=4),

    #                   paper_bgcolor='skyblue', 
    #                  ) 
    
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 타이틀  
    # add a title 옵션
    # fig.update_layout(title=dict(text='<b>     관련 불량 위치 수</b><br><sup>Check All Error Pin Point by Portion</sup>',        # <br> 태크와 <sup>태그 사용해서 서브 타이틀을 작성할 수 있음 
    #                              x=0.0, 
    #                              y=0.9, 
    #                              font=dict(family="Arial", size=25, color="#000000"), 
    #                             ),
    #                  )   
    
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 범례  
    # legend 감추기 ... 
    # fig.update_layout(showlegend=True) 

    # add a legend 옵션 
    # fig.update_layout(# 범례 위치
    #                   legend_x = 0.01,  # (0~1) 사이값
    #                   legend_y = 0.99,  # (0~1) 사이값
    #                   legend_xanchor = "left",  # (`auto","left","center","right")
    #                   legend_yanchor = "top",   # ("auto","top","middle","bottom")

    #                   # 범례 스타일 
    #                   legend_title_text='성별',                     # 타이틀명 text 입력       
    #                   legend_title_font_family = "Times New Roman", # 범례 타이틀 서체 (HTML font family)
    #                   legend_title_font_color="red",                # 범례 타이틀 색
    #                   legend_title_font_size= 20,                   # 범례 타이틀 글자 크기
    #                   legend_font_family="Courier",         # 범례 서체 (HTML font family)
    #                   legend_font_size=12,                  # 범례 글자 크기
    #                   legend_font_color="black",            # 범례 색
    #                   legend_bgcolor="LightSteelBlue",  # 범례 배경색
    #                   legend_bordercolor="Black",       # 범례 테두리 색
    #                   legend_borderwidth=2,             # 범례 테두리 두깨

    #                   margin = dict(l=10, r=10, b=10), 
    #                  ) 
    

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ x축 
    # Set xaxis title
    # fig.update_xaxes(title_text="<b>xaxis</b> title") 
    # fig.update_xaxes(title_font=dict(size=38, family='Courier', color='orange')) 

    # xaxis tick 감추기 ... 
    # fig.update_xaxes(showticklabels=False) 

    # add a xaxis tick 옵션 
    fig.update_xaxes(tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'
    fig.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=14))
    fig.update_xaxes(ticks='inside', tickwidth=4, tickcolor='orange', ticklen=5) 

    # fig.update_xaxes(range=[0, 5])

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ y축 
    # Set yaxis titles
    # fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False) 
    # fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True) 

    # fig.update_yaxes(title_font=dict(size=18, family='Courier', color='black')) 

    # yaxis tick 감추기 ... 
    # fig.update_yaxes(showticklabels=True)  

    # add a yaxis tick 옵션
    # fig.update_yaxes(tickformat = '%') 
    fig.update_yaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=14))
    # fig.update_yaxes(ticks='outside', tickwidth=2, tickcolor='purple', ticklen=10, col=1) 

    # fig.update_yaxes(range=[0, 10])

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 기타  
    # Set a grid and zeroline 감추기 ...
    # fig.update_xaxes(showgrid=False, zeroline=False)
    # fig.update_yaxes(showgrid=False, zeroline=False)

    # Set a grid 옵션  
    fig.update_xaxes(showgrid=True, linewidth=3, linecolor='red')  #, mirror=True)
    fig.update_yaxes(showgrid=True, linewidth=3, linecolor='red')   #, mirror=True)
   
    # Set a zeroline 옵션  
    # fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='blue')
    # fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='orange') 



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 옵션 종료 @ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    return fig 



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create go Candlestick 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_go_Candlestick(organ, kind1): 
    # data  
    # month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================
    t = np.linspace(0, 10, 5)
    y1 = np.random.randn(5).cumsum()
    y2 = np.random.randn(5).cumsum()
    y3 = np.random.randn(5).cumsum()
    y4 = np.random.randn(5).cumsum()

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Create subplot grid
    fig = make_subplots(rows=1, cols=1,   specs= [  [  {"secondary_y": True}  ]  ]   )

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Add traces to the subplot grid : Candlestrick chart
    fig.add_trace(go.Candlestick(x=t,
                                 open=y1,
                                 high=y2,
                                 low=y3, 
                                 close=y4,
                                 increasing_line_color='red', 
                                 decreasing_line_color='blue',),
                  row=1, col=1, secondary_y=False, 
                  )
    # fig.update_traces( )
    # fig.update_layout( )
    return fig 
        


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create go Box 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_go_Box(organ, kind1): 
    # data  
    # month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================
    y1 = np.random.randn(50)
    y2 = np.random.randn(50) + 5



    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Create subplot grid
    fig = make_subplots(rows=1, cols=1,   specs= [  [  {"secondary_y": True}  ]  ]   )

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Add traces to the subplot grid : Bar chart 
    fig.add_trace(go.Box(y=y1, 

                         line_color='green',
                         marker_color='green', 
                         name="Box A",
                         ), 
                  row=1, col=1, secondary_y=False, 
                  )  
    
    fig.add_trace(go.Box(y=y2, 
                         
                         line_color='royalblue', 
                         marker_color='skyblue', 
                         name="Box B",

                         ), 
                  row=1, col=1, secondary_y=False, 
                  )  
    # fig.update_traces( )   
    # fig.update_layout(
    #     # showlegend=False, 
    #                   ) 

    return fig 



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create go Histogram  
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_go_Histogram(organ, kind1): 
    # data  
    # month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================
    n1 = np.random.randn(100)
    n2 = np.random.randn(100) + 1



    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Create subplot grid
    fig = make_subplots(rows=1, cols=1,   specs= [  [  {"secondary_y": True}  ]  ]   )

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Add traces to the subplot grid : Bar chart 
    fig.add_trace(go.Histogram(x=n1,                                
                         name="Histogram A",
                         ), 
                  row=1, col=1, secondary_y=False, 
                  )  
    
    fig.add_trace(go.Histogram(x=n2, 
                         name="Histogram B",
                         ), 
                  row=1, col=1, secondary_y=False, 
                  )  

    fig.update_traces(opacity=0.7)   
    fig.update_layout(barmode='overlay',       # barmode='stack' 음수값 에러 ~~ 
                    #   showlegend=False, 
                      ) 

    return fig 



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create go Heatmap   
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_go_Heatmap(organ, kind1): 
    # data  
    # month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================
    t = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    w = ['Morning', 'Afternoon', 'Evening']
    n = np.random.randint(1, 100, size=(3, 7)) 

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Create subplot grid
    fig = make_subplots(rows=1, cols=1,   specs= [  [  {"secondary_y": True}  ]  ]   )

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Add traces to the subplot grid : Bar chart 
    fig.add_trace(go.Heatmap(x=t, y=w, z=n,                                 
                         name="Heatmap A",
                         ), 
                  row=1, col=1, secondary_y=False, 
                  )  
    
    # fig.update_traces( )   
    fig.update_layout(
        # showlegend=False, 
                      ) 

    return fig 



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ CSS COLOR 
# aliceblue, antiquewhite, aqua, aquamarine, azure,
# beige, bisque, black, blanchedalmond, blue,
# blueviolet, brown, burlywood, cadetblue,
# chartreuse, chocolate, coral, cornflowerblue,
# cornsilk, crimson, cyan, darkblue, darkcyan,
# darkgoldenrod, darkgray, darkgrey, darkgreen,
# darkkhaki, darkmagenta, darkolivegreen, darkorange,
# darkorchid, darkred, darksalmon, darkseagreen,
# darkslateblue, darkslategray, darkslategrey,
# darkturquoise, darkviolet, deeppink, deepskyblue,
# dimgray, dimgrey, dodgerblue, firebrick,
# floralwhite, forestgreen, fuchsia, gainsboro,
# ghostwhite, gold, goldenrod, gray, grey, green,
# greenyellow, honeydew, hotpink, indianred, indigo,
# ivory, khaki, lavender, lavenderblush, lawngreen,
# lemonchiffon, lightblue, lightcoral, lightcyan,
# lightgoldenrodyellow, lightgray, lightgrey,
# lightgreen, lightpink, lightsalmon, lightseagreen,
# lightskyblue, lightslategray, lightslategrey,
# lightsteelblue, lightyellow, lime, limegreen,
# linen, magenta, maroon, mediumaquamarine,
# mediumblue, mediumorchid, mediumpurple,
# mediumseagreen, mediumslateblue, mediumspringgreen,
# mediumturquoise, mediumvioletred, midnightblue,
# mintcream, mistyrose, moccasin, navajowhite, navy,
# oldlace, olive, olivedrab, orange, orangered,
# orchid, palegoldenrod, palegreen, paleturquoise,
# palevioletred, papayawhip, peachpuff, peru, pink,
# plum, powderblue, purple, red, rosybrown,
# royalblue, rebeccapurple, saddlebrown, salmon,
# sandybrown, seagreen, seashell, sienna, silver,
# skyblue, slateblue, slategray, slategrey, snow,
# springgreen, steelblue, tan, teal, thistle, tomato,
# turquoise, violet, wheat, white, whitesmoke,
# yellow, yellowgreen



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create go Bar  
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_go_ScatterBar(organ, kind1): 
    # data  
    month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

    month_df = month_df.iloc[:5,:] 

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Create subplot grid
    fig = make_subplots(rows=1, cols=1,   specs= [  [  {"secondary_y": True}  ]  ]   )

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Add traces to the subplot grid : Bar chart 
    fig.add_trace(go.Bar(x=month_df.DATE, y=month_df.NUMBER, 

                         marker_color = px.colors.qualitative.Dark24,  # '_pct_change'
                         text=month_df.NUMBER, textposition="inside",   # ['inside', 'outside', 'auto', 'none']
                         hoverinfo="x+y",                          
                         name="월 발생(건)",
                         ), 
                  row=1, col=1, secondary_y=False, 
                  )  
    
    fig.add_trace(go.Scatter(x=month_df.DATE, y=month_df.NUMBER_pct_change, 
                             mode="lines+markers+text", # fill='tonexty',   # lines+markers+text   /  tozeroy
                             line=dict(width=1.5, color='red'),   # skyblue
                             marker=dict(size=50, # month_df.NUMBER,
                                         color='antiquewhite', 
                                        #  color=np.random.randn(400).cumsum(), colorscale='YlOrRd', showscale=True
                                         ), 
                             text=month_df.NUMBER_pct_change, # textposition="top center",  # "bottom center" 
                             hoverinfo="x+y",                          
                             name="월 증감(%)",
                             ), 
                  row=1, col=1, secondary_y=True, 
                  )  
    
    fig.update_traces(
                      textfont_size=20, textfont_color='black', 
                     ) 
    
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 옵션 시작 @ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 센터 
    # Bar mode 옵션 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ center 1
    # fig.update_layout(barmode='relative',          # barmode='stack' 음수값 에러 ~~ 
    #                 #   bargap=0.5,                  # barmode='group', bargroupgab=0.5, 
    #                  )

    # 가로 세로 마진 배경 옵션 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ center 2
    # fig.update_layout(autosize=False, width=400, height=400,
    #                   margin=dict(l=10, r=20, t=30, b=40, pad=4),

    #                   paper_bgcolor='skyblue', 
    #                  ) 
    
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 타이틀  
    # add a title 옵션
    # fig.update_layout(title=dict(text=f'<b>📢 {organ} : 민원 건 수</b> 현황',        # <br> 태크와 <sup>태그 사용해서 서브 타이틀을 작성할 수 있음 
    #                              x=0.0, 
    #                              y=0.9, 
    #                              font=dict(family="Arial", size=22, color="#000000"), 
    #                             ),
    #                  )   
    
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 범례  
    # legend 감추기 ... 
    fig.update_layout(showlegend=True) 

    # add a legend 옵션 
    fig.update_layout(# 범례 위치
                      legend_orientation = "h",
                      legend_x = 0.90,  # (0~1) 사이값
                      legend_y = 0.01,  # (0~1) 사이값
                      legend_xanchor = "right",  # ("auto","left","center","right")
                      legend_yanchor = "auto",   # ("auto","top","middle","bottom")

    #                   # 범례 스타일 
    #                   legend_title_text='성별',                     # 타이틀명 text 입력       
    #                   legend_title_font_family = "Times New Roman", # 범례 타이틀 서체 (HTML font family)
    #                   legend_title_font_color="red",                # 범례 타이틀 색
                    #   legend_title_font_size= 20,                   # 범례 타이틀 글자 크기
    #                   legend_font_family="Courier",         # 범례 서체 (HTML font family)
                      legend_font_size=14,                  # 범례 글자 크기
    #                   legend_font_color="black",            # 범례 색
    #                   legend_bgcolor="LightSteelBlue",  # 범례 배경색
    #                   legend_bordercolor="Black",       # 범례 테두리 색
    #                   legend_borderwidth=2,             # 범례 테두리 두깨

    #                   margin = dict(l=10, r=10, b=10), 
                     ) 
    

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ x축 
    # Set xaxis title
    # fig.update_xaxes(title_text="<b>xaxis</b> title") 
    # fig.update_xaxes(title_font=dict(size=38, family='Courier', color='orange')) 

    # xaxis tick 감추기 ... 
    # fig.update_xaxes(showticklabels=False) 

    # add a xaxis tick 옵션 
    fig.update_xaxes(tickformat = '%m<br>%Y', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'
    fig.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=18))
    fig.update_xaxes(ticks='inside', tickwidth=4, tickcolor='orange', ticklen=5) 

    # fig.update_xaxes(range=[0, 5])

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ y축 
    # Set yaxis titles
    # fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False) 
    # fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True) 

    # fig.update_yaxes(title_font=dict(size=18, family='Courier', color='black')) 

    # yaxis tick 감추기 ... 
    fig.update_yaxes(showticklabels=False)  

    # add a yaxis tick 옵션
    # fig.update_yaxes(tickformat = '%') 
    fig.update_yaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=18))
    # fig.update_yaxes(ticks='outside', tickwidth=2, tickcolor='purple', ticklen=10, col=1) 

    # fig.update_yaxes(range=[0, 10])

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 기타  
    # Set a grid and zeroline 감추기 ...
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    # Set a grid 옵션  
    # fig.update_xaxes(showgrid=True, linewidth=3, linecolor='red')  #, mirror=True)
    # fig.update_yaxes(showgrid=True, linewidth=3, linecolor='red')   #, mirror=True)
   
    # Set a zeroline 옵션  
    # fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='blue')
    # fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='orange')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 옵션 종료 @ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    return fig 



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ figure factory @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create ff Heatmap   
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_ff_Heatmap(organ, kind1): 
    # data  
    # month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================
    t = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    w = ['Morning', 'Afternoon', 'Evening']
    n = np.random.randint(1, 100, size=(3, 7)) 

    fig = ff.create_annotated_heatmap(x=t, y=w, z=n)

    return fig 




    # fig.add_trace(
    #     go.Bar(x=month_df.DATE, y=month_df.NUMBER, 
    #            marker_color=px.colors.qualitative.Dark24, 
    #            text=month_df.NUMBER, textposition="inside",   # ['inside', 'outside', 'auto', 'none']
    #            name='bA'), 
    #     row=1, col=1, secondary_y=False,                  
    # )

    # fig.add_trace(
    #     go.Bar(x=month_df.DATE, y=month_df.NUMBER, 
    #            marker_color=px.colors.qualitative.Dark24,
    #            text=month_df.NUMBER, textposition="inside",   # ['inside', 'outside', 'auto', 'none']
    #            name='bA'), 
    #     row=1, col=1, secondary_y=True,                  
    # )

    # fig.add_trace(
    #     go.Scatter(x=month_df.DATE, 
    #                y=month_df.NUMBER, 
    #                mode="lines+markers+text", marker_color='darkblue'
    #                name="Lines, Markers and Text",
    #                text=month_df.NUMBER,              #["Text A", "Text B", "Text C"],
    #                textposition="top center"),  # "bottom center"), 
    #     row=1, col=1                                    
    # )         

    # Update figure if necessary ????




#     # Update layout if necessary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``
#     # Add figure title
#     fig.update_layout(title=dict(text='<b>     관련 불량 위치 수</b><br><sup>Check All Error Pin Point by Portion</sup>',        # <br> 태크와 <sup>태그 사용해서 서브 타이틀을 작성할 수 있음 
#                                  x=0.0, 
#                                  y=0.9, 
#                                  font=dict(family="Arial",
#                                            size=25,
#                                            color="#000000", ), 
#                                 ),
#                       # 범례  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                       showlegend=True,         

#                       # 범례 위치
#                       legend_x = 0.01,  # (0~1) 사이값
#                       legend_y = 0.99,  # (0~1) 사이값
#                       legend_xanchor = "left",  # (`auto","left","center","right")
#                       legend_yanchor = "top",   # ("auto","top","middle","bottom")

#                       # 범례 스타일 
#                       legend_title_text='성별',                     # 타이틀명 text 입력       
#                       legend_title_font_family = "Times New Roman", # 범례 타이틀 서체 (HTML font family)
#                       legend_title_font_color="red",                # 범례 타이틀 색
#                       legend_title_font_size= 20,                   # 범례 타이틀 글자 크기
#                       legend_font_family="Courier",         # 범례 서체 (HTML font family)
#                       legend_font_size=12,                  # 범례 글자 크기
#                       legend_font_color="black",            # 범례 색
#                       legend_bgcolor="LightSteelBlue",  # 범례 배경색
#                       legend_bordercolor="Black",       # 범례 테두리 색
#                       legend_borderwidth=2,             # 범례 테두리 두깨

#                       margin = dict(l=10, r=10, b=10), 
#     ) 

#     # Set x-axes titles    
#     fig.update_xaxes(title_text="xaxis title")

#     # Set y-axes titles
#     fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
#     fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)
    
#     title=dict(text='<b>     관련 불량 위치 수</b><br><sup>Check All Error Pin Point by Portion</sup>',        # <br> 태크와 <sup>태그 사용해서 서브 타이틀을 작성할 수 있음 
#                                 x=0.0, 
#                                 y=0.9, 
#                                 font=dict(family="Arial",
#                                           size=25,
#                                           color="#000000", ), 
#                                ),
#     )
#                       xaxis_title=dict(text="<b>Fail Point</b>", ), 

#                       yaxis_title=dict(text="<b>Portion(%)</b>", 
#                                        font=dict(family="Courier New, Monospace",
#                                                  size=12,
#                                                  color="#000000",  ),
#                                     #   ), 
#     )
        

#     )
  
#     return fig, month_df, point_df, kind1_df, wc_data 

# ##################################################################################### 세로 막대 create vbar 
# # arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# # arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
# # def create_px_vbar(organ, kind1): 
# #     # data  
# #     month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

# #     fig = px.bar(month_df, x='DATE', y='NUMBER', color='DATE', 
# #                  title="민원 건 수 현황",
# #                  labels={"DATE":"월별", 'NUMBER':'민원 건 수', 'NUMBER_GROWTH_RATE':'증감율(%)'},
# #                 #  hover_name='DATE',
# #                  hover_data={'DATE':"|%B, %Y",
# #                              'NUMBER':True, 
# #                              'NUMBER_GROWTH_RATE':":.2f"
# #                              }, 
# #                 # # facet_row= 'species',          
# #                 # # facet_col= "species_id",
# #                 # #  width=600 , height=300 ,
# #                  ) 
# #     fig.update_layout(showlegend=False)
    
    # return fig, month_df, point_df, kind1_df, wc_data 




# ##################################################################################### 가로 막대 create sns hbar 
# # arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# # arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
# def create_sns_hbar(organ, kind1): 
#     # data  
#     month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

#     data_x = kind1_df.index.values
#     data_y = kind1_df['건수'] 

#     # preprocessing ---------------------------
#     fig,  ax = plt.subplots(figsize=(10,6)) 
#     ax.tick_params(
#         # axis=x or axis=y,
#         labelsize=20,
#         direction='inout',
#         color = 'red',
#         colors = 'blue',
#         # rotation=20, 
#         bottom = False, labelbottom=False,        # tick 수정
#         top = False, labeltop=False,
#         left = True, labelleft=True,
#         right= False, labelright=False
#         )
#     ax.set_facecolor('white')                  # figure 배경색 

#     # paint 
#     sns.barplot(x=data_y, y=data_x, 
#                 hue=data_x, 
#                 dodge=False,
#                 ax=ax) 

#     for i in range(len(data_x)):               # bar text 표시
#         width = data_y[i]+1.5 
#         width_str = str(data_y[i])+'건'
#         ax.text(width, i, width_str,
#                 # ha='center', va='bottom', 
#                 color='green',
#                 fontsize=20)                   # bar text 폰크

#     return fig, month_df, point_df, kind1_df, wc_data 

