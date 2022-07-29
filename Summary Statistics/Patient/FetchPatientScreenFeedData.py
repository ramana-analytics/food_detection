import psycopg2 
from Config.config import config
import pandas as pd


def FetchPatientScreenFeed(patient_id):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        #in this query add the timeframe for which you want to track and pass it as a variable make sure this data is fetched from dietiitians table
        sql_usersaved = """SELECT DD.dietitian_name, D.dietitian_id, M.image, P.patient_id, P.meal_type, P.patient_selected_data, 
jsonb_build_object('dietitian_id',DD.dietitian_id, 'image_id', D.dietitian_selected_data->>'image_id','food_name', D.dietitian_selected_data->>'food_name','food_groups', D.dietitian_selected_data->>'food_groups') as dietitian_selected_data, P.insert_ts,
jsonb_array_length(M.comments) as comment_count,P.location_details
 FROM public."_PatientSelectedGroups" as P
                           LEFT JOIN public."_DietitianSelectedGroups" as D
						   ON P.patient_selected_data->>'image_id' = D.dietitian_selected_data->>'image_id'
                           LEFT JOIN public."_DietitianData" as DD
						   ON DD.dietitian_id = D.dietitian_id
						   Inner JOIN public."_ModelPredictedGroups" as M
						   ON P.patient_selected_data->>'image_id' = cast( M.image_id as varchar(255))
                           WHERE P.patient_id= """ + patient_id +"""
						   ORDER BY P.insert_ts desc"""
        print(sql_usersaved)
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

#df = FetchPatientScreenFeed("151")

#print(df)