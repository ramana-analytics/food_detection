import psycopg2 
from Config.config import config
import pandas as pd

#add functionality in get rate api so that other dietitians can rate a patients uploaded image, one image can have multiple ratings from different dietitians
def FetchAllPatientFeedData(dietitian_id):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        #in this query add the timeframe for which you want to track and pass it as a variable make sure this data is fetched from dietiitians table
        sql_usersaved = """SELECT M.image, P.*, PD.patient_name  FROM public."_PatientSelectedGroups" as P
                           INNER JOIN public."_ModelPredictedGroups" as M
						   ON P.patient_selected_data->>'image_id' = M.image_id::varchar(255)
						   Inner Join public."_PatientData" as PD
						   ON P.patient_id = PD.patient_id
						   Where P.patient_selected_data->>'image_id' NOT in(
						   Select D.dietitian_selected_data->>'image_id' from  public."_DietitianSelectedGroups" as D
						   Where dietitian_id = '""" +dietitian_id + """')"""
        df_usersaved= pd.read_sql_query(sql_usersaved, conn)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_usersaved


#this is the api part to fetch the history data of a user.
# list=[1082]

#df = FetchAllPatientFeedData('9')
#print(df)
# dict = df.saved_data.to_dict()
#print(df)
# list =[]
# for i in dict:
#   list.append(dict.get(i).get('foodGroups'))

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


