# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from pydactyl import PterodactylClient
from dotenv import load_dotenv
from datetime import datetime
import time, os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from geopy.geocoders import Nominatim

# Set page to wide mode
st.set_page_config(layout="wide")

import credentials
connection = credentials.connection
SCHEMA_MINECRAFT = credentials.SCHEMA_MINECRAFT
SCHEMA_PTERODACTYL = credentials.SCHEMA_PTERODACTYL
SCHEMA_KUMA = credentials.SCHEMA_KUMA


# Get activity_analisis info
engine = create_engine(connection)
with engine.connect() as conn:
    activity_analysis = conn.execute(text(f'SELECT * FROM {SCHEMA_MINECRAFT}.activity_analysis'))
    activity_analysis = pd.DataFrame(activity_analysis)

# Get activity info
with engine.connect() as conn:
    activity = conn.execute(text(f'SELECT * FROM {SCHEMA_MINECRAFT}.activity'))
    activity = pd.DataFrame(activity)

# Get activity info
with engine.connect() as conn:
    utilization = conn.execute(text(f'SELECT * FROM {SCHEMA_PTERODACTYL}.utilization'))
    utilization = pd.DataFrame(utilization)



'''THIS FILE IS ONLY FOR TEST SOME PLOTS IN ORDER TO DON'T MAKE A MESS IN THE FINAL PAGES'''


# Assuming 'utilization' is your DataFrame for server utilization metrics
# Assuming 'activity' is your DataFrame for activity data

# Add a title or subheader for the three columns
st.subheader("Servers Utilization Metrics")

# Create a dropdown for selecting the server
selected_server = st.selectbox("Select Server", utilization['server_identifier'].unique())

# Filter the data based on the selected server for utilization metrics
filtered_utilization_data = utilization[utilization['server_identifier'] == selected_server]

# Create the three columns for utilization metrics
col1, col2, col3 = st.columns(3)

# Define the number of decimals you want
decimals = 2  # Change this to 1 if you want one decimal place

# Add metrics to each column and round the values
col1.metric("Ram", round(filtered_utilization_data['ram_mean'].mean(), decimals), round(filtered_utilization_data['ram_std'].mean(), decimals))
col2.metric("CPU", round(filtered_utilization_data['cpu_mean'].mean(), decimals), round(filtered_utilization_data['cpu_std'].mean(), decimals))
col3.metric("Disk", round(filtered_utilization_data['disk_mean'].mean(), decimals), round(filtered_utilization_data['disk_std'].mean(), decimals))

# Assuming 'activity' is your DataFrame
# Assuming 'date' is in string format, convert it to datetime
activity['date'] = pd.to_datetime(activity['date'])

# Extract the hour and create a new column
activity['hour'] = activity['time'].apply(lambda x: x.hour)

# Extract the day of the week and create a new column
activity['day_of_week'] = activity['date'].dt.day_name()

# Define the order of days of the week
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Convert 'day_of_week' to a category with the specified order
activity['day_of_week'] = pd.Categorical(activity['day_of_week'], categories=days_order, ordered=True)

# Group by hour and calculate the count for activity data
activity_counts_per_hour = activity.groupby('hour').size().reset_index(name='count')

fig_bar_time = px.bar(activity_counts_per_hour, x='hour', y='count', height=400, width=500)
fig_bar_time.update_xaxes(tickmode='array', tickvals=list(range(24)))

# Group by day of the week and calculate the count for activity data
activity_counts_per_day = activity.groupby('day_of_week').size().reset_index(name='count')

fig_bar_day = px.bar(activity_counts_per_day, x='day_of_week', y='count', height=400, width=500)

# Create a selectbox to filter servers for activity data
selected_server_activity = st.selectbox('Select a Server for Activity', activity['server_identifier'].unique())

# Filter the DataFrame based on the selected server for activity data
filtered_data_activity = activity[activity['server_identifier'] == selected_server_activity]

col1, col2 = st.columns(2)
col1.subheader(f'Activity Per Hour of the Day - {selected_server_activity}')
col1.plotly_chart(fig_bar_time)

col2.subheader(f'Activity Per Day of the Week - {selected_server_activity}')
col2.plotly_chart(fig_bar_day)





import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample DataFrame
df = pd.DataFrame({
    'A': np.random.randn(100),
    'B': np.random.randn(100)
})

# Title
st.title('Customizable Streamlit Dashboard')

# First Row: DataFrame
st.header('DataFrame Section')

# Display DataFrame
st.dataframe(df)

# Second Row: Scatter Plot
st.header('Scatter Plot Section')

# Display Scatter Plot
fig, ax = plt.subplots()
ax.scatter(df['A'], df['B'])
st.pyplot(fig)

# Third Row: Custom Layout
st.header('Custom Layout Section')

# Two Columns
col1, col2 = st.columns(2)

# Column 1: Bar Chart
with col1:
    st.subheader('Bar Chart')
    bar_data = pd.DataFrame({
        'Category': ['A', 'B', 'C'],
        'Value': [3, 7, 2]
    })
    st.bar_chart(bar_data.set_index('Category'))

# Column 2: Line Chart
with col2:
    st.subheader('Line Chart')
    line_data = pd.DataFrame({
        'X': np.arange(10),
        'Y': np.random.randn(10)
    })
    st.line_chart(line_data.set_index('X'))

# Fourth Row: Map and Text
st.header('Map and Text Section')

# Full-width Map
st.map()

# Text Area
st.text_area('Enter Text:', '')

# Fifth Row: Sidebar with Controls
st.sidebar.header('Sidebar Controls')
show_data = st.sidebar.checkbox('Show DataFrame')
show_plot = st.sidebar.checkbox('Show Scatter Plot')

# Display DataFrame based on checkbox
if show_data:
    st.subheader('Custom DataFrame')
    st.dataframe(df)

# Display Scatter Plot based on checkbox
if show_plot:
    st.subheader('Custom Scatter Plot')
    fig, ax = plt.subplots()
    ax.scatter(df['A'], df['B'])
    st.pyplot(fig)