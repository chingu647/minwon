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

import tab0 
import tab1 
# import tab2

# import tab3 
# import tab4 
# import tab5 
# import tab6 
# import tab7 

st.set_page_config(layout="wide")

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ mpl 한글 설정  
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

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ css 설정
st.markdown(""" 
            <style> 
                table{background-color:#f0f0f0;} 
                # div{border:1px solid #00ff00;}
                img {max-width: 600px; max-height: 600px;}    # 이미지 파일 최대크기 제한 
            
                tabs-bui5-tab-0 {
                    font-size: 32px;
                    font-family: "Source Sans Pro", sans-serif;
                    font-weight: 400;
                    line-height: 1.6;
                    text-size-adjust: 100%;
                    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
                    -webkit-font-smoothing: auto;
                    color: rgb(49, 51, 63);
                    color-scheme: light;
                    box-sizing: border-box;
                    position: relative;
                    display: flex;
                    flex-wrap: nowrap;
                    -webkit-box-flex: 1;
                    flex-grow: 1;
                    -webkit-box-orient: horizontal;
                    -webkit-box-direction: normal;
                    flex-direction: row;
                    padding-bottom: 0.125rem;
                    margin-bottom: -0.125rem;
                    overflow-x: scroll;
                    gap: 1rem;
                    overflow-y: hidden;
                }

            </style> """, 
            unsafe_allow_html=True
            ) 

################################################################################# title
st.markdown("""
            <center><h2>한눈에 보는 민원지도<h2></center>
            """, 
            unsafe_allow_html=True) 

################################################################################# layout

tab_titles = ['광주전남', '광 주', '담 양', '순 천', '함 평', '구 례', '보 성', '남 원']
tabs = st.tabs(tab_titles)
sbar = st.sidebar
sbar.markdown(""" 
              <h3>🌸 광주 <a href="tel:010-6637-4525">민원실</a></h3><p>
              """, unsafe_allow_html=True ) 
sbar.markdown(""" 
              <h3>🌸 담양 <a href="tel:010-6637-4525">민원실</a></h3><p> 
              """, unsafe_allow_html=True ) 
sbar.markdown(""" 
              <h3>🌸 순천 <a href="tel:010-6637-4525">민원실</a></h3><p> 
              """, unsafe_allow_html=True ) 
sbar.markdown(""" 
              <h3>🌸 함평 <a href="tel:010-6637-4525">민원실</a></h3><p> 
              """, unsafe_allow_html=True ) 
sbar.markdown(""" 
              <h3>🌸 구례 <a href="tel:010-6637-4525">민원실</a></h3><p> 
              """, unsafe_allow_html=True ) 
sbar.markdown(""" 
              <h3>🌸 보성 <a href="tel:010-6637-4525">민원실</a></h3><p> 
              """, unsafe_allow_html=True ) 
sbar.markdown(""" 
              <h3>🌸 남원 <a href="tel:010-6637-4525">민원실</a></h3><p> 
              """, unsafe_allow_html=True ) 

# 각 탭에 콘텐츠 추가
with tabs[0]: 
    tab0.run_tab()
 
with tabs[1]:
    tab1.run_tab()

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