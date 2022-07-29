from unicodedata import category
import psycopg2 
from Config.config import config
import pandas as pd
import calendar
import datetime as dt
from datetime import datetime, timedelta
from fetch_commonfoodgroups import fetch_commonfoodgroups

# using jeevan's id for testing purposes
patientId = '5'
timeNow = dt.datetime.utcnow()
timeYest = dt.datetime.utcnow() - timedelta(days = 1)

# fetches most of the data needed for recall template, the rest to be appended later in this script
def FetchDataFromSelectedGroups(patient_id, start_date, end_date):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        sql_history_data = """ SELECT m.insert_ts, p.meal_type, m.image, p.patient_selected_data->>'food_name' AS food_name, m.ingredients, p.patient_selected_data->>'food_groups' AS food_groups, p.location_details

                                 FROM public."_ModelPredictedGroups" AS m JOIN public."_PatientSelectedGroups" AS p
                                   ON p.patient_selected_data->>'image_id' = m.image_id::varchar(255)
                            
                                WHERE m.patient_id = %(patient_id)s 
                                  AND m.insert_ts > TIMESTAMP %(start_date)s
                                  AND m.insert_ts <= TIMESTAMP %(end_date)s 
                           """.format(patient_id = patient_id, start_date = "2022-06-08 12:30:00", end_date = "2022-06-15 12:30:00")

        df_history_data = pd.read_sql_query(sql_history_data, conn, params={"patient_id":patient_id, "start_date":"2022-06-08 12:30:00", "end_date":"2022-06-15 12:30:00"})
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_history_data

df = FetchDataFromSelectedGroups(patientId, timeYest, timeNow)


df['food_name'] = df['food_name'].str.replace('$', '')
df['insert_ts'] = df['insert_ts'].dt.tz_convert('US/Eastern')

# get day from insert_ts 
days = list()
for ts in df['insert_ts']:
    day = calendar.day_name[ts.weekday()]
    days.append(day)

df['day'] = days

# get date from insert_ts
dates = list()
for ts in df['insert_ts']:
    date = ts.date()
    dates.append(date)

df['date'] = dates

# get time from insert_ts
times = list()
for ts in df['insert_ts']:
    times.append("{:d}:{:02d}".format(ts.hour, ts.minute))

df['time'] = times

# reformat ingredients (take only ingredient name, not probability)
ingredients = list()
for ingredient in df['ingredients']:
    if ingredient:
        ingredients.append(list(ingredient.keys()))
    else:
        ingredients.append('')

df['ingredients'] = ingredients

# get ingredient categories
cfg_df = fetch_commonfoodgroups()
cfg_df['ingredient'] = cfg_df['ingredient'].str.lower()

def fetch_ingredient_category(ingredient):
    cfg_df['contains'] = cfg_df['ingredient'].str.contains(r"\b{}\b".format(ingredient))
    contains_ingred_db = cfg_df[cfg_df['contains'] == True]
    return contains_ingred_db['ingredient_category'].drop_duplicates().tolist()

categories = list()
for ingredientList in ingredients:
    categoryList = list()
    for ingredient in ingredientList:
        categoryList.append(fetch_ingredient_category(ingredient))
    categories.append(categoryList)
df['ingredient_category'] = categories

# reorder columns, remove insert_ts
df = df[['date', 'day', 'time', 'meal_type', 'image', 'food_name', 'ingredients', 'ingredient_category', 'food_groups', 'location_details' ]]

#print(df)
df.to_excel(r'/Users/jamiekim/Desktop/Book2.xlsx', index = False, header = True)


