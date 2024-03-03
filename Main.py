# CNE 340 - Network Databases and Structured Query Language (SQL)
# Winter 2024
# Group project name: USA Crime Rate 2024
# Project members: Tyler Sabin, Van Vuong

# Import section
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sqlalchemy import create_engine

# SQL connection and Database
hostname = '172.0.0.1'
uname = 'root'
pwd = ''
dbname = 'USA_Crime_Rate_2024'

connection_string = f'mysql+pymysql://{uname}:{pwd}@{hostname}/{dbname}'
engine = create_engine(connection_string)