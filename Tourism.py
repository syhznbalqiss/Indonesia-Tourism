import pandas as pd

data1 = pd.read_csv(r'D:\\balqis\\Data Analytics\\Indonesia Tourism\\tourism_with_id.csv', on_bad_lines='skip', sep=';', encoding= 'cp775')
data2 = pd.read_csv(r'D:\\balqis\\Data Analytics\\Indonesia Tourism\\tourism_rating.csv', on_bad_lines='skip', sep=';', encoding= 'cp775')
data3 = pd.read_csv(r'D:\\balqis\\Data Analytics\\Indonesia Tourism\\user.csv', on_bad_lines='skip', sep=';', encoding= 'cp775')

#DATA1 CLEANING
print(data1)
print('Rows: ', len(data1))

#search for missing values
full_range = set(range(data1['Place_Id'].min(), data1['Place_Id'].max()+1))
existing_range = set(data1['Place_Id']) 
missing_values = sorted(full_range - existing_range)
print("Missing place_id: ", missing_values)
del_value = set(missing_values)
del_value = [x for x in del_value if x not in missing_values]
#no info about the place_id that has missing values, 
#so theres no way to fill out those missing data

#count total place
tourism_total = data1['Place_Name'].count()
print('Total tourism places: ', tourism_total)

#search for duplicates
duplicates = data1[data1.duplicated()]
print("Duplicate rows: ", duplicates)

#checking data type
print(data1.dtypes) 

#drop irrelevant columns
data1 = data1.drop(['Coordinate', 'Lat', 'Long', 'Description'], axis=1)
print(data1)

#DATA2 CLEANING
print(data2)
print('Rows: ', len(data2))

#search for missing values
full_range = set(range(data2['User_Id'].min(), data2['User_Id'].max()+1))
existing_range = set(data2['User_Id']) 
missing_values = sorted(full_range - existing_range)
print("Missing place_id: ", missing_values)

#search and remove duplicates
all_duplicates = data2[data2.duplicated(keep=False)]
print("Duplicate rows: ", all_duplicates)
duplicates = data2[data2.duplicated()]
no_duplicates = data2.drop_duplicates()
print("Without duplicates: \n", no_duplicates)

#checking data type
print(data2.dtypes)

#drop irrelevant columns
data2 = data2.drop(['Place_Ratings'], axis=1)
print(data2)

#DATA3 CLEANING
print(data3)
#search for missing values
full_range = set(range(data3['User_Id'].min(), data3['User_Id'].max()+1))
existing_range = set(data3['User_Id']) 
missing_values = sorted(full_range - existing_range)
print("Missing place_id: ", missing_values)

#search for duplicates
all_duplicates = data3[data3.duplicated(keep=False)]
print("Duplicate rows: ", all_duplicates)

#total users
print("Total users: ", data3.User_Id.count())

#checking data type
print(data3.dtypes)

#DATA MANIPULATION 
#sorting highest ratings
sorted_data1 = data1.sort_values(by='Rating', ascending=False)
print(sorted_data1.head())

#sorting lowest ratings
sorted_data1 = data1.sort_values(by='Rating', ascending=True)
print(sorted_data1.head())

#most category
most_category = data1['Category'].value_counts()
print("Most category\n", most_category.head())

#cities with the most tourism place
city_tourism = data1['City'].value_counts()
print("City with the most tourism\n", city_tourism)

#most popular tourism in Yogyakarta
city_tourism_cat = data1[data1['City'] == 'Yogyakarta']
cat_counts = city_tourism_cat['Category'].value_counts()
cat_price = city_tourism_cat.groupby('Category')['Price'].mean().reset_index()
print("Most popular tourism in Yogyakarta\n", cat_counts, cat_price)

#combine tables
data1n2 = pd.merge(data1, data2, how='outer', on='Place_Id')
print(data1n2)

#counts visit per category
visit_counts = data1n2['Place_Name'].value_counts().reset_index()
visit_counts.columns = ['Place_Name', 'Visit_Count']
#Merge to get Place_ID
visit_freq = data1n2[['Place_Id', 'Place_Name', 'Price']].drop_duplicates().merge(visit_counts, on='Place_Name')
#most
print("Place with the most visits\n", visit_freq.nlargest(5, 'Visit_Count'))
#least
print("Place with the least visits\n", visit_freq.nsmallest(5, 'Visit_Count'))

#average age
age_avg = data3.Age.mean()
print("Average age: ", age_avg)
#oldest
oldest = data3.Age.max()
print("Oldest user: ", oldest)
#youngest
youngest = data3.Age.min()
print("Youngest user: ", youngest)

#combine tables
alldata = pd.merge(data3, data1n2, how='outer', on='User_Id')

#common category for the older
spec_user_old = data3[data3['Age'] >=35]
filtered_places = alldata[alldata['User_Id'].isin(spec_user_old['User_Id'])]
print(filtered_places[['User_Id', 'Category']])
print("Top category for the older gen: ", filtered_places[['Category']].mode())
#common category for the younger
spec_user_young = data3[data3['Age'] <25]
filtered_places = alldata[alldata['User_Id'].isin(spec_user_young['User_Id'])]
print(filtered_places[['User_Id', 'Category']])
print("Top category for the younger gen: ", filtered_places[['Category']].mode())
#common category for the mid
spec_user_mid = data3[(data3['Age'] >25) & (data3['Age'] <=40)]
filtered_places = alldata[alldata['User_Id'].isin(spec_user_mid['User_Id'])]
print(filtered_places[['User_Id', 'Category']])
print("Top category for the middle gen: ", filtered_places[['Category']].mode())

#City preferences for older generation (age >= 35)
spec_user_old = data3[data3['Age'] >= 35] 
filtered_places_old = alldata[(alldata['User_Id'].isin(spec_user_old['User_Id']))]
print("Older Generation Users and Cities:\n", filtered_places_old[['User_Id', 'City']])
print("City older gen prefer: ", filtered_places_old[['City']].mode())
# City preferences for younger generation (age < 25)
spec_user_young = data3[data3['Age'] < 25]
filtered_places_young = alldata[alldata['User_Id'].isin(spec_user_young['User_Id'])]
print("Younger Generation Users and Cities:\n", filtered_places_young[['User_Id', 'City']])
print("City younger gen prefer: ", filtered_places_young[['City']].mode())
# City preferences for middle generation (age between 25 and 40)
spec_user_mid = data3[(data3['Age'] > 25) & (data3['Age'] <= 40)]
filtered_places_mid = alldata[alldata['User_Id'].isin(spec_user_mid['User_Id'])]
print("Middle Generation Users and Cities:\n", filtered_places_mid[['User_Id', 'City']])
print("City middle gen prefer: ", filtered_places_mid[['City']].mode())