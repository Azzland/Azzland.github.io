import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Read the Census CSV files for 17b, 17c and 43b (personal weekly income and employment status)
folder = 'C:/Users/Azzla/Documents/Data Science MIT/assignment2/'

input_file = folder + 'Completed_Employment_Status_by_Age_Group.csv'

data = pd.read_csv(input_file,index_col=0)

ages = data.columns

#Initialise arrays to store age categories and values for % in labour force
age_categories = []# age group
values = []# % in labour force

for age in ages:
    #For each age group allocate the right % in labour force value
    age_categories.append(age)
    labour_force_num = data.loc['Total in Labour Force'].at[age]
    total = data.loc['Total'].at[age]
    n = labour_force_num/total
    pc = n*100
    a = [age, pc]
    values.append(list(a))
    
#Create the dataframe
labour_force_by_age = pd.DataFrame(values, columns = ['Age Group', 'PC In Labour Force'])

#Display in Jupyter (if in IDLE or PyCharm use print)
display(labour_force_by_age)
