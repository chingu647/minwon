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

from PIL import Image 

from streamlit_option_menu import option_menu 

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-1) ST CACHE 사용
import mf 


import tab0 
import tab1 
import tab2
import tab3 
import tab4 
import tab5 
import tab6 
import tab7 

st.set_page_config(layout="wide",
                   page_title="Multipage App", 
                   page_icon="✋", 
                   )  #### 1번만 실행해야 함 !!! 


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-2) mpl 한글 설정  
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


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
st.markdown(""" 
            <style> 
                table{background-color:#f0f0f0;} 
                img {max-width: 1000px; max-height: 500px; }    # 이미지 파일 최대크기 제한 
            
            </style> """, 
            unsafe_allow_html=True
            ) 


################################################################################# title 
st.title(f'한눈에 보는 :blue[광주전남] 민원 지도 :sunglasses:',divider='rainbow') 
# st.markdown("""
#             <center><h2>한눈에 보는 <font color='blue'>광주전남</font> 민원 지도<h2></center>
#             """, 
#             unsafe_allow_html=True) 

################################################################################# layout

# tab_titles = ['광주전남', '광 주', '담 양', '순 천', '함 평', '구 례', '보 성', '남 원']
# tabs = st.tabs(tab_titles)

# sbar.markdown(""" 
#               <script>
#                 function isDesktopOs() {
#                     return ("win16|win32|win64|windows|mac|machine|linux|freebsd|openbsd|sunos".indexOf( navigator.platform.toLowerCase() ))
#                 }  
#                 if( isDesktopOs() ) { 
#                     document.write("<h3>🌸 광주 민원실 </h3><p>")  
#                 }
#                 else {
#                     document.write("<h3>🌸 광주 <a href="tel:010-6637-4525">민원실</a></h3><p>")
#                 }
#               </script>
#               """, unsafe_allow_html=True ) 

# 각 탭에 콘텐츠 추가

selected = option_menu(menu_title=None,
                        options=["본부","광주","담양","순천","함평","구례","보성","남원"],
                        icons=[None,None,None,None,None,None,None,None,],  
                        menu_icon="cast",
                        default_index=0,
                        orientation='horizontal', 
                        styles={"container": {"padding": "0px", # {"padding": "0!important", 
                                              "margin" : "0px",
                                              "background-color": "#fafafa"},
                                "icon": {"color": "orange",  
                                         "margin":"0px", 
                                        "padding":"0px",
                                         "font-size": "0px"}, 
                                "nav-link": {"font-size": "13px", 
                                             "text-align": "center", 
                                             "margin":"0px", 
                                             "padding":"0px",
                                             "--hover-color": "#eee"},
                                "nav-link-selected": {"background-color": "green"}, 
                                } 
)

if selected == "광주전남":
    tab0.run_tab() 

elif selected == "광주": 
    tab1.run_tab()
    
elif selected == "담양":
    tab2.run_tab()

elif selected == "순천":
    tab3.run_tab()
    
elif selected == "함평":
    tab4.run_tab()

elif selected == "구례":
    tab5.run_tab()
    
elif selected == "보성":
    tab6.run_tab()

elif selected == "남원":
    tab7.run_tab()



# with tabs[0]: 
#     tab0.run_tab()
 
# with tabs[1]:
#     tab1.run_tab()

# with tabs[2]:
#     tab2.run_tab()

# with tabs[3]: 
#     tab3.run_tab()

# with tabs[4]:
#     tab4.run_tab() 

# with tabs[5]:
#     tab5.run_tab()

# with tabs[6]:
#     tab6.run_tab()

# with tabs[7]:
#     tab7.run_tab()


################################################################################# input -> layout
# 셀렉트 박스 -----------------------------------------------------------------
#sr_variety_list = list(sr_variety) 
#생성 sb1 = sbar.selectbox('확인하고 싶은 종을 선택하세요', sr_variety_list) 
#db temp_df = df0[df0.variety == sb1]
#layout con10.dataframe(temp_df) 

# 멀티셀렉트  -----------------------------------------------------------------
#sr_variety_list = list(sr_variety) 
#생성 ms1 = sbar.multiselect('확인하고 싶은 종은? (복수선택 가능)', sr_variety_list) 
#db temp_df1 = df0[df0.variety.isin(ms1)] 

# flag0 = True
# if ms1: 
#layout 	con10.dataframe(temp_df1) 
# else:
# 	pass

# 라디오 ---------------------------------------------------------------------
#column_list = list(df0.columns[:-1]) 
#생성 rd1 = sbar.radio("what is key column ?", column_list, horizontal=True) 

# 슬라이더 --------------------------------------------------------------------
#생성 slider_range = sbar.slider('choose range key column', 0.0, 10.0, (2.5, 7.5) )

# 버튼 -------------------------------------------------------------------- 
#생성 start_button = sbar.button('filter apply 📊') 
    
################################################################################# see
# plotly_chart
# fig --------------------------------------------------------------------
# fig = px.scatter( df0.query("sepal_length >= 4.0" ),
# 	x='sepal_length',
# 	y='sepal_width',
# 	size='sepal_width', 
# 	color='variety', 
# 	hover_data =['sepal_width'],
# )    


# # map
# base_position = [37.5073423, 127.0572734] 
# map_data = pd.DataFrame(np.random.randn(5,1)/[20,20] + base_position,
# 	columns=['lat','lon'] 
# 	) 
# #print(map_data) 
# tabs[2].code('con11.map(map_data)')
# tabs[2].map(map_data) 