#!/usr/bin/python

import psycopg2
from Config.config import config


def insert_foodgroup(food_itemId,food_item,food_groups):
    sql = """INSERT INTO public."PredictTest"(food_itemId,food_item,food_groups)
             VALUES(%s, %s, %s) RETURNING model_run_id;"""
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
        cur.execute(sql, (food_itemId,food_item,food_groups,))
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

if __name__ == '__main__':
    insert_foodgroup('Banana', 'Fruit')
