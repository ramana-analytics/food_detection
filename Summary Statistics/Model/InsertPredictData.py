#!/usr/bin/python

import psycopg2
from Config.config import config
import glob
from PIL import Image
import os, os.path

def InsertPredictData(patient_id, image,food_item, food_groups,ingredients):
    sql = """INSERT INTO public."_ModelPredictedGroups"(patient_id, image, food_item, food_groups,ingredients)
             VALUES (%s, %s , %s , %s, %s) RETURNING image_id;"""
    conn = None
    model_run_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (patient_id, image, food_item, food_groups, ingredients,))
        # get the generated id back
        model_run_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return model_run_id


def InsertImage(image_path):
    sql_image = """INSERT INTO public."_ModelPredictedGroups"(food_image)
                    VALUES(bytea(%s)) RETURNING image_id;"""
    conn = None
    image_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql_image, (image_path,))
        # get the generated id back
        image_id = cur.fetchone()[0]
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

# def InsertIngredientsData(ingredients):
#     sql = """INSERT INTO public."_ModelPredictedGroups"(ingredients)
#              VALUES (%s) 
#              RETURNING image_id;"""
#     conn = None
#     model_run_id = None
#     try:
        
#         # read database configuration
#         params = config()
#         # connect to the PostgreSQL database
#         conn = psycopg2.connect(**params)
#         # create a new cursor
#         cur = conn.cursor()
#         # execute the INSERT statement
#         cur.execute(sql, (ingredients,))
#         print(sql)
#         # get the generated id back
#         model_run_id = cur.fetchone()[0]
#         # commit the changes to the database
#         conn.commit()
#         # close communication with the database
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()

#     return model_run_id

# path = "download.jpg"
# # imgs = Image.open(path)
# # print(imgs)
# a = insert_image(path)
# print(a)

# if __name__ == "__main__":
#     InsertPredictData('AAAAAA', 'BBBB,CCC,DDD')