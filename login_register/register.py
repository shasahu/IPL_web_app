# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 11:39:59 2021

@author: 1605309
"""
import streamlit as st
import mysql.connector as mc
from PIL import Image,ImageDraw,ImageFilter
import pandas as pd
from datetime import datetime

def mask_circle_transparent(pil_img, blur_radius, offset=0):
        offset = blur_radius * 2 + offset
        mask = Image.new("L", pil_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

        result = pil_img.copy()
        result.putalpha(mask)

        return result
    
def check_it(up_file) :
    ck_name = st.session_state.nameregister
    ck_usr = st.session_state.userIDregister
    ck_mail = st.session_state.emailregister
    ck_pass = st.session_state.passwordregister
    ck_repass = st.session_state.repasswordregister
    
    if(ck_name == "") :
        st.warning("please fill Name")
        return
    if(ck_mail == "") :
        st.warning("please fill email address")
        return
    if(ck_pass == "") :
        st.warning("please fill password")
        return
    if(ck_repass == ""):
        st.warning("please re-enter the password")
        return
    if(ck_pass != ck_repass) :
        st.warning("Please re-enter password correctly")
        return
    
    db_conn = mc.connect(user='root',password='Summer@1',host='localhost', database='ipl')
    db_cursor = db_conn.cursor()
    
    query = '''select userID,email from user'''
    db_cursor.execute(query)
    res = db_cursor.fetchall()
    for r in res:
        if(r[0] == ck_usr) : 
            st.warning("{} User ID not available".format(ck_usr))
            return
        if(r[1] == ck_mail) : 
            st.warning("Already user exist with same email")
            return
    
    if(up_file is not None) : 
        image = Image.open(up_file)
        image.save('pics/profile/original/{}.png'.format(ck_usr))
        image = image.resize((70,70))
        image = mask_circle_transparent(image,1)
        image.save('pics/profile/thumbnail/{}.png'.format(ck_usr))
        
        query = '''insert into user(userID,name,email,password,profilePic) 
               values("{}","{}","{}","{}","pics/profile/thumbnail/{}.png")'''.format(ck_usr,ck_name,ck_mail,ck_pass,ck_usr)
    else : 
        query = '''insert into user(userID,name,email,password) 
               values("{}","{}","{}","{}")'''.format(ck_usr,ck_name,ck_mail,ck_pass)
    
    db_cursor.execute(query)
    db_conn.commit()
    db_conn.close()
        
    df = pd.DataFrame(columns = ["DateTime","Activity","Description"])
    df.loc[0] = [str(datetime.now()),"REGISTER","Created Account {}".format(ck_usr)]
    df.to_csv("log/{}.csv".format(ck_usr),index=False)
    
    st.success("Sucessfully added you, Now please login!")
         
    
def app() : 
    st.text_input(label = "Enter Full Name : ",key = "nameregister")
    st.text_input(label = "Email : ",key = "emailregister")
    st.text_input(label = "Unique User Name : ",key="userIDregister")
    st.text_input(label = "Enter Password : ",key = "passwordregister",type = "password")
    st.text_input(label = "Confirm Password : ",key = "repasswordregister",type = "password")
    up_file = st.file_uploader("Upload Profile Pic",type=['jpeg','png','jpg'],key="uploadPic")
    
    st.button("Register",key="register",on_click=check_it,args=[up_file])
    #st.button("login",key="gotologin",on_click=login.app)
        