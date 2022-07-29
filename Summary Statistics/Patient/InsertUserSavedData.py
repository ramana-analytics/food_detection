#!/usr/bin/python
import json
import psycopg2
from Config.config import config

from PIL import Image
import os, os.path

def UserSavedData(patient_id,meal_type,location_details,json_data):
    # print(json_data)
    sql = """INSERT INTO public."_PatientSelectedGroups"(rated, patient_id, meal_type, patient_selected_data, location_details)
    VALUES (False,%s,%s,%s,%s) RETURNING insert_ts;"""
    conn = None
    insert_ts = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (patient_id,meal_type,json_data,location_details))
        # print(sql)
        insert_ts = cur.fetchone()[0]
        # commit the changes to the database
        
        conn.commit()
        
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return insert_ts

# path = "download.jpg"
# # imgs = Image.open(path)
# # print(imgs)
# a = insert_image(path)
# print(a)

# patient_id = '1082'
# meal_type = 'Breakfast'
# json_={'image_id': '11111', 'food_name': 'Boiled_eggs' , 'food_groups': 'Protein'}
# json_=json.dumps(json_)
# if __name__ == "__main__":
#     print(UserSavedData(patient_id, meal_type, json_))
    