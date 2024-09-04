import pandas as pd
import os
import matplotlib.pyplot as plt
 
#
# Ví dụ về 1 filepath
#
path = '/Users/duclun/Desktop/stupy/salesreport/'
data = pd.read_csv(path + 'sales2019_1.csv')
print(data)

#
# Merge file
#
filepaths = []
frame = []
length = []
for file in os.listdir(path):
    if file.endswith('.csv'):
    # Gộp các file lại thành 1 
        filepath = path + file  # filepath = path + data (ở trên)
        df = pd.read_csv(filepath)
        frame.append(df)
        result = pd.concat(frame)
    # Check số row của file
        fileLength = len(df.index)
        length.append(fileLength)
#        
# Output        
#
print(result)
print(sum(length))
result.to_csv('sales2019.csv', index = False)

mergeData = pd.read_csv('sales2019.csv')
mergeData['Month'] = mergeData['Order Date'].str[0:2]

#
# Clean Data
#
mergeData = mergeData.dropna()
mergeData = mergeData[mergeData['Month'] != 'Or']

mergeData['Price Each'] = pd.to_numeric(mergeData['Price Each'], downcast='float')
mergeData['Quantity Ordered'] = pd.to_numeric(mergeData['Quantity Ordered'], downcast='float')
print(mergeData['Quantity Ordered'].dtypes)

#
# Doanh thu từng row 
#
mergeData['Sales'] = mergeData['Price Each'] * mergeData['Quantity Ordered']
print(mergeData)

#
# 1.1.Top Sales theo tháng
#
totalSales = mergeData.groupby('Month').sum('Sales')
print(totalSales)

#months = range(1,13)
#plt.bar(x=months, height=totalSales)
#plt.show()

#
# 1.2. Top Sales theo Thành phố 
#

getCity = lambda city:city.split(',')[1]
mergeData['City'] = mergeData['Purchase Address'].apply(getCity)

citySales = mergeData.groupby('City').sum()['Sales']
print(citySales)
City = ['Atlanta', 'Austin', 'Boston', 'Dallas', 'Los Angeles', 'New York City', 'Portland', 'San Francisco', 'Seattle']

#plt.bar(x=City,height=citySales)
#plt.xticks(City, rotation = 45)
#plt.show()

#
# 1.3. Khoảng thời gian nên chọn để quảng cáo
# 
mergeData['Time'] = mergeData['Order Date'].str[9:11]
print(mergeData['Time'])
saleTime = mergeData.groupby('Time').count()['Sales']
print(saleTime)
hours = range(0,24)
#plt.plot(hours, saleTime)
#plt.show()


#
# 1.4. Sản phẩm nào được bán cùng nhau
#
duplicateData =  mergeData[mergeData['Order ID'].duplicated(keep = False)]
print(duplicateData)