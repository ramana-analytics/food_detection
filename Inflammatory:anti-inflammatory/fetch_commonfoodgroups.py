import psycopg2 
from Config.config import config
import pandas as pd
def fetch_commonfoodgroups():
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        
        sql_foodgrouptest = """ SELECT * FROM public."_CommonFoodGroups"; """

        df_foodgroups= pd.read_sql_query(sql_foodgrouptest, conn)
        # print("df-> ",df_foodgroups)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_foodgroups

# print(fetch_commonfoodgroups())