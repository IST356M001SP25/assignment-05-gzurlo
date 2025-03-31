import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here
import pandas as pd
import streamlit as st
from pandaslib import clean_country_usa, clean_currency
import os

def load_cached_data():
    """Load all cached datasets"""
    # Load states data
    states = pd.read_csv('cache/states.csv')
    
    # Load survey data
    survey = pd.read_csv('cache/survey.csv')
    
    # Load COL data for all years
    col_data = []
    for file in os.listdir('cache'):
        if file.startswith('col_') and file.endswith('.csv'):
            year = file.split('_')[1].split('.')[0]
            df = pd.read_csv(f'cache/{file}')
            col_data.append(df)
    col = pd.concat(col_data) if col_data else pd.DataFrame()
    
    return states, survey, col

def transform_data(states, survey, col):
    """Perform all data transformations"""
    st.write("## Data Transformation Pipeline")
    
    with st.status("Processing data...", expanded=True) as status:
        # Step 1: Clean country data
        st.write("Cleaning country data...")
        survey['_country'] = survey['Which country do you work in?'].apply(clean_country_usa)
        
        # Step 2: Merge with state codes
        st.write("Merging state codes...")
        survey_states = pd.merge(
            survey,
            states,
            left_on='If you\'re in the U.S., what state do you work in?',
            right_on='State',
            how='inner'
        )
        
        # Step 3: Create full city string
        st.write("Creating location identifiers...")
        survey_states['_full_city'] = (
            survey_states['What city do you work in?'] + ', ' + 
            survey_states['Code'] + ', ' + 
            survey_states['_country']
        )
        
        # Step 4: Merge with COL data
        st.write("Merging with cost of living data...")
        combined = pd.merge(
            survey_states,
            col,
            left_on=['year', '_full_city'],
            right_on=['year', 'city'],
            how='left'
        )
        
        # Step 5: Clean and adjust salary
        st.write("Adjusting salaries for cost of living...")
        combined['__annual_salary_cleaned'] = combined['What is your annual salary?'].apply(clean_currency)
        combined['_annual_salary_adjusted'] = combined['__annual_salary_cleaned'] * (100 / combined['col_index'])
        
        status.update(label="Transformation complete!", state="complete")
    
    return combined

def generate_reports(combined):
    """Generate the required reports"""
    st.write("## Report Generation")
    
    with st.status("Creating reports...", expanded=True) as status:
        # Save engineered dataset
        st.write("Saving full dataset...")
        combined.to_csv('cache/survey_dataset.csv', index=False)
        
        # Report 1: By location and age
        st.write("Creating location vs age report...")
        age_report = pd.pivot_table(
            combined,
            values='_annual_salary_adjusted',
            index='_full_city',
            columns='How old are you?',
            aggfunc='mean'
        )
        age_report.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')
        
        # Report 2: By location and education
        st.write("Creating location vs education report...")
        edu_report = pd.pivot_table(
            combined,
            values='_annual_salary_adjusted',
            index='_full_city',
            columns='What is your highest level of education completed?',
            aggfunc='mean'
        )
        edu_report.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')
        
        status.update(label="Reports generated!", state="complete")
    
    return age_report, edu_report

def main():
    st.title("Data Transformation Pipeline")
    
    # Load cached data
    states, survey, col = load_cached_data()
    
    # Transform data
    combined = transform_data(states, survey, col)
    
    # Generate reports
    age_report, edu_report = generate_reports(combined)
    
    # Show sample results
    st.success("Transformation completed successfully!")
    st.write("### Sample Adjusted Salary Data", combined[['_full_city', '_annual_salary_adjusted']].head())
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Age Report Preview", age_report.head())
    with col2:
        st.write("### Education Report Preview", edu_report.head())

if __name__ == "__main__":
    main()
