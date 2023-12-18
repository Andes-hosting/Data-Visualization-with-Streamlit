
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

# Load .env file credentials
load_dotenv()

# Database connection
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
database = os.getenv('POSTGRES_DATABASE')
username = os.getenv('POSTGRES_USERNAME')
password = os.getenv('POSTGRES_PASSWORD')
connection = f'postgresql://{username}:{password}@{host}:{port}/{database}'

# Pterodactyl connection
pterodactyl_url = os.getenv('PTERODACTYL_URL')
application_api_key = os.getenv('PTERODACTYL_APP_KEY')
client_api_key = os.getenv('PTERODACTYL_CLI_KEY')

# Connecto to Pterodactyl Application API
api_app = PterodactylClient(pterodactyl_url, application_api_key, debug=False)
# Connecto to Pterodactyl Client API
api_cli = PterodactylClient(pterodactyl_url, client_api_key, debug=False)

# Schemas from PostgreSQL
SCHEMA_PTERODACTYL = 'pterodactyl'
SCHEMA_MINECRAFT = 'minecraft'

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