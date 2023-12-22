
import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime
import time, os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from geopy.geocoders import Nominatim

import credentials
connection = credentials.connection
SCHEMA_MINECRAFT = credentials.SCHEMA_MINECRAFT


# Set page to wide mode
st.set_page_config(layout="wide")


# Get activity_analisis info
engine = create_engine(connection)
with engine.connect() as conn:
    activity_analysis = conn.execute(text(f'SELECT * FROM {SCHEMA_MINECRAFT}.activity_analysis'))
    activity_analysis = pd.DataFrame(activity_analysis)

# Get activity info
with engine.connect() as conn:
    activity = conn.execute(text(f'SELECT * FROM {SCHEMA_MINECRAFT}.activity'))
    activity = pd.DataFrame(activity)

# Create the title'''
st.title('STIV PROJECT')