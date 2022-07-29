import psycopg2 
from Config.config import config
import pandas as pd

def GetAllDietitianData():
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        
        sql_dietitian_data = 'SELECT * from public."_DietitianData"'
        df_dietitian_data= pd.read_sql_query(sql_dietitian_data, conn)

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_dietitian_data

def GetDietitianDataById(dietitian_id):
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        
        sql_dietitian_data = """SELECT * from public."_DietitianData" where dietitian_id =""" + dietitian_id
        
        df_dietitian_data= pd.read_sql_query(sql_dietitian_data, conn)

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_dietitian_data


def  InsertDietitianData(dietitian_id,dietitian_name):
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        
        sql_patient_data = """INSERT INTO public."_DietitianData"( dietitian_id, dietitian_name)
        VALUES (%s,%s);"""
        print(sql_patient_data)
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql_patient_data, (dietitian_id,dietitian_name))

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_patient_data


#df = GetDietitianDataById("11")
#print(df)