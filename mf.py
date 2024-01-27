import streamlit as st 
import plotly.express as px
import plotly.graph_objects as go 
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


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-1) ST CACHE 사용

############################################################################################################################# load_df 
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
    month_df['NUMBER_GROWTH_RATE'] = month_df['NUMBER'].pct_change(periods=1)
    month_df['NUMBER_CUMSUM'] = month_df['NUMBER'].transform('cumsum') 
    # month_df = month_df.assign(NUMBER_DELTA=month_df.NUMBER_CUMSUM - month_df.NUMBER) 
    
    # map data : 위경도 없는 자료는 제외 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    point_df = df[ ~( (df[f'{LATITUDE}'].isna()) | (df[f'{LONGITUDE}'].isna()) ) ] 

    kind1_df = point_df.groupby(by=f'{kind1}').count().reset_index()  #.sort_values(by=f'{kind1}', ascending=False) 
    # kind1_df = kind1_df.iloc
    # kind1_df['건수'] = kind1_df['건수'].astype(int)
    # kind1_df['비율(%)'] = ( kind1_df.iloc[0,0]/(kind1_df.iloc[0,0].sum())*100).astype(int)

    # kind1_df = kind1_df.sort_values(by='건수', ascending=False) 

    # map data
    # point_df = df[ (df['latitude'].str.strip() != '') and (df['longitude'].str.strip() != '') ] 

    # wc data
    wc_sr = df.loc[:, f'{KEYWORD}']
    wc_data = ' '.join( map(str,wc_sr) )

    return month_df, point_df, kind1_df, wc_data  

load_df('본부','KIND1')

# ############################################################################################################################# load wc 
# # arg1 : text_raw 
# @st.cache_resource 
# def load_wc(organ, kind1): # target_layout 에러 발생 
#     # data  
#     month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <================================================== 
#     t = Okt()
#     text_nouns = t.nouns(wc_data) 
#     stopwords =['시어','및','조치','예정','민원','처리','해당','통해','방향','후','검토','확인','완료','내','노력','등','위해','위하여','지사',
#                 '대하','대하여','대해','대한','도록','토록','하도록','되도록','말씀','수','음','귀하','주신','답변','향','중','향','사항','아래','다음',
#                 '문의사항','내용','요청','요지','안내','일부','부분','미완료','관내','박준혁','대리','박준혁 대리','관련','저희','것','함','구간','고객']
#     text_nouns = [n for n in text_nouns if n not in stopwords]
#     text_str = ' '.join(text_nouns)
#     wc = WordCloud(background_color='#fdf0fd', font_path=r"data/NanumGothic.ttf", max_words=20).generate(text_str)   # '#ECF8E0'
    
#     fig, ax = plt.subplots(figsize=(6,2)) 
#     ax.axis('off')
#     ax.imshow(wc) 
#     # target_layout.pyplot(fig) 
#     return fig, month_df, point_df, kind1_df, wc_data  



# ############################################################################################################################# load map
# # arg1 : organ_ t?? ---------- 탭 페이지에서 입력
# # arg2 : kind1_ t?? ---------- 탭 페이지에서 입력
# # base_position_ t?? --------- 탭 페이지에서 입력

# @st.cache_resource 
# def load_map(organ, kind1, base_position): 

#     # CSV 컬럼 변수
#     LATITUDE = 'LATITUDE'
#     LONGITUDE = 'LONGITUDE'
#     KIND2 = 'KIND2'
#     KEYWORD = 'KEYWORD'

#     # data  
#     month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

#     map = folium.Map( location=base_position, zoom_start=9 ) #, tiles='Stamentoner') 
    
#     gpf_line = gpd.read_file("data/ex_line_KWANGJU.shp") 
#     folium.GeoJson(gpf_line, 
#                     style_function=lambda feature: {
#                         'fillColor': 'blue' , #feature['properties']['color'],
#                         'color': '#F5F6CE',
#                         'weight': 3,
#                         'dashArray': '5, 5',
#                         'fillOpacity': 0.3, 
#                     }
#                 ).add_to(map) 
    
