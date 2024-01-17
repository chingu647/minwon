import streamlit as st 
import plotly.express as px
import pandas as pd
import numpy as np 
import geopandas as gpd 
import folium 
from streamlit_folium import folium_static 

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
    t1_gpf = t1_gpf[ ['노선번호','X좌표값', 'Y좌표값'] ]
    t1_gpf.columns = ['노선번호','latitude','longitude'] 


    t1_gpf = t1_gpf.iloc[:5, :]


    base_position = [35.18668601, 126.87954220] 

    t1_map = folium.Map( location=base_position, zoom_start=12, tiles='cartodbpositron') 

    for index, row in t1_gpf.iterrows():
        folium.CircleMarker( location=[ row['latitude'], row['longitude'] ],  # 원 중심
                            radius=1,            # 원 반지름
                            color='blue',        # 원 테두리 색상
                            fill=True,           # 원 채움
                            fill_opacity=1.0     # 원 채움 투명도
                            ).add_to(t1_map) 
        
        folium.Marker( location=[ row['latitude'], row['longitude'] ],  # 값 중심 
                      popup=row['노선번호'],
                      tooltip=row['latitude'],
                      icon=folium.Icon(color='red', icon='star'), 
                    #   icon=folium.DivIcon(                              # 값 표시방식
                    #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
                      ).add_to(t1_map) 



    folium_static(t1_map) #, width=800, height=600)

    # t1_tail1.dataframe(t1_gpf) 

    # t1_gpf = {'latitude':[37.7749,34.0522,40.7128],
    #                'longitude':[126.87954220,126.87554220,126.87964220]}
    # t1_gpf_df = gpd.GeoDataFrame(t1_gpf) 
    # t1_tail1.dataframe(t1_gpf_df)   

    # base_position = [35.18668601, 126.87954220] 

    # t1_tail1.map(data=t1_gpf, latitude='latitude', longitude='longitude')  

