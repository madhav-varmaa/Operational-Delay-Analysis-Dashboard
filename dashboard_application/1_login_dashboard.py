#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
from st_pages import hide_pages 
from time import sleep
import streamlit as st

import mysql.connector

import bcrypt


# In[3]:


# Connect to MySQL database
db_host = 'localhost'
db_user = 'root'
db_password = '123456'
db_name = 'dashboard'
auth   ='mysql_native_password'

conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    auth_plugin=auth
)

cursor = conn.cursor()


# In[4]:


hide_pages(["Dashboard" , "Delays_Entry", "Shop_wise_Major_Delays", "Date_wise_Delays", "Continued_Delays", "Conveyor_Delays", "Raw_Material_Delays", "Agency_wise_Delays" ])


# In[11]:


# Streamlit UI
st.title("LOGIN")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

        # Check user credentials
        sql = "SELECT hash FROM users WHERE username = %s" 
        cursor.execute(sql, (username,))
        
        data = cursor.fetchone()
        hash_pw = data[0].encode('utf-8')
        
        pw_bytes = password.encode('utf-8')

        # Check if the entered password matches the stored hash
        if bcrypt.checkpw(pw_bytes, hash_pw):
            st.session_state.logged_in = True
             
        else:
            st.error("Invalid credentials. Please try again.")
        
# Close database connection
conn.close()

if st.session_state.get("logged_in"):
    sleep(1)
    st.switch_page("pages/1_Dashboard.py")
    show_pages(["1_Dashboard.py", "1_Delays_Entry.py", "2_Shop_wise_Major_Delays.py", "3_Date_wise_Delays.py", "4_Continued_Delays.py", "5_Conveyor_Delays.py", "6_Raw_Material_Delays.py", "7_Agency_wise_Delays.py"])
    
    


# In[ ]:




