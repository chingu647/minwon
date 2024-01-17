import streamlit as st 
import plotly.express as px
import pandas as pd
import numpy as np 
import geopandas as gpd 
import folium 

from streamlit_folium import folium_static 

def run_tab(): 
    # ----------------------------------------------------------------------- layout 
    t1_head0, t1_head1, t1_head2 = st.columns( [0.001, 0.998, 0.001] )
    
    t1_body0, t1_body1, t1_body2, t1_body3 = st.columns( [0.001, 0.499, 0.499, 0.001] )

    t1_tail0, t1_tail1, t1_tail2 = st.columns( [0.001, 0.998, 0.001] )

    # -----------------------------------------------------------------------  
    t1_head1.markdown("###### 안내문") 
    t1_head1.markdown(r"""
	1. 현대 사회에서 부동산은 모든 사람들의 관심사항이 되었으며, 특히 서울시 소재 부동산 가격에 대한 관심은 매우 크다고 할 수 있습니다.
	2. 이번 프로젝트에서는 서울시 구별로 부동산 가격차이를 데이터 시각화를 통해 알아보고, 회귀모델을 통해 주요 원인을 찾아보고자 합니다.
    """)

    # -----------------------------------------------------------------------  
    t1_body1.markdown("###### 이달의 이슈") 
    t1_body1_df = pd.read_csv("data/민원처리현황.csv")
    t1_body1_df = t1_body1_df.query("organ==구례지사" )
    t1_body1.table(t1_body1_df) 

    # -----------------------------------------------------------------------  
    t1_body2.markdown("###### 키워드 클라우드") 
    t1_body2_data = {'1':['a','b','c'],
                     'bool':[True, True, False]}
    t1_body2_df = pd.DataFrame(data=t1_body2_data) 
    t1_body2.table(t1_body2_df) 

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
    t1_gpf_point = gpd.read_file("data/ex_point_KWANGJU.geojson")
    t1_gpf_point = t1_gpf_point[ ['노선번호','X좌표값', 'Y좌표값'] ]
    t1_gpf_point.columns = ['노선번호','latitude','longitude'] 


    t1_gpf_point = t1_gpf_point.iloc[:5, :]

    base_position = [35.18668601, 126.87954220] 

    t1_map = folium.Map( location=base_position, zoom_start=9) #, tiles='Stamentoner') 


    t1_gpf_line = gpd.read_file("data/ex_line_KWANGJU.shp") 
    folium.GeoJson(t1_gpf_line,
                   style_function=lambda feature: {
                       'fillColor': 'blue' , #feature['properties']['color'],
                       'color': '#F5F6CE',
                       'weight': 3,
                       'dashArray': '5, 5',
                       'fillOpacity': 0.3, 
                       }
                    ).add_to(t1_map)


    for index, row in t1_gpf_point.iterrows():
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

    
    folium_static(t1_map, width=600) #, height=str(80))

     # t1_gpf = {'latitude':[37.7749,34.0522,40.7128],
    #                'longitude':[126.87954220,126.87554220,126.87964220]}
    # t1_gpf_df = gpd.GeoDataFrame(t1_gpf) 
    # t1_tail1.dataframe(t1_gpf_df)   

    # base_position = [35.18668601, 126.87954220] 

    # t1_tail1.map(data=t1_gpf, latitude='latitude', longitude='longitude')  

