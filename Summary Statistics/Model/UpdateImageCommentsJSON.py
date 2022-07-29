#!/usr/bin/python
import json
from xml.etree.ElementTree import Comment
import psycopg2
from sklearn.manifold import trustworthiness
from Config.config import config

from PIL import Image
import os, os.path

def UpdateImageComments(image_id, dietitian_id, patient_id, timestamp, comment):
    # print(json_data)
    sql = """UPDATE public."_ModelPredictedGroups"
             SET comments = (
             CASE
             WHEN comments IS NULL THEN '[]'::JSONB
             ELSE comments
             END) || jsonb_build_object('dietitian_id',"""+ "'" + dietitian_id + "'," + "'patient_id','" + patient_id + "'," + "'comment','" + comment +"','timestamp','" + timestamp + "')" + "::JSONB WHERE image_id ='" + image_id + "';" 
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
        cur.execute(sql, (image_id, dietitian_id,patient_id, timestamp, comment,))
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

    return image_id

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
# patient_comment = "Thank you for your feedback!"
# image_id = '1122'
# dietitian_comment = "Welcome!"
# # patient_id = '11111'
# # json_={'image_id': '1122', 'patient_id': '11111', 'patient_name' : 'Jenny', 'comment': 'Thank you for your feedback!', 'timestamp' : '2022-05-07 10:05:43' }
# # comment_json=json.dumps(json_)

# # if __name__ == "__main__":
# a= PatientCommentJSON(image_id, dietitian_comment)
# print(a)