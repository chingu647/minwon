import streamlit as st 
import plotly.express as px 

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


st.markdown("#### 서울시 아파트 가격 추세 분석 및 회귀모델 분석") 
st.markdown("""---""") 

tab_titles = ['Project 개요', '느낀점 부터', 'Project 가설 3가지', '가설1 분석', '가설2 분석', '가설3 분석', '결 론', 'Data source']
tabs = st.tabs(tab_titles)
sbar = st.sidebar
sbar.title('Iris Species🌸') 
 
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
