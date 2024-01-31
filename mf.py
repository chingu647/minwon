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


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ DATABASE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ load_df 
# arg1 : global organ_ t?? ---------- 탭 페이지에서 입력
# arg2 : global kind1_ t?? ---------- 탭 페이지에서 입력
@st.cache_resource 
def load_df(organ, choice):         # choice -  kind1, kind2, team, road 
    df = pd.read_csv("data/민원처리현황.csv") 

    # DATE 컬럼 DatetimeIndex로 변환 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    df['DATE'] = pd.to_datetime(df['DATE'])
    # st.write(df.dtypes )
    # st.write(df['DATE'].unique())

    # CSV 컬럼 변수 
    LATITUDE = 'LATITUDE'
    LONGITUDE = 'LONGITUDE'
    KEYWORD = 'KEYWORD' 

    if organ == 'ALL':
        df = df 
    else:
        df = df.query( f"ORGAN == '{organ}'" ) 
    
    # 시계열 data
    month_df = df.groupby(pd.Grouper(key='DATE', freq='M'))['NUMBER'].count().reset_index() 
    month_df['NUMBER_pct_change'] = (   month_df['NUMBER'].pct_change(periods=1)*100   ).round(1)
    month_df['NUMBER_cumsum'] = month_df['NUMBER'].transform('cumsum') 
    # month_df = month_df.assign(NUMBER_DELTA=month_df.NUMBER_CUMSUM - month_df.NUMBER) 
    
    # map data : 위경도 없는 자료는 제외 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    point_df = df[ ~( (df[f'{LATITUDE}'].isna()) | (df[f'{LONGITUDE}'].isna()) ) ] 

    # choice data
    choice_df = point_df.groupby(by=f'{choice}')['NUMBER'].count().reset_index().sort_values(by=f'{choice}', ascending=False) 
    choice_df['NUMBER_pct'] = (   choice_df['NUMBER'] / choice_df['NUMBER'].sum()*100   ).astype(int) 
 
    # wc data
    df[f'{KEYWORD}'] = df[f'{KEYWORD}'].str.replace('[\s+]', ' ') 
    df[f'{KEYWORD}'].dropna(inplace=True) 
    wc_sr = df.loc[:, f'{KEYWORD}'] 
    wc_data = ' '.join( map(str,wc_sr) )

    return month_df, point_df, choice_df, wc_data 


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ M A P @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ load wc 
# arg1 : text_raw 
@st.cache_resource 
def load_wc(organ, choice): # target_layout 에러 발생 
    # data  
    month_df, point_df, choice_df, wc_data= load_df(organ, choice)  #   <================================================== 
    t = Okt() 
    text_nouns = t.nouns(wc_data) 
    stopwords =['시어','및','조치','예정','민원','처리','해당','통해','방향','후','검토','확인','완료','내','노력','등','위해','위하여','지사',
                '대하','대하여','대해','대한','도록','토록','하도록','되도록','말씀','수','음','귀하','주신','답변','향','중','향','사항','아래','다음',
                '문의사항','내용','요청','요지','안내','일부','부분','미완료','관내','박준혁','대리','박준혁 대리','관련','저희','것','함','구간','고객']
    text_nouns = [n for n in text_nouns if n not in stopwords] 

    # # Term Frequency - word_count 옵션 --------------------------------- X
    # tf_words = []
    # for i in range(len(text_nouns)):
    #     tf_words.append(text_nouns[i]) 

    # tf_words = list( set( tf_words ) ) 

    # word_count = {} 
    # for word in tf_words:
    #     if word in word_count: 
    #         word_count[word] += 1
    #     else: 
    #         word_count[word] = 1

    # Documnent Frequency - word_count 옵션 ------------------------------ ok
    # df_words = []
    # for i in range(len(text_nouns)):
    #     df_words.append( list(set( text_nouns[i] )) ) 

    # word_count = {}
    # for words_list in df_words:
    #     word = tuple(words_list)
    #     if word in word_count: 
    #         word_count[word] += 1
    #     else: 
    #         word_count[word] = 1
    # ------------------------------------------------------------------
    
    text_str = ' '.join(text_nouns)
    wc = WordCloud(background_color='#fdf0fd', font_path=r"data/NanumGothic.ttf", max_words=50).generate(text_str)   # '#ECF8E0'
    
    # 방법 1 - matplotlib -> pyplot 출력
    fig, ax = plt.subplots(figsize=(18,8)) 
    ax.axis('off')
    ax.imshow(wc) 
            
    # fig = px.colors.qualitative.swatches()


    # 방법 2 - word_count 사용
    # cloud = wc.fit_words(word_count)
    # fig = cloud
   
    return fig, month_df, point_df, choice_df, wc_data#, word_count 


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ load map 1
# arg1 : organ_ t?? ---------- 탭 페이지에서 입력
# arg2 : kind1_ t?? ---------- 탭 페이지에서 입력
# base_position_ t?? --------- 탭 페이지에서 입력