#     for index, row in point_df.iterrows(): 
#         if not pd.isna(row[f'{LATITUDE}']) and not pd.isna(row[f'{LONGITUDE}']):
#             folium.CircleMarker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 원 중심
#                                 radius=1,            # 원 반지름
#                                 color='blue',        # 원 테두리 색상
#                                 fill=True,           # 원 채움
#                                 fill_opacity=0.5,     # 원 채움 투명도
#                                 ).add_to(map) 
                      
#             folium.Marker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 값 중심 
#                         popup=f"{row[f'{KIND2}']} ( {row[f'{KEYWORD}']} ) ", 
#                         tooltip=row[f'{LATITUDE}'], 
#                         icon=folium.Icon(color='red', icon='star'), 
#                         #   icon=folium.DivIcon(                              # 값 표시방식
#                         #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
#                         ).add_to(map) 

#     folium_map = map._repr_html_()
#     st.components.v1.html(folium_map, height=900) #, width=800, height=600)
#     # st_folium(map) #, width=600, height=400)
#     # t1_tail1.map(data=t1_gpf, latitude='latitude', longitude='longitude')  

#     return month_df, point_df, kind1_df, wc_data 



# ############################################################################################################################# load map
# # arg1 : organ_ t?? ---------- 탭 페이지에서 입력
# # arg2 : kind1_ t?? ---------- 탭 페이지에서 입력
# # base_position_ t?? --------- 탭 페이지에서 입력

# @st.cache_resource 
# def load_map_kind1(organ, kind1, base_position): 

#     # CSV 컬럼 변수
#     LATITUDE = 'LATITUDE'
#     LONGITUDE = 'LONGITUDE'
#     KIND2 = 'KIND2'
#     KEYWORD = 'KEYWORD'

#     # data  
#     month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

#     # kind1 상위 5개 : Grouped Layer Control 준비...
    
#     # if kind1 in point_df.columns:
#     #     result = folium.FeatureGroup(name=f'@kind1_df.index[0]')
#     # else:
#     #     result = "해당 열이 존재하지 않습니다." 
#     kind1_df_indexes = list(kind1_df.index)  #   -------------------------------------------------- kind1 5개는 본부 전체로 고정하면?

#     fg_k0_df = point_df.query(f' `{kind1}` == "{kind1_df_indexes[0]}" ')
#     fg_k1_df = point_df.query(f' `{kind1}` == @kind1_df.index[1] ') 
#     fg_k2_df = point_df.query(f' `{kind1}` == @kind1_df.index[2] ')
#     fg_k3_df = point_df.query(f' `{kind1}` == @kind1_df.index[3] ')
#     fg_k4_df = point_df.query(f' `{kind1}` == @kind1_df.index[4] ')

#     fg_k0 = folium.FeatureGroup(name=f'{kind1_df.index[0]}') 
#     fg_k1 = folium.FeatureGroup(name=f'{kind1_df.index[1]}') 
#     fg_k2 = folium.FeatureGroup(name=f'{kind1_df.index[2]}') 
#     fg_k3 = folium.FeatureGroup(name=f'{kind1_df.index[3]}') 
#     fg_k4 = folium.FeatureGroup(name=f'{kind1_df.index[4]}') 

#     map = folium.Map( location=base_position, zoom_start=9 ) #, tiles='Stamentoner') 

#     gpf_line = gpd.read_file("data/ex_line_KWANGJU.shp") 
#     folium.GeoJson(gpf_line, 
#                     style_function=lambda feature: {
#                         'fillColor': 'blue' , #feature['properties']['color'],
#                         'color': '#F5F6CE',
#                         'weight': 3,
#                         'dashArray': '5, 5',
#                         'fillOpacity': 0.3, 
#                     }
#                 ).add_to(map) 
    
#     # folium.Marker([, ]).add_to(fg_k0) -------------------------------
#     for index, row in fg_k0_df.iterrows(): 
#         if not pd.isna(row[f'{LATITUDE}']) and not pd.isna(row[f'{LONGITUDE}']):
#             folium.CircleMarker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 원 중심
#                                 radius=1,            # 원 반지름
#                                 color='blue',        # 원 테두리 색상
#                                 fill=True,           # 원 채움
#                                 fill_opacity=0.5,     # 원 채움 투명도
#                                 ).add_to(fg_k0) 
                      
