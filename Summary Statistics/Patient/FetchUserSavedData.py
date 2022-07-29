import psycopg2 
from Config.config import config
import pandas as pd

def FetchUserSavedData(userId,status):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        #in this query add the timeframe for which you want to track and pass it as a variable make sure this data is fetched from dietiitians table
        sql_usersaved = """SELECT * FROM usersavedTest 
                           WHERE saved_data->>'userId' =  %(userId)s
                           AND saved_data->>'status'= %(status)s """.format(userId=userId, status=status)
        df_usersaved= pd.read_sql_query(sql_usersaved, conn, params={"userId":userId, "status":status})
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_usersaved


#this is the api part to fetch the history data of a user.

df = FetchUserSavedData('0001', 'rated')

dict = df.saved_data.to_dict()
# # print(dict)
list =[]
for i in dict:
  list.append(dict.get(i).get('foodGroups'))

str= ', '.join(list).lower()
# x = dict.get(0).get('status')
# print(x)
# print(df.saved_data)

str= str.split(', ')
print(str)
fat_count= str.count('fat')
vegetables_count= str.count('vegetables')
protein_count= str.count('protein')
grains_count= str.count('grains')
print("fat serving-> ", fat_count)
print("veg serving-> ",vegetables_count)
print("protein serving-> ",protein_count)
print("grains serving-> ",grains_count)


