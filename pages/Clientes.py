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


# Get clients info
engine = create_engine(connection)
with engine.connect() as conn:
    clients_info = conn.execute(text(f'SELECT * FROM {SCHEMA_PTERODACTYL}.clients_info'))
    clients_info = pd.DataFrame(clients_info)

# Get clients historical info
engine = create_engine(connection)
with engine.connect() as conn:
    clients_hist = conn.execute(text(f'SELECT * FROM {SCHEMA_PTERODACTYL}.clients_historical_info'))
    clients_hist = pd.DataFrame(clients_hist)

# Get clients last connection info
engine = create_engine(connection)
with engine.connect() as conn:
    clients_last_conn = conn.execute(text(f'SELECT * FROM {SCHEMA_PTERODACTYL}.clients_last_connection'))
    clients_last_conn = pd.DataFrame(clients_last_conn)


'''STILL NEEDS TO ADJUST THE LAST TWO TABLES'''
# Create and display clients information table
st.subheader('Clients Information')
st.dataframe(clients_info, hide_index=True)

# Create and display historical server information table
st.subheader('Historical Server Information')
st.dataframe(clients_hist, hide_index=True)

# Create and display clients last connection table
st.subheader("Client's Last Connection")
st.dataframe(clients_last_conn, hide_index=True)