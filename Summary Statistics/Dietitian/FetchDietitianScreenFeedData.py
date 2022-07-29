import psycopg2 
from Config.config import config
import pandas as pd


def FetchDietitianScreenFeedData():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        #in this query add the timeframe for which you want to track and pass it as a variable make sure this data is fetched from dietiitians table
#         sql_usersaved = """SELECT PD.patient_name, M.image, P.* FROM public."_PatientSelectedGroups" as P
#                            INNER JOIN public."_ModelPredictedGroups" as M
# 						   ON P.patient_selected_data->>'image_id' = M.image_id::varchar(255) 
#                            INNER JOIN public."_PatientData" as PD
# 						   ON P.patient_id = PD.patient_id
#                            WHERE P.patient_id in """ + patient_id + """
#                            --AND rated = False
#                            ORDER BY insert_ts ASC""".format(patient_id=patient_id)
        sql_usersaved = """SELECT DD.dietitian_name, D.dietitian_id, M.image, P.patient_id, PD.patient_name, P.rated, P.meal_type, P.patient_selected_data, 
jsonb_build_object('dietitian_id',DD.dietitian_id, 'image_id', D.dietitian_selected_data->>'image_id','food_name', D.dietitian_selected_data->>'food_name','food_groups', D.dietitian_selected_data->>'food_groups') as dietitian_selected_data, P.insert_ts,
jsonb_array_length(M.comments) as comment_count,P.location_details
 FROM public."_PatientSelectedGroups" as P
                           LEFT JOIN public."_DietitianSelectedGroups" as D
						   ON P.patient_selected_data->>'image_id' = D.dietitian_selected_data->>'image_id'
                           Left JOIN public."_DietitianData" as DD
						   ON DD.dietitian_id = D.dietitian_id
						   INNER JOIN public."_ModelPredictedGroups" as M
						   ON P.patient_selected_data->>'image_id' = cast( M.image_id as varchar(255))  
						   LEFT JOIN public."_PatientData" as PD
						   ON P.patient_id = PD.patient_id
						   ORDER BY P.insert_ts desc"""
        df_usersaved= pd.read_sql_query(sql_usersaved, conn)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_usersaved


#this is the api part to fetch the history data of a user.
#list=[1082]

#df = FetchDietitianScreenFeedData()

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


