# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 14:08:38 2021

@author: 1605309
"""

import streamlit as st
from analysis.matches.questions import que1
from analysis.matches.questions import que2
from analysis.matches.questions import que3
from analysis.matches.questions import que4
from analysis.matches.questions import que5

def call_func():
    if(st.session_state.selectboxAnalysisMatchQues["serialNo"] == "none"):
        st.session_state.indexes[2] = 0
    else : st.session_state.indexes[2] = int(st.session_state.selectboxAnalysisMatchQues["serialNo"].split()[1])
    
def match_func():
    lst = [{"serialNo" : "none"}]
    lst.append({"serialNo" : "Analysis 1","ques" : que1.question,"func" : que1.app})
    lst.append({"serialNo" : "Analysis 2","ques" : que2.question,"func" : que2.app})
    lst.append({"serialNo" : "Analysis 3","ques" : que3.question,"func" : que3.app})
    lst.append({"serialNo" : "Analysis 4","ques" : que4.question,"func" : que4.app})
    lst.append({"serialNo" : "Analysis 5","ques" : que5.question,"func" : que5.app})

    cols = st.columns((2,1,1))
    
    with cols[0]:
        for i in range(5):
            st.write(lst[i+1]["serialNo"]," > ",lst[i+1]["ques"])
    with cols[2]:
        st.selectbox("Choose :",lst,format_func = lambda x : x["serialNo"],index = st.session_state.indexes[2],key="selectboxAnalysisMatchQues",on_change=call_func)
        
    
    with st.container():
        for i in range(10):st.write("")
        typ = st.session_state.selectboxAnalysisMatchQues
        if(typ["serialNo"] == "Analysis 1"):
            typ["func"]()
        elif(typ["serialNo"] == "Analysis 2"):
            typ["func"]()
        elif(typ["serialNo"] == "Analysis 3"):
            typ["func"]()
        elif(typ["serialNo"] == "Analysis 4"):
            typ["func"]()
        elif(typ["serialNo"] == "Analysis 5"):
            typ["func"]()