@st.cache_resource 
def load_map(base_position, organ, choice): 

    # CSV 컬럼 변수
    LATITUDE = 'LATITUDE'
    LONGITUDE = 'LONGITUDE'
    KIND2 = 'KIND2'          ## ??????????????????????????????????????????????
    KEYWORD = 'KEYWORD'

    # data  
    month_df, point_df, choice_df, wc_data= load_df(organ, choice)  #   <==================================================

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
                        popup=f"{index} ( {row[f'{KEYWORD}']} ) ", 
                        # popup=f"{row[f'{KIND2}']} ( {row[f'{KEYWORD}']} ) ", 
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
def load_map_choice(base_position, organ, choice): 

    # CSV 컬럼 변수
    LATITUDE = 'LATITUDE'
    LONGITUDE = 'LONGITUDE'
    KIND2 = 'KIND2' 
    KEYWORD = 'KEYWORD'

    # data  
    month_df, point_df, choice_df, wc_data= load_df(organ, choice)  #   <==================================================

    # kind1 상위 5개 : Grouped Layer Control 준비...
    
    # if choice in choice_df.columns:
    #     result = folium.FeatureGroup(name=f'@choice_df.index[0]')
    # else:
    #     result = "해당 열이 존재하지 않습니다." 

    # choice 종류 리스트 계산 
    choice_df = choice_df[f'{choice}']

    choice_list = list( set( choice_df ) ) 

    # fg_df 리스트 
    choice_df_list = [] 

    for i in range( len(choice_df) ): 
        fg_df = point_df.query(f" `{choice}` == @choice_list[{i}] ") 
        # st.write( fg_df )
        choice_df_list.append(fg_df)  

    # fg 그룹 리스트 
    choice_fg_list = [] 
    for i in range( len(choice_df) ): 
        fg_temp = folium.FeatureGroup(name=f"{choice_list[i]}")
        # st.write(fg_temp)
        choice_fg_list.append(fg_temp) 

    # map 생성 
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
    
    # fg 리스트에 folium Marker 생성 # folium.Marker([, ]).add_to(fg_k0) -------------------------------
    color_list = ['blue','red','darkgreen','orange','blue','pink','lightsalmon','lightseagreen','lightskyblue','lightslategray','lightyellow','lime','mediumvioletred', ]
    icon_list  = ['star','star','star','star','star','star','star','star','star','star','star','star','star', ]
    for i in range( len( choice_df) ): 

      for index, row in choice_df_list[i].iterrows():           
          if not pd.isna(row[f'{LATITUDE}']) and not pd.isna(row[f'{LONGITUDE}']):
              folium.CircleMarker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 원 중심
                                  radius=1,            # 원 반지름
                                  color='blue',        # 원 테두리 색상
                                  fill=True,           # 원 채움
                                  fill_opacity=0.5,     # 원 채움 투명도
                                  ).add_to( choice_fg_list[i] ) 
                      
              folium.Marker( location=[ row[f'{LATITUDE}'], row[f'{LONGITUDE}'] ],  # 값 중심 
                            popup=f"{index} ( {row[f'{KEYWORD}']} ) ", 
                            tooltip=row[f'{LATITUDE}'], 
                            icon=folium.Icon(color=f'{color_list[i]}', icon=f'{icon_list[i]}'), 
                            # icon=folium.DivIcon(                              # 값 표시방식
                            #     html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
                           ).add_to( choice_fg_list[i] )  
              
    # map.add_child(fg_???) 
    for i in range( len( choice_df) ): 
        map.add_child( choice_fg_list[i] ) 

    
    # folium.LayerControl(collapsed=False).add_to(map)

    GroupedLayerControl(groups={  f'{choice}': choice_fg_list  }, 
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



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px chart - month @@@ 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px scatter
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_scatter_month(organ, choice): 
    # data  
    month_df, point_df, choice_df, wc_data= load_df(organ, choice)  #   <==================================================

    fig = px.scatter(month_df, x='DATE', y='NUMBER',                                  # kind1_df.index
                     color='DATE', # color_discrete_sequence=px.colors.qualitative.D3,
                     text='NUMBER', 
                    #  color='NUMBER', 
                     labels={ 'NUMBER':'발생 건수'}, 
                    ) 
    
    fig.update_traces(marker=dict(size=60), 
                      textfont_size=20, 
                      textfont_color='black', 
                    #   textposition='top center',   # ['top left', 'top center', 'top right', 'middle left', 'middle center', 'middle right', 'bottom left', 'bottom center', 'bottom right'] 
                    #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False,
                     ) 
    fig.update_coloraxes(showscale=False) # ---------------------------------- @@@@@@@@@@@@@@@@@@@@@@@@

    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)

    fig.update_xaxes(showticklabels = True, 
                     tickformat = '%Y-%m',                # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'
                    #  dtick="M1", 
                     dtick=30 * 24 * 60 * 60 * 1000,   # 한 달 간격을 밀리초로 계산 
                     ) 
    fig.update_xaxes(
        showticklabels=True,
        tickangle=45  # 텍스트 각도 (선택적)
)


    # fig = px.colors.qualitative.swatches() 
    return fig, month_df, point_df, choice_df, wc_data



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px line 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_line_month(organ, choice): 
    # data  
    month_df, point_df, choice_df, wc_data= load_df(organ, choice)  #   <==================================================

    fig = px.line(month_df, x='DATE', y='NUMBER',                                  # kind1_df.index
                #   color='NUMBER', 
                  text='NUMBER',
                #   title='hello',
                  labels={ 'NUMBER':'발생 건수'},
                  markers=True
                  ) 
                    #  trendline='lowess')   # 연속 데이터 만 ['lowess', 'rolling', 'ewm', 'expanding', 'ols']
    
    fig.update_traces(marker=dict(size=30, color='#f0f5ed'), 
                      textfont_size=20, 
    #                   textfont_color ='white',
    #                 #   textposition='top center',   # ['top left', 'top center', 'top right', 'middle left', 'middle center', 'middle right', 'bottom left', 'bottom center', 'bottom right'] 
    #                 #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False,
                     ) 
    
    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)
    
    fig.update_xaxes(showticklabels = True,
                     tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'

    return fig, month_df, point_df, choice_df, wc_data

# fig = px.colors.qualitative.swatches()
# fig.show()

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px bar 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_bar_month(organ, choice): 
    # data  
    month_df, point_df, choice_df, wc_data= load_df(organ, choice)  #   <==================================================

    fig = px.bar(month_df, x='DATE', y='NUMBER',    # kind1_df.index 
                 color='DATE', 
                 text='NUMBER', 
                #   title='hello',
                 labels={ 'NUMBER':'발생 건수'}, 
                #  hover_data=['  ', '  '], 
                #  barmode='group', 
                #  orientation='h'
                      ) 
    
    fig.update_traces(#marker=dict(size=60), 
                      textfont_size=20, 
                    #   textfont_color ='black',
                      textposition='auto',   # ['inside', 'outside', 'auto', 'none']   
                    #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False
                     ) 
    
    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)
    
    fig.update_xaxes(showticklabels = True, 
                     tickformat = '%Y-%m',                # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'
                    #  dtick="M1", 
                     dtick=30 * 24 * 60 * 60 * 1000,   # 한 달 간격을 밀리초로 계산 
                    ) 
    return fig, month_df, point_df, choice_df, wc_data



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px chart - kind1 @@@ 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px scatter
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_scatter_kind1(organ, kind1): 
    # data  
    month_df, point_df, kind1_df, wc_data= load_df(organ, kind1)  #   <==================================================

    fig = px.scatter(kind1_df, x=f'{kind1}', y='NUMBER',                                  # kind1_df.index
                     color=f'{kind1}', # color_discrete_sequence=px.colors.qualitative.D3,
                     text='NUMBER', 
                    #  color='NUMBER', 
                     labels={ 'NUMBER':'발생 건수'}, 
                    ) 
    
    fig.update_traces(marker=dict(size=60), 
                      textfont_size=20, 
                      textfont_color='black', 
                    #   textposition='top center',   # ['top left', 'top center', 'top right', 'middle left', 'middle center', 'middle right', 'bottom left', 'bottom center', 'bottom right'] 
                    #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False,
                     ) 
    fig.update_coloraxes(showscale=False) # ---------------------------------- @@@@@@@@@@@@@@@@@@@@@@@@

    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)

    fig.update_xaxes(showticklabels = True,
                     tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'

    # fig = px.colors.qualitative.swatches() 
    return fig, month_df, point_df, kind1_df, wc_data



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px line 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_line_kind1(organ, kind1): 
    # data  
    month_df, point_df, kind1_df, wc_data= load_df(organ, kind1)  #   <==================================================

    fig = px.line(kind1_df, x=f'{kind1}', y='NUMBER',                                  # kind1_df.index
                #   color=f'{kind1}', 
                  text='NUMBER',
                #   title='hello',
                  labels={ 'NUMBER':'발생 건수'},
                  markers=True
                  ) 
                    #  trendline='lowess')   # 연속 데이터 만 ['lowess', 'rolling', 'ewm', 'expanding', 'ols']
    
    fig.update_traces(marker=dict(size=30, color='#f0f5ed'), 
                      textfont_size=20, 
    #                   textfont_color ='white',
    #                 #   textposition='top center',   # ['top left', 'top center', 'top right', 'middle left', 'middle center', 'middle right', 'bottom left', 'bottom center', 'bottom right'] 
    #                 #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False,
                     ) 
    
    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)
    
    fig.update_xaxes(showticklabels = True,
                     tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'

    return fig, month_df, point_df, kind1_df, wc_data

# fig = px.colors.qualitative.swatches()
# fig.show()

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px bar 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_bar_kind1(organ, kind1): 
    # data  
    month_df, point_df, kind1_df, wc_data= load_df(organ, kind1)  #   <==================================================

    fig = px.bar(kind1_df, x=f'{kind1}', y='NUMBER',    # kind1_df.index 
                 color=f'{kind1}', 
                 text='NUMBER', 
                #   title='hello',
                 labels={ 'NUMBER':'발생 건수'}, 
                #  hover_data=['  ', '  '], 
                #  barmode='group', 
                #  orientation='h'
                      ) 
    
    fig.update_traces(#marker=dict(size=60), 
                      textfont_size=20, 
                    #   textfont_color ='black',
                      textposition='auto',   # ['inside', 'outside', 'auto', 'none']   
                    #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False
                     ) 
    
    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)
    
    fig.update_xaxes(showticklabels = True,
                     tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'

    return fig, month_df, point_df, kind1_df, wc_data

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px pie 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_pie_kind1(organ, kind1): 
    # data  
    month_df, point_df, kind1_df, wc_data= load_df(organ, kind1)  #   <==================================================

    fig = px.pie(kind1_df, values=kind1_df.NUMBER, names=kind1_df[f'{kind1}'], 
                #  text = kind1_df[f'{kind1}'], 
                #  title='hello',
                 labels={ 'NUMBER':'발생 건수'}, 
                 hole=0.4,) 

    fig.update_traces(textfont_size=20, 
                    #   textfont_color ='black',
                      textposition='auto',    # ['inside', 'outside', 'auto', 'none']   
                      textinfo='percent+value',   # 'label+percent+value'
                    #   showlegend=False
                      ) 
    
    fig.update_layout(legend=dict(#orientation = 'h',
                                  xanchor="auto",   # ("auto","left","center","right") 
                                  x=0.02,   
                                  yanchor="top",    # ("auto","top","middle","bottom")
                                  y=0.99,
                                  font=dict(family="Courier",
                                            size=16, 
                                            color="black" 
                                            ), 
                                #   bgcolor="LightSteelBlue", 
                                #   bordercolor="Black", 
                                #   borderwidth=2 
                                  ) 
                     ) 

    return fig, month_df, point_df, kind1_df, wc_data



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px chart - kind2 @@@ 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px scatter
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_scatter_kind2(organ, kind2): 
    # data  
    month_df, point_df, kind2_df, wc_data= load_df(organ, kind2)  #   <==================================================

    fig = px.scatter(kind2_df, x=f'{kind2}', y='NUMBER',                                  # kind1_df.index
                     color=f'{kind2}', # color_discrete_sequence=px.colors.qualitative.D3,
                     text='NUMBER', 
                    #  color='NUMBER', 
                     labels={ 'NUMBER':'발생 건수'}, 
                    ) 
    
    fig.update_traces(marker=dict(size=60), 
                      textfont_size=20, 
                      textfont_color='black', 
                    #   textposition='top center',   # ['top left', 'top center', 'top right', 'middle left', 'middle center', 'middle right', 'bottom left', 'bottom center', 'bottom right'] 
                    #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False,
                     ) 
    fig.update_coloraxes(showscale=False) # ---------------------------------- @@@@@@@@@@@@@@@@@@@@@@@@

    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)

    fig.update_xaxes(showticklabels = True,
                     tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'

    # fig = px.colors.qualitative.swatches() 
    return fig, month_df, point_df, kind2_df, wc_data



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px line 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_line_kind2(organ, kind2): 
    # data  
    month_df, point_df, kind2_df, wc_data= load_df(organ, kind2)  #   <==================================================

    fig = px.line(kind2_df, x=f'{kind2}', y='NUMBER',                                  # kind1_df.index
                #   color=f'{kind2}', 
                  text='NUMBER',
                #   title='hello',
                  labels={ 'NUMBER':'발생 건수'},
                  markers=True
                  ) 
                    #  trendline='lowess')   # 연속 데이터 만 ['lowess', 'rolling', 'ewm', 'expanding', 'ols']
    
    fig.update_traces(marker=dict(size=30, color='#f0f5ed'), 
                      textfont_size=20, 
    #                   textfont_color ='white',
    #                 #   textposition='top center',   # ['top left', 'top center', 'top right', 'middle left', 'middle center', 'middle right', 'bottom left', 'bottom center', 'bottom right'] 
    #                 #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False,
                     ) 
    
    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)
    
    fig.update_xaxes(showticklabels = True,
                     tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'

    return fig, month_df, point_df, kind2_df, wc_data

# fig = px.colors.qualitative.swatches()
# fig.show()

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px bar 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_bar_kind2(organ, kind2): 
    # data  
    month_df, point_df, kind2_df, wc_data= load_df(organ, kind2)  #   <==================================================

    fig = px.bar(kind2_df, x=f'{kind2}', y='NUMBER',    # kind1_df.index 
                 color=f'{kind2}', 
                 text='NUMBER', 
                #   title='hello',
                 labels={ 'NUMBER':'발생 건수'}, 
                #  hover_data=['  ', '  '], 
                #  barmode='group', 
                #  orientation='h'
                      ) 
    
    fig.update_traces(#marker=dict(size=60), 
                      textfont_size=20, 
                    #   textfont_color ='black',
                      textposition='auto',   # ['inside', 'outside', 'auto', 'none']   
                    #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False
                     ) 
    
    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)
    
    fig.update_xaxes(showticklabels = True,
                     tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'

    return fig, month_df, point_df, kind2_df, wc_data

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px pie 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_pie_kind2(organ, kind2): 
    # data  
    month_df, point_df, kind2_df, wc_data= load_df(organ, kind2)  #   <==================================================

    fig = px.pie(kind2_df, values=kind2_df.NUMBER, names=kind2_df[f'{kind2}'], 
                #  text = kind1_df[f'{kind1}'], 
                #  title='hello',
                 labels={ 'NUMBER':'발생 건수'}, 
                 hole=0.4,) 

    fig.update_traces(textfont_size=20, 
                    #   textfont_color ='black',
                      textposition='auto',    # ['inside', 'outside', 'auto', 'none']   
                      textinfo='percent+value',   # 'label+percent+value'
                    #   showlegend=False
                      ) 
    
    fig.update_layout(legend=dict(#orientation = 'h',
                                  xanchor="auto",   # ("auto","left","center","right") 
                                  x=0.02,   
                                  yanchor="top",    # ("auto","top","middle","bottom")
                                  y=0.99,
                                  font=dict(family="Courier",
                                            size=16, 
                                            color="black" 
                                            ), 
                                #   bgcolor="LightSteelBlue", 
                                #   bordercolor="Black", 
                                #   borderwidth=2 
                                  ) 
                     ) 

    return fig, month_df, point_df, kind2_df, wc_data



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px chart - team  @@@ 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px scatter
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_scatter_team(organ, team): 
    # data  
    month_df, point_df, team_df, wc_data= load_df(organ, team)  #   <==================================================

    fig = px.scatter(team_df, x=f'{team}', y='NUMBER',                                  # kind1_df.index
                     color=f'{team}', # color_discrete_sequence=px.colors.qualitative.D3,
                     text='NUMBER', 
                    #  color='NUMBER', 
                     labels={ 'NUMBER':'발생 건수'}, 
                    ) 
    
    fig.update_traces(marker=dict(size=60), 
                      textfont_size=20, 
                      textfont_color='black', 
                    #   textposition='top center',   # ['top left', 'top center', 'top right', 'middle left', 'middle center', 'middle right', 'bottom left', 'bottom center', 'bottom right'] 
                    #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False,
                     ) 
    fig.update_coloraxes(showscale=False) # ---------------------------------- @@@@@@@@@@@@@@@@@@@@@@@@

    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)

    fig.update_xaxes(showticklabels = True,
                     tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'

    # fig = px.colors.qualitative.swatches() 
    return fig, month_df, point_df, team_df, wc_data



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px line 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_line_team(organ, team): 
    # data  
    month_df, point_df, team_df, wc_data= load_df(organ, team)  #   <==================================================

    fig = px.line(team_df, x=f'{team}', y='NUMBER',                                  # kind1_df.index
                #   color=f'{team}', 
                  text='NUMBER',
                #   title='hello',
                  labels={ 'NUMBER':'발생 건수'},
                  markers=True
                  ) 
                    #  trendline='lowess')   # 연속 데이터 만 ['lowess', 'rolling', 'ewm', 'expanding', 'ols']
    
    fig.update_traces(marker=dict(size=30, color='#f0f5ed'), 
                      textfont_size=20, 
    #                   textfont_color ='white',
    #                 #   textposition='top center',   # ['top left', 'top center', 'top right', 'middle left', 'middle center', 'middle right', 'bottom left', 'bottom center', 'bottom right'] 
    #                 #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False,
                     ) 
    
    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)
    
    fig.update_xaxes(showticklabels = True,
                     tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'

    return fig, month_df, point_df, team_df, wc_data

# fig = px.colors.qualitative.swatches()
# fig.show()

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px bar 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_bar_team(organ, team): 
    # data  
    month_df, point_df, team_df, wc_data= load_df(organ, team)  #   <==================================================

    fig = px.bar(team_df, x=f'{team}', y='NUMBER',    # kind1_df.index 
                 color=f'{team}', 
                 text='NUMBER', 
                #   title='hello',
                 labels={ 'NUMBER':'발생 건수'}, 
                #  hover_data=['  ', '  '], 
                #  barmode='group', 
                #  orientation='h'
                      ) 
    
    fig.update_traces(#marker=dict(size=60), 
                      textfont_size=20, 
                    #   textfont_color ='black',
                      textposition='auto',   # ['inside', 'outside', 'auto', 'none']   
                    #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False
                     ) 
    
    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)
    
    fig.update_xaxes(showticklabels = True,
                     tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'

    return fig, month_df, point_df, team_df, wc_data

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px pie 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_pie_team(organ, team): 
    # data  
    month_df, point_df, team_df, wc_data= load_df(organ, team)  #   <==================================================

    fig = px.pie(team_df, values=team_df.NUMBER, names=team_df[f'{team}'], 
                #  text = kind1_df[f'{kind1}'], 
                #  title='hello',
                 labels={ 'NUMBER':'발생 건수'}, 
                 hole=0.4,) 

    fig.update_traces(textfont_size=20, 
                    #   textfont_color ='black',
                      textposition='auto',    # ['inside', 'outside', 'auto', 'none']   
                      textinfo='percent+value',   # 'label+percent+value'
                    #   showlegend=False
                      ) 
    
    fig.update_layout(legend=dict(#orientation = 'h',
                                  xanchor="auto",   # ("auto","left","center","right") 
                                  x=0.02,   
                                  yanchor="top",    # ("auto","top","middle","bottom")
                                  y=0.99,
                                  font=dict(family="Courier",
                                            size=16, 
                                            color="black" 
                                            ), 
                                #   bgcolor="LightSteelBlue", 
                                #   bordercolor="Black", 
                                #   borderwidth=2 
                                  ) 
                     ) 

    return fig, month_df, point_df, team_df, wc_data



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px chart - road  @@@ 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px scatter
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_scatter_road(organ, road): 
    # data  
    month_df, point_df, road_df, wc_data= load_df(organ, road)  #   <==================================================

    fig = px.scatter(road_df, x=f'{road}', y='NUMBER',                                  # kind1_df.index
                     color=f'{road}', # color_discrete_sequence=px.colors.qualitative.D3,
                     text='NUMBER', 
                    #  color='NUMBER', 
                     labels={ 'NUMBER':'발생 건수'}, 
                    ) 
    
    fig.update_traces(marker=dict(size=60), 
                      textfont_size=20, 
                      textfont_color='black', 
                    #   textposition='top center',   # ['top left', 'top center', 'top right', 'middle left', 'middle center', 'middle right', 'bottom left', 'bottom center', 'bottom right'] 
                    #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False,
                     ) 
    fig.update_coloraxes(showscale=False) # ---------------------------------- @@@@@@@@@@@@@@@@@@@@@@@@

    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)

    fig.update_xaxes(showticklabels = True,
                     tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'

    # fig = px.colors.qualitative.swatches() 
    return fig, month_df, point_df, road_df, wc_data



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px line 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_line_road(organ, road): 
    # data  
    month_df, point_df, road_df, wc_data= load_df(organ, road)  #   <==================================================

    fig = px.line(road_df, x=f'{road}', y='NUMBER',                                  # kind1_df.index
                #   color=f'{road}', 
                  text='NUMBER',
                #   title='hello',
                  labels={ 'NUMBER':'발생 건수'},
                  markers=True
                  ) 
                    #  trendline='lowess')   # 연속 데이터 만 ['lowess', 'rolling', 'ewm', 'expanding', 'ols']
    
    fig.update_traces(marker=dict(size=30, color='#f0f5ed'), 
                      textfont_size=20, 
    #                   textfont_color ='white',
    #                 #   textposition='top center',   # ['top left', 'top center', 'top right', 'middle left', 'middle center', 'middle right', 'bottom left', 'bottom center', 'bottom right'] 
    #                 #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False,
                     ) 
    
    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)
    
    fig.update_xaxes(showticklabels = True,
                     tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'

    return fig, month_df, point_df, road_df, wc_data

# fig = px.colors.qualitative.swatches()
# fig.show()

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px bar 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_bar_road(organ, road): 
    # data  
    month_df, point_df, road_df, wc_data= load_df(organ, road)  #   <==================================================

    fig = px.bar(road_df, x=f'{road}', y='NUMBER',    # kind1_df.index 
                 color=f'{road}', 
                 text='NUMBER', 
                #   title='hello',
                 labels={ 'NUMBER':'발생 건수'}, 
                #  hover_data=['  ', '  '], 
                #  barmode='group', 
                #  orientation='h'
                      ) 
    
    fig.update_traces(#marker=dict(size=60), 
                      textfont_size=20, 
                    #   textfont_color ='black',
                      textposition='auto',   # ['inside', 'outside', 'auto', 'none']   
                    #   textinfo='label+percent+value',   # 'label+percent+value'
                      showlegend=False
                     ) 
    
    # fig.update_layout(legend=dict(#orientation = 'h', 
    #                               xanchor="left",   # ("auto","left","center","right") 
    #                               x=0.01,   
    #                               yanchor="top",    # ("auto","top","middle","bottom")
    #                               y=0.99,
    #                               font=dict(family="Courier",
    #                                         size=12, 
    #                                         color="black" 
    #                                         ), 
    #                               bgcolor="LightSteelBlue", 
    #                               bordercolor="Black", 
    #                               borderwidth=2 
    #                               ) 
    #                  ) 
    # fig.update_layout(xaxis_visible=False)
    # fig.update_layout(yaxis_visible=False)
    
    fig.update_xaxes(showticklabels = True,
                     tickformat = '%Y-%m', dtick="M1") # '%d %B (%a)<br>%Y' / '%Y-%b-%d(%a)'

    return fig, month_df, point_df, road_df, wc_data

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ create px pie 
# arg1 : organ_ t?? --------- 탭 페이지에서 입력 
# arg2 : kind1_ t?? --------- 탭 페이지에서 입력 
@st.cache_resource 
def create_px_pie_road(organ, road): 
    # data  
    month_df, point_df, road_df, wc_data= load_df(organ, road)  #   <==================================================

    fig = px.pie(road_df, values=road_df.NUMBER, names=road_df[f'{road}'], 
                #  text = kind1_df[f'{kind1}'], 
                #  title='hello',
                 labels={ 'NUMBER':'발생 건수'}, 
                 hole=0.4,) 

    fig.update_traces(textfont_size=20, 
                    #   textfont_color ='black',
                      textposition='auto',    # ['inside', 'outside', 'auto', 'none']   
                      textinfo='percent+value',   # 'label+percent+value'
                    #   showlegend=False
                      ) 
    
    fig.update_layout(legend=dict(#orientation = 'h',
                                  xanchor="auto",   # ("auto","left","center","right") 
                                  x=0.02,   
                                  yanchor="top",    # ("auto","top","middle","bottom")
                                  y=0.99,
                                  font=dict(family="Courier",
                                            size=16, 
                                            color="black" 
                                            ), 
                                #   bgcolor="LightSteelBlue", 
                                #   bordercolor="Black", 
                                #   borderwidth=2 
                                  ) 
                     ) 

    return fig, month_df, point_df, road_df, wc_data

