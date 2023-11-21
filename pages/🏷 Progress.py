import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
st.set_option('deprecation.showPyplotGlobalUse', False)
import plotly.graph_objs as go

#uncomment this line if you use mysql
#from query import *

st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
st.header("의류 시장 트렌드 데이터 분석 | 상품, 지역, 국가별 ")

#all graphs we use custom css not streamlit 
theme_plotly = None 


# load Style css
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#uncomment these two lines if you fetch data from mysql
#result = view_all_data()
#df=pd.DataFrame(result,columns=["Policy","Expiry","Location","State","Region","Investment","Construction","BusinessType","Earthquake","Flood","Rating","id"])
df=pd.read_excel('통합 문서3.xlsx', sheet_name='통합 문서3')
st.write("- 개별 상품 구매 데이터셋")

st.dataframe(df,use_container_width=True)
        
#load excel file | comment this line when  you fetch data from mysql
df=pd.read_excel('data.xlsx', sheet_name='Sheet1')

#side bar logo


#switcher

region=st.sidebar.multiselect(
    "스타일",
     options=df["Style"].unique(),
     default=df["Style"].unique()
)
location=st.sidebar.multiselect(
    "성별",
     options=df["Gender"].unique(),
     default=df["Gender"].unique()
)


df_selection = df[df["Style"].isin(region) & df["Gender"].isin(location)]





#this function performs basic descriptive analytics like Mean,Mode,Sum  etc
def Home():
    with st.expander("- 국가별 판매 데이터셋 보기"):
        showData=st.multiselect('Filter: ',df_selection.columns,default=["Expiry","Gender","Brand","Style","Revenue","Age","Rating"])
        st.dataframe(df_selection[showData],use_container_width=True)
    

   

#graphs
def graphs():
    #total_investment=int(df_selection["Investment"]).sum()
    #averageRating=int(round(df_selection["Rating"]).mean(),2) 
    #simple bar graph  investment by business type
    investment_by_business_type=(
        df_selection.groupby(by=["Age"]).count()[["Revenue"]].sort_values(by="Revenue")
    )
    fig_investment=px.bar(
       investment_by_business_type,
       x="Revenue",
       y=investment_by_business_type.index,
       orientation="h",
       title="<b> 연령대별 판매량 </b>",
       color_discrete_sequence=["#0083B8"]*len(investment_by_business_type),
       template="plotly_white",
    )
    fig_investment.update_layout(
     plot_bgcolor="rgba(0,0,0,0)",
     font=dict(color="black"),  
    xaxis=(dict(showgrid=True))
     )

    #simple line graph investment by state
    investment_state=df_selection.groupby(by=["Brand"]).count()[["Revenue"]]
    fig_state=px.line(
       investment_state,
       x=investment_state.index,
       y="Revenue",
       orientation="v",
       title="<b> 브랜드별 판매량 </b>",
       color_discrete_sequence=["#0083b8"]*len(investment_state),
       template="plotly_white",
    )
    fig_state.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
     )

    left,right,center=st.columns(3)
    left.plotly_chart(fig_state,use_container_width=True)
    right.plotly_chart(fig_investment,use_container_width=True)
    
    with center:
      #pie chart
      fig = px.pie(df_selection, values='Rating', names='Brand', title='<b>브랜드별 판매 비율</b>')
      fig.update_layout(legend_title="브랜드", legend_y=0.9)
      fig.update_traces(textinfo='percent+label', textposition='inside')
      st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

#function to show current earnings against expected target     
def Progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
    target=3000000000
    current=df_selection["Revenue"].sum()
    percent=round((current/target*100))
    mybar=st.progress(0)

    if percent>100:
        st.subheader("Target done !")
    else:
     st.write("you have ",percent, "% " ,"of ", (format(target, 'd')), "TZS")
     for percent_complete in range(percent):
        time.sleep(0.1)
        mybar.progress(percent_complete+1,text=" Target Percentage")

#menu bar
def sideBar():
 with st.sidebar:
    selected=option_menu(
        menu_title="Main Menu",
        options=["Home","Progress"],
        icons=["house","eye"],
        menu_icon="cast",
        default_index=0
    )
 if selected=="Home":
    #st.subheader(f"Page: {selected}")
    Home()
    graphs()
 if selected=="Progress":
    #st.subheader(f"Page: {selected}")
    Progressbar()
    graphs()

sideBar()
st.sidebar.image("./뉴로고.jpg",caption="")






#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""

