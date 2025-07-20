import pandas as pd
import os
import matplotlib.pyplot as plt
# Step 1: Path to your folder
base = r'C:\Users\kapil\Downloads\SalesData (3) (2)\SalesData'

# Step 2: List all files inside the folder
files = os.listdir(base)
print("📂 Files found:", files)

# Step 3: Empty DataFrame to store all data
all_data = pd.DataFrame()

# Step 4: Loop through each file and merge
for file in files:
    if file.endswith('.csv'):  # only merge CSV files
        file_path = os.path.join(base, file)  # full path of file
        df = pd.read_csv(file_path)  # read CSV
        all_data = pd.concat([all_data, df], ignore_index=True)  # add to main data

# Step 5: Save the merged data
all_data.to_csv('merged_sales_data.csv', index=False)

print("✅ Merged successfully! File saved as 'merged_sales_data.csv'")

# Reload merged data
all_data = pd.read_csv('merged_sales_data.csv')

# Print full data, null rows, and column names
print(all_data)
print(all_data[all_data.isnull().any(axis=1)])
print(all_data.columns)

# 🚫 Remove bad header rows (e.g. 'Order Date' in data)
temp = all_data.loc[all_data['Order Date'] == 'Order Date']
print(temp)
all_data = all_data.loc[all_data['Order Date'] != 'Order Date']
print(all_data)

# ✅ FIX: Don't specify format, let pandas detect the correct date format
all_data['Order Date'] = all_data['Order Date'].str.replace('/','-')
print(all_data['Order Date'])
# all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
# print(all_data)
all_data['Order Date'] = pd.to_datetime(all_data['Order Date'], format='%m-%d-%y %H:%M', errors='coerce')
print(all_data['Order Date'])
all_data = all_data.dropna(subset=['Order Date'])
print(all_data)
all_data['Month']=all_data['Order Date'].dt.month_name()
print(all_data['Month'])
all_data['Quantity Ordered']=all_data['Quantity Ordered'].astype('float')
all_data['Price Each']=all_data['Price Each'].astype('float')
all_data['cal']=all_data['Quantity Ordered']*all_data['Price Each']
print(all_data.head())
monthly_sale=all_data.groupby('Month')['cal'].sum()
print(monthly_sale)

months=range(1,13)
plt.bar(months,monthly_sale)
plt.xticks(months)
plt.xlabel('Month')
plt.ylabel('Sales')
plt.show()

all_data['City'] = all_data['Purchase Address'].str.split(',',expand=True)[1]
print(all_data)
new=all_data.groupby('City')['Quantity Ordered'].sum().sort_values()
print(new)
plt.bar(new.index, new.values)
plt.xlabel('City')
plt.ylabel('Total Quantity Ordered')
plt.title('Quantity Ordered per City')
plt.xticks(rotation='vertical', fontsize=8)
plt.tight_layout()
plt.show()


