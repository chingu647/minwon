import streamlit as st 
# import plotly.express as px

def run_tab(): 
    # ----------------------------------------------------------------------- layout 
    head0, head1, head2 = st.columns( [0.2, 0.6, 0.2] )
    headt0,headt1,headt2= st.columns( [0.01, 0.98, 0.01] )

    body0, body1, body2 = st.columns( [0.2, 0.6, 0.2] )
    bodyt0,bodyt1,bodyt2= st.columns( [0.01, 0.98, 0.01] )

    tail0, tail1, tail2 = st.columns( [0.2, 0.6, 0.2] ) 

    # -----------------------------------------------------------------------  
    head0.markdown("###### 오늘의 이슈") 
    head0.markdown("오늘의 이슈") 
    head0.markdown("오늘의 이슈") 
    head0.markdown("오늘의 이슈") 
    head0.markdown("오늘의 이슈") 
    head0.markdown("오늘의 이슈") 
    head0.markdown("오늘의 이슈") 
    head0.markdown("오늘의 이슈") 
    head0.markdown("오늘의 이슈") 
    # -----------------------------------------------------------------------  
    head1.markdown("###### 민원건수 현황") 

    # -----------------------------------------------------------------------  
    head2.markdown("###### 지사.노선별 현황") 
    
    # -----------------------------------------------------------------------  
    headt1.markdown("""---""")     
    # -----------------------------------------------------------------------  
    body0.markdown("###### 민원 키워드 클라우드") 

    # -----------------------------------------------------------------------  
    body1.markdown("###### 공지사항") 

