import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here

# transform.py
import pandas as pd
import os
from pandaslib import clean_country_usa, clean_currency

# 1. Load cached data
states_df = pd.read_csv('cache/states.csv')
survey_df = pd.read_csv('cache/survey.csv')

# 2. Clean and merge data
survey_df['_country'] = survey_df['Which country do you work in?'].apply(clean_country_usa)
survey_states_combined = pd.merge(
    survey_df,
    states_df,
    left_on="If you're in the U.S., what state do you work in?",
    right_on="State",
    how='inner'
)

# Create full city column
survey_states_combined['_full_city'] = (
    survey_states_combined['What city do you work in?'] + ', ' +
    survey_states_combined['Code'] + ', ' +
    survey_states_combined['_country']
)

# 3. Load and combine COL data
# This would need implementation based on COL data source
# col_data = ...

# 4. Merge with COL data
combined = pd.merge(
    survey_states_combined,
    col_data,
    left_on=['year', '_full_city'],
    right_on=['year', 'city'],
    how='left'
)

# 5. Calculate adjusted salary
combined['__annual_salary_cleaned'] = combined['What is your annual salary?'].apply(clean_currency)
combined['_annual_salary_adjusted'] = combined['__annual_salary_cleaned'] * (100 / combined['col_index'])

# 6. Create reports
# Save engineered dataset
combined.to_csv('cache/survey_dataset.csv', index=False)

# Create pivot tables
report_age = combined.pivot_table(
    values='_annual_salary_adjusted',
    index='_full_city',
    columns='How old are you?',
    aggfunc='mean'
)
report_age.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')

report_edu = combined.pivot_table(
    values='_annual_salary_adjusted',
    index='_full_city',
    columns='What is your highest level of education completed?',
    aggfunc='mean'
)
report_edu.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')