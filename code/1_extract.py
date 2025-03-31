import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
  
#TODO Write your extraction code here
import pandas as pd
import os
from pandaslib import extract_year_mdy

def ensure_cache_dir():
    """Ensure cache directory exists"""
    os.makedirs('cache', exist_ok=True)

def extract_states():
    """Extract state abbreviations data"""
    url = "https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv"
    df = pd.read_csv(url)
    df.to_csv('cache/states.csv', index=False)
    return df

def extract_survey():
    """Extract and process survey data"""
    url = "https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?format=csv"
    df = pd.read_csv(url)
    
    # Add year column using helper function
    df['year'] = df['Timestamp'].apply(extract_year_mdy)
    
    df.to_csv('cache/survey.csv', index=False)
    return df

def extract_col(year):
    """Extract cost of living data for a specific year"""
    # This is a placeholder - you'll need to implement actual COL data extraction
    # For now, we'll create mock data
    data = {
        'city': ['New York, NY, United States', 'Los Angeles, CA, United States'],
        'col_index': [168.7, 146.3],
        'year': [year, year]
    }
    df = pd.DataFrame(data)
    df.to_csv(f'cache/col_{year}.csv', index=False)
    return df

def main():
    st.title("Data Extraction Pipeline")
    
    ensure_cache_dir()
    
    with st.status("Extracting data...", expanded=True) as status:
        st.write("Extracting states data...")
        states_df = extract_states()
        st.write(f"Extracted {len(states_df)} states")
        
        st.write("Extracting survey data...")
        survey_df = extract_survey()
        st.write(f"Extracted {len(survey_df)} survey responses")
        
        # Get unique years from survey
        years = survey_df['year'].unique()
        
        st.write("Extracting cost of living data...")
        for year in years:
            col_df = extract_col(year)
            st.write(f"Extracted COL data for {year}: {len(col_df)} cities")
        
        status.update(label="Extraction complete!", state="complete")
    
    st.success("Data extraction completed successfully!")

if __name__ == "__main__":
    main()