#             folium.Marker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 값 중심 
#                         popup=f"{row[f'{KIND2}']} ( {row[f'{KEYWORD}']} ) ", 
#                         tooltip=row[f'{LATITUDE}'], 
#                         icon=folium.Icon(color='red', icon='star'), 
#                         #   icon=folium.DivIcon(                              # 값 표시방식
#                         #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
#                         ).add_to(fg_k0) 

#     # folium.Marker([, ]).add_to(fg_k1) -------------------------------
#     for index, row in fg_k1_df.iterrows(): 
#         if not pd.isna(row[f'{LATITUDE}']) and not pd.isna(row[f'{LONGITUDE}']):
#             folium.CircleMarker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 원 중심
#                                 radius=1,            # 원 반지름
#                                 color='blue',        # 원 테두리 색상
#                                 fill=True,           # 원 채움
#                                 fill_opacity=0.5,     # 원 채움 투명도
#                                 ).add_to(fg_k1) 
                      
#             folium.Marker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 값 중심 
#                         popup=f"{row[f'{KIND2}']} ( {row[f'{KEYWORD}']} ) ", 
#                         tooltip=row[f'{LATITUDE}'], 
#                         icon=folium.Icon(color='darkgreen', icon='star'), 
#                         #   icon=folium.DivIcon(                              # 값 표시방식
#                         #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
#                         ).add_to(fg_k1) 

#     # folium.Marker([, ]).add_to(fg_k2) -------------------------------
#     for index, row in fg_k2_df.iterrows(): 
#         if not pd.isna(row[f'{LATITUDE}']) and not pd.isna(row[f'{LONGITUDE}']):
#             folium.CircleMarker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 원 중심
#                                 radius=1,            # 원 반지름
#                                 color='blue',        # 원 테두리 색상
#                                 fill=True,           # 원 채움
#                                 fill_opacity=0.5,     # 원 채움 투명도
#                                 ).add_to(fg_k2) 
                      
#             folium.Marker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 값 중심 
#                         popup=f"{row[f'{KIND2}']} ( {row[f'{KEYWORD}']} ) ", 
#                         tooltip=row[f'{LATITUDE}'], 
#                         icon=folium.Icon(color='orange', icon='star'), 
#                         #   icon=folium.DivIcon(                              # 값 표시방식
#                         #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
#                         ).add_to(fg_k2) 

#     # folium.Marker([, ]).add_to(fg_k3) -------------------------------
#     for index, row in fg_k3_df.iterrows(): 
#         if not pd.isna(row[f'{LATITUDE}']) and not pd.isna(row[f'{LONGITUDE}']):
#             folium.CircleMarker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 원 중심
#                                 radius=1,            # 원 반지름
#                                 color='blue',        # 원 테두리 색상
#                                 fill=True,           # 원 채움
#                                 fill_opacity=0.5,     # 원 채움 투명도
#                                 ).add_to(fg_k3) 
                      
#             folium.Marker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 값 중심 
#                         popup=f"{row[f'{KIND2}']} ( {row[f'{KEYWORD}']} ) ", 
#                         tooltip=row[f'{LATITUDE}'], 
#                         icon=folium.Icon(color='blue', icon='star'), 
#                         #   icon=folium.DivIcon(                              # 값 표시방식
#                         #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
#                         ).add_to(fg_k3) 

#     # folium.Marker([, ]).add_to(fg_k4) -------------------------------
#     for index, row in fg_k4_df.iterrows(): 
#         if not pd.isna(row[f'{LATITUDE}']) and not pd.isna(row[f'{LONGITUDE}']):
#             folium.CircleMarker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 원 중심
#                                 radius=1,            # 원 반지름
#                                 color='blue',        # 원 테두리 색상
#                                 fill=True,           # 원 채움
#                                 fill_opacity=0.5,     # 원 채움 투명도
#                                 ).add_to(fg_k4) 
                      
#             folium.Marker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 값 중심 
#                         popup=f"{row[f'{KIND2}']} ( {row[f'{KEYWORD}']} ) ", 
#                         tooltip=row[f'{LATITUDE}'], 
#                         icon=folium.Icon(color='yellow', icon='star'), 
#                         #   icon=folium.DivIcon(                              # 값 표시방식
#                         #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
#                         ).add_to(fg_k4)  

#     # map.add_child(fg_???) 
#     map.add_child(fg_k0)
#     map.add_child(fg_k1)
#     map.add_child(fg_k2)
#     map.add_child(fg_k3)
#     map.add_child(fg_k4)

#     # 
#     # folium.LayerControl(collapsed=False).add_to(map)

#     GroupedLayerControl(groups={  f'{kind1}': [fg_k0, fg_k1, fg_k2, fg_k3, fg_k4]  }, 
#                         exclusive_groups=False, 
#                         collapsed=True, 
#                         ).add_to(map)

#     folium_map = map._repr_html_()
#     st.components.v1.html(folium_map, height=900) #, width=800, height=600) 

#     return month_df, point_df, kind1_df, wc_data 



# ############################################################################################################################# create pie
# # arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# def create_pie(organ, kind1): 
#     # data  
#     month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

#     data_x = kind1_df.index.values
#     data_y = kind1_df['건수'] 

#     # preprocessing
#     fig, ax = plt.subplots(figsize=(10,4)) 
#     ax.tick_params(
#         # axis=x or axis=y,
#         # labelsize=20,
#         direction='inout',
#         color = 'red',
#         colors = 'blue',
#         # rotation=20, 
#         bottom = True, labelbottom=True,        # tick 수정
#         top = False, labeltop=False,
#         left = True, labelleft=True,
#         right= False, labelright=False
#         )
#     ax.set_facecolor('white')                  # figure 배경색 

#     # paint 
#     explode = [0.05 for i in data_x]
#     wedgeprops={'width': 0.5, 'edgecolor': 'w', 'linewidth': 3}
#     ax.pie(data_y, labels=data_x, 
#            startangle=260,
#            counterclock=False, 
#            autopct="%.1f%%", 
#            # explode=explode,
#            # shadow=True,
#            wedgeprops=wedgeprops, 
#            textprops={'size':9}) 
#     data_cx = 0
#     data_cy = 0
#     data_val= '총' + str(kind1_df['건수'].sum()) + '건'
#     ax.text(data_cx, data_cy, data_val, 
#             ha='center', va='center', 
#             color='red',
#             fontsize=23)                           # bar text 폰크 
    
#     return fig, month_df, point_df, kind1_df, wc_data 



# ############################################################################################################################# 세로 막대 create vbar 
# # arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# # arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
# def create_vbar(organ, kind1): 
#     # data  
#     month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================

#     data_x = kind1_df.index.values
#     data_y = kind1_df['건수'] 

#     # preprocessing 
#     fig, ax = plt.subplots(figsize=(10,4)) 
#     ax.tick_params(
#         # axis=x or axis=y,
#         labelsize=20,
#         direction='inout',
#         color = 'red',
#         colors = 'blue',
#         # rotation=20, 
#         bottom = True, labelbottom=True,        # tick 수정
#         top = False, labeltop=False,
#         left = False, labelleft=False,
#         right= False, labelright=False,  
#         )
#     ax.set_facecolor('white')                  # figure 배경색 

#     # paint 
#     ax.bar(data_x, data_y, color='#E0ECF8')            # bar plot 표시
#     for i in range(len(data_x)):                        # bar text 표시
#         height = data_y[i]+0.5 
#         height_str = str(data_y[i])+'건'
#         ax.text(data_x[i], height, height_str, 
#                 ha='center', va='bottom', 
#                 color='green',
#                 fontsize=20)                           # bar text 폰크 
    
#     return fig, month_df, point_df, kind1_df, wc_data 

