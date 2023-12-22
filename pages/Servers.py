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

# Get utilization info
with engine.connect() as conn:
    utilization = conn.execute(text(f'SELECT * FROM {SCHEMA_PTERODACTYL}.utilization'))
    utilization = pd.DataFrame(utilization)




'''WE ARE STILL TRYING TO MAKE A VISUALIZATION OF THIS, FOR NOW IS ONLY A EARLY PLOT'''
# st.dataframe(utilization)
# st.dataframe(activity_analysis)

# # Group by 'identifier' and calculate the mean for each metric
# grouped_df = utilization.groupby('server_identifier').mean().reset_index().drop('status', axis=1)
# st.dataframe(grouped_df)
# # Reshape the DataFrame for box plot
# df_long = pd.melt(grouped_df, id_vars='server_identifier', var_name='Metric', value_name='Mean')

# # Plot a box plot using Plotly Express
# fig = px.box(df_long, x='Metric', y='Mean', title='Box Plot of Metrics Mean Grouped by Servers')

# # Show the plot using Streamlit
# st.plotly_chart(fig)




# FIRST ROW OF PLOTS
# Create two columns
col1, col2 = st.columns(2)

# Create and display the horizontal barplot for total users per server
users_per_server = px.bar(activity_analysis, x='total_users', y='name', height=300, width=500)
col1.subheader('Total Users Per Server')
col1.plotly_chart(users_per_server)

# Create and display the horizontal barplot for total activity per server
activity_per_server = px.bar(activity_analysis, x='total_activity', y='name', height=300, width=500)
col2.subheader('Total Activity Per Server')
col2.plotly_chart(activity_per_server)




# SECOND ROW OF PLOTS
# Extract the hour and create a new column
activity['hour'] = activity['time'].apply(lambda x: x.hour)

# Group by hour and calculate the count
activity_counts_per_hour = activity.groupby('hour').size().reset_index(name='count')

fig_bar_time = px.bar(activity_counts_per_hour, x='hour', y='count', height=400, width=500)

# Set x-axis tick values for every hour from 00 to 23
fig_bar_time.update_xaxes(tickmode='array', tickvals=list(range(24)))

# Convert 'data' to datetime
activity['date'] = pd.to_datetime(activity['date'])

# Extract the day of the week and create a new column
activity['day_of_week'] = activity['date'].dt.day_name()

# Define the order of days of the week
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Convert 'day_of_week' to a category with the specified order
activity['day_of_week'] = pd.Categorical(activity['day_of_week'], categories=days_order, ordered=True)

# Group by day of the week and calculate the count
activity_counts_per_day = activity.groupby('day_of_week').size().reset_index(name='count')

fig_bar_day = px.bar(activity_counts_per_day, x='day_of_week', y='count', height=400, width=500)


# Create two columns
col1, col2 = st.columns(2)

# Create and display total activity per hour of the day
col1.subheader('Activity Per Hour of the Day')
col1.plotly_chart(fig_bar_time)

# Create and display total activity per day of the week
col2.subheader('Activity Per Day of the Week')
col2.plotly_chart(fig_bar_day)




# THIRD ROW OF PLOTS
# Add a subheader for the metrics
st.subheader("Servers Utilization Metrics")

# Create a dropdown for selecting the server
selected_server = st.selectbox("Select Server", utilization['server_identifier'].unique())

# Filter the data based on the selected server
filtered_data = utilization[utilization['server_identifier'] == selected_server]

# Define the number of decimals you want
decimals = 2  # Change this to 1 if you want one decimal place

# Create three columns
col1, col2, col3 = st.columns(3)

# Create and display the ram metrics
col1.metric("Ram", round(filtered_data['ram_mean'].mean(), decimals), round(filtered_data['ram_std'].mean(), decimals))

# Create and display the cpu metrics
col2.metric("CPU", round(filtered_data['cpu_mean'].mean(), decimals), round(filtered_data['cpu_std'].mean(), decimals))

# Create and display the disk metrics
col3.metric("Disk", round(filtered_data['disk_mean'].mean(), decimals), round(filtered_data['disk_std'].mean(), decimals))




# FOURTH ROW OF PLOT
# Convert 'data' to datetime
activity['date'] = pd.to_datetime(activity['date'])

# Extract the hour and create a new column
activity['hour'] = activity['time'].apply(lambda x: x.hour)

# Extract the day of the week and create a new column
activity['day_of_week'] = activity['date'].dt.day_name()

# Define the order of days of the week
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Convert 'day_of_week' to a category with the specified order
activity['day_of_week'] = pd.Categorical(activity['day_of_week'], categories=days_order, ordered=True)

# Create a selectbox to filter servers
selected_server = st.selectbox('Select a Server', activity['server_identifier'].unique())

# Filter the DataFrame based on the selected server
filtered_data = activity[activity['server_identifier'] == selected_server]

# Group by hour and calculate the count
activity_counts_per_hour = filtered_data.groupby('hour').size().reset_index(name='count')

fig_bar_time = px.bar(activity_counts_per_hour, x='hour', y='count', height=400, width=500)
fig_bar_time.update_xaxes(tickmode='array', tickvals=list(range(24)))

# Group by day of the week and calculate the count
activity_counts_per_day = filtered_data.groupby('day_of_week').size().reset_index(name='count')

fig_bar_day = px.bar(activity_counts_per_day, x='day_of_week', y='count', height=400, width=500)

# Create two columns
col1, col2 = st.columns(2)

# Create and display activity per hour of the day, using a dropdown button to filter between the server identifier (change in the future for server name)
col1.subheader(f'Activity Per Hour of the Day - {selected_server}')
col1.plotly_chart(fig_bar_time)

# Create and display activity per day of the week, using a dropdown button to filter between the server identifier (change in the future for server name)
col2.subheader(f'Activity Per Day of the Week - {selected_server}')
col2.plotly_chart(fig_bar_day)