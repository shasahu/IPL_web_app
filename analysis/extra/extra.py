# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 14:08:38 2021

@author: 1605309
"""

import streamlit as st
from analysis.extra.questions import que1
from analysis.extra.questions import que2
from analysis.extra.questions import que3

def call_func():
    if(st.session_state.selectboxAnalysisExtraQues["serialNo"] == "none"):
        st.session_state.indexes[2] = 0
    else : st.session_state.indexes[2] = int(st.session_state.selectboxAnalysisExtraQues["serialNo"].split()[1])
    
def extra_func():
    lst = [{"serialNo" : "none"}]
    lst.append({"serialNo" : "Analysis 1","ques" : que1.question,"func" : que1.app})
    lst.append({"serialNo" : "Analysis 2","ques" : que2.question,"func" : que2.app})
    lst.append({"serialNo" : "Analysis 3","ques" : que3.question,"func" : que3.app})

    cols = st.columns((2,1,1))
    
    with cols[0]:
        for i in range(3):
            st.write(lst[i+1]["serialNo"]," > ",lst[i+1]["ques"])
    with cols[2]:
        st.selectbox("Choose :",lst,format_func = lambda x : x["serialNo"],index = st.session_state.indexes[2],key="selectboxAnalysisExtraQues",on_change=call_func)
        
    
    with st.container():
        for i in range(10):st.write("")
        typ = st.session_state.selectboxAnalysisExtraQues
        if(typ["serialNo"] == "Analysis 1"):
            typ["func"]()
        elif(typ["serialNo"] == "Analysis 2"):
            typ["func"]()
        elif(typ["serialNo"] == "Analysis 3"):
            typ["func"]()
    