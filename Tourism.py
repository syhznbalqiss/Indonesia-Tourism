import pandas as pd

data1 = pd.read_csv(r'D:\\balqis\\Data Analytics\\Indonesia Tourism\\tourism_with_id.csv', on_bad_lines='skip', sep=';', encoding= 'cp775')
data2 = pd.read_csv(r'D:\\balqis\\Data Analytics\\Indonesia Tourism\\tourism_rating.csv', on_bad_lines='skip', sep=';', encoding= 'cp775')

#DATA1 CLEANING
print(data1)
print('Rows: ', len(data1))

#search for missing values
full_range = set(range(data1['Place_Id'].min(), data1['Place_Id'].max()+1))
existing_range = set(data1['Place_Id']) 
missing_values = sorted(full_range - existing_range)
print("Missing place_id: ", missing_values)

#no info about the places that has missing values, 
#so theres no way to fill out those missing data

#search for duplicates
duplicates = data1[data1.duplicated()]
print("Duplicate rows: ", duplicates)

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

#drop irrelevant columns
data2 = data2.drop(['Place_Ratings'], axis=1)
print(data2)

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
print("Most popular tourism in Yogyakarta\n", cat_counts)

#combine tables
result = pd.merge(data1, data2, how='outer', on='Place_Id')
print(result)

visit_counts = result['Place_Name'].value_counts().reset_index()
visit_counts.columns = ['Place_Name', 'Visit_Count']

# Merge to get Place_ID
visit_freq = result[['Place_Id', 'Place_Name']].drop_duplicates().merge(visit_counts, on='Place_Name')

#most
print("Place with the most visits\n", visit_freq.nlargest(5, 'Visit_Count'))
#least
print("Place with the least visits\n", visit_freq.nsmallest(5, 'Visit_Count'))

