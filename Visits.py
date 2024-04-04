# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import hmac
from sqlalchemy import create_engine, text
from pydactyl import PterodactylClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time, os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from geopy.geocoders import Nominatim


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.


# Set page to wide mode
st.set_page_config(layout="wide")

# Add a big title for the full dashboard
st.title("Shlink Visit Data")

import credentials
connection = credentials.connection
SCHEMA_SHLINK = credentials.SCHEMA_SHLINK

# Get activity_analisis info
engine = create_engine(connection)
with engine.connect() as conn:
    shlink_analysis = conn.execute(text(f'SELECT * FROM {SCHEMA_SHLINK}.analysis'))
    shlink_analysis = pd.DataFrame(shlink_analysis)


# shlink_analysis data: 
    # tags 
    # referer 
    # date 
    # countryname 
    # regionname 
    # browser,
    # operating_system 
    # device


# Create a sidebar for global filters
st.sidebar.header('Filters')

# Add a date range selector
date_range_selection = st.sidebar.radio('Select Date Range', ('Last 24 hours', 'Last 7 days', 'Last 30 days', 'All Time'))

if date_range_selection == 'Last 24 hours':
    start_date = datetime.now() - timedelta(hours=24)
    end_date = datetime.now()
elif date_range_selection == 'Last 7 days':
    start_date = datetime.now() - timedelta(days=7)
    end_date = datetime.now()
elif date_range_selection == 'Last 30 days':
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()
else:
    start_date = shlink_analysis['date'].min().tz_convert(None)  # Convert to timezone-naive
    end_date = shlink_analysis['date'].max().tz_convert(None)  # Convert to timezone-naive

# Convert the start and end dates to pandas Timestamp objects with UTC timezone
start_date = pd.Timestamp(start_date, tz='UTC')
end_date = pd.Timestamp(end_date, tz='UTC')

# Filter the DataFrame based on the selected date range
if date_range_selection != 'All Time':
    shlink_analysis = shlink_analysis[(shlink_analysis['date'] >= start_date) & (shlink_analysis['date'] <= end_date)]
else:
    shlink_analysis = shlink_analysis







# Convert lists in 'tags' column back to strings
shlink_analysis['tags'] = shlink_analysis['tags'].apply(lambda x: ', '.join(x))

# Split the comma-separated tags and explode them into separate rows
exploded_tags = shlink_analysis['tags'].str.split(',').explode().str.strip()

# Remove duplicates and empty strings
unique_tags = exploded_tags[exploded_tags != ''].unique()

# Sidebar to select filtering tag
filter_tags = st.sidebar.multiselect("Filter by Tags", unique_tags)

# Sidebar to select filtering title
filter_titles = st.sidebar.multiselect("Filter by Title", shlink_analysis['title'].unique())

# Apply filter to the DataFrame
if not filter_tags and not filter_titles:  # If no tags or titles are selected, show all data
    shlink_analysis = shlink_analysis
else:
    shlink_analysis = shlink_analysis
    if filter_tags:
        shlink_analysis = shlink_analysis[shlink_analysis['tags'].str.contains('|'.join(filter_tags), na=False)]
    if filter_titles:
        shlink_analysis = shlink_analysis[shlink_analysis['title'].isin(filter_titles)]

# Convert 'date' column to datetime format
shlink_analysis['date'] = pd.to_datetime(shlink_analysis['date'])

# Group by date and count the number of occurrences
plot_data = shlink_analysis.groupby('date').size().reset_index(name='count')

# Plot the line plot using Plotly Express
fig = px.line(plot_data, x='date', y='count', title='Visits Over Time', labels={'date': 'Date', 'count': 'Visits'})

# Configure y-axis to display only integer numbers
fig.update_yaxes(tickmode='linear', tickformat=',d')

st.plotly_chart(fig)








# Grouping data by 'operating_system' and counting occurrences
os_counts = shlink_analysis['operating_system'].value_counts()

# Creating a donut plot for operating systems
fig_os = px.pie(names=os_counts.index, values=os_counts.values, title='Operating System Distribution', hole=0.5,
                width=400, height=400)

# Grouping data by 'browser' and counting occurrences
browser_counts = shlink_analysis['browser'].value_counts()

# Creating a donut plot for browsers
fig_browser = px.pie(names=browser_counts.index, values=browser_counts.values, title='Browser Distribution', hole=0.5,
                     width=400, height=400)

# Displaying the plots side by side
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_os)
with col2:
    st.plotly_chart(fig_browser)







# Grouping data by 'referer' and counting occurrences
referer_counts = shlink_analysis['referer'].value_counts().reset_index()
referer_counts.columns = ['referer', 'count']

# Creating a bar plot for referers with inverted axes
fig_referer = px.bar(referer_counts, y='referer', x='count', title='Referer Counts', 
                     labels={'referer': 'Referer', 'count': 'Count'}, orientation='h')

# Grouping data by 'countryname' and counting occurrences
country_counts = shlink_analysis['countryname'].value_counts().reset_index()
country_counts.columns = ['countryname', 'count']

# Creating a bar plot for countrynames with inverted axes and smaller size
fig_country = px.bar(country_counts, y='countryname', x='count', title='Visits by Country', 
                     labels={'countryname': 'Country', 'count': 'Visits'}, orientation='h',
                     width=500, height=400)

# Grouping data by 'regionname' and counting occurrences
region_counts = shlink_analysis['regionname'].value_counts().reset_index()
region_counts.columns = ['regionname', 'count']

# Creating a bar plot for regionnames with inverted axes and smaller size
fig_region = px.bar(region_counts, y='regionname', x='count', title='Visits by Region', 
                    labels={'regionname': 'Region', 'count': 'Visits'}, orientation='h',
                    width=500, height=400)

# Displaying the plots
st.plotly_chart(fig_referer)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_country)
with col2:
    st.plotly_chart(fig_region)






