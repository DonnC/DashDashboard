import pandas as pd

# load static data
# TODO: Install xlrd for xlsx
from utility import parse_data

df_ait = parse_data(filename='data/ait.csv', isFileOnly=True)
df_eind = parse_data(filename='data/eco-data.csv', isFileOnly=True)

df = df_ait
print(df.head)
print(df[0])
# transpose to convert first column to a row
'''
df = df_ait.T

print('[INFO] DF-AIT')

print(df.head)

print(df.describe())

print('[INFO] Year data=')
print(df[1])

print('#' * 80 + '\n\n')
'''

df = df_eind.T

print('[INFO] DF-ECO')
print('[INFO] Year data=')

#print(df[0], df[1], df[2])

#print(df.head)

#print(df.describe())

#print('*' * 80)