#!/usr/bin/env python
# coding: utf-8

# # INSERT RECORDS

# In[154]:


import streamlit as st
from datetime import datetime as dt, timedelta
import pandas as pd

import mysql.connector


# In[155]:


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


# In[159]:


@st.cache_data
def load_csv(url):
    # Simulate an expensive data loading operation
    data = pd.read_csv(url)
    return data
def load_xls(url):
    # Simulate an expensive data loading operation
    data = pd.read_excel(url)
    return data

url2 ='master_data.xls'
df = load_xls(url2)
url = 'sample.csv'
df_delay = load_csv(url)


# In[160]:


#basic pre-processing
df_delay = df_delay.fillna('others')
df_delay = pd.merge(df_delay, df, how='left', left_on=['SHOP_CODE', 'EQPT'], right_on=['SHOP_CODE', 'EQPT'])
df_delay = df_delay.fillna('others')


# In[168]:


if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.switch_page("login_dashboard.py")

    
# Streamlit UI
st.title("ADD DELAY")


date = st.date_input("Date:")

    
st.markdown("""---""")

    
time1 = st.time_input("Enter delay start time: ")
time2 = st.time_input("Enter delay end time: ")

time1_obj = dt.strptime(str(time1), "%H:%M:%S")
time2_obj = dt.strptime(str(time2), "%H:%M:%S")

time_1 = timedelta(hours = time1_obj.hour, minutes = time1_obj.minute)
time_2 = timedelta(hours = time2_obj.hour, minutes = time2_obj.minute)
time_3 = timedelta(hours = 24, minutes = 0)
   

st.markdown("""---""")


checked = st.checkbox("Is the delay continued?")
if checked:
    st.write("Checkbox is checked!")
    continued = 'Y'
    durn = time_3 - time_1 + time_2
else:
    st.write("Checkbox is unchecked.")
    continued = 'N'
    durn = time_2 - time_1
    
eff_durn = durn.seconds / 3600
    
if checked and eff_durn == 0:
    eff_durn = 24

st.markdown("""---""")


m_shop = st.selectbox("Select the SHOP:", options=df["MASTER_SHOP"].unique() )


st.markdown("""---""")


df_eqpt = df.query("MASTER_SHOP == @m_shop")['EQPT']
eqpt = st.selectbox("Select the Equipment:", options = df_eqpt )


df_sub_eqpt = df_delay.query("MASTER_SHOP == @m_shop & EQPT == @eqpt")['SUB_EQPT']
sub_eqpt = st.selectbox("Select Sub-Equipment:", options = df_sub_eqpt.unique() )


shop = df.query("MASTER_SHOP == @m_shop & EQPT == @eqpt ")['SHOP_CODE']
shop = shop.to_string()

df_mat = df_delay.query("MASTER_SHOP == @m_shop & EQPT == @eqpt & SUB_EQPT == @sub_eqpt")["MATERIAL"]
mat = st.selectbox("Select the material: " , options = df_mat.unique())

if durn < timedelta(seconds = 1):
    st.warning("Enter valid time of the delay or check  the 'continued'")
    st.stop()

if st.button("ADD"):
    try:
        sql = "INSERT INTO delay VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"
        values = (date, shop , m_shop, time1.strftime("%H:%M:%S"), time2.strftime("%H:%M:%S"), durn, str(eqpt), continued, eff_durn, str(sub_eqpt), str(mat))
        cursor.execute(sql, values)
        conn.commit()
        st.success("Delay Record added successfully!")
    except mysql.connector.Error as e:
        st.warning(e)

conn.close()


    


# In[ ]:





# In[ ]:





# In[ ]:



    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




