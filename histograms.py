#Import the three Python modules numpy, pandas and matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Declare the input file name and folder location
folder = 'C:/Users/Azzla/Documents/Data Science MIT/assignment2/'

input_file = folder + 'Income_and_Employment_by_Age_Group.csv'


#Put the csv data into a new dataframe
data = pd.read_csv(input_file,index_col=0)

#Put the columns into an array and find the number of them
attributes = data.columns
num_cols = len(attributes)

#Find the row attributes and put all the Census age groups into an array (last 6 rows are the total and the modified age groups)
ages = data.index
num_rows = len(ages)
census_age_groups = ages[0:num_rows-6]


#Set up dictionaries for the bar graphs for the credit card eligibility bar graphs by age group             
cc_plotdata1 = {}
cc_plotdata2 = {}
cc_plotdata3 = {}
cc_plotdata4 = {}
cc_plotdata5 = {}
cc_plotdata6 = {}
cc_plotdata7 = {}
cc_plotdata8 = {}
#Set up dictionaries for the bar graphs for the employment type bar graphs by age group  
w_plotdata1 = {}
w_plotdata2 = {}
w_plotdata3 = {}

all_dictionaries = []


#Go through each row, which represents an age group and extract values for eligiblity, percentage eligibility and percentage employment type and put into their appropriate dictionaries
for age in census_age_groups:
    row = data.loc[age]
    cc_plotdata1[age] = row.at['Eligible CC $15000/yr income minimum']
    all_dictionaries.append(cc_plotdata1)
    cc_plotdata2[age] = row.at['Ineligible CC $15000/yr income minimum']
    all_dictionaries.append(cc_plotdata2)
    cc_plotdata3[age] = row.at['Eligible CC $35000/yr income minimum']
    all_dictionaries.append(cc_plotdata3)
    cc_plotdata4[age] = row.at['Ineligible CC $35000/yr income minimum']
    all_dictionaries.append(cc_plotdata4)
    cc_plotdata5[age] = row.at['PC Eligible CC $15000/yr income minimum']
    all_dictionaries.append(cc_plotdata5)
    cc_plotdata6[age] = row.at['PC Ineligible CC $15000/yr income minimum']
    all_dictionaries.append(cc_plotdata6)
    cc_plotdata7[age] = row.at['PC Eligible CC $35000/yr income minimum']
    all_dictionaries.append(cc_plotdata7)
    cc_plotdata8[age] = row.at['PC Ineligible CC $35000/yr income minimum']
    all_dictionaries.append(cc_plotdata8)
    w_plotdata1[age] = row.at['PC Employed Full Time']
    all_dictionaries.append(w_plotdata1)
    w_plotdata2[age] = row.at['PC Employed']
    all_dictionaries.append(w_plotdata2)
    w_plotdata3[age] = row.at['PC Unemployed']
    all_dictionaries.append(w_plotdata3)

#Create an array that stores a title for each bar graph
titles = []
titles.append('Number Of People Eligible For Low Income Credit Card')
titles.append('Number Of People Ineligible For Low Income Credit Card')
titles.append('Number Of People Eligible For Credit Card Requiring Income Of At Least $35000/year')
titles.append('Number Of People Ineligible For Credit Card Requiring Income Of At Least $35000/year')
titles.append('Percentage Of People Eligible For Low Income Credit Card')
titles.append('Percentage Of People Ineligible For Low Income Credit Card')
titles.append('Percentage Of People Eligible For Credit Card Requiring Income Of At Least $35000/year')
titles.append('Percentage Of People Ineligible For Credit Card Requiring Income Of At Least $35000/year')
titles.append('Percentage Of People Working Full Time')
titles.append('Percentage Of People Employed')
titles.append('Percentage Of People Unemployed')

#Create an array that contains y-axis labels for each bar graph
y_labels = ['No. Eligible', 'No. Ineligible', 'No. Eligible', 'No. Ineligible', '%. Eligible', '%. Ineligible', '%. Eligible', '%. Ineligible', '% Full Time', '% Employed', '% Unemployed']


#Plot all graphs for all Census age groups
num_graphs = 11
fig_num = 1
for i in range(num_graphs):
    dic = all_dictionaries[i]
    age_groups = list(dic.keys())
    values = list(dic.values())
    fig = plt.figure(figsize = (12, 10))
    #If it is the 5th, 6th, 7th and 8th graphs (%elgiblibility and %ineligibility bar graphs)
    if (fig_num > 4) and (fig_num < 9):
        #Set the color, width and the x and y values for the bars
        plt.bar(age_groups, values, color ='c',width = 0.5)
        #Set the y value limit on the graph equal to 120% the maximum value
        plt.ylim(0, int(1.2*max(values)))
        #Create the formatting and positioning of the text showing the value represented by each bar, align vertically with a fontsize of 20 and make it black.
        for j, v in enumerate(values):
            pos = v + 2
            plt.text(j,pos,'%.2f'% v,color='black', fontsize=20, rotation ='vertical',horizontalalignment='left')
    #if the figure is the 9th, 10th or 11th plot (employment status)
    elif fig_num > 8:
        #Make bars green
        plt.bar(age_groups, values, color ='g',width = 0.5)
        plt.ylim(0, int(1.2*max(values)))
        for j, v in enumerate(values):
            if fig_num == 11:
                #Unemployment rates are very low so positioning value is different
                pos = v + 0.5
                plt.text(j,pos,'%.2f'% v,color='black', fontsize=20, rotation ='vertical',horizontalalignment='left')
            else:
                pos = v + 2
                plt.text(j,pos,'%.2f'% v,color='black', fontsize=20, rotation ='vertical',horizontalalignment='left')
    else:
        #For other graphs, set colour as orange for the bars
        plt.bar(age_groups, values, color ='orange',width = 0.5)
        #Create the y axis labels and ticks
        plt.ticklabel_format(style='plain', useOffset=False, axis='y')
        #Set the limit on the y values
        plt.ylim(0, int(1.5*max(values)))
        for j, v in enumerate(values):
            pos = v + 10000
            plt.text(j,pos,'%d'% v,color='black', fontsize=20, rotation ='vertical',horizontalalignment='left')

    #X axis label is Age Groups
    plt.xlabel("Age Groups")
    #Y axis label equal to the appropriate element in the y labels array
    plt.ylabel(y_labels[i])
    #Graph title equal to the appropriate element in the titles array
    plt.title(titles[i])
    #Create filename
    filename = "Figure_1_" + str(fig_num) + ".jpg"
    #Save the graph
    plt.savefig(filename)
    #Close the plot to remove from memory
    plt.close()
    #Move on to the next graph by increasing id fig_num by 1. 
    fig_num += 1
    


#Now do all the bar plots for the modified age categories.
titles_c = ["Eligible Low Income\n Credit Card", "Ineligible Low Income\n Credit Card", "Eligible Credit Card\n Annual Income $35000 Or Higher", "Ineligible Credit Card\n Annual Income $35000 Or Higher", "Full Time Employed", "Employed", "Unemployed"]
y_labels = ["% Eligible", "% Eligible", "% Eligible", "% Eligible", "% Full Time", "% Employed", "% Unemployed"]
                
#15-24 years vs 25 and over
all_dictionaries = []
cc_u25_25ov_1 = {}
cc_u25_25ov_2 = {}
cc_u25_25ov_3 = {}
cc_u25_25ov_4 = {}
w_u25_25ov_1 = {}
w_u25_25ov_2 = {}
w_u25_25ov_3 = {}

#Create the dictionaries containing the values
for age in ["15 to 24 years", "25 over years"]:
    row = data.loc[age]
    cc_u25_25ov_1[age] = row.at['PC Eligible CC $15000/yr income minimum']
    all_dictionaries.append(cc_u25_25ov_1)
    cc_u25_25ov_2[age] = row.at['PC Ineligible CC $15000/yr income minimum']
    all_dictionaries.append(cc_u25_25ov_2)
    cc_u25_25ov_3[age] = row.at['PC Eligible CC $35000/yr income minimum']
    all_dictionaries.append(cc_u25_25ov_3)
    cc_u25_25ov_4[age] = row.at['PC Ineligible CC $35000/yr income minimum']
    all_dictionaries.append(cc_u25_25ov_4)
    w_u25_25ov_1[age] = row.at['PC Employed Full Time']
    all_dictionaries.append(w_u25_25ov_1)
    w_u25_25ov_2[age] = row.at['PC Employed']
    all_dictionaries.append(w_u25_25ov_2)
    w_u25_25ov_3[age] = row.at['PC Unemployed']
    all_dictionaries.append(w_u25_25ov_3)

#Plot the graphs
num_graphs = 7
fig_num = 1
for i in range(num_graphs):
    dic = all_dictionaries[i]
    age_groups = list(dic.keys())
    values = list(dic.values())
    fig = plt.figure(figsize = (12, 10))
    if (fig_num > 4):
        plt.bar(age_groups, values, color ='g',width = 0.7)
        plt.tick_params(axis='x', which='major', labelsize=30)
        for j, v in enumerate(values):
            pos = 0.1*v
            plt.text(j,pos,'%.2f'% v,color='black', fontsize=40, rotation ='vertical',horizontalalignment='left')            
    else:
        plt.bar(age_groups, values, color ='c',width = 0.7)
        plt.tick_params(axis='x', which='major', labelsize=30)
        for j, v in enumerate(values):
            pos = 0.1*v
            plt.text(j,pos,'%.2f'% v,color='black', fontsize=40, rotation ='vertical',horizontalalignment='left')            
    plt.ylim(0, int(max(values)+10))
    plt.xlabel("Age Groups", fontsize=20)
    plt.ylabel(y_labels[i], fontsize=20)
    plt.title(titles_c[i], fontsize=35)
    filename = "Figure_2_" + str(fig_num) + ".jpg"
    plt.savefig(filename)
    plt.close()
    fig_num += 1

#15-24 years vs 25 to 64 years
all_dictionaries = []
cc_u25_25_64_1 = {}
cc_u25_25_64_2 = {}
cc_u25_25_64_3 = {}
cc_u25_25_64_4 = {}
w_u25_25_64_1 = {}
w_u25_25_64_2 = {}
w_u25_25_64_3 = {}

#Create the dictionaries containing the plotting info
for age in ["15 to 24 years", "25 to 64 years"]:
    row = data.loc[age]
    cc_u25_25_64_1[age] = row.at['PC Eligible CC $15000/yr income minimum']
    all_dictionaries.append(cc_u25_25_64_1)
    cc_u25_25_64_2[age] = row.at['PC Ineligible CC $15000/yr income minimum']
    all_dictionaries.append(cc_u25_25_64_2)
    cc_u25_25_64_3[age] = row.at['PC Eligible CC $35000/yr income minimum']
    all_dictionaries.append(cc_u25_25_64_3)
    cc_u25_25_64_4[age] = row.at['PC Ineligible CC $35000/yr income minimum']
    all_dictionaries.append(cc_u25_25_64_4)
    w_u25_25_64_1[age] = row.at['PC Employed Full Time']
    all_dictionaries.append(w_u25_25_64_1)
    w_u25_25_64_2[age] = row.at['PC Employed']
    all_dictionaries.append(w_u25_25_64_2)
    w_u25_25_64_3[age] = row.at['PC Unemployed']
    all_dictionaries.append(w_u25_25_64_3)

#Plot the graphs
num_graphs = 7
fig_num = 1
for i in range(num_graphs):
    dic = all_dictionaries[i]
    age_groups = list(dic.keys())
    values = list(dic.values())
    fig = plt.figure(figsize = (12, 10))
    if (fig_num > 4):
        plt.bar(age_groups, values, color ='g',width = 0.7)
        plt.tick_params(axis='x', which='major', labelsize=30)
        for j, v in enumerate(values):
            pos = 0.1*v
            plt.text(j,pos,'%.2f'% v,color='black', fontsize=40, rotation ='vertical',horizontalalignment='left')
    else:
        plt.bar(age_groups, values, color ='c',width = 0.7)
        plt.tick_params(axis='x', which='major', labelsize=30)
        for j, v in enumerate(values):
            pos = 0.1*v
            plt.text(j,pos,'%.2f'% v,color='black', fontsize=40, rotation ='vertical',horizontalalignment='left')          
    plt.ylim(0, int(max(values)+10))
    plt.xlabel("Age Groups", fontsize=20)
    plt.ylabel(y_labels[i], fontsize=20)
    plt.title(titles_c[i], fontsize=35)
    filename = "Figure_3_" + str(fig_num) + ".jpg"
    plt.savefig(filename)
    plt.close()
    fig_num += 1

#Under 20 years v 20 years and over
all_dictionaries = []
cc_u20_20ov_1 = {}
cc_u20_20ov_2 = {}
cc_u20_20ov_3 = {}
cc_u20_20ov_4 = {}
w_u20_20ov_1 = {}
w_u20_20ov_2 = {}
w_u20_20ov_3 = {}

#Create the dictionaries containing the plot into
for age in ["15-19 yrs", "20 over years"]:
    row = data.loc[age]
    cc_u20_20ov_1[age] = row.at['PC Eligible CC $15000/yr income minimum']
    all_dictionaries.append(cc_u20_20ov_1)
    cc_u20_20ov_2[age] = row.at['PC Ineligible CC $15000/yr income minimum']
    all_dictionaries.append(cc_u20_20ov_2)
    cc_u20_20ov_3[age] = row.at['PC Eligible CC $35000/yr income minimum']
    all_dictionaries.append(cc_u20_20ov_3)
    cc_u20_20ov_4[age] = row.at['PC Ineligible CC $35000/yr income minimum']
    all_dictionaries.append(cc_u20_20ov_4)
    w_u20_20ov_1[age] = row.at['PC Employed Full Time']
    all_dictionaries.append(w_u20_20ov_1)
    w_u20_20ov_2[age] = row.at['PC Employed']
    all_dictionaries.append(w_u20_20ov_2)
    w_u20_20ov_3[age] = row.at['PC Unemployed']
    all_dictionaries.append(w_u20_20ov_3)

#Plot the graphs
num_graphs = 7
fig_num = 1
for i in range(num_graphs):
    dic = all_dictionaries[i]
    age_groups = list(dic.keys())
    values = list(dic.values())
    fig = plt.figure(figsize = (12, 10))
    if (fig_num > 4):
        plt.bar(age_groups, values, color ='g',width = 0.7)
        plt.tick_params(axis='x', which='major', labelsize=30)
        for j, v in enumerate(values):
            pos = 0.1*v
            plt.text(j,pos,'%.2f'% v,color='black', fontsize=40, rotation ='vertical',horizontalalignment='left')
            
    else:
        plt.bar(age_groups, values, color ='c',width = 0.7)
        plt.tick_params(axis='x', which='major', labelsize=30)
        for j, v in enumerate(values):
            pos = 0.1*v
            plt.text(j,pos,'%.2f'% v,color='black', fontsize=40, rotation ='vertical',horizontalalignment='left')
    plt.ylim(0, int(max(values)+10))
    plt.xlabel("Age Groups", fontsize=20)
    plt.ylabel(y_labels[i], fontsize=20)
    plt.title(titles_c[i], fontsize=35)
    filename = "Figure_4_" + str(fig_num) + ".jpg"
    plt.savefig(filename)
    plt.close()
    fig_num += 1

#Under 19 years vs 20 to 64 years
all_dictionaries = []
cc_u20_20_64_1 = {}
cc_u20_20_64_2 = {}
cc_u20_20_64_3 = {}
cc_u20_20_64_4 = {}
w_u20_20_64_1 = {}
w_u20_20_64_2 = {}
w_u20_20_64_3 = {}

#Create the dictionaries containing the plot info
for age in ["15-19 yrs", "20 to 64 years"]:
    row = data.loc[age]
    cc_u20_20_64_1[age] = row.at['PC Eligible CC $15000/yr income minimum']
    all_dictionaries.append(cc_u20_20_64_1)
    cc_u20_20_64_2[age] = row.at['PC Ineligible CC $15000/yr income minimum']
    all_dictionaries.append(cc_u20_20_64_2)
    cc_u20_20_64_3[age] = row.at['PC Eligible CC $35000/yr income minimum']
    all_dictionaries.append(cc_u20_20_64_3)
    cc_u20_20_64_4[age] = row.at['PC Ineligible CC $35000/yr income minimum']
    all_dictionaries.append(cc_u20_20_64_4)
    w_u20_20_64_1[age] = row.at['PC Employed Full Time']
    all_dictionaries.append(w_u20_20_64_1)
    w_u20_20_64_2[age] = row.at['PC Employed']
    all_dictionaries.append(w_u20_20_64_2)
    w_u20_20_64_3[age] = row.at['PC Unemployed']
    all_dictionaries.append(w_u20_20_64_3)

#Plot the graphs
num_graphs = 7
fig_num = 1
for i in range(num_graphs):
    dic = all_dictionaries[i]
    age_groups = list(dic.keys())
    values = list(dic.values())
    fig = plt.figure(figsize = (12, 10))
    if (fig_num > 4):
        plt.bar(age_groups, values, color ='g',width = 0.7)
        plt.tick_params(axis='x', which='major', labelsize=30)
        for j, v in enumerate(values):
            pos = 0.1*v
            plt.text(j,pos,'%.2f'% v,color='black', fontsize=40, rotation ='vertical',horizontalalignment='left')            
    else:
        plt.bar(age_groups, values, color ='c',width = 0.7)
        plt.tick_params(axis='x', which='major', labelsize=30)
        for j, v in enumerate(values):
            pos = 0.1*v
            plt.text(j,pos,'%.2f'% v,color='black', fontsize=40, rotation ='vertical',horizontalalignment='left')            
    plt.ylim(0, int(max(values)+10))
    plt.xlabel("Age Groups", fontsize=20)
    plt.ylabel(y_labels[i], fontsize=20)
    plt.title(titles_c[i], fontsize=35)
    filename = "Figure_5_" + str(fig_num) + ".jpg"
    plt.savefig(filename)
    plt.close()
    fig_num += 1 

