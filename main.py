# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 11:19:11 2021

@author: 1605309
"""

import streamlit as st
from sidebar import Sidebar
from edit_profile import edit_profile 
from admin import admin
from analysis import analysis
from about import about

#root page

def app() : 

#EDIT PROFILE
#ADMIN
#ANALYSIS
#ABOUT

#sidebar options
   side_bar = Sidebar()
   side_bar.add_app("ABOUT",about.app)
   side_bar.add_app("EDIT PROFILE",edit_profile.change)
   if(st.session_state.isAdmin == 1):
         side_bar.add_app("ADMIN",admin.app)
   side_bar.add_app("ANALYSIS",analysis.app)

#run app
   side_bar.run()

#show about content using this only when
#all keys are False
  

