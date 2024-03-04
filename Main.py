import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
import matplotlib.cm as cm

# todo Created database in LAMP/WAMP database (This can be done before and use same database you used for other assignments)
hostname="127.0.0.1"
uname="root"
pwd=""
dbname="USA_Crime_Rate_2024"

connection_string = f"mysql+pymysql://{uname}:{pwd}@{hostname}/{dbname}"
engine = create_engine(connection_string)


# todo Python code pulls data from a data source and puts data into Database
# we need to put csv in the same project folder as .py file.
# this is my local location for testing but needs csv to be accessed non-locally in same file as cloned
# for final version.

file_path = 'C:\\Users\\sabin\\Downloads\\crime-rate-by-state-2024.csv' # for testing, not final path
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
colors = cm.rainbow(np.linspace(0, 1, num_states))

# plot top 3 crime rate states
plt.figure(figsize=(10, 6))
for i, (state, crime_rate) in enumerate(zip(top_3_states['state'], top_3_states['CrimeViolentRate'])):
    plt.bar(state, crime_rate, color=colors[i])

plt.title('Top 3 States with Highest Crime Rates in 2024')
plt.xlabel('State')
plt.ylabel('Crime Violent Rate per 100,000 population')
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
# manually hit x in figure upper right corner to close figure and complete code

# sort bottom 3 Van
# plot graph 2 Van


engine.dispose()
print(f"DataFrame successfully sent to the '{table_name}' table in the '{dbname}' database.")
