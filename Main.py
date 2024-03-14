# CNE340 Winter Quarter
# 3/13/2024
# follow instructions below to complete program
# https://rtc.instructure.com/courses/2439016/assignments/31830681?module_item_id=79735823
# https://rtc.instructure.com/courses/2439016/files/236685445?module_item_id=79735228
# further instructions from instructor
# source Tyler Sabin
# source Van Luong Vuong
# source Ix Procopios


# Import section
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
import matplotlib.cm as cm

#Install cryptography
# SQL connection and Database
hostname = 'localhost'
uname = 'root'
pwd = ''
dbname = 'USA_Crime_Rate_2024'

# connect to MySQL on W/LAMP Server
connection_string = f"mysql+pymysql://{uname}:{pwd}@{hostname}/{dbname}"
engine = create_engine(connection_string)

# opens csv file from GitHub Project Folder
with open('crime-rate-by-state-2024.csv') as file_path:
    df = pd.read_csv(file_path)

# table name
table_name = '50_states_and_dc_crime_statistics'  # 'CrimeRate', a column name in csv file, not table name applicable
df.to_sql(table_name, engine, if_exists='replace', index=False)

# query from table from our database
query = f"SELECT * FROM {table_name} ORDER BY CrimeRate DESC"  # pulling data from table in db
db_sorted = pd.read_sql(query, engine)

# sort out top 3 states from database
top_3_states = db_sorted.nlargest(3, 'CrimeViolentRate')  # first 3 highest states by row from db filtered
num_states = len(top_3_states)
colors = cm.rainbow(np.linspace(0, 1, num_states))  # module method seems to work

# plotting figure and using enumerate to add a counter i and zip to make two column tuple
plt.figure(figsize=(6, 6))
bar_width = 0.25
for i, (state, crime_rate) in enumerate(zip(top_3_states['state'], top_3_states['CrimeViolentRate'])):
    plt.bar(state, crime_rate, color=colors[i], edgecolor='black', width=bar_width)
    plt.text(state, crime_rate, str(round(crime_rate, 2)), ha='center', va='bottom', fontweight='bold')  # adding text to the top of bar

plt.title('Top 3 states or districts Crime Violence Rate \nper 100,000 population in 2024', fontweight='bold')
plt.xlabel('50 States and D.C', fontweight='bold')
plt.ylabel('Crime Violent Rate per 100,000 population', fontweight='bold')


# calculate average rate
avg_crime_rate = db_sorted['CrimeViolentRate'].mean()

# def sorting all states
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


# graph 2
low_3_states, low_3_crime_violent_rate = three_lowest_state(table_name, engine)

# defined figure size
plt.figure(figsize=(6, 6))

# # Plot the bar chart
bar_colors = ['blue', 'orange', 'green']
bar_width = 0.25
plt.bar(low_3_states, low_3_crime_violent_rate, width=bar_width, color=bar_colors, edgecolor='black')
# Add values on top of each bar
for i in range(len(low_3_states)):
    plt.text(low_3_states[i], low_3_crime_violent_rate[i], str(low_3_crime_violent_rate[i]), ha='center', va='bottom', fontweight='bold')
# Making chart title, X and Y labels:
plt.title('3 States with Lowest Crime Violence Rate \nper 100,000 population in 2024',fontweight='bold')
plt.xlabel('\nState or District of Columbia', fontweight='bold')
plt.ylabel('Crime Violent Rate per 100,000 population', fontweight='bold')
plt.tight_layout()


# Plot chart including all states' rate and the Average rate
all_state, all_state_Crime_Violent_Rate = sort_all_states(table_name, engine)

plt.figure(figsize=(12, 6))
all_states_bar_colors = np.random.rand(len(all_state), 3)
plt.bar(all_state, all_state_Crime_Violent_Rate, color=all_states_bar_colors, edgecolor='black')
plt.axhline(avg_crime_rate, color='red', linestyle='--', linewidth=2)
plt.text(+44, avg_crime_rate, f'Average Rate: {avg_crime_rate:.2f}', color='red', fontsize=10, fontweight='bold')

# adding title and label
plt.title('All State and D.C. Crime Violence Rate per 100,000 population in 2024', fontweight='bold')
plt.xlabel('All 50 States or District of Columbia', fontweight='bold')
plt.ylabel('Crime Violent Rate per 100,000 population', fontweight='bold')
plt.xticks(rotation=90)
plt.tight_layout()

# plot only once at the end to show all plots
plt.show()
print("Manually hit x in figures upper right corner to close and each figure and complete code")

# close connection made by engine
engine.dispose()
