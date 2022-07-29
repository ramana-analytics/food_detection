import psycopg2 
from Config.config import config
import pandas as pd

def FetchImageComments(image_id):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        #in this query add the timeframe for which you want to track and pass it as a variable make sure this data is fetched from dietiitians table
        
        sql= """SELECT comments FROM public."_ModelPredictedGroups"
                           WHERE image_id =  %(image_id)s;
                           """.format(image_id=image_id)
        
        # df_usersaved= pd.read_sql_query(sql_usersaved, conn, params={"image_id":image_id, "status":status})
        df_comments= pd.read_sql_query(sql, conn, params={"image_id":image_id})
        
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_comments


#this is the api part to fetch the history data of a user.

# df = FetchImageComments('1122')
# # df[‘meal_type’]= frame[‘DataFrame Column’].map(str)
# print(df)
# dict = df.iat[0,0]
# print(dict)
# print(type(dict))
# list =[]
# for i in dict:
#   list.append(dict.get(i).get('meal_type'))

# print(list)
# # str= ', '.join(list).lower()
# x = dict.get(0)
# print(x)
# # # print(df.saved_data)

# str= str.split(', ')
# print(str)
# fat_count= str.count('fat')
# vegetables_count= str.count('vegetables')
# protein_count= str.count('protein')
# grains_count= str.count('grains')
# print("fat serving-> ", fat_count)
# print("veg serving-> ",vegetables_count)
# print("protein serving-> ",protein_count)
# print("grains serving-> ",grains_count)

