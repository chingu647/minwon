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


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ DATABASE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ load_df 
# arg1 : global organ_ t?? ---------- 탭 페이지에서 입력
# arg2 : global kind1_ t?? ---------- 탭 페이지에서 입력
@st.cache_resource 
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


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ M A P @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ load wc 
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


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ load map 1
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



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ load map 2 
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


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ p x @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

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
    
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px scatter 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_px_scatter(organ, kind1): 
    # data  
    month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

    fig = px.scatter(kind1_df, x='KIND1', y='NUMBER',                                  # kind1_df.index
                     text='NUMBER', 
                     color='KIND1', # color_discrete_sequence=px.colors.qualitative.D3,
                    #  color='NUMBER', 
                    #  labels={'KIND1':'민원 유형', 'NUMBER':'발생 건수'}, 
                    ) 
    
    fig.update_traces(marker=dict(size=60), 
                      textfont_size=20, textfont_color='black', # textposition='top center',   # ['top left', 'top center', 'top right', 'middle left', 'middle center', 'middle right', 'bottom left', 'bottom center', 'bottom right'] 
                      showlegend=False,
                     ) 
    fig.update_coloraxes(showscale=False) 

    # fig = px.colors.qualitative.swatches() 
    return fig, month_df, point_df, kind1_df, wc_data 

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px line 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_px_line(organ, kind1): 
    # data  
    month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

    fig = px.line(kind1_df, x='KIND1', y='NUMBER',                                  # kind1_df.index
                  color='NUMBER', 
                #   labels={'KIND1':'민원 유형', 'NUMBER':'발생 건수'},
                  text='NUMBER' ) 
                    #  trendline='lowess')   # 연속 데이터 만 ['lowess', 'rolling', 'ewm', 'expanding', 'ols']
    
    fig.update_traces(textfont_size=20, textposition='top center',   # ['top left', 'top center', 'top right', 'middle left', 'middle center', 'middle right', 'bottom left', 'bottom center', 'bottom right'] 
                    #   showlegend=False,
                     ) 

    return fig, month_df, point_df, kind1_df, wc_data 


# fig = px.colors.qualitative.swatches()
# fig.show()

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px bar 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_px_bar(organ, kind1): 
    # data  
    month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

    fig = px.bar(kind1_df, x='KIND1', y='NUMBER',    # kind1_df.index
                 color='KIND1', 
                #  labels={'KIND1':'민원 유형', 'NUMBER':'발생 건수'}, 
                 text='NUMBER', 
                #  hover_data=['  ', '  '], 
                #  barmode='group', 
                      ) 
    
    fig.update_traces(textfont_size=20, textposition='auto',   # ['inside', 'outside', 'auto', 'none']   
                    #   showlegend=False
                     )

    return fig, month_df, point_df, kind1_df, wc_data 

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px pie 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_px_pie(organ, kind1): 
    # data  
    month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

    fig = px.pie(kind1_df, values=kind1_df.NUMBER, names=kind1_df.KIND1, 
                #  labels={'KIND1':'민원 유형', 'NUMBER':'발생 건수'}, 
                 hole=0.4,) 

    fig.update_traces(textfont_size=20, textposition='auto',    # ['inside', 'outside', 'auto', 'none']   
                    #   showlegend=False
                      )

    return fig, month_df, point_df, kind1_df, wc_data 
