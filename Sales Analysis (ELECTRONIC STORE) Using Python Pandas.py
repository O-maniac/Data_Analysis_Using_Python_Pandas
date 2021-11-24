#!/usr/bin/env python
# coding: utf-8

# # Sales Analysis

# We will go on a journey from:
# 1. Currating the data
# 2. Asking Business Question
# 3. Analysing the questions using the curated Datasets

# #### IMPORT NECESSARY LIBRARIES
# #### TO ADD AND UPLOAD DATASET
# #### MERGE DATASETS INTO 1 CSV FILE

# 1. import necessary libraries

# In[1]:


import pandas as pd
import os 
import matplotlib.pyplot as plt


# 2. Merge the Datasets (12 months of datasets together)

# In[2]:


## To load 1month of dataset on the notebook
df = pd.read_csv("./Sales_Data/Sales_April_2019.csv")
df.head()


# 2.B. Merge the months of sales data into a single file

# In[3]:


files = [file for file in os.listdir('./Sales_Data')]

for file in files:
    print(file)


# 3. To Concatenate all the datasets into a single dataframe

# In[4]:


files = [file for file in os.listdir('./Sales_Data')]

all_months_data = pd.DataFrame()

for file in files:
    df = pd.read_csv("./Sales_Data/"+file)
    all_months_data = pd.concat([all_months_data, df])
    
    all_months_data.to_csv("all_data.csv", index=False)


# 4. To Read Updated DataFrame

# In[5]:


all_data = pd.read_csv("all_data.csv")
all_data.head()


# ### To Clean Up The Data 
# 
# ###### i.e Drop The Nan rows

# To indentify rows with NAN

# In[6]:


nan_df = all_data[all_data.isna().any(axis=1)]
nan_df.head()


# To Drop NAN rows

# In[7]:


all_data = all_data.dropna(how='all')
all_data.head()


# In[8]:


all_data.head()


# 
# # To Add Month Column

# In[9]:


all_data['Month'] = 4
all_data.head()


# In[10]:


all_data['Month'] = all_data['Order Date'].str[0:2]
all_data.head()


# In[11]:


all_data = all_data.dropna(how='all')
all_data.head()


# To find or delete OR

# In[12]:


all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']


# In[13]:


all_data['Month'] = all_data['Order Date'].str[0:2] 
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# # To Add Sales Column

# To Convert Columns To Correct Type

# In[14]:


## to make int. 
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered']) 
## to make float
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])
all_data.head()


# To Add Sales Column

# In[15]:


all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
all_data.head()


# In[ ]:





# ###### LET'S GET INTO PROPER ANALYSIS

# FINDING 1 -  what was the BEST MONTHS for SALES and by HOW MUCH 

# In[16]:


all_data.groupby('Month').sum()


# To Plot This on The Chart

# In[38]:


result = all_data.groupby('Month').sum()


# In[39]:


Month = range(1,13)
plt.bar(Month, result['Sales'])
plt.show()


# In[40]:


Months = range(1,13)
plt.bar(Month, result['Sales'])
plt.xticks(Months)
plt.ylabel('Sales In (USD $)')
plt.xlabel('Month In Number')
plt.grid()
plt.show()


# #### DEDUCTION: The best Months of sales are October and December

# FINDING 2 - WHAT CITY HAS THE HIGHEST NUMBER OF SALES

# ADD A CITY COLUMN

# In[25]:


all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
all_data.head()


# By imploring .apply() to get the city column

# In[41]:


def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

all_data['city'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")
all_data.head()


# In[42]:


all_data.groupby('city').sum()


# In[44]:


import matplotlib.pyplot as plt

cities = [city for city, df in all_data.groupby(['city'])]

plt.bar(cities,all_data.groupby(['city']).sum()['Sales'])
plt.ylabel('Sales in USD ($)')
plt.xlabel('City')
plt.xticks(cities, rotation='vertical', size=8)
plt.grid()
plt.show()


# #### DEDUCTION: San Francisco (CA) has the highest number of sales

# FINDING 3: AT WHAT TIME SHOULD THE COMPANY DISPLAY ADVERTS TO MAXIMIZE THE PUBLIC ATTENTION TO BUYING OUR PRODUCTS

# In[45]:


all_data.head()


# converting the "Order Date" into day/time object 

# In[46]:


all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])


