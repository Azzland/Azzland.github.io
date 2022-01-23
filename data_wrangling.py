import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Read the Census CSV files for 17b, 17c and 43b (personal weekly income and employment status)
folder = 'C:/Users/Azzla/Documents/Data Science MIT/assignment2/'

input_file_17b = folder + '2016Census_G17B_AUS.csv'
input_file_17c = folder + '2016Census_G17C_AUS.csv'
input_file_43b = folder + '2016Census_G43B_AUS.csv'

data_17b = pd.read_csv(input_file_17b)
data_17c = pd.read_csv(input_file_17c)
data_43b = pd.read_csv(input_file_43b)

#Extract the column names from the dataframe from Table 17B
cols_17b = data_17b.columns

#Calculate the number of columns in dataframe 17B and find the column number of where the "P" (all persons) attributes start.
num_cols_17b = len(cols_17b)
start_col = 0
for attribute in cols_17b:
    if attribute[0] == "P":
        break
    start_col += 1


#Set up array appending all the columns to delete from the dataframe that are not required (e.g. all the attributes except the first one before the start of the 'P' attributes)
delete_from_data_17b = []

k = 1
while k < start_col:
    delete_from_data_17b.append(cols_17b[k])
    k += 1
 
#Drop all non-required columns from the dataframe as defined by the array above
data_17b.drop(delete_from_data_17b, axis=1, inplace=True)

#Find all the attributes from Table (dataframe) 17C.
cols_data_17c = data_17c.columns
num_cols_data_17c = len(cols_data_17c)

#Add all attributes (except the first one which is the same as the first attribute in 17B) to dataframe 17B
for i in range(1, num_cols_data_17c):
    data_17b[cols_data_17c[i]] = data_17c[cols_data_17c[i]]
    
#Export modified dataframes into csv files
output_17 = data_17b.to_csv(folder + 'Personal_Income_Bracket_by_Age_Group.csv')

columns_17 = data_17b.columns
num_cols_df17 = len(columns_17)

#Count the numeric values in the dataframe 17b. Go through each column value for the only row and convert to string, check if it is numeric, if true than it is added to the values tally num_values. 
num_values = 0
n = data_17b.loc[0]
for i in n:
    if str(i).isdigit():
        num_values += 1
    
print('Number of columns in DataFrame 17: ' + str(num_cols_df17))
print('Number of numerical values in DataFrame 17: ' + str(num_values))
if num_values == num_cols_df17:
    print('There are no missing values nor erraneous values in the income by age dataframe')

#Extract the column names from the dataframe from Table 43B
cols_43b = data_43b.columns

#Calculate the number of columns in dataframe 17B and find the column number of where the "P" (all persons) attributes start.
num_cols_43b = len(cols_43b)
start_col = 0
for attribute in cols_43b:
    if attribute[0] == "P":
        break
    start_col += 1


#Set up array appending all the columns to delete from the dataframe that are not required (e.g. all the attributes except the first one before the start of the 'P' attributes)
delete_from_data_43b = []

k = 1
while k < start_col:
    delete_from_data_43b.append(cols_43b[k])
    k += 1
 
#Drop all non-required columns from the dataframe as defined by the array above
data_43b.drop(delete_from_data_43b, axis=1, inplace=True)

#Export modified dataframes into csv files
output_43 = data_43b.to_csv(folder + 'Employment_Status_by_Age_Group.csv')

columns_43 = data_43b.columns
num_cols_df43 = len(columns_43)

#Count the numeric values in the dataframe 43b. Go through each column value for the only row and convert to string, check if it is numeric, if true than it is added to the values tally num_values. 
num_values = 0
n = data_43b.loc[0]
for i in n:
    if str(i).isdigit():
        num_values += 1

print('Number of columns in DataFrame 43: ' + str(num_cols_df43))
print('Number of numerical values in DataFrame 43: ' + str(num_values))
if num_values == num_cols_df43:
    print('There are no missing values nor erraneous values in the employment status by age dataframe')

#For both tables drop the first column which is the AUSCODE as it is not required.
all_counts_income_with_code = np.array(data_17b.loc[0])
all_counts_income = np.delete(all_counts_income_with_code,0)

all_attributes_income_with_code = np.array(columns_17)
all_attributes_income = np.delete(all_attributes_income_with_code,0)

all_counts_employment_with_code = np.array(data_43b.loc[0])
all_counts_employment = np.delete(all_counts_employment_with_code,0)

all_attributes_employment_with_code = np.array(columns_43)
all_attributes_employment = np.delete(all_attributes_employment_with_code,0)

#Use numpy to find the number of columns and values for dataframe 17b
size_array_income_counts = all_counts_income.size
size_array_income_attributes = all_attributes_income.size

#If the number of columns matches the number of values for the table print a message
if size_array_income_counts == size_array_income_attributes:
    print('The number of values match the number of columns like in the dataframe 17b')

#Do the previous two steps for datframe 43b
size_array_employment_counts = all_counts_employment.size
size_array_employment_attributes = all_attributes_employment.size

if size_array_employment_counts == size_array_employment_attributes:
    print('The number of values match the number of columns like in the dataframe 43b')


#Set up arrays that store part of the attributes likely to be stored in the dataframe 17b
age_group_cols = ['15_19', '20_24', '25_34','35_44', '45_54', '55_64','65_74', '75_84', '85', 'Tot']
income_rows = ['Neg_Nil_income','1_149','150_299','300_399','400_499','500_649','650_799','800_999','1000_1249','1250_1499','1500_1749','1750_1999','2000_2999','3000_more','PI_NS','Tot']

#Set up arrays to contain the output indices and column headers for the new dataframe
age_labels = ['15-19 yrs', '20-24 yrs', '25-34 yrs','35-44 yrs', '45-54 yrs', '55-64 yrs','65-74 yrs', '75-84 yrs', '85ov yrs', 'Total']
income_labels = ['Neg to Nil income','$1 to $149','$150 to $299','$300 to $399','$400 to $499','$500 to $649','$650 to $799','$800 to $999','$1000 to $1249','$1250 to $1499','$1500 to $1749','$1750 to $1999','$2000 to $2999','$3000 or more','Income Not Stated','Total']

#Do the above for 43b
employment_group_rows = ['Emp_FullT','Emp_PartT','Emp_awy_f_wrk','Hours_wkd_NS','Tot_Emp','Umem_look_FTW','Unem_look_PTW','Tot_Unemp','Tot_LF','Not_in_LF','LFS_NS','Tot']
employment_labels = ['Employed Full Time','Employed Part Time','Employed (away from work)','Hours worked are not stated','Total Employed','Unemployed (looking for FT work)','Unemployed (looking for PT work)','Total Unemployed','Total in Labour Force','Not in the Labour Force','Labour Force Status Not Stated','Total']

num_cols = len(age_group_cols) #Each row in all arrays will represent an age group, so there will be 10 rows for all 4 arrays.
num_rows_income = int(size_array_income_counts/num_cols) #Each column represents and income category

#Work out the number of columns for the 43b reshaped dataframe
num_rows_employment = int(size_array_employment_counts/num_cols)

#Reshape both dataframes so that each column represents an age group and each row represents an income (or employment) category
reshaped_income_value_array = all_counts_income.reshape(num_rows_income,num_cols)
reshaped_income_attribute_array = all_attributes_income.reshape(num_rows_income,num_cols)

reshaped_employment_value_array = all_counts_employment.reshape(num_rows_employment,num_cols)
reshaped_employment_attribute_array = all_attributes_employment.reshape(num_rows_employment,num_cols)

#Create a new dataframe for the income by age group data
new_data_17b = pd.DataFrame(reshaped_income_value_array, columns=age_labels, index= income_labels)


#Create a new dataframe for the employment by age group data
new_data_43b = pd.DataFrame(reshaped_employment_value_array, columns=age_labels, index= employment_labels)

#Write out output to new CSV file
output_rshpd_17 = new_data_17b.to_csv(folder + 'Sorted_Personal_Income_Bracket_by_Age_Group.csv')
output_rshpd_43 = new_data_43b.to_csv(folder + 'Sorted_Employment_Status_by_Age_Group.csv')

#Check the total counts for each age group and the total in the income dataframe as we are assuming the income categories are mutually exclusive. If they
#are not mutually exclusive, still print out a message but it won't really matter as the total reported by the census will still be used and
#maybe there are errors in cencus participant input
for attribute in age_labels:
    col = new_data_17b[attribute]
    values = []
    for income in income_labels:
        if income != "Total":
            count = col.at[income]
            values.append(count)
    calculated_total = sum(values)
    census_total = col.at["Total"]
    if calculated_total == census_total:
        print('Calculated and Census totals agree')
    else:
        print('The total value reported in the Census is ' + str(census_total) + '. The calculated total of the column values are actually ' + str(calculated_total))

#Creating dataframe info for $15000 elgibility
#Income per week for $15000 salary accoridng to paycalculator.com.au is $288. 
#So that makes all categories below 300 to 399/week ineligible and the rest eligible
eligible_15000 = []
ineligible_15000 = []
percentage_eligible_15000 = []
percentage_ineligible_15000 = []

#Creating dataframe info for $35000 elgibility
#Income per week for $35000 salary accoridng to paycalculator.com.au is $600. 
#So that makes all categories below 650 to 799/week ineligible and the rest eligible
eligible_35000 = []
ineligible_35000 = []
percentage_eligible_35000 = []
percentage_ineligible_35000 = []

display(new_data_17b)


for age in age_labels:
    #For each age category, calculate the population count and percentage of the age group total of the people earning in the
    #weekly income bracket below $300 (earning an annual pay of under $15000 a year and therefore are not eligible for a low income
    #credit card. Append to an array
    col = new_data_17b[age]
    values = [col.at["Neg to Nil income"],col.at["$1 to $149"],col.at["$150 to $299"]]
    s = sum(values)
    pc = (s/(col.at["Total"] - col.at["Income Not Stated"]))*100
    ineligible_15000.append(s)
    percentage_ineligible_15000.append(pc)
    values = [col.at["$300 to $399"], col.at["$400 to $499"], col.at["$500 to $649"], col.at["$650 to $799"], col.at["$800 to $999"], col.at["$1000 to $1249"], col.at["$1250 to $1499"], col.at["$1500 to $1749"], col.at["$1750 to $1999"], col.at["$2000 to $2999"], col.at["$3000 or more"]]
    s = sum(values)
    pc = (s/(col.at["Total"] - col.at["Income Not Stated"]))*100
    eligible_15000.append(s)
    percentage_eligible_15000.append(pc)

    #For each age category, calculate the population count and percentage of the age group total of the people earning in the
    #weekly income bracket below $650 (earning an annual pay of under $35000 a year and therefore are not eligible for a
    #credit card with such an incoem requirement. Append to an array
    values = [col.at["Neg to Nil income"],col.at["$1 to $149"],col.at["$150 to $299"],col.at["$300 to $399"], col.at["$400 to $499"], col.at["$500 to $649"]]
    s = sum(values)
    pc = (s/(col.at["Total"] - col.at["Income Not Stated"]))*100
    ineligible_35000.append(s)
    percentage_ineligible_35000.append(pc)
    values = [col.at["$650 to $799"], col.at["$800 to $999"], col.at["$1000 to $1249"], col.at["$1250 to $1499"], col.at["$1500 to $1749"], col.at["$1750 to $1999"], col.at["$2000 to $2999"], col.at["$3000 or more"]]
    s = sum(values)
    pc = (s/(col.at["Total"] - col.at["Income Not Stated"]))*100
    eligible_35000.append(s)
    percentage_eligible_35000.append(pc)

#add new rows to the dataframe
new_data_17b.loc['Eligible CC $15000/yr income minimum'] = eligible_15000
new_data_17b.loc['PC Eligible CC $15000/yr income minimum'] = percentage_eligible_15000
new_data_17b.loc['Ineligible CC $15000/yr income minimum'] = ineligible_15000
new_data_17b.loc['PC Ineligible CC $15000/yr income minimum'] = percentage_ineligible_15000
new_data_17b.loc['Eligible CC $35000/yr income minimum'] = eligible_35000
new_data_17b.loc['PC Eligible CC $35000/yr income minimum'] = percentage_eligible_35000
new_data_17b.loc['Ineligible CC $35000/yr income minimum'] = ineligible_35000
new_data_17b.loc['PC Ineligible CC $35000/yr income minimum'] = percentage_ineligible_35000

#Calculate values for all income categories for 20 and over, 25 and over, 15 to 24, 20 to 65 and 25 to 65
all_15_to_24_i = []
all_25_over_i = []
all_20_over_i = []
all_20_to_64_i = []
all_25_to_64_i = []
row_categories = new_data_17b.index
num_row_categories = len(row_categories)

#Create an array to access the eligiblity attributes for these modified age group data
eligibility_categories = ['Eligible CC $15000/yr income minimum','Ineligible CC $15000/yr income minimum','Eligible CC $35000/yr income minimum','Ineligible CC $35000/yr income minimum']

display(new_data_17b)
display(new_data_43b)

for category in row_categories:
    if category in income_labels:
        #For each category with a persons count value calculate the values for the new age groups
        row = new_data_17b.loc[category]
        value = row.at['15-19 yrs'] + row['20-24 yrs']
        all_15_to_24_i.append(value)
        value = row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']+ row['65-74 yrs'] + row.at['75-84 yrs'] + row['85ov yrs']
        all_25_over_i.append(value)
        value = row.at['20-24 yrs'] + row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']+ row['65-74 yrs'] + row.at['75-84 yrs'] + row['85ov yrs']
        all_20_over_i.append(value)
        value = row['20-24 yrs'] + row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']
        all_20_to_64_i.append(value)
        value = row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']
        all_25_to_64_i.append(value)
    else:
        if category in eligibility_categories:
            #For each category with a percentage value calculate the values for the new age groups
            total = new_data_17b.loc["Total"]
            row = new_data_17b.loc[category]
            count = row.at['15-19 yrs'] + row['20-24 yrs']
            tot = total.at['15-19 yrs'] + total['20-24 yrs']
            all_15_to_24_i.append(count)
            pc = (count/tot)*100
            all_15_to_24_i.append(pc)
            count = row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']+ row['65-74 yrs'] + row.at['75-84 yrs'] + row['85ov yrs']
            tot = total.at['25-34 yrs'] + total['35-44 yrs'] + total.at['45-54 yrs'] + total['55-64 yrs']+ total['65-74 yrs'] + total.at['75-84 yrs'] + total['85ov yrs']
            all_25_over_i.append(count)
            pc = (count/tot)*100
            all_25_over_i.append(pc)
            count = row.at['20-24 yrs'] + row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']+ row['65-74 yrs'] + row.at['75-84 yrs'] + row['85ov yrs']
            tot = total.at['20-24 yrs'] + total.at['25-34 yrs'] + total['35-44 yrs'] + total.at['45-54 yrs'] + total['55-64 yrs']+ total['65-74 yrs'] + total.at['75-84 yrs'] + total['85ov yrs']
            all_20_over_i.append(count)
            pc = (count/tot)*100
            all_20_over_i.append(pc)
            count = row['20-24 yrs'] + row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']
            tot = total['20-24 yrs'] + total.at['25-34 yrs'] + total['35-44 yrs'] + total.at['45-54 yrs'] + total['55-64 yrs']
            all_20_to_64_i.append(count)
            pc = (count/tot)*100
            all_20_to_64_i.append(pc)
            count = row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']
            tot = total.at['25-34 yrs'] + total['35-44 yrs'] + total.at['45-54 yrs'] + total['55-64 yrs']
            all_25_to_64_i.append(count)
            pc = (count/tot)*100
            all_25_to_64_i.append(pc)
      

#Add the new columns to the data_frame
new_data_17b['15 to 24 years'] = all_15_to_24_i
new_data_17b['25 over years'] = all_25_over_i
new_data_17b['20 over years'] = all_20_over_i
new_data_17b['20 to 64 years'] = all_20_to_64_i
new_data_17b['25 to 64 years'] = all_25_to_64_i

#Set up arrays to store values for full time employment, total employment and unemployment as percentage values of age group totals
pc_full_time = []
pc_employed = []
pc_unemployed = []


for age in age_labels:
    #For each age group calculate percentage totals for full time employment, total employment and unemployment as percentages and append to the
    #appropriate arrays
    col = new_data_43b[age]
    pc = (col.at["Employed Full Time"]/(col.at["Total"]))*100
    pc_full_time.append(pc)
    pc = (col.at["Total Employed"]/(col.at["Total"]))*100
    pc_employed.append(pc)
    pc = (col.at["Total Unemployed"]/(col.at["Total"]))*100
    pc_unemployed.append(pc)

#Create new columns for the dataframe 43b appending the appropriate array values
new_data_43b.loc['PC Full Time Employed'] = pc_full_time
new_data_43b.loc['PC Employed'] = pc_employed
new_data_43b.loc['PC Unemployed'] = pc_unemployed

#Calculate values for all employment categories for 20 and over, 25 and over, 15 to 24, 20 to 65 and 25 to 65
all_15_to_24_e = []
all_25_over_e = []
all_20_over_e = []
all_20_to_64_e = []
all_25_to_64_e = []

for category in employment_labels:
    #For each category with a persons count value calculate the values for the new age groups
    row = new_data_43b.loc[category]
    value = row.at['15-19 yrs'] + row['20-24 yrs']
    all_15_to_24_e.append(value)
    value = row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']+ row['65-74 yrs'] + row.at['75-84 yrs'] + row['85ov yrs']
    all_25_over_e.append(value)
    value = row.at['20-24 yrs'] + row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']+ row['65-74 yrs'] + row.at['75-84 yrs'] + row['85ov yrs']
    all_20_over_e.append(value)
    value = row['20-24 yrs'] + row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']
    all_20_to_64_e.append(value)
    value = row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']
    all_25_to_64_e.append(value)

calculate_percentages_with = ["Employed Full Time", "Total Employed", "Total Unemployed"]
for category in employment_labels:
    if category in calculate_percentages_with:
        #For each category with a persons count value calculate the values for the new age groups
        total = new_data_43b.loc["Total"]
        row = new_data_43b.loc[category]
        count = row.at['15-19 yrs'] + row['20-24 yrs']
        tot = total.at['15-19 yrs'] + total['20-24 yrs']
        pc = (count/tot)*100
        all_15_to_24_e.append(pc)
        count = row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']+ row['65-74 yrs'] + row.at['75-84 yrs'] + row['85ov yrs']
        tot = total.at['25-34 yrs'] + total['35-44 yrs'] + total.at['45-54 yrs'] + total['55-64 yrs']+ total['65-74 yrs'] + total.at['75-84 yrs'] + total['85ov yrs']
        pc = (count/tot)*100
        all_25_over_e.append(pc)
        count = row.at['20-24 yrs'] + row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']+ row['65-74 yrs'] + row.at['75-84 yrs'] + row['85ov yrs']
        tot = total.at['20-24 yrs'] + total.at['25-34 yrs'] + total['35-44 yrs'] + total.at['45-54 yrs'] + total['55-64 yrs']+ total['65-74 yrs'] + total.at['75-84 yrs'] + total['85ov yrs']
        pc = (count/tot)*100
        all_20_over_e.append(pc)
        count = row['20-24 yrs'] + row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']
        tot = total['20-24 yrs'] + total.at['25-34 yrs'] + total['35-44 yrs'] + total.at['45-54 yrs'] + total['55-64 yrs']
        pc = (count/tot)*100
        all_20_to_64_e.append(pc)
        count = row.at['25-34 yrs'] + row['35-44 yrs'] + row.at['45-54 yrs'] + row['55-64 yrs']
        tot = total.at['25-34 yrs'] + total['35-44 yrs'] + total.at['45-54 yrs'] + total['55-64 yrs']
        pc = (count/tot)*100
        all_25_to_64_e.append(pc)

