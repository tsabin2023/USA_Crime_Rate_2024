# CNE 340 - Network Databases and Structured Query Language (SQL)
# Winter 2024
# Group project name: USA Crime Rate 2024
# Project members: Tyler Sabin, Van Vuong

# Import section
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt, cm
from sqlalchemy import create_engine

def three_lowest_state(table, engine):
    df = pd.read_sql_table(table, con=engine)
    lowest_crime_data = df.sort_values(by='CrimeRate').head(3)[['state', 'CrimeRate']]
    print(lowest_crime_data)
    states = lowest_crime_data['state'].tolist()
    crime_rates = lowest_crime_data['CrimeRate'].tolist()
    return states, crime_rates


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
    print(df)

# we need to pick a new table name.
table_name = 'test_table_name' # 'CrimeRate' is a column name in csv file so the table name must be different
df.to_sql(table_name, engine, if_exists='replace', index=False)

# todo Python code pulls data from database and analyzes analytics
# python code pulls data from database and analyzes analytics, is what we want it to do
query = f"SELECT * FROM {table_name} ORDER BY CrimeRate DESC" # pulling data from table in db
db_sorted = pd.read_sql(query, engine)

# sort out top 3 states from database

print(df.columns)
# might want to rename columns and then use new column names for plotting

top_3_states = db_sorted.head(3)  # first 3 highest states by row from db
num_states = len(top_3_states)
colors = cm.rainbow(np.linspace(0, 1, num_states))  # module method seems to work

# plot top 3 crime rate states
plt.figure(figsize=(10, 6))
for i, (state, crime_rate) in enumerate(zip(top_3_states['state'], top_3_states['CrimeViolentRate'])):
    plt.bar(state, crime_rate, color=colors[i])

plt.title('Top 3 States with Highest Crime Violence Rate per 100,000 population in 2024')
plt.xlabel('State or District of Columbia')
plt.ylabel('Crime Violent Rate per 100,000 population')
plt.xticks(rotation=45)  # angle seems good, but can be changed
plt.tight_layout()

# sort bottom 3, Van
low_3_states, low_3_CrimeRate = three_lowest_state(table_name, engine)
# plot graph 2, Van
plt.figure(figsize=(10, 6))

# Plot the bar chart
bar_colors = ['blue', 'orange', 'green']
bar_width=0.5
plt.bar(low_3_states, low_3_CrimeRate, width=bar_width, color=bar_colors)
# Add values on top of each bar
for i in range(len(low_3_states)):
    plt.text(low_3_states[i], low_3_CrimeRate[i], str(low_3_CrimeRate[i]), ha='center', va='bottom')

plt.title('3 States with Lowest Crime Violence Rate per 100,000 population in 2024')
plt.xlabel('State or District of Columbia')
plt.ylabel('Crime Violent Rate per 100,000 population')
plt.xticks(rotation=45)  # angle seems good, but can be changed
plt.tight_layout()

# Plot chart including all states' rate and the Average rate
# Plot all states' rate chart, Van

# Plot Average rate chart, Tyler
avg_crime_rate = db_sorted['CrimeViolentRate'].mean()

# create plot of all 50 states Crime Violence Rate per 100,000 Population in 2024 for All States
# then figure out how to add avg to that plot
all_states_dc_2 = db_sorted  # all states and dc
num_states2 = len(all_states_dc_2)
# trying two different color maps and alternate them
colormap1 = cm.tab20  # different python colormap than other attempts, seems to work
colormap2 = cm.tab20b  # another unique python color map, seems to work
# find a way to add tab20c so that no colors repeat in next version.

# plot crime rate of states and d.c.
plt.figure(figsize=(12, 6))
for i, (state, crime_rate) in enumerate(zip(all_states_dc_2['state'], all_states_dc_2['CrimeViolentRate'])):
    if i % 2 == 0:
        color = colormap1(i // 2 % colormap1.N)
    else:
        color = colormap2(i // 2 % colormap2.N)
    plt.bar(state, crime_rate, color=color)
# almost every state is a different color than the other, maybe leave as is

# gives dashed black bar or avg on 50 states plot
plt.axhline(avg_crime_rate, color='black', linestyle='--', linewidth=2)
plt.text(-0.5, avg_crime_rate, f'Average Rate: {avg_crime_rate:.2f}', color='black', fontsize=10, fontweight='bold')
plt.title('All State and D.C. Crime Violence Rate per 100,000 population in 2024')
plt.xlabel('50 States and D.C')
plt.ylabel('Crime Violent Rate per 100,000 population')
plt.xticks(rotation=90)  # 90 needed to read, 0 degrees might also work
plt.tight_layout()

# plot only once at the end to show all plots
plt.show()
# manually hit x in figures upper right corner to close and each figure and complete code

# close connection made by engine
engine.dispose()
print(f"DataFrame successfully sent to the '{table_name}' table in the '{dbname}' database.")