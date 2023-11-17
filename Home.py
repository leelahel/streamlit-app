import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objs as go

# Uncomment this line if you use mysql
# from query import *

st.set_option('deprecation.showPyplotGlobalUse', False)

# Load Style css
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Uncomment these two lines if you fetch data from mysql
# result = view_all_data()
# df = pd.DataFrame(result, columns=["Policy","Expiry","Location","State","Region","Investment","Construction","BusinessType","Earthquake","Flood","Rating","id"])

# Load excel file | comment this line when you fetch data from mysql
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# Sidebar Logo
region = st.sidebar.multiselect(
    "SELECT REGION",
    options=df["Region"].unique(),
    default=df["Region"].unique(),
)
location = st.sidebar.multiselect(
    "SELECT LOCATION",
    options=df["Location"].unique(),
    default=df["Location"].unique(),
)
construction = st.sidebar.multiselect(
    "SELECT CONSTRUCTION",
    options=df["Construction"].unique(),
    default=df["Construction"].unique(),
)

df_selection = df.query(
    "Region==@region & Location==@location & Construction ==@construction"
)

# Function for basic descriptive analytics like Mean, Mode, Sum, etc.
def Home():
    with st.expander("VIEW EXCEL DATASET"):
        showData = st.multiselect('Filter: ', df_selection.columns, default=["Policy", "Expiry", "Location", "State", "Region", "Investment", "Construction", "BusinessType", "Earthquake", "Flood", "Rating"])
        st.dataframe(df_selection[showData], use_container_width=True)
    
    # Compute top analytics
    total_investment = float(df_selection['Investment'].sum())
    investment_mode = float(df_selection['Investment'].mode())
    investment_mean = float(df_selection['Investment'].mean())
    investment_median = float(df_selection['Investment'].median())
    rating = float(df_selection['Rating'].sum())

    total1, total2, total3, total4, total5 = st.columns(5, gap='small')
    with total1:
        st.info('Total Sum Investment', icon="💰")
        st.metric(label="Sum TZS", value=f"{total_investment:,.0f}")

    with total2:
        st.info('Most Frequent Investment', icon="💰")
        st.metric(label="Mode TZS", value=f"{investment_mode:,.0f}")

    with total3:
        st.info('Average Mean', icon="💰")
        st.metric(label="Average TZS", value=f"{investment_mean:,.0f}")

    with total4:
        st.info('Central Earnings', icon="💰")
        st.metric(label="Median TZS", value=f"{investment_median:,.0f}")

    with total5:
        st.info('Ratings', icon="💰")
        st.metric(label="Rating", value=numerize(rating), help=f""" Total Rating: {rating} """)
    style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938")

    # Variable distribution Histogram
    with st.expander("EXPLORATORY VARIABLE DISTRIBUTIONS BY FREQUENCY"):
        df.hist(figsize=(16, 8), color='#898784', zorder=2, rwidth=0.9, legend=['Investment'])
        st.pyplot()

# Graphs
def graphs():
    # Simple bar graph investment by business type
    investment_by_business_type = (
        df_selection.groupby(by=["BusinessType"]).count()[["Investment"]].sort_values(by="Investment")
    )
    fig_investment = px.bar(
        investment_by_business_type,
        x="Investment",
        y=investment_by_business_type.index,
        orientation="h",
        title="<b> INVESTMENT BY BUSINESS TYPE </b>",
        color_discrete_sequence=["#0083B8"] * len(investment_by_business_type),
        template="plotly_white",
    )
    fig_investment.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        xaxis=(dict(showgrid=True))
    )

    # Simple line graph investment by state
    investment_state = df_selection.groupby(by=["State"]).count()[["Investment"]]
    fig_state = px.line(
        investment_state,
        x=investment_state.index,
        y="Investment",
        orientation="v",
        title="<b> INVESTMENT BY STATE </b>",
        color_discrete_sequence=["#0083b8"] * len(investment_state),
        template="plotly_white",
    )
    fig_state.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False))
    )

    left, right, center = st.columns(3)
    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_investment, use_container_width=True)

    with center:
        # Pie chart
        fig = px.pie(df_selection, values='Rating', names='State', title='RATINGS BY REGIONS')
        fig.update_layout(legend_title="Regions", legend_y=0.9)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

# Function to show current earnings against expected target
def Progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""", unsafe_allow_html=True,)
    target = 3000000000
    current = df_selection["Investment"].sum()
    percent = round((current / target * 100))
    mybar = st.progress(0)

    if percent > 100:
        st.subheader("Target done !")
    else:
        st.write("you have ", percent, "% ", "of ", (format(target, 'd')), "TZS")
        for percent_complete in range(percent):
            time.sleep(0.1)
            mybar.progress(percent_complete + 1, text=" Target Percentage")

# Sidebar Menu
def sideBar():
    with st.sidebar:
        st.button("🏷 CAMERA", key="camera_btn")  # Add a new button
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Progress"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0
        )
    if selected == "Home":
        Home()
        graphs()
    if selected == "Progress":
        Progressbar()
        graphs()

# Define action when the "CAMERA" button is clicked
if st.sidebar.button("🏷 CAMERA", key="camera_btn"):
    st.write("You clicked the CAMERA button! Add your camera-related content here.")

sideBar()
st.sidebar.image("data/logo1.png", caption="")

# Theme
hide_st_style = """ 
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""