############################################################################################################################# 세로 막대 create vbar 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_go_scatter(organ, kind1): 
    # data  
    # month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================
    t = np.linspace(0, 10, 5)
    y1 = np.random.randn(5).cumsum()
    y2 = np.random.randn(5).cumsum()

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Create subplot grid
    fig = make_subplots(rows=1, cols=1,   specs= [  [  {"secondary_y": True}  ]  ]   )

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Add traces to the subplot grid : Scatter chart 
    fig.add_trace(go.Scatter(x=t, y=y1, 
                             mode="lines+markers", fill='tozeroy',   # lines+markers+text 
                             line=dict(width=0.5, 
                                       color='skyblue'),
                             marker=dict(size=t*5,
                                         color=t, # 'darkblue', 
                                         ), 
                            #  marker_color='darkblue', 
                            # # CSS COLOR @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
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
                             name="Markers A",
                             text=y1, textposition="top center",  # "bottom center" 
                             hoverinfo="x+y", 
                             ), 
                  row=1, col=1, secondary_y=False, 
                  )  
    fig.add_trace(go.Scatter(x=t, y=y2, 
                             mode="lines+markers", fill='tonexty', 
                             line=dict(width=0.5, 
                                       color='indigo'),
                             marker=dict(color='indigo',) , 
                             name="Markers B",
                             text=y2, textposition="top center",  # "bottom center" 
                             hoverinfo="x+y", 
                             ), 
                  row=1, col=1, secondary_y=False, 
                  )    
    return fig 



############################################################################################################################# 세로 막대 create vbar 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_go_candlestick(organ, kind1): 
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
        


############################################################################################################################# 막대 bar chart 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
def create_go_bar(organ, kind1): 
    # data  
    # month_df, point_df, kind1_df, wc_data = load_df(organ, kind1)  #   <==================================================
    t = [1, 5, 3, 4, 2]
    y1 = list(range(1,6))
    y2 = list(range(11,16))
    y3 = list(range(21,26))
    y4 = list(range(31,36))


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Create subplot grid
    fig = make_subplots(rows=1, cols=1,   specs= [  [  {"secondary_y": True}  ]  ]   )

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Add traces to the subplot grid : Bar chart 
    fig.add_trace(go.Bar(x=t, y=y1, 
                        #  mode="lines+markers", fill='tonexty', 
                        #  line=dict(width=0.5, 
                        #            color='indigo'),
                        #  width=[1, 2.1, 0.8, 2.6, 1.4], 
                         marker_color = 'crimson',  # px.colors.qualitative.Dark24,
                         name="Bar A",
                         text=y1, textposition="inside",   # ['inside', 'outside', 'auto', 'none']
                         hoverinfo="x+y", 
                         ), 
                  row=1, col=1, secondary_y=False, 
                  )  
    
    fig.add_trace(go.Bar(x=t, y=y2, 
                        #  mode="lines+markers", fill='tonexty', 
                        #  line=dict(width=0.5, 
                        #            color='indigo'),
                        #  width=[1, 2.1, 0.8, 2.6, 1.4], 
                         marker_color = 'limegreen',  # px.colors.qualitative.Dark24,
                         name="Bar B",
                         text=y2, textposition="inside",   # ['inside', 'outside', 'auto', 'none']
                         hoverinfo="x+y", 
                         ), 
                  row=1, col=1, secondary_y=False, 
                  )   
    
    fig.add_trace(go.Bar(x=t, y=y3, 
                        #  mode="lines+markers", fill='tonexty', 
                        #  line=dict(width=0.5, 
                        #            color='indigo'), 
                        #  width=[1, 2.1, 0.8, 2.6, 1.4], 
                         marker_color = 'blue',  # px.colors.qualitative.Dark24,
                         name="Bar C",
                         text=y3, textposition="inside",   # ['inside', 'outside', 'auto', 'none']
                         hoverinfo="x+y", 
                         ), 
                  row=1, col=1, secondary_y=False, 
                  )  
    # fig.update_traces(mode='markers', marker_line_width=1) # , marker_size=10)   
    fig.update_layout(barmode='relative',
                      xaxis={'categoryorder':'category descending'},   # ['trace', 'category ascending', 'category descending', 
                                                                      # 'array', 'total ascending', 'total descending', 
                                                                      # 'min ascending', 'min descending', 'max ascending', 'max descending', 
                                                                      # 'sum ascending', 'sum descending', 'mean ascending', 'mean descending', 
                                                                      # 'median ascending', 'median descending']
                      showlegend=False, 
                      )  # barmode='stack' 음수값 에러 ~~ 

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

