import psycopg2 
from Config.config import config
import pandas as pd
import json

def FetchAssignedPatients(dietitian_id):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        #in this query add the timeframe for which you want to track and pass it as a variable make sure this data is fetched from dietiitians table
        sql_assigned_patients = """SELECT P.patient_id, P.patient_name FROM public."_PatientData" as P
                           INNER JOIN public."_DietitianData" as D
						   ON P.dietitian_id = D.dietitian_id
                           WHERE D.dietitian_id = %(dietitian_id)s """.format(dietitian_id=dietitian_id)
        df_assigned_patients= pd.read_sql_query(sql_assigned_patients, conn, params={"dietitian_id":dietitian_id})
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_assigned_patients


#this is the api part to fetch the history data of a user.

# df = FetchAssignedPatients('22')

# dict = df['patient_id'].to_dict()
# print(dict)
# list =[]
# for i in dict:
#   list.append(dict.get(i))
# print(list)

# s = ""
# for i in list: 
#         s += str(i) + ',' 
# print(s)


# str= ''.join(str(df.iat[1,0]))
# print(str)

# str= ''.join(str(list))
# print(str)

# str= ', '.join(list).lower()
# # x = dict.get(0).get('status')
# # print(x)
# # print(df.saved_data)

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


