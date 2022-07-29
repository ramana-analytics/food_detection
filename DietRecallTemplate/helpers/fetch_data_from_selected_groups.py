import psycopg2 
import pandas as pd
from Config.config import config

def FetchDataFromSelectedGroups(patient_id, start_date, end_date):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        sql_history_data = """ SELECT m.insert_ts, p.meal_type, m.image, p.patient_selected_data->>'food_name' AS food_name, m.ingredients, p.patient_selected_data->>'food_groups' AS food_groups, p.location_details

                                 FROM public."_ModelPredictedGroups" AS m JOIN public."_PatientSelectedGroups" AS p
                                   ON p.patient_selected_data->>'image_id' = m.image_id::varchar(255)
                            
                                WHERE m.patient_id = %(patient_id)s 
                                  AND m.insert_ts > TIMESTAMP %(start_date)s
                                  AND m.insert_ts <= TIMESTAMP %(end_date)s 
                           """.format(patient_id = patient_id, start_date = start_date, end_date = end_date)

        df_history_data = pd.read_sql_query(sql_history_data, conn, params={"patient_id":patient_id, "start_date":start_date, "end_date":end_date})
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    df_history_data['food_name'] = df_history_data['food_name'].str.replace('$', '')
    return df_history_data