#Add the new columns to the data_frame
new_data_43b['15 to 24 years'] = all_15_to_24_e
new_data_43b['25 over years'] = all_25_over_e
new_data_43b['20 over years'] = all_20_over_e
new_data_43b['20 to 64 years'] = all_20_to_64_e
new_data_43b['25 to 64 years'] = all_25_to_64_e


#Write updated dataframes to CSV for backup
income_csv = new_data_17b.to_csv(folder + 'Completed_Personal_Income_Bracket_by_Age_Group.csv')
employment_csv = new_data_43b.to_csv(folder + 'Completed_Employment_Status_by_Age_Group.csv')

age_groups = new_data_17b.columns
num_age_categories = len(age_groups)

#Now lets put the percentages and totals for CC eligbility and employment status (full time, total employed and unemployed) into another dataframe.
attributes = ['Eligible CC $15000/yr income minimum','Ineligible CC $15000/yr income minimum','Eligible CC $35000/yr income minimum','Ineligible CC $35000/yr income minimum','PC Eligible CC $15000/yr income minimum','PC Ineligible CC $15000/yr income minimum','PC Eligible CC $35000/yr income minimum','PC Ineligible CC $35000/yr income minimum','Employed Full Time','Total Employed','Total Unemployed','PC Employed Full Time','PC Employed','PC Unemployed','Total']
income_employment_by_age = pd.DataFrame(columns=attributes,index=age_groups)



new_data = []
for age in age_groups:
    #Set up and append the appropriate attribute values to the new age group columns, then append to the new dataframe
    col = []
    income_data = new_data_17b[age]
    employment_data = new_data_43b[age]
    col.append(income_data.at['Eligible CC $15000/yr income minimum'])
    col.append(income_data.at['Ineligible CC $15000/yr income minimum'])
    col.append(income_data.at['Eligible CC $35000/yr income minimum'])
    col.append(income_data.at['Ineligible CC $35000/yr income minimum'])
    col.append(income_data.at['PC Eligible CC $15000/yr income minimum'])
    col.append(income_data.at['PC Ineligible CC $15000/yr income minimum'])
    col.append(income_data.at['PC Eligible CC $35000/yr income minimum'])
    col.append(income_data.at['PC Ineligible CC $35000/yr income minimum'])
    col.append(employment_data.at['Employed Full Time'])
    col.append(employment_data.at['Total Employed'])
    col.append(employment_data.at['Total Unemployed'])
    col.append(employment_data.at['PC Full Time Employed'])
    col.append(employment_data.at['PC Employed'])
    col.append(employment_data.at['PC Unemployed'])
    col.append(employment_data.at['Total'])
    new_data.append(col)


for i in range(num_age_categories):
    age = age_groups[i]
    income_employment_by_age.loc[age] = new_data[i]

#Display new dataframe
display(income_employment_by_age)

#Write out to CSV
all_data_csv = income_employment_by_age.to_csv(folder + 'Income_and_Employment_by_Age_Group.csv')
    














    
