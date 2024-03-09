import streamlit as st
import os
from datetime import datetime, timedelta
import subprocess
import sys
import pandas as pd
import plotly.express as px
from streamlit_card import card


@st.cache_data
def get_data_from_csv(filename):
    df = pd.read_csv(filename)
    return df.dropna(subset=['Continent'])


def main():
    st.set_page_config(page_title="🦠 Corona Tracker DashBoard 🚑", page_icon="🦠", layout="wide")
    run_spider()
    df = get_data_from_csv('data.csv')
    st.title("🦠 :blue[Corona] :red[DashBoard] :green[Tracker] 🚑")
    st.sidebar.header("Corona Filter 🚑")
    continent = st.sidebar.multiselect(
        "Select the Continent:",
        options=df['Continent'].unique(),
        default=df['Continent'].unique()[0]
    )
    country = st.sidebar.multiselect(
        "Select the Country:",
        options=df['Country'].unique(),
        default=df['Country'].unique()[0]
    )
    st.sidebar.markdown('''
    ---
    Created with ❤️ by A00N.
    ''')
    df_selection = df.query(
        "Country == @country | Continent == @continent"
    )
    if df_selection.empty:
        st.warning("No data available based on the current filter settings!")
        st.stop()
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        card(
            title="{:,}".format(df_selection['Total Cases'].sum() if 'World' not in df_selection['Country'].values else
                                df_selection[df_selection['Country'] == 'World']['Total Cases'].sum()),
            text="Total Cases",
            key="card1",
            styles={
                "card": {
                    "width": "100%",
                    "height": "200px",
                    "padding": "0px",
                    "margin": "0px",
                    "background-color": "#387ADF",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    "border": "1px solid #374558"
                },
                "text": {
                    'font-size': '20px'
                }
            }
        )
    with col2:
        card(
            title="{:,}".format(df_selection['Total Deaths'].sum() if 'World' not in df_selection['Country'].values else
                                df_selection[df_selection['Country'] == 'World']['Total Deaths'].sum()),
            text="Total Deaths",
            key="card2",
            styles={
                "card": {
                    "width": "100%",
                    "height": "200px",
                    "padding": "0px",
                    "margin": "0px",
                    "background-color": "#7F27FF",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    "border": "1px solid #374558"
                },
                "text": {
                    'font-size': '20px'
                }
            }
        )
    with col3:
        card(
            title="{:,}".format(df_selection['Total Tests'].sum() if 'World' not in df_selection['Country'].values else
                                df_selection[df_selection['Country'] == 'World']['Total Tests'].sum()),
            text="Total Tests",
            key="card3",
            styles={
                "card": {
                    "width": "100%",
                    "height": "200px",
                    "padding": "0px",
                    "margin": "0px",
                    "background-color": "#416D19",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    "border": "1px solid #374558"
                },
                "text": {
                    'font-size': '20px'
                }
            }
        )
    with col4:
        card(
            title="{:,}".format(
                df_selection['Total Recovered'].sum() if 'World' not in df_selection['Country'].values else
                df_selection[df_selection['Country'] == 'World']['Total Recovered'].sum()),
            text="Total Recovered",
            key="card4",
            styles={
                "card": {
                    "width": "100%",
                    "height": "200px",
                    "padding": "0px",
                    "margin": "0px",
                    "background-color": "#D04848",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    "border": "1px solid #374558"
                },
                "text": {
                    'font-size': '20px'
                }
            }
        )
    grouped_df = df_selection.groupby("Continent")[['New Cases', 'New Deaths', 'New Recovered']].sum().reset_index()
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            fig = px.bar(grouped_df, x='Continent', y=['New Cases', 'New Deaths', 'New Recovered'], barmode='group',
                         labels={'value': 'Count', 'variable': 'Category'},
                         title='<b>New Cases, New Deaths, and New Recovered by Continent</b>')
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        with st.container(border=True):
            left, right = st.columns(2)
            with left:
                attribute_selectbox = st.selectbox('Select Attribute', [column for column in df.columns if
                                                                        column not in ['Country', 'Continent']])
            with right:
                top_k_options = {
                    'Top 5': 5,
                    'Top 10': 10,
                    'Top 15': 15,
                    'Top 20': 20
                }
                top_k_selectbox = st.selectbox('Select Top K', list(top_k_options.keys()))

            fig = px.bar(
                df.sort_values(attribute_selectbox, ascending=False).iloc[:top_k_options[top_k_selectbox]],
                x='Country', y=attribute_selectbox, title=f"Top Countries by {top_k_selectbox} in descending order")
            st.plotly_chart(fig, use_container_width=True)
    with st.container(border=True):
        box_option = st.selectbox("Select an option", ['Deaths/ 1M pop', 'Tests/ 1M pop '])
        fig = px.box(df[df['Continent'] != 'All'], x='Continent', y=box_option,
                     title='Box Plot of Total Cases by Continent', color='Continent')
        st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            fig = px.scatter(df_selection, x='Total Tests', y='Total Cases', color='Continent',
                             title='Total Tests vs Total Cases')
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        with st.container(border=True):
            fig = px.pie(df_selection, names='Continent', values='Total Deaths', title='Total Deaths by Continent')
            st.plotly_chart(fig, use_container_width=True)
    with st.container(border=True):
        continent_option = st.selectbox("Select a continent",
                                        ['Africa', 'Asia', 'Europe', 'North america', 'South america', 'USA', 'World'])
        fig = px.choropleth(df,
                            locations='Country',
                            locationmode='country names',
                            color='Total Cases',
                            hover_name='Country',
                            color_continuous_scale='RdYlGn_r',
                            title='Total Cases by Country',
                            range_color=(1, df['Total Cases'].max() / 1000),
                            scope=continent_option.lower(),
                            height=800,
                            width=1400
                            )
        st.plotly_chart(fig, use_container_width=True)


# @st.cache_resource
def run_spider():
    # subprocess.call(sys.executable + " -m scrapy crawl covid")
    if os.path.exists("last_execution.txt"):
        with open("last_execution.txt", "r") as file:
            last_execution_str = file.read().strip()
        last_execution_time = datetime.strptime(last_execution_str, "%Y-%m-%d %H:%M:%S")

        current_time = datetime.now()
        time_difference = current_time - last_execution_time

        if time_difference > timedelta(minutes=10):
            st.toast("Please wait for the spider to finish")
            subprocess.call([sys.executable, "-m", "scrapy", "crawl", "covid"])
            with open("last_execution.txt", "w") as file:
                file.write(current_time.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        st.toast("Please wait for the spider to finish")
        subprocess.call([sys.executable, "-m", "scrapy", "crawl", "covid"])
        with open("last_execution.txt", "w") as file:
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == '__main__':
    main()
