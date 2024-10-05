# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 11:44:21 2021

@author: 1605309
"""
import streamlit as st
from csv import writer
from datetime import datetime

class Sidebar : 
    
    def __init__(self):
        self.apps = {}
        
    def add_app(self,name,func):
        self.apps[name] = func
        
    def call_func(self):
        with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
            write = writer(f)
            write.writerow([str(datetime.now()),"LOGOUT","Logout as {}".format(st.session_state.curUserID)])
            f.close()
        
        for key in st.session_state.keys():
            del st.session_state[key]
            
    def call_func2(self):
        st.session_state.indexes[1] = 0
        st.session_state.indexes[2] = 0
        if(st.session_state.selectBox == "ABOUT"):
            st.session_state.indexes[0] = 0
        elif(st.session_state.selectBox == "EDIT PROFILE") :
            st.session_state.indexes[0] = 1
        elif(st.session_state.selectBox == "ADMIN") :
            st.session_state.indexes[0] = 2
        else : 
            if(st.session_state.isAdmin == 1) : st.session_state.indexes[0] = 3
            else : st.session_state.indexes[0] = 2
            
    def run(self):
        cols = st.sidebar.columns(2)
        cols[0].image(st.session_state.profilePic,use_column_width='always')
        cols[1].write('')
        cols[1].write('')
        cols[1].write('')
        cols[1].header(st.session_state.curUser.upper())
        
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.write('')
        st.sidebar.selectbox("Choose Among :",self.apps.keys(),index = st.session_state.indexes[0],key="selectBox",on_change=self.call_func2)
        st.sidebar.button("Logout",key="logout",on_click=self.call_func)
        self.apps[st.session_state.selectBox]()

        