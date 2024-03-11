# CNE 340 - Network Databases and Structured Query Language (SQL)
# Winter 2024
# Group project name: USA Crime Rate 2024
# Project members: Tyler Sabin, Van Vuong

# Import section
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt, cm
from sqlalchemy import create_engine

def sort_all_states(table, engine):
    df = pd.read_sql_table(table, con=engine)
    all_states = df.sort_values(by='state')
    all_states_CrimeViolentRate = all_states['state'].tolist()
    crime_violent_rate = all_states['CrimeViolentRate'].tolist()
    return all_states_CrimeViolentRate, crime_violent_rate

# def to sort out the 3 lowest states based on the criteria of Crime Violent Rates
def three_lowest_state(table, engine):
     df = pd.read_sql_table(table, con=engine)
     lowest_crime_violent_rate_data = df.sort_values(by='CrimeViolentRate').head(3)[['state', 'CrimeViolentRate']]
     states = lowest_crime_violent_rate_data['state'].tolist()
     crime_rates = lowest_crime_violent_rate_data['CrimeViolentRate'].tolist()
     return states, crime_rates

#Install cryptography
# SQL connection and Database
hostname = 'localhost'
uname = 'root'
pwd = ''
dbname = 'USA_Crime_Rate_2024'

# connect to MySQL on LAMP Server
connection_string = f"mysql+pymysql://{uname}:{pwd}@{hostname}/{dbname}"
engine = create_engine(connection_string)

# todo Python code pulls data from a data source and puts data into Database
with open('crime-rate-by-state-2024.csv') as file_path:
    df = pd.read_csv(file_path)
 #   print(df)

# we need to pick a new table name.
table_name = 'test_table_name' # 'CrimeRate' is a column name in csv file so the table name must be different
df.to_sql(table_name, engine, if_exists='replace', index=False)

# todo Python code pulls data from database and analyzes analytics
# python code pulls data from database and analyzes analytics, is what we want it to do
query = f"SELECT * FROM {table_name} ORDER BY CrimeRate DESC" # pulling data from table in db
db_sorted = pd.read_sql(query, engine)

# sort bottom 3, Van
low_3_states, low_3_crime_violent_rate = three_lowest_state(table_name, engine)
print(low_3_states, low_3_crime_violent_rate)

# plot graph 2, Van
# defined figure size
plt.figure(figsize=(6, 6))

# # Plot the bar chart
bar_colors = ['blue', 'orange', 'green']
bar_width=0.25
plt.bar(low_3_states, low_3_crime_violent_rate, width=bar_width, color=bar_colors)
# Add values on top of each bar
for i in range(len(low_3_states)):
     plt.text(low_3_states[i], low_3_crime_violent_rate[i], str(low_3_crime_violent_rate[i]), ha='center', va='bottom', fontweight='bold')
# Making chart title, X and Y labels:
plt.title('3 States with Lowest Crime Violence Rate \nper 100,000 population in 2024',fontweight='bold')
plt.xlabel('\nState or District of Columbia', fontweight='bold')
plt.ylabel('Crime Violent Rate per 100,000 population', fontweight='bold')
plt.tight_layout()


# Plot chart including all states' rate and the Average rate

# Plot Average rate chart, Tyler
avg_crime_rate = db_sorted['CrimeViolentRate'].mean()


# Plot all states' rate chart, Van
#all_state = db_sorted['state']
#all_state_Crime_Violent_Rate = db_sorted['CrimeViolentRate']
all_state, all_state_Crime_Violent_Rate = sort_all_states(table_name, engine)

plt.figure(figsize=(12, 6))
all_states_bar_colors = np.random.rand(len(all_state), 3)
plt.bar(all_state, all_state_Crime_Violent_Rate, color=all_states_bar_colors)
plt.axhline(avg_crime_rate, color='red', linestyle='--', linewidth=2)
plt.text(+44, avg_crime_rate, f'Average Rate: {avg_crime_rate:.2f}', color='red', fontsize=10, fontweight='bold')

#Add title and label
plt.title('All State and D.C. Crime Violence Rate per 100,000 population in 2024', fontweight='bold')
plt.xlabel('All 50 States or District of Columbia', fontweight='bold')
plt.ylabel('Crime Violent Rate per 100,000 population', fontweight='bold')
plt.xticks(rotation=90)  # 90 needed to read, 0 degrees might also work
plt.tight_layout()

# plot only once at the end to show all plots
plt.show()
# manually hit x in figures upper right corner to close and each figure and complete code



# close connection made by engine
engine.dispose()
print(f"DataFrame successfully sent to the '{table_name}' table in the '{dbname}' database.")