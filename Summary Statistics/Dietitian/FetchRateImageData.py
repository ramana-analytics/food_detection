import psycopg2 
from Config.config import config
import pandas as pd

def FetchRateImageData():
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        
        # sql_image = """ SELECT image FROM public."_ModelPredictedGroups" WHERE image_id = %s; """
        sql_image = """ SELECT M.image, P.* FROM public."_PatientSelectedGroups" as P
                           INNER JOIN public."_ModelPredictedGroups" as M
						   ON P.patient_selected_data->>'image_id' = M.image_id::varchar(255)
                           WHERE P.rated = False
						   ORDER BY insert_ts ASC
						   LIMIT 10 """
        df_image= pd.read_sql_query(sql_image, conn)
        # print("df_image-> ",df_image)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_image


df = FetchRateImageData()

# image_byte=bytearray(image_df['image'])
# print(image_df)
print(df)

data = df['image'][0]


# data = df['image']
print(data)
bytearray = bytearray(data)
print(bytearray)
