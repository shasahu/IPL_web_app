# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 09:03:02 2021

@author: 1605309
"""

import streamlit as st
import mysql.connector as mc
import os
from PIL import Image,ImageDraw,ImageFilter
from csv import writer
from datetime import datetime    


def check_it_u() : 
    if(st.session_state.newname == "") : 
        st.warning("Enter something")
    elif(st.session_state.curUser == st.session_state.newname) : 
        st.warning("You've entered same name, please change!")
    else : 
        db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
        db_cursor = db_conn.cursor()
        query = '''update user
                   set name="{}"
                   where name="{}"'''.format(st.session_state.newname,st.session_state.curUser)
        db_cursor.execute(query)
        db_conn.commit()
        db_conn.close()
        with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
            write = writer(f)
            write.writerow([str(datetime.now()),"CHANGE USERNAME","User change name from {} to {}".format(st.session_state.curUser,st.session_state.newname)])
            f.close()
        st.session_state.curUser = st.session_state.newname
        st.session_state.newname = ""
        st.success("Successfully change username")

def check_it_p() : 
    if(st.session_state.newPassword == "") : 
        st.warning("Enter something")
    elif(st.session_state.curPass == st.session_state.newPassword) : 
        st.warning("You've entered same password, please change!")
    else : 
        db_conn = mc.connect(user='root',password='Summer@1',host='localhost',database="ipl")
        db_cursor = db_conn.cursor()
        query = '''update user
                   set password="{}"
                   where password="{}"'''.format(st.session_state.newPassword,st.session_state.curPass)
        db_cursor.execute(query)
        db_conn.commit()
        db_conn.close()
        with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
            write = writer(f)
            write.writerow([str(datetime.now()),"CHANGE PASSWORD","User change password from {} to {}".format(st.session_state.curPass,st.session_state.newPassword)])
            f.close()
        st.session_state.curPass = st.session_state.newPassword
        st.session_state.newPassword = ""
        st.success("Successfully change Password")

def mask_circle_transparent(pil_img, blur_radius, offset=0):
        offset = blur_radius * 2 + offset
        mask = Image.new("L", pil_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

        result = pil_img.copy()
        result.putalpha(mask)

        return result
        
def check_it_pic(up_file,result):
    if(up_file is None) : 
        st.warning("Upload Something First!")
        return
    
    if(result == True):
       os.remove("pics/profile/original/{}.png".format(st.session_state.curUserID))
       os.remove(st.session_state.profilePic)
    else :
       db_conn = mc.connect(user='root',password='Summer@1',host='localhost', database='ipl')
       db_cursor = db_conn.cursor()
    
       query = '''update user
                  set profilePic="pics/profile/thumbnail/{}.png"
                  where userID = "{}"'''.format(st.session_state.curUserID,st.session_state.curUserID)
       db_cursor.execute(query)
       db_conn.commit()
       st.session_state.profilePic = "pics/profile/thumbnail/{}.png".format(st.session_state.curUserID)

    
    image = Image.open(up_file)
    image.save('pics/profile/original/{}.png'.format(st.session_state.curUserID))
    image = image.resize((100,90))
    image = mask_circle_transparent(image,1)
    image.save('pics/profile/thumbnail/{}.png'.format(st.session_state.curUserID)) 
    
    with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
            write = writer(f)
            write.writerow([str(datetime.now()),"UPLOAD NEW PROFILE PIC","User uploaded new profile pic"])
            f.close()

def check_it_rem():
    os.remove("pics/profile/original/{}.png".format(st.session_state.curUserID))
    os.remove(st.session_state.profilePic)
    
    db_conn = mc.connect(user='root',password='Summer@1',host='localhost', database='ipl')
    db_cursor = db_conn.cursor()
    
    query = '''update user
               set profilePic="pics/profile/thumbnail/default.png"
               where userID = "{}"'''.format(st.session_state.curUserID)
    db_cursor.execute(query)
    db_conn.commit()
    st.session_state.profilePic = "pics/profile/thumbnail/default.png"
    
    with open("log/{}.csv".format(st.session_state.curUserID),"a") as f:
            write = writer(f)
            write.writerow([str(datetime.now()),"REMOVE PROFILE PIC","User removed profile pic"])
            f.close()
        
def change() :
    cols = st.columns((3,1,3))
    cols[0].markdown("<h3>CHANGE NAME</h3>",unsafe_allow_html=True)
    cols[0].write('')
    cols[0].write('')
    cols[0].text_input("Enter New Name",key="newname")
    cols[0].button("Change Name",key="changename",on_click=check_it_u)
    
    cols[2].markdown("<h3>CHANGE PASSWORD</h3>",unsafe_allow_html=True)
    cols[2].write('')
    cols[2].write('')
    cols[2].text_input("Enter New Password",key="newPassword")
    cols[2].button("Change Password",key="changePassword",on_click=check_it_p)
    
    with st.container():
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.markdown("<h3>CHANGE PROFILE PICTURE</h3>",unsafe_allow_html=True)
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        s = "pics/profile/original/{}.png".format(st.session_state.curUserID)
        result = os.path.isfile(s)
        cols = st.columns(2)
        if(result == False) : cols[0].write("No profile pic")
        else : 
            image = Image.open(s)
            image = image.resize((200,200))
            cols[0].image(image)
        
        up_file = cols[1].file_uploader("New Profile Upload",type=['jpeg','png','jpg'],key="uploadNew")
        cols[1].button("Upload",on_click=check_it_pic,args=[up_file,result])
        if(result) : cols[1].button("Remove",on_click=check_it_rem)