#!/usr/bin/python
import json
import psycopg2
from sklearn.manifold import trustworthiness
from Config.config import config

from PIL import Image
import os, os.path

def DietitianRatedData(image_id, dietitian_id, meal_type, json_data):
    # print(json_data)
    sql = """INSERT INTO public."_DietitianSelectedGroups" (dietitian_id, meal_type, dietitian_selected_data) VALUES (""" + "'" +dietitian_id + "'" +',' + "'" + meal_type + "'" + ',' + "'" + json_data + "'" + " ) RETURNING insert_ts;" + """ UPDATE public."_PatientSelectedGroups" SET rated = True , update_ts = NOW() WHERE patient_selected_data->>'image_id' = '""" + image_id + "' ;"   
    print(sql)
    conn = None
    # insert_ts = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (image_id, dietitian_id, meal_type, json_data,))
        # print(sql)
        # insert_ts = cur.fetchone()[0]
        # commit the changes to the database
        
        conn.commit()
        
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return dietitian_id

# path = "download.jpg"
# # imgs = Image.open(path)
# # print(imgs)
# a = insert_image(path)
# print(a)

# json_={'image_id': '11111', 'patient_id': '1082', 'food_name': 'Boiled_eggs', 'food_groups': 'Protein'}
# json_=json.dumps(json_)
# status_ = 'unrated'
# meal_type = "BreakFastt"
# dietitian_id = '11111'
# image_id = '11111'
# # sql =  "'"+ status_ + "'," + "'" + json_ + "'"
# if __name__ == "__main__":
#     a= DietitianRatedData(image_id, dietitian_id, meal_type, json_)
#     print(a)