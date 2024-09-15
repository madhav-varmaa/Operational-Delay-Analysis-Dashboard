

import pandas as pd  
import plotly.express as px  
import streamlit as st  



# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")



@st.cache_data
def load_csv(url):
    # Simulate an expensive data loading operation
    data = pd.read_csv(url)
    return data
def load_xls(url):
    # Simulate an expensive data loading operation
    data = pd.read_excel(url)
    return data
url = 'sample.csv'
url2 ='master_data.xls'
df = load_csv(url)
df_master = load_xls(url2)



#basic pre-processing
df = df.fillna('others')

#extracting year,month and day from the date

df['DEL_DATE'] = pd.to_datetime(df['DEL_DATE'])

# Extract the year and month
df['year'] = df['DEL_DATE'].dt.year
df['month'] = df['DEL_DATE'].dt.month
df['day'] = df['DEL_DATE'].dt.day


df = pd.merge(df, df_master, how='left', left_on=['SHOP_CODE', 'EQPT'], right_on=['SHOP_CODE', 'EQPT'])



df = df.fillna('others')



# ---- SIDEBAR ----
st.sidebar.header("DELAYS")
st.sidebar.markdown("Process delays in steel plants can occur due to various factors related to machinery, operations, and external influences. Let’s explore some common reasons for process delays in steel plants: Equipment Breakdowns, Supply Chain Disruptions, Quality Control and Inspection, Design Changes and Modifications, Unplanned Maintenance and Repairs, Process Optimization Challenge, Human Factors, Environmental Factors, Complex Production Sequences")

year_slider = st.sidebar.slider('Slide:', min_value=2003, max_value=2005, value=2003)

df_selection = df.query(
    "year == @year_slider" )

if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.switch_page("login_dashboard.py")


# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.



# ---- MAINPAGE ----
st.title(":bar_chart: Delays Dashboard")
st.markdown("##")

# TOP KPI's
total_delay_count = int(df_selection["EFF_DURATION"].count())
total_delay = int(df_selection["EFF_DURATION"].sum())
average_delay = round(df_selection["EFF_DURATION"].mean(), 2)

left_col,middle_col, right_col = st.columns(3)

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


# DELAYS BY MONTH [LINE CHART]
delays_by_mon_line = df_selection.groupby(by=["month"])["EFF_DURATION"].mean().reset_index()

fig_mon_delays = px.line(
    delays_by_mon_line,
    x = "month",
    y = "EFF_DURATION",
    title="DELAYS BY MONTH ",
    template="plotly_white",
)
fig_mon_delays.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)



fig_shop_pie  = px.pie(df_selection, names='MASTER_SHOP',
                           values='EFF_DURATION',
                           color='MASTER_SHOP',  # Specify the color column
                           color_discrete_sequence=px.colors.qualitative.Plotly,  #built=in color function of plotly
                           title='DELAYS BY SHOPS')



bar_selection = df_selection.groupby("EQPT")["EFF_DURATION"].mean().reset_index()

fig_eqpt_bar = px.bar(bar_selection, x="EQPT", y="EFF_DURATION", title = "Delays by EQUIPMENT")


st.plotly_chart(fig_mon_delays, use_container_width=True)
st.markdown("""---""")
st.plotly_chart(fig_eqpt_bar, use_container_width=True)
st.markdown("""---""")
st.plotly_chart(fig_shop_pie, use_container_width=True)
st.markdown("""---""")


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

