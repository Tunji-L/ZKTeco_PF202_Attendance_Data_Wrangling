#import libraries
import numpy as np
import pandas as pd

#Recieve file name
filename = input("Enter the attendance file name: ")

#reading the attendance file to dataframe
attendance = pd.read_csv(filename)
attendance.drop(['Department','Location ID','ID Number','VerifyCode','CardNo'], axis=1, inplace=True)

#Extracting date
new = attendance["Date/Time"].str.split(" ", n = 1, expand = True)
attendance['Date'] = new[0]
attendance.drop('Date/Time', axis=1, inplace = True)

#Removing Sundays for the night shift
attendance['Date'] = attendance['Date'].str.replace('2-28-2021','3-1-2021')
attendance['Date'] = attendance['Date'].str.replace('3-7-2021','3-8-2021')
attendance['Date'] = attendance['Date'].str.replace('3-14-2021','3-15-2021')
attendance['Date'] = attendance['Date'].str.replace('3-21-2021','3-22-2021')

attendance.drop_duplicates("Date")
# confirming the number of days generated
print(f"The number of work days is {attendance['Date'].nunique()}")

# Formating the column names(Date)
col = ['2-26-2021', '2-27-2021', '3-1-2021','3-2-2021','3-3-2021', '3-4-2021',
       '3-5-2021', '3-6-2021', '3-8-2021', '3-9-2021', '3-10-2021', '3-11-2021',
       '3-12-2021', '3-13-2021', '3-15-2021', '3-16-2021', '3-17-2021',
       '3-18-2021', '3-19-2021', '3-20-2021', '3-22-2021',
       '3-23-2021', '3-24-2021', '3-25-2021']

#Assigning present for all staff through the month
attendance[col] = 1

# Getting the formatted table
month = attendance.drop(['No.', 'Date'],axis = 1)
month.drop_duplicates(inplace=True)
month.reset_index(drop=True, inplace=True)

# Getting the number of staff
print(f"The total number of staff on the list is {len(month)}")

#Getting an empty columns
record = attendance.drop(list(range(len(attendance))))

# Appending record
k = 0
staff = attendance.loc[attendance['Name'] == month['Name'][k]]
while k < len(month):
    staff = attendance.loc[attendance['Name'] == month.loc[k,'Name']]

    for i in col:
        if i not in list(staff['Date']):
            month.loc[k,i]=0
        else:
            month.loc[k,i]=1
    k += 1

# Giving the sum of present and absent
month["Present"] = month.sum(axis = 1)
month["Absent"] = (attendance['Date'].nunique()) - (month["Present"])

#Saving to CSV
month.to_csv("March.csv")




