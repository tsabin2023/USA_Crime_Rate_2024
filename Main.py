# CNE340 Winter Quarter
# 3/8/2024
# follow instructions below to complete program
# https://rtc.instructure.com/courses/2439016/assignments/31830681?module_item_id=79735823
# https://rtc.instructure.com/courses/2439016/files/236685445?module_item_id=79735228
# further instructions from instructor
# source Tyler Sabin
# source Van Loung Voung
# source Ix Procopios

# import libraries and install packages
# python interpreter 3.11
# pandas package
# matplot lib package
# pymysql package

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
import matplotlib.cm as cm

# todo Created database in LAMP/WAMP database (This can be done before and use same database you used for other assignments)
hostname = "127.0.0.1"
uname = "root"
pwd = ""
dbname = "USA_Crime_Rate_2024"

connection_string = f"mysql+pymysql://{uname}:{pwd}@{hostname}/{dbname}"
engine = create_engine(connection_string)


# todo Python code pulls data from a data source and puts data into Database
# we need to put csv in the same project folder as .py file.
# this is my local location for testing but needs csv to be accessed non-locally in same file as cloned
# for final version.

with open('crime-rate-by-state-2024.csv') as file_path:
    df = pd.read_csv(file_path)
    # print(df)
# we need to pick a new table name.
table_name = 'test_table_name'  # 'CrimeRate' is a column name in csv file so the table name must be different
df.to_sql(table_name, engine, if_exists='replace', index=False)

# todo Python code pulls data from database and analyzes analytics
# python code pulls data from database and analyzes analytics, is what we want it to do
query = f"SELECT * FROM {table_name} ORDER BY CrimeRate DESC" # pulling data from table in db
db_sorted = pd.read_sql(query, engine)

# sort out top 3 states from database

# print(df.columns)
values_at = db_sorted['CrimeViolentRate'].head(3)
# print(values_at)
# print(db_sorted['CrimeViolentRate'])

top_3_states = db_sorted.nlargest(3, 'CrimeViolentRate')  # first 3 highest states by row from db filtered
num_states = len(top_3_states)
colors = cm.rainbow(np.linspace(0, 1, num_states))  # module method seems to work

# plotting figure and using enumerate to add a counter i and zip to make two column tuple
plt.figure(figsize=(10, 6))
for i, (state, crime_rate) in enumerate(zip(top_3_states['state'], top_3_states['CrimeViolentRate'])):
    plt.bar(state, crime_rate, color=colors[i])
    plt.text(state, crime_rate, str(round(crime_rate, 2)), ha='center', va='bottom')  # adding text to the top of bar

plt.title('Top 3 states or districts Crime Violence Rate per 100,000 population in 2024')
plt.xlabel('50 States and D.C')
plt.ylabel('Crime Violent Rate per 100,000 population')

# Plot chart including all states' rate and the Average rate
# Plot all states' rate chart, Van

# Plot Average rate chart, Tyler
avg_crime_rate = db_sorted['CrimeViolentRate'].mean()

# create plot of all 50 states Crime Violence Rate per 100,000 Population in 2024 for All States
all_states_dc_2 = db_sorted  # all states and dc
num_states2 = len(all_states_dc_2)

# plot crime rate of states and d.c., tab20c colors displayed in reverse for distinguishing colors
plt.figure(figsize=(12, 6))

# plotting figure and using enumerate to add a counter i and zip to make two column tuple
for i, (state, crime_rate) in enumerate(zip(all_states_dc_2['state'], all_states_dc_2['CrimeViolentRate'])):
    if i % 3 == 0:
        color = cm.tab20(i // 3 % 20)
    elif i % 3 == 1:
        color = cm.tab20b(i // 3 % 20)
    else:
        color = cm.tab20c(19 - (i // 3 % 20))  # Reverses the order of tab20c colors

    plt.bar(state, crime_rate, color=color)
# all 50 states and distinct have different colors in an order that is easier to view

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
