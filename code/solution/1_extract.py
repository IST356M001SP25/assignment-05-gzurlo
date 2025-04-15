import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl

#TODO Write your extraction code here

# extract.py
import pandas as pd
import os
from pandaslib import extract_year_mdy

# Create cache directory if it doesn't exist
os.makedirs('cache', exist_ok=True)

# 1. Extract states data
states_url = "https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv"
states_df = pd.read_csv(states_url)
states_df.to_csv('cache/states.csv', index=False)

# 2. Extract survey data
survey_url = "https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?format=csv"
survey_df = pd.read_csv(survey_url)

# Add year column
survey_df['year'] = survey_df['Timestamp'].apply(extract_year_mdy)
survey_df.to_csv('cache/survey.csv', index=False)

# 3. Extract cost of living data for each year
# This part would need more implementation based on where the COL data comes from
# You would need to find a source for historical cost of living data