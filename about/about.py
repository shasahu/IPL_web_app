# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 11:42:35 2021

@author: 1605309
"""

import streamlit as st
import pandas as pd


def call_func(tup):
    lst = list(tup)
    if(st.session_state.isAdmin == 1):lst.insert(0,3)
    else : lst.insert(0,2)
    st.session_state.indexes = lst.copy()
    
def app() :
    text = "<p>"
    with open("about/text.txt") as f: 
        for t in f.readlines(): text += t
    text += "</p>"
    st.header("IPL DATA ANALYSIS SYSTEM")
    st.markdown(text,unsafe_allow_html=True)

    with st.container():
        
        df = pd.read_csv("log/{}.csv".format(st.session_state.curUserID))
        most_visit = list(df[df['Activity'] == "ANALYSIS"].groupby("Description").count().sort_values("Activity",ascending=False).index)
        
            
        n = min(len(most_visit),4)
        if(n == 0) : return
        
        st.markdown("<br /><h1>MOST FREQUENTLY ACCESS BY YOU</h1>",unsafe_allow_html=True)
        index = []
        question = []    
        for i in range(n):
            tmp = most_visit[i].split('/')
            index.append([int(x) for x in tmp[0].split()])
            question.append(tmp[1])
        
        
        for i in range(n) :
            with st.expander(question[i]):
                st.button("Go",key="mostlyVisitButton"+str(i),on_click = call_func,args=[tuple(index[i].copy())])
                