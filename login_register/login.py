# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 21:54:07 2021

@author: 1605309
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 11:39:59 2021

@author: 1605309
"""
import streamlit as st
import mysql.connector as mc
from csv import writer
from datetime import datetime

def check_it() :
    ck_usr = st.session_state.userIDlogin
    ck_pass = st.session_state.passwordlogin
    
    if(ck_usr == "") :
        st.warning("please fill user ID")
        return
    if(ck_pass == "") :
        st.warning("please fill password")
        return
    
        
    db_conn = mc.connect(user='root',password='Summer@1',host='localhost', database='ipl')
    db_cursor = db_conn.cursor()
        
    query = '''select *
               from user
               where userID="{}" and password="{}"'''.format(ck_usr,ck_pass)
           
    db_cursor.execute(query)
    tmp = db_cursor.fetchall()
    db_conn.close()
    if(len(tmp) == 0) :
        st.warning("Wrong user ID and password!")
    else :
        st.session_state["isAdmin"] = tmp[0][6]
        st.session_state["success"] = True
        st.session_state["curUserID"] = tmp[0][0]
        st.session_state["curUser"] = tmp[0][1]
        st.session_state["curemail"] = tmp[0][2]
        st.session_state["curPass"] = tmp[0][3]
        st.session_state["profilePic"] = tmp[0][5]
        
        with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
            write = writer(f)
            write.writerow([str(datetime.now()),"LOGIN","Login as {}".format(st.session_state.curUserID)])
            f.close()

def app() : 
    st.text_input(label="User ID : ",key="userIDlogin")
    st.text_input(label="Enter Password : ",key="passwordlogin",type="password")
    st.button("Login",key="login",on_click=check_it)
        
