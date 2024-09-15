#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd  
import plotly.express as px  
import streamlit as st  


# In[ ]:





# In[2]:


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


# In[5]:


@st.cache_data
def load_csv(url):
    # Simulate an expensive data loading operation
    data = pd.read_csv(url)
    return data
def load_xls(url):
    # Simulate an expensive data loading operation
    data = pd.read_excel(url)
    return data
url = 'conveyor.csv'
url2 ='master_data.xls'
df = load_csv(url)
df_master = load_xls(url2)


# In[6]:


#basic pre-processing
df = df.fillna('others')


# In[7]:


#extracting year,month and day from the date

df['DEL_DATE'] = pd.to_datetime(df['DEL_DATE'])

# Extract the year and month
df['year'] = df['DEL_DATE'].dt.year
df['month'] = df['DEL_DATE'].dt.month
df['day'] = df['DEL_DATE'].dt.day


# In[8]:


df = pd.merge(df, df_master, how='left', left_on=['SHOP_CODE', 'EQPT'], right_on=['SHOP_CODE', 'EQPT'])


# In[9]:


df = df.fillna('others')


# In[11]:


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")


from_date = st.sidebar.date_input('From date:', pd.to_datetime('2003-07-27'))

to_date = st.sidebar.date_input('To date:', pd.to_datetime('2003-07-27'))

eqpt = st.sidebar.multiselect(
    "Select the Equipment:",
    options=df["EQPT"].unique(),
)

shop_code = st.sidebar.multiselect(
    "Select the SHOP:",
    options=df["MASTER_SHOP"].unique(),
)

if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.switch_page("login_dashboard.py")


if from_date and to_date and shop_code and not eqpt:
    df_selection = df.query("DEL_DATE >= @from_date & DEL_DATE <= @to_date & MASTER_SHOP== @shop_code  ")
    
elif from_date and to_date and eqpt and not shop_code :
    df_selection = df.query("DEL_DATE >= @from_date & DEL_DATE <= @to_date & EQPT == @eqpt ")
    
elif from_date and to_date and shop_code and not eqpt :
    df_selection = df.query("DEL_DATE >= @from_date & DEL_DATE <= @to_date & MASTER_SHOP == @shop_code ")

elif not eqpt and not shop_code:
    df_selection = df.query(" DEL_DATE >= @from_date & DEL_DATE <= @to_date")
    
else:
    df_selection = df.query(" EQPT == @eqpt & DEL_DATE >= @from_date & DEL_DATE <= @to_date & MASTER_SHOP == @shop_code")

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.



# In[ ]:





# In[12]:


# ---- MAINPAGE ----
st.title(":bar_chart: Delays Dashboard")
st.markdown("##")

# TOP KPI's
total_delay_count = int(df_selection["EFF_DURATION"].count())
total_delay = int(df_selection["EFF_DURATION"].sum())
average_delay = round(df_selection["EFF_DURATION"].mean(), 2)

left_col, middle_col, right_col = st.columns(3)

with left_col:
    st.subheader("Total Delays count")
    st.subheader(f" {total_delay_count:,}")
    
with middle_col:
    st.subheader("Total Delay in Hours")
    st.subheader(f" {total_delay:,}")  
    
with right_col:
    st.subheader("Average Delay in Hours")
    st.subheader(f"{average_delay}")
    
st.markdown("""---""")


# In[13]:


bar_selection= df_selection.groupby(["EQPT"])["EFF_DURATION"].mean().reset_index()

fig_bar_eqpt = px.bar(bar_selection, x="EQPT", y="EFF_DURATION", title="DELAYS BY EQUIPMENT")

fig_bar_eqpt.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


# In[14]:


bar_con_selection= df_selection.groupby(["SUB_EQPT"])["EFF_DURATION"].mean().reset_index()

fig_bar_con = px.bar(bar_con_selection, x="SUB_EQPT", y="EFF_DURATION", title="DELAYS BY CONVEYORS")

fig_bar_con.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


# In[15]:


fig_con_pie  = px.pie(df_selection, names='SUB_EQPT',
                           values='EFF_DURATION',
                           color='SUB_EQPT',  # Specify the color column
                           color_discrete_sequence=px.colors.qualitative.Plotly,  #built=in color function of plotly
                           title='DELAYS BY CONVEYORSs')


# In[16]:


fig_shop_code_pie  = px.pie(df_selection, names='MASTER_SHOP',
                           values='EFF_DURATION',
                           color='MASTER_SHOP',  # Specify the color column
                           color_discrete_sequence=px.colors.qualitative.Plotly,  #built=in color function of plotly
                           title='DELAYS BY SHOP')


# In[17]:


st.plotly_chart(fig_bar_con, use_container_width=True)
st.plotly_chart(fig_con_pie, use_container_width=True)
st.plotly_chart(fig_bar_eqpt, use_container_width=True)
st.plotly_chart(fig_shop_code_pie, use_container_width=True)


# In[ ]:





# In[ ]:





# In[ ]:




