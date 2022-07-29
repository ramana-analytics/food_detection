import psycopg2 
from Config.config import config
import pandas as pd

def fetch_image(image_id):
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        
        # sql_image = """ SELECT image FROM public."_ModelPredictedGroups" WHERE image_id = %s; """
        sql_image = """ SELECT image FROM public."_ModelPredictedGroups" WHERE image_id=""" + image_id + ";"
        df_image= pd.read_sql_query(sql_image, conn)
        # print("df_image-> ",df_image)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_image


# print(fetch_image('1000'))