from dotenv import load_dotenv
import os
import streamlit as st

# Load .env file credentials
env_file = load_dotenv()
if env_file:

    # Database connection
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    database = os.getenv('POSTGRES_DATABASE')
    username = os.getenv('POSTGRES_USERNAME')
    password = os.getenv('POSTGRES_PASSWORD')
    connection = f'postgresql://{username}:{password}@{host}:{port}/{database}'

    # Schemas from PostgreSQL
    SCHEMA_PTERODACTYL = 'pterodactyl'
    SCHEMA_MINECRAFT = 'minecraft'
    SCHEMA_KUMA = 'kuma'
    SCHEMA_SHLINK = 'shlink'

else:
    # Database connection
    host = st.secrets['POSTGRES_HOST']
    port = st.secrets['POSTGRES_PORT']
    database = st.secrets['POSTGRES_DATABASE']
    username = st.secrets['POSTGRES_USERNAME']
    password = st.secrets['POSTGRES_PASSWORD']
    connection = f'postgresql://{username}:{password}@{host}:{port}/{database}'

    # Schemas from PostgreSQL
    SCHEMA_PTERODACTYL = 'pterodactyl'
    SCHEMA_MINECRAFT = 'minecraft'
    SCHEMA_KUMA = 'kuma'
