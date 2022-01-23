import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Read the Census CSV files for 17b, 17c and 43b (personal weekly income and employment status)
folder = 'C:/Users/Azzla/Documents/Data Science MIT/assignment2/'

input_file = folder + 'Income_and_Employment_by_Age_Group.csv'


data = pd.read_csv(input_file,index_col=0)
attributes = data.columns
num_cols = len(attributes)
ages = data.index
num_rows = len(ages)
census_age_groups = ages[0:num_rows-6]


#Set up arrays tpo store the x values (eligibility percentages) and the y values (employment status)
xvalues_lowincomecc = []# % eligible low income CC
yvalues_totalemp = []# % employed
xvalues_35000 = []# % earning 35000 and over
yvalues_fulltime = []# % working full time
xvalues_noteligiblecc = []# % not eligible for a CC
yvalues_unemployed = []# % unemployed

for age in census_age_groups:
    #For each age group access the appropriate values from the dataframe and put into appropriate arrays
    row = data.loc[age]
    xvalue = row.at['PC Eligible CC $15000/yr income minimum']
    xvalues_lowincomecc.append(xvalue)
    yvalue = row.at['PC Employed']
    yvalues_totalemp.append(yvalue)
    xvalue = row.at['PC Ineligible CC $15000/yr income minimum']
    xvalues_noteligiblecc.append(xvalue)
    yvalue = row.at['PC Unemployed']
    yvalues_unemployed.append(yvalue)
    xvalue = row.at['PC Eligible CC $35000/yr income minimum']
    xvalues_35000.append(xvalue)
    yvalue = row.at['PC Employed Full Time']
    yvalues_fulltime.append(yvalue)

#Append all x value and y value arrays into the one array
xvalues = [xvalues_noteligiblecc, xvalues_35000, xvalues_lowincomecc]
yvalues = [yvalues_unemployed, yvalues_fulltime, yvalues_totalemp]

#Create the x and y axis labels and store in array
x_labels = ["% Unemployed", "% Employed Full Time", "% Employed"]
y_labels = ["% Ineligible", "% Eligible", "% Eligible"]

#Create the titles for each scatter plot and store in array
Titles_Scatter = []
Titles_Scatter.append("Percentage Unemployed v Percentage Ineligible For Any Credit Card")
Titles_Scatter.append("Percentage Employed Full Time v Percentage Eligible For Credit Card\n On Income At Least $35000/year")
Titles_Scatter.append("Percentage Employed v Percentage Eligible For Low Income Credit Card")

for i in range(3):
    #For the three scatter plots plot x values (percentage eligibility/ineligibilty) v y values (% employment status)
    fig = plt.figure(figsize = (12, 10))
    plt.title(Titles_Scatter[i])
    plt.xlabel(x_labels[i])
    plt.ylabel(y_labels[i])
    plt.scatter(xvalues[i], yvalues[i])
    filename = "Figure_6_" + str(i+1) + ".jpg"
    plt.savefig(filename)
    plt.close()

#Create the correlation matrices and diaplay
input_data = {"% Eligible CC $15000/year":xvalues_lowincomecc,
              "% Employed": yvalues_totalemp}
df = pd.DataFrame(input_data, columns=input_data.keys())
corr = df.corr()
print(corr)


input_data = {"% Eligible CC $35000/year":xvalues_35000,
              "% FT Employed": yvalues_fulltime}
df = pd.DataFrame(input_data, columns=input_data.keys())
corr = df.corr()
print(corr)


input_data = {"% Ineligible CC":xvalues_noteligiblecc,
              "% Unemployed": yvalues_unemployed}
df = pd.DataFrame(input_data, columns=input_data.keys())
corr = df.corr()
print(corr)

    
    
