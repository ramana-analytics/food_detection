import psycopg2 
from Config.config import config
import pandas as pd
import json

def FetchRatedByDietitianIds(image_id):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        #in this query add the timeframe for which you want to track and pass it as a variable make sure this data is fetched from dietiitians table
        sql_usersaved = """SELECT rated_by FROM public."_PatientSelectedGroups" 
                           WHERE patient_selected_data->>'image_id' =  %(image_id)s""".format(image_id=image_id)
        df_usersaved= pd.read_sql_query(sql_usersaved, conn, params={"image_id":image_id})
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_usersaved


# #this is the api part to fetch the history data of a user.
# image_id="1158"
# df = FetchRatedByDietitianIds(image_id)
# print(df)
# dict = df.rated_by.to_dict()
# print(type(dict[0]))
# dietitian_ids = dict[0]
# dietitian_id= str(55)
# dietitan_ids=dietitian_ids+','+dietitian_id
# print(dietitan_ids)

# json_={'image_id': '1158', 'food_name': 'Boiled_eggs', 'food_groups': 'Proteins, Fats'}
# json_=json.dumps(json_)
# # status_ = 'unrated'
# meal_type = "BreakFastt"
# dietitian_id = dietitian_id
# image_id = '1158'
# rated_by = dietitian_ids
# # # sql =  "'"+ status_ + "'," + "'" + json_ + "'"
# if __name__ == "__main__":
#     a= DietitianRatedData(image_id, dietitian_id, meal_type, json_, rated_by)
#     print(a)

# list =[]
# for i in dict:
#   list.append(dict.get(i).get('foodGroups'))

# str= ', '.join(list).lower()
# x = dict.get(0).get('status')
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


