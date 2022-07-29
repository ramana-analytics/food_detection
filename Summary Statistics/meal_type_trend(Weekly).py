from ast import Break
import psycopg2 
from Config.config import config
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from fetch_commonfoodgroups import fetch_commonfoodgroups

# using jeevan's id for testing purposes
patientId = '5'
#end_date = pd.Timestamp.utcnow()
#start_date = end_date - pd.DateOffset(days = 7)
start_date = "2022-06-01 12:30:00"
end_date = "2022-06-08 12:30:00"


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
                           """.format(patient_id = patient_id, start_date = start_date, end_date = end_date)

        df_history_data = pd.read_sql_query(sql_history_data, conn, params={"patient_id":patient_id, "start_date": start_date, "end_date":end_date})
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_history_data

Breakfast = 0
Lunch = 0
Dinner = 0
Snack = 0
mealtypeDF = FetchDataFromSelectedGroups(patientId, start_date, end_date)[['meal_type']]

for meal in mealtypeDF:
    mealtypeList = mealtypeDF[meal].values

for i in mealtypeList:
    if i == "Breakfast":
        Breakfast += 1
    elif i == "Lunch":
        Lunch += 1
    elif i == "Dinner":
        Dinner += 1
    elif i == "Snack":
        Snack += 1

mealtype = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
values = [Breakfast, Lunch, Dinner, Snack]
N = len(mealtype)
values += values[:1]
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
plt.polar(angles, values)
plt.fill(angles, values, alpha = 0.3)
plt.xticks(angles[:-1], mealtype)
plt.yticks(values.sort(), color = "grey", size = 8)
plt.ylim(0, max(values))
plt.show()

