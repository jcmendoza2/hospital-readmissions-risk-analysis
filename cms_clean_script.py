import pandas as pd 
import sqlite3

df = pd.read_excel('CMS data.xlsx')

# Need to clean the number of hospital readmissions 
# problem areas:
# "Too Few to Report" -> convert to NaN
df['Number of Readmissions'] = pd.to_numeric(df['Number of Readmissions'], errors='coerce')

# Need to add a flag column for the (too few cases) type of data 
df['is_suppressed'] = df['Excess Readmission Ratio'].isna()

# Need to map the coded measure names to human readable labels
condition_map = { 
    'READM-30-AMI-HRRP':        'Heart Attack',
    'READM-30-HF-HRRP':         'Heart Failure',
    'READM-30-PN-HRRP':         'Pneumonia',
    'READM-30-COPD-HRRP':       'COPD',
    'READM-30-HIP-KNEE-HRRP':   'Hip/Knee Replacement',
    'READM-30-CABG-HRRP':       'Bypass Surgery'
}
df['Condition'] = df['Measure Name'].map(condition_map)

# Need to rename columns to have no spaces and be easily translated to sql 
df.columns = ['facility_name', 'facility_id', 'state', 'measure_code', 
              'num_discharges', 'footnote', 'excess_readmission_ratio', 
              'predicted_rate', 'expected_rate', 'num_readmissions', 'start_date',
              'end_date', 'is_suppressed', 'condition']

# Now need to load into SQLite 
conn = sqlite3.connect('cms_readmissions.db')
df.to_sql('readmissions', conn, if_exists='replace', index=False)
df.to_csv('cms_cleaned.csv', index=False)
print("Done. Rows loaded: ", len(df))