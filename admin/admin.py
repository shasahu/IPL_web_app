# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 11:41:59 2021

@author: 1605309
"""
import streamlit as st
import mysql.connector as mc
import os
from csv import writer
from datetime import datetime  
import pandas as pd  

def remove_u_pic(userid):
    s = "pics/profile/original/{}.png".format(userid)
    s1 = "pics/profile/thumbnail/{}.png".format(userid)
    result = os.path.isfile(s)
    if(result == True) :
        os.remove(s)
        os.remove(s1)

def remove_u_log(userid):
    os.remove("log/{}.csv".format(userid))
        
def remove_u(accounts) : 
    db_conn = mc.connect(user="root",password="Summer@1",host="localhost",database="ipl")
    db_cursor = db_conn.cursor()
    query = '''delete from user
               where userID="{}"'''
    
    for account in accounts:
        if(st.session_state["adminCheckbox"+account[0]]) :
            if(account[0] != st.session_state.curUserID) :
                remove_u_pic(account[0])
                remove_u_log(account[0])
                db_cursor.execute(query.format(account[0]))
                with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
                        write = writer(f)
                        write.writerow([str(datetime.now()),"REMOVE USER","Remove user {}".format(account[0])])
                        f.close()
            else :st.warning("Cannot delete yourself!")
            
    db_conn.commit()
    db_conn.close()
    
def make_a(accounts) : 
    db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
    db_cursor = db_conn.cursor()
    query = '''update user
               set isAdmin={}
               where userID="{}"'''
    
           
    for account in accounts:
        if(st.session_state["adminCheckbox"+account[0]]) :
            if(account[0] != st.session_state.curUserID) :
                if(account[6] == 0):
                    with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
                        write = writer(f)
                        write.writerow([str(datetime.now()),"GRANT ADMIN PRIVILEGE","Grant admin privileges to {}".format(account[0])])
                        f.close()
                    db_cursor.execute(query.format(True,account[0]))
                else :st.warning("Already an Admin")
            else :st.warning("You are already Admin")          
    
    db_conn.commit()
    db_conn.close()
        

def remove_a(accounts) : 
    db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
    db_cursor = db_conn.cursor()
    query = '''update user
               set isAdmin={}
               where userID="{}"'''
               
    
    for account in accounts:
        if(st.session_state["adminCheckbox"+account[0]]) :
            if(account[0] != st.session_state.curUserID) :
                if(account[6] == 1):
                    with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
                        write = writer(f)
                        write.writerow([str(datetime.now()),"REMOVE ADMIN PRIVILEGE","Remove admin privileges of {}".format(account[0])])
                        f.close()
                    db_cursor.execute(query.format(False,account[0]))
                else :st.warning("Already not Admin")
            else :st.warning("Cannot change admin rights for yourself!")          
    
    db_conn.commit()
    db_conn.close()
        
def app() :
    db_conn = mc.connect(user="root",password="Summer@1",host="localhost",database="ipl")
    db_cursor = db_conn.cursor()
    
    query = '''select * from user'''
    db_cursor.execute(query)
    accounts = db_cursor.fetchall()
    
    with st.container():
        st.subheader("USERS DETAILS")
        st.write('')
        st.write('')
        st.dataframe(pd.read_sql("select userID,name,email,createdON,profilePic,isAdmin from user",db_conn))
        st.write('')
    
    with st.container():
        cols_1 = st.columns(2)
        with cols_1[0]:
            st.subheader("ACCOUNTS")
            st.write('')
            st.write('')
            for account in accounts:
                s = account[1] + " | " + account[0]
                if(account[6] == 1): s += " | "+"ADMIN"
                else : s += " | " + "NOT ADMIN"
                st.checkbox(s,value=False,key="adminCheckbox"+account[0])
            
        
        accounts_1 = [tuple(accounts)]
        
        with cols_1[1]:
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.button("Remove",key="removeUser",on_click=remove_u,args=accounts_1)
            st.button("Make Admin",key="makeAdminUser",on_click=make_a,args=accounts_1)
            st.button("Remove Admin Privileges",key="removeAdminUser",on_click=remove_a,args=accounts_1)
    
    with st.container():
        cols_2 = st.columns(2)
        
        accounts_2 = ["none"]
        
        for account in accounts:
            accounts_2.append(account[1]+" | "+account[0])
        
        with cols_2[0]:
            st.subheader("LOG")
            st.radio("",accounts_2,key="radioAdminLog")
        
        with cols_2[1]:
            if(st.session_state.radioAdminLog != "none") :
                st.write('')
                st.write('')
                temp = st.session_state.radioAdminLog.split(" | ")
                df = pd.read_csv("log/{}.csv".format(temp[1][0:]))
                st.write('')
                st.write('')
                st.dataframe(df)
                
                with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
                        write = writer(f)
                        write.writerow([str(datetime.now()),"CHECKED LOG","Checked log of user {}".format(temp[1][0:-1])])
                        f.close()