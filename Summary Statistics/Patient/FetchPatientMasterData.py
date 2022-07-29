import psycopg2 
from Config.config import config
import pandas as pd

def GetAllPatientsData():
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        
        sql_patient_data = 'SELECT * from public."_PatientData"'
        print(sql_patient_data)
        df_patient_data= pd.read_sql_query(sql_patient_data, conn)

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_patient_data

def GetPatientDataById(patient_id):
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        
        sql_patient_data = """SELECT * from public."_PatientData" where patient_id =""" + patient_id
        print(sql_patient_data)
        df_patient_data= pd.read_sql_query(sql_patient_data, conn)

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_patient_data

def  InsertPatientsData(patient_id,patient_name,dietitian_id):
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        
        sql_patient_data = """INSERT INTO public."_PatientData"(patient_id, patient_name, dietitian_id)
        VALUES (%s,%s,%s);"""
        print(sql_patient_data)
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql_patient_data, (patient_id,patient_name,dietitian_id))

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_patient_data


#df = GetAllPatientsData()
#print(df)