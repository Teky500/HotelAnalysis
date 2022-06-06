import csv
import datetime
import pandas as pd
import seaborn as sns
import fitz
import datetime
import matplotlib.pyplot as plt
import matplotlib
from dateutil import parser


# Open transactions CSV file, and make a new one with an easier to utilize format.

with open("transactions.csv",'r') as f:
    with open("transactionsfixed.csv",'w') as f1:
        next(f) # skip header line
        for line in f:
            f1.write(line)
file = open('transactionsfixed.csv')
csv = csv.reader(file)

# Append all lines in the CSV file to LineList.

LineList = []
for i in csv:
    LineList.append(i)
FixedLineList = []

# Final entry in every list is just empty quotes, so remove that.

for i in range(len(LineList)):
    x = LineList[i]
    del x[len(x)-1]
    FixedLineList.append(x)

# Get Headers for the table, and remove them from the list.

headers = FixedLineList[0]
del FixedLineList[0]

# Initialize all list variables. Will be later used to form the table.

Date = []
AcctN = []
Merchant = []
Debit = []
Credit = []
Weekday = []
Month = []
DataDict = {}
for i in FixedLineList:
    TheDate = parser.parse(i[0])
    Date.append(TheDate)
    AcctN.append(i[1])
    Merchant.append(i[2])
    Debit.append(float(i[3]))
    Credit.append(i[4])

    Weekday.append(TheDate.weekday())
    Month.append(TheDate.month)

# Parsed weekdays/months come out in a format from 0-6 and 1-12 respectively. Adjust these to strings.

for i in range(len(Weekday)):
    if Weekday[i] == 0:
        Weekday[i] = 'Monday'
    if Weekday[i] == 1:
        Weekday[i] = 'Tuesday'
    if Weekday[i] == 2:
        Weekday[i] = 'Wednesday'
    if Weekday[i] == 3:
        Weekday[i] = 'Thursday'
    if Weekday[i] == 4:
        Weekday[i] = 'Friday'
    if Weekday[i] == 5:
        Weekday[i] = 'Saturday'
    if Weekday[i] == 6:
        Weekday[i] = 'Sunday'
for i in range(len(Month)):
    if Month[i] == 5:
        Month[i] = 'May'
    if Month[i] == 6:
        Month[i] = 'June'
    if Month[i] == 7:
        Month[i] = 'July'
    if Month[i] == 8:
        Month[i] = 'August'

# Utilize a dictionary to use with DataFrame later.

DataDict['Date'] = Date
DataDict['AcctN'] = AcctN
DataDict['Merchant'] = Merchant
DataDict['Debit'] = Debit
DataDict['Credit'] = Credit
DataDict['Weekday'] = Weekday
DataDict['Month'] = Month
DataNeeded = pd.DataFrame(DataDict)

# Filter Data according to whatever is needed.
# Direct Bill and Cash payments are usually outliers (noted from looking at historical data), so they're filtered out in the main analysis.


DataFilter = DataNeeded[(DataNeeded['Merchant'] != 'Direct Bill') & (DataNeeded['Merchant'] != 'Cash')]
DataFilter2 = DataFilter.groupby(['Date', 'Merchant']).sum(['Debit'])
DataFilter3 = DataFilter.groupby(['Date']).sum(['Debit'])
DataFilter4 = DataFilter.groupby(['Month']).sum(['Debit'])
print(DataFilter)
print(DataFilter2)
print('Total: ' + str(DataFilter3['Debit'].sum()))
print(DataFilter4)

sns.set_style('white')
sns.set_context('paper', font_scale = 1.5)
sns.set_color_codes("pastel")
ax = sns.countplot(x='Weekday', data=DataFilter, hue = 'Month')
ax.set(xlabel='Weekday', ylabel='Transactions')
plt.show()
ax2 = sns.barplot(data = DataFilter, x = 'Merchant', y = 'Debit', hue='Weekday')
ax2.set(xlabel='Merchant', ylabel='Debit')
plt.show()

# This last plot is usually only useful on cumulative basis. It is not very valuable on specific sections.

ax3 = sns.lineplot(data = DataFilter3, x = 'Date', y = 'Debit')
plt.show()
