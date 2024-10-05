# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 04:16:43 2021

@author: 1605309
"""

from login_register import login,register
import streamlit as st
import main

st.set_page_config(layout="wide",page_title="Indian Premier League",page_icon='favicon.ico')
hide_footer_style = """
<style>
.reportview-container .main footer {visibility: hidden;}    
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)

if("isAdmin" not in st.session_state.keys()) : 
    st.session_state["isAdmin"] = 0
if("success" not in st.session_state.keys()) : 
    st.session_state["success"] = False
if("curUser" not in st.session_state.keys()) : 
    st.session_state["curUser"] = ""
if("curPass" not in st.session_state.keys()) : 
    st.session_state["curPass"] = ""
if("curUserID" not in st.session_state.keys()) : 
    st.session_state["curUserID"] = ""
if("curemail" not in st.session_state.keys()) : 
    st.session_state["curemail"] = ""
if("profilePic" not in st.session_state.keys()) : 
    st.session_state["profilePic"] = ""
if("indexes" not in st.session_state.keys()) : 
    st.session_state["indexes"] = [0,0,0]


if(st.session_state["success"] == True)  :main.app()
else :
    c = st.container()
    c.write('')
    c.write('')
    c.write('')
    c.write('')  
    cols = st.columns(5)
    with cols[3]:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        res = st.selectbox("",["LOGIN","REGISTER"],index=0,key="selectBox")
    with cols[1]:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        if(res == "LOGIN") : login.app()
        elif(res == "REGISTER"): register.app()
    
    with cols[2]:
        st.title(res)
    
    #st.write(st.session_state)