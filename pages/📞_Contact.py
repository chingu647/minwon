import streamlit as st 
import streamlit.components.v1 as components 

st.title('Contact')

with open('activity1.html') as file:
    components.html( file.read() )