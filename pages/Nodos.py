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

#Set page to wide mode
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

# Get nodes utilization
with engine.connect() as conn:
    consumption = conn.execute(text(f'SELECT * FROM {SCHEMA_PTERODACTYL}.nodes_utilization'))
    consumption = pd.DataFrame(consumption)

# Get nodes uptime and ping
with engine.connect() as conn:
    uptime = conn.execute(text(f'SELECT name AS "Node", avg_ping AS "Average Ping", uptime_24hours AS "SLA" FROM {SCHEMA_KUMA}.nodes JOIN {SCHEMA_PTERODACTYL}.nodes  ON node_id = pterodactyl.nodes.id'))
    uptime = pd.DataFrame(uptime)   

# Get nodes address
with engine.connect() as conn:
    locations = conn.execute(text(f'SELECT * FROM {SCHEMA_PTERODACTYL}.nodes_address'))
    locations = pd.DataFrame(locations)

# Get servers uptime and ping
with engine.connect() as conn:
    servers = conn.execute(text(f'SELECT * FROM {SCHEMA_PTERODACTYL}.servers_uptime_ping'))
    servers = pd.DataFrame(servers)


# CREATING THE PLOTS

# FIRST ROW OF PLOTS
# Create three columns
col1, col2, col3 = st.columns(3)

# Create and display average ping and SLA table
col1.subheader('Nodes Average Ping and SLA')
col1.dataframe(uptime, hide_index=True)

# Create and display nodes utilization table
col2.subheader('Nodes Utilization')
col2.dataframe(consumption.set_index('Node').transpose())

# Create and display bar plot to show SLA per node 
fig_bar = px.bar(uptime, x='Node', y='SLA', height=450, width=400)
col3.subheader('Nodes Uptime')
col3.plotly_chart(fig_bar)




# SECOND ROW OF PLOTS
# Create pie plots for each node
# Get unique nodes
nodes = consumption['Node'].unique()

# Create subplot with 'pie' type
fig = make_subplots(rows=1, cols=len(nodes), subplot_titles=nodes, specs=[[{'type': 'pie'}] * len(nodes)])

# Loop through each node and add a pie chart to the subplot
for i, node in enumerate(nodes, start=1):
    # Filter the DataFrame for the current node
    consumption_node = consumption[consumption['Node'] == node]

    # Melt the DataFrame to reshape it for Plotly Express
    consumption_melted = pd.melt(consumption_node, id_vars=['Node'], var_name='Metrics', value_name='Values')

    # Create a pie chart trace
    trace = go.Pie(labels=consumption_melted['Metrics'], values=consumption_melted['Values'], name=node)

    # Add the trace to the subplot
    fig.add_trace(trace, row=1, col=i)

# Create bar plot to show SLA per server
fig_bar2 = px.bar(servers, x='Node', y='SLA' ,height=450, width=400)

# Create three columns
col1, col2, col3 = st.columns(3)

# Display the pie plots in the first column
col1.subheader('Nodes Utilization')
col1.plotly_chart(fig)

# Display the barplot in the second column
col3.subheader('Server Uptime')
col3.plotly_chart(fig_bar2)




# THIRD ROW OF PLOTS
# Geocode addresses and create 'Latitude' and 'Longitude' columns
geolocator = Nominatim(user_agent="my_app")
locations['location'] = locations['Address'].apply(geolocator.geocode)
locations['Latitude'] = locations['location'].apply(lambda loc: loc.latitude if loc else None)
locations['Longitude'] = locations['location'].apply(lambda loc: loc.longitude if loc else None)

# Rename columns to match the expected names
locations = locations.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})

# Display the map 
st.map(locations)