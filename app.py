import streamlit as st 
import plotly.express as px 
import pandas as pd 
import numpy as np 

from PIL import Image 

import tab0 
import tab1 
import tab2

# import tab3 
# import tab4 
# import tab5 
# import tab6 
# import tab7 

st.set_page_config(layout="wide")

################################################################################# title
st.markdown("#### 한눈에 보는 민원지도 < 광주전남본부>🌸") 
st.markdown("""---""") 


################################################################################# layout
tab_titles = ['민원 개요', '광주지사', '담양지사', '순천지사', '함평지사', '구례지사', '보성지사', '남원지사']
tabs = st.tabs(tab_titles)
sbar = st.sidebar
sbar.header('통계 정보🌸') 
sbar.header('분석 정보🌸') 
sbar.header('분석 리포트🌸') 
sbar.header('맞춤형 통계🌸') 

# 각 탭에 콘텐츠 추가
with tabs[0]: 
    tab0.run_tab()
 
with tabs[1]:
    tab1.run_tab()

with tabs[2]:
    tab2.run_tab()

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


# map
base_position = [37.5073423, 127.0572734] 
map_data = pd.DataFrame(np.random.randn(5,1)/[20,20] + base_position,
	columns=['lat','lon'] 
	) 
#print(map_data) 
tabs[2].code('con11.map(map_data)')
tabs[2].map(map_data) 