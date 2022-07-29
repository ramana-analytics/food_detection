from unicodedata import category
import psycopg2 
from Config.config import config
import pandas as pd
import calendar
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime, timedelta
from fetch_commonfoodgroups import fetch_commonfoodgroups

# using jeevan's id for testing purposes
patientId = '5'
end_date = pd.Timestamp.utcnow()
start_date = end_date - pd.DateOffset(months = 1)

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

tempDF = pd.DataFrame()
finalDF = pd.DataFrame(index = ['Proteins', 'Dairy', 'Vegetables', 'Grains', 'Fruits'])
period = list()
temp = list()
idx = 0

cutoff = pd.date_range(start = start_date, end = end_date, periods = 8).astype(str)
for i in cutoff:
    i = i[0:19]
    period.append(i)
print(period)

dateTime = pd.DataFrame({'time' : period})
dateTime['time'] = pd.to_datetime(dateTime['time']).dt.date
for d in dateTime:
    date = dateTime[d].values


while idx < 7:
    Proteins = 0
    Dairy = 0
    Vegetables = 0
    Grains = 0
    Fruits = 0

    tempDF = FetchDataFromSelectedGroups(patientId, period[idx], period[idx+1])
    tempDF = tempDF['food_groups']

    for i in tempDF:
        for j in i.split(','):
            if j == "Proteins":
                Proteins += 1
            elif j == "Dairy":
                Dairy += 1
            elif j == "Starchy Vegetables" or j == "Nonstarchy Vegetables" or j == "Vegetables":
                Vegetables += 1
            elif j == "Grains":
                Grains += 1
            elif j == "Fruits":
                Fruits += 1
            else:
                continue

    finalDF[date[idx]] = [Proteins, Dairy, Vegetables, Grains, Fruits]
    idx += 1

finalDF = finalDF.transpose()
print(finalDF)
finalDF.plot()
plt.xticks(rotation = 45)
plt.show()


