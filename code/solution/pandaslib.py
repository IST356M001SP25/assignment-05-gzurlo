# pandaslib.py
import pandas as pd

def extract_year_mdy(timestamp_str):
    """Extract year from MM/DD/YYYY timestamp string"""
    if pd.isna(timestamp_str):
        return None
    parts = timestamp_str.split('/')
    if len(parts) >= 3:
        return int(parts[2])
    return None

def clean_country_usa(country_str):
    """Standardize US country names to 'United States'"""
    if pd.isna(country_str):
        return country_str
    country = str(country_str).strip().lower()
    usa_aliases = ['us', 'usa', 'united states', 'united states of america']
    if country in usa_aliases:
        return 'United States'
    return country_str

def clean_currency(currency_str):
    """Clean currency strings into float values"""
    if pd.isna(currency_str):
        return None
    if isinstance(currency_str, (int, float)):
        return float(currency_str)
    # Remove $, commas, and any non-numeric characters except .
    cleaned = ''.join(c for c in str(currency_str) 
                     if c.isdigit() or c == '.')
    try:
        return float(cleaned)
    except ValueError:
        return None