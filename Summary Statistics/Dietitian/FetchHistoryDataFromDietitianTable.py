import psycopg2 
from Config.config import config
import pandas as pd
import json

def FetchHistoryData(patient_id, dietitian_id, start_date, end_date):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        #in this query add the timeframe for which you want to track and pass it as a variable make sure this data is fetched from dietiitians table
        sql_history_data = """SELECT * FROM public."_DietitianSelectedGroups" 
                           WHERE dietitian_selected_data->>'patient_id' =  %(patient_id)s
                           --AND meal_type = %(meal_type)s
                           AND dietitian_id = %(dietitian_id)s
                           AND insert_ts > %(start_date)s
                           AND insert_ts < %(end_date)s """.format(patient_id=patient_id, dietitian_id=dietitian_id, start_date=start_date,end_date=end_date)
        df_history_data= pd.read_sql_query(sql_history_data, conn, params={"patient_id":patient_id, "dietitian_id":dietitian_id,"start_date":start_date,"end_date":end_date})
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_history_data


#this is the api part to fetch the history data of a user.
# FetchHistoryData(patient_id, meal_type, dietitian_id, start_date, end_date):
# df = FetchHistoryData('13111', '1113', '2022-04-13', '2022-04-14')

# dict = df.dietitian_selected_data.to_dict()
# print(dict)
# list =[]
# for i in dict:
#   list.append(dict.get(i).get('food_groups'))

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

# history_data = {}
# history_data['Fat'] = fat_count
# history_data['Vegetables'] = vegetables_count
# history_data['Protein'] = protein_count
# history_data['Grains'] = grains_count

# json_data = json.dumps(history_data)
# print(json_data)

