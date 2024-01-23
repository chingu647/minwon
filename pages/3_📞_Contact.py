import streamlit as st 
import streamlit.components.v1 as components 

import pandas as pd 
import numpy as np 

import matplotlib as mpl 
import matplotlib.pyplot as plt 
import matplotlib.font_manager as fm 

import seaborn as sns 


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ global 변수 설정
# global map_t1  # ----------------------------------------------------------------------- 
# global organ_t1
# global kind1_t1 
# global base_position_t1

# organ_t1 = "광주지사" 
# kind1_t1 = '서비스유형(대)'
# base_position_t1 = [35.18668601, 126.87954220] 

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ (3-3) css 설정
st.markdown(""" 
            <style> 
                table{background-color:#f0f0f0;} 
                img {max-width: 1000px; max-height: 600px; }    # 이미지 파일 최대크기 제한 
            
            </style> """, 
            unsafe_allow_html=True
            ) 


st.title('Contact')

# ##################################################################### layout 
ch0, ch1, ch2 = st.columns( [0.001, 0.998, 0.001] ) 

cb0, cb1, cb2, cb3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
cb4, cb5, cb6, cb7 = st.columns( [0.001, 0.499, 0.499, 0.001] )
cb8, cb9, cb10,cb11= st.columns( [0.001, 0.499, 0.499, 0.001] )

ct0, ct1, ct2 = st.columns( [0.001, 0.998, 0.001] ) 


# ##################################################################### head 1  


# ###################################################################### body 1      
cb1.markdown(f"##### 📢 :rainbow[지사별 연락처] ") 

cb1_data = {'지사별':['광주전남본부','광주지사','담양지사','순천지사','함평지사','구례지사','보성지사','남원지사',], 
            '연락처':['000-0000-0000','000-0000-0000','000-0000-0000','000-0000-0000','000-0000-0000','000-0000-0000','000-0000-0000','000-0000-0000']
            }
cb1_df = pd.DataFrame(cb1_data) 

cb1.table(cb1_df.style.background_gradient(cmap='Blues')) 



# with open('activity1.html') as file:
#     components.html( file.read() )

