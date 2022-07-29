import pandas as pd
import calendar
import datetime as dt
from datetime import datetime, timedelta
from helpers.fetch_data_from_selected_groups import FetchDataFromSelectedGroups
from helpers.map_and_improve_ingredient_predictions import mapAndImproveIngredientPredictions
pd.set_option('display.max_rows', 1000)

timeNow = dt.datetime.utcnow()
timeYest = dt.datetime.utcnow() - timedelta(days = 1)

# using jeevan's (5), jessicas (256) or pauls (35) id for testing purposes
patientId = '35'
# change start and end date if you want a different range
startDate = timeYest
endDate = timeNow

# fetches most of the data needed for recall template, the rest to be appended later in this script
df = FetchDataFromSelectedGroups(patientId, startDate, endDate)

# convert to eastern timezone
if len(df.index) > 0:
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

# format and improve ingredients based on food name
df['concepts'] = df['ingredients']
df = mapAndImproveIngredientPredictions(df)

# reorder columns, remove insert_ts
df = df[['date', 'day', 'time', 'meal_type', 'image', 'food_name', 'concepts', 'ingredient_class', 'ingredients', 'food_groups', 'location_details' ]]

# export to spreadsheet
# print(df)
# df.to_excel(r'/Users/ericrohrer/Desktop/Book1.xlsx', index = False, header = True)


