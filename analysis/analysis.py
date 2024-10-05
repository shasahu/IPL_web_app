# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 11:42:20 2021

@author: 1605309
"""
import streamlit as st
from analysis.matches import matches
from analysis.batting import batting
from analysis.bowling import bowling
from analysis.player import player
from analysis.extra import extra

def call_func():
    st.session_state.indexes[2] = 0
    if(st.session_state.selectboxAnalysisType == "none"):
        st.session_state.indexes[1] = 0
    elif(st.session_state.selectboxAnalysisType == "matches") : 
        st.session_state.indexes[1] = 1
    elif(st.session_state.selectboxAnalysisType == "batting"):
        st.session_state.indexes[1] = 2
    elif(st.session_state.selectboxAnalysisType == "bowling"):
        st.session_state.indexes[1] = 3
    elif(st.session_state.selectboxAnalysisType == "players"):
        st.session_state.indexes[1] = 4
    elif(st.session_state.selectboxAnalysisType == "extra"):
        st.session_state.indexes[1] = 5

def app() :
    text = []
    with open("analysis/text.txt") as f: text = f.readlines()
    
    st.markdown("<style>h1{text-align:center;}</style>",unsafe_allow_html=True)
    st.title('ANALYSIS')
    st.write("")
        
    st.write(text[0])
    st.write("")
    
    lst = ["none","matches","batting","bowling","players","extra"]
    
    with st.container():
        for i in range(5):
            with st.container():
                cols = st.columns((1,4))
                with cols[0]:
                    st.image("analysis/icon{}.jpg".format(i+1),use_column_width=True)
                with cols[1]: 
                    st.subheader(lst[i+1].upper()) 
                    st.expander(text[i+1][0:80]).write(text[i+1])

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        cols1 = st.columns((1,1,1))
        cols1[1].selectbox("Choose Analysis Type",lst,format_func=lambda x:x.upper(),index = st.session_state.indexes[1],key="selectboxAnalysisType",on_change = call_func)
    
    with st.container():
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        typ = st.session_state.selectboxAnalysisType
        if(typ == "matches"):matches.match_func()
        elif(typ == "batting"):batting.bat_func()
        elif(typ == "bowling"):bowling.bowl_func()
        elif(typ == "players"):player.player_func()
        elif(typ == "extra"):extra.extra_func()
    