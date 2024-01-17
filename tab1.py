import streamlit as st 
import plotly.express as px
import pandas as pd
import numpy as np 
import geopandas as gpd 

def run_tab(): 
    # ----------------------------------------------------------------------- layout 
    t1_head0, t1_head1, t1_head2 = st.columns( [0.001, 0.899, 0.1] )
    
    t1_body0, t1_body1, t1_body2, t1_body3, t1_body4 = st.columns( [0.2, 0.2, 0.2, 0.2, 0.2] )

    t1_tail0, t1_tail1, t1_tail2 = st.columns( [0.001, 0.899, 0.1] )

    # -----------------------------------------------------------------------  
    t1_head1.markdown("###### 주요 민원별 현황") 
    t1_head1.markdown(r"""
	1. 현대 사회에서 부동산은 모든 사람들의 관심사항이 되었으며, 특히 서울시 소재 부동산 가격에 대한 관심은 매우 크다고 할 수 있습니다.
	2. 이번 프로젝트에서는 서울시 구별로 부동산 가격차이를 데이터 시각화를 통해 알아보고, 회귀모델을 통해 주요 원인을 찾아보고자 합니다.
    """)

    # -----------------------------------------------------------------------  
    t1_head2.markdown("###### 날짜") 
    
    # -----------------------------------------------------------------------  
    t1_body0.markdown("###### 포트홀 민원") 
    t1_body0_data = {'1':['a','b','c'],
                     'bool':[True, True, False]}
    t1_body0_df = pd.DataFrame(data=t1_body0_data) 
    t1_body0.write(t1_body0_df) 

    # -----------------------------------------------------------------------  
    t1_body1.markdown("###### 휴게소 민원") 
    t1_body1_data = {'1':['a','b','c'],
                     'bool':[True, True, False]}
    t1_body1_df = pd.DataFrame(data=t1_body1_data) 
    t1_body1.write(t1_body1_df) 

    # -----------------------------------------------------------------------  
    t1_body2.markdown("###### 서비스 민원") 
    t1_body2_data = {'1':['a','b','c'],
                     'bool':[True, True, False]}
    t1_body2_df = pd.DataFrame(data=t1_body2_data) 
    t1_body2.write(t1_body2_df) 

    # -----------------------------------------------------------------------  
    t1_body3.markdown("###### 서비스2 민원") 
    t1_body3_data = {'1':['a','b','c'],
                     'bool':[True, True, False]}
    t1_body3_df = pd.DataFrame(data=t1_body3_data) 
    t1_body3.write(t1_body3_df) 

    # -----------------------------------------------------------------------  
    t1_body4.markdown("###### 기타 민원") 
    t1_body4_data = {'1':['a','b','c'],
                     'bool':[True, True, False]}
    t1_body4_df = pd.DataFrame(data=t1_body4_data) 
    t1_body4.write(t1_body4_df) 

    # -----------------------------------------------------------------------  
    # map 
    # base_position = [35.18668601, 126.87954220] 
    # map_data = pd.DataFrame(np.random.randn(5,1)/[20,20] + base_position,
    #     columns=['lat','lon'] 
    #     ) 
    # #print(map_data) 
    # t1_tail1.code('con11.map(map_data)')
    # t1_tail1.map(map_data) 

    # map 
    t1_gpf = gpd.read_file("data/ex_point_KWANGJU.geojson")
    # t1_gpd_file = {'latitude':[37.7749,34.0522,40.7128],
    #                'longitude':[126.87954220,126.87554220,126.87964220]}
    t1_gpf_df = pd.DataFrame(t1_gpf) 

    base_position = [35.18668601, 126.87954220] 

    t1_tail1.map(t1_gpf_df)    