# In[47]:


all_data.head()


# We need the Hour Column to get the time to push our advert to maximize reach

# In[48]:


all_data['Hour'] = all_data['Order Date'].dt.hour
all_data.head()


# we will add the minute column also 

# In[49]:


all_data['minute'] = all_data['Order Date'].dt.minute
all_data.head()


# In[50]:


hours = [hour for hour, df in all_data.groupby(['Hour'])]
plt.plot(hours, all_data.groupby(['Hour']).count())
all_data.groupby(['Hour']).count()
plt.ylabel('NO of Orders')
plt.xlabel('Time (Hrs)')
plt.xticks(hours)
plt.grid()
plt.show()


# ##### Deduction:
#     Peak Orders are around 1200hrs and 1900hrs, respectively
# ##### Sugestion: 
# It is advice that Ads should be pushed betwwen 1100hrs to 1200hrs, and also between 1900hrs

# FINDINGS 4: WHAT PRODUCTS ARE MOSTLY SOLD TOGETHER

# In[51]:


all_data.head()


# Same ORDER ID indicates that the ORDERS were made from the same ADDRESS. 

# ###### Identifying the SPOTS in the DATAFRAME that has DUPLICATE ROWS 
# ###### I.E DUPLICATE ORDER ID means PRODUCTS WERE ORDERED TOGETHER 

# In[52]:


df = all_data[all_data['Order ID'].duplicated(keep=False)]
df.head(10)


# ##### Now to group the same ORDER ID together

# In[53]:


df ['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df.head(50)


# To get rids of duplicate

# In[54]:


df = df[['Order ID', 'Grouped']].drop_duplicates()
df.head(10)


# To Iterates over all the rows and count the pairs

# In[55]:


## first we need to import few libraries 
from itertools import combinations
from collections import Counter

count = Counter()

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))
    
for key, value in count.most_common(10):
    print(key, value)


# DEDUCTIONS:
#     The Products Ordered together can used as push for smart deals

# FINDING 4: THE MOST SOLD PRODUCTS AND WHY

# In[60]:


all_data.head()


# In[63]:


product_group = all_data.groupby('Product')

quantity_ordered = product_group.sum()['Quantity Ordered']


# To plot this on a bar chart

# In[65]:


products = [product for product, df in product_group]

plt.bar(products, quantity_ordered)

plt.ylabel('Quantity Ordered')
plt.xlabel('Products')
plt.xticks(products, rotation='vertical', size=8)
plt.show()


# DEDUCTIONS: The cheaper products are ordered the most

# Now, let's overlay the above graph showing the products ordered and their actual prices
# 
# But first, lets show the products against their coreesponding prices

# In[66]:


prices = all_data.groupby('Product').mean()['Price Each']

print(prices)


# Overly Products ordered against price

# In[67]:


prices = all_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color='y')
ax2.plot(products, prices, 'g-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quanity Ordered', color='y')
ax2.set_ylabel('Price($)', color='r')
ax1.set_xticklabels(products, rotation='vertical', size=10)

plt.show()


# OBSERVATION: whenever the QUANTITY ORDERED is HIGH, the PRICE is LOW (E.G AA BATTERIES,)
#              whenever the QUANTITY ORDERED is LOW, the PRICE is HIGH (e.g LG DRYER, LG WASHING MACHINE)
# IN EXCEPTIONAL CASES: PRODUCTS LIKE MACBOOK PRO LAPTOP, THINKPAD LAPTOP (due to neccessity and preference)
#     
# DEDUCTIONS: The cheaper products are ordered the most

# # THE END.............

# In[ ]:




