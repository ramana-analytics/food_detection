#from asyncio.windows_events import NULL
import psycopg2 
from Config.config import config
import pandas as pd
import json

def FetchAggStatsData(patient_id, start_date, end_date):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        #in this query add the timeframe for which you want to track and pass it as a variable make sure this data is fetched from dietiitians table
        sql_history_data = """Select P.patient_id, p.meal_type, P.patient_selected_data->>'image_id' as image_id ,P.patient_selected_data->>'food_name' as food_name,P.patient_selected_data->>'food_groups' as PatientFoodGroup,
                            count(D.dietitian_id) as DietitianCount, json_agg(jsonb_build_object('d_food_groups', D.dietitian_selected_data->>'food_groups', 'd_dietitian_id', D.dietitian_id ) ) as Dietitian_Data FROM public."_DietitianSelectedGroups" as D
                            INNER Join public."_PatientSelectedGroups" as P
                            ON P.patient_selected_data->>'image_id' = D.dietitian_selected_data->>'image_id'
                            where P.patient_id= %(patient_id)s 
                            AND P.insert_ts > TIMESTAMP %(start_date)s
                            AND P.insert_ts <= TIMESTAMP %(end_date)s
                            Group By P.patient_selected_data, P.patient_id, p.meal_type""".format(patient_id=patient_id, start_date=start_date,end_date=end_date)
        df_history_data= pd.read_sql_query(sql_history_data, conn, params={"patient_id":patient_id, "start_date":start_date,"end_date":end_date})
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_history_data


#this is the api part to fetch the history data of a user.
# FetchHistoryData(patient_id, meal_type, dietitian_id, start_date, end_date):
df = FetchAggStatsData('18', '2022-04-19 00:00:00', '2022-04-19 23:59:59')
# print(df['image_id'][0])
# print(df.loc[df['image_id'] == '1132'].patientfoodgroup.to_dict().get(0))


# if df['image_id'][0]=='1132':
    # dict = df['patientfoodgroup'].to_dict()
# print(dict)
# dict_p= df.dietitian_food_groups.to_dict()
# print(dict_p)
def GetMealStats(df,meal_type):
    pdict=df.loc[df['meal_type'] == meal_type].patientfoodgroup.to_dict()
    # count=df.loc[df['meal_type'] == 'Dinner']['dietitiancount']
    # print(count)
    dcount=sum(df.loc[df['meal_type'] == meal_type]['dietitiancount'])
    ratingcount=dcount+1
    # print(ratingcount)
    if dcount>0:
        plist =[]
        for i in pdict:
            plist.append(pdict.get(i))
        # print(list)
        plst=[]
        for i in plist:
            plst.append(i.split(','))
        # print(plst)

        ddict=df.loc[df['meal_type'] == meal_type].dietitian_data.to_dict()
        # print(ddict)

        dlist =[]
        for i in ddict:
            dlist.append(ddict.get(i)[0]['d_food_groups'])
            dlst=[]
        for i in dlist:
            dlst.append(i.split(','))
        # print(dlst)

        pfat_count = 0
        pvegetables_count= 0
        pprotein_count= 0
        pgrains_count= 0
        pdairy_count= 0

        for i in plst:
            pfat_count += i.count('Fats')
            pvegetables_count += i.count('Vegetables')
            pprotein_count += i.count('Proteins')
            pgrains_count += i.count('Grains')
            pdairy_count += i.count('Dairy')

        for i in dlst:
            pfat_count += i.count('Fats')
            pvegetables_count += i.count('Vegetables')
            pprotein_count += i.count('Proteins')
            pgrains_count += i.count('Grains')
            pdairy_count += i.count('Dairy')

        history_data = {}
        history_data['Fats'] = pfat_count/ratingcount
        history_data['Vegetables'] = pvegetables_count/ratingcount
        history_data['Proteins'] = pprotein_count/ratingcount
        history_data['Grains'] = pgrains_count/ratingcount
        history_data['Dairy'] = pdairy_count/ratingcount
        # json_data = json.dumps(history_data)
        meal_history = {}
        meal_history[meal_type] = history_data
        return json.dumps(meal_history)
    empty_data = {"Fats": 0.0, "Vegetables": 0.0, "Proteins": 0.0, "Grains": 0.0, "Dairy": 0.0}
    meal_history={}
    meal_history[meal_type] = empty_data
    return json.dumps(meal_history)
# print(meal_history)

# snack= json.loads(GetMealStats(df,'Snack'))
# dinner= json.loads(GetMealStats(df,'Dinner'))
# lunch= json.loads(GetMealStats(df,'Lunch'))
# breakfast= json.loads(GetMealStats(df,'Breakfast'))

# stats={**snack,**breakfast,**lunch,**dinner}

# print(stats)

#     lst=[]
#     for i in list:
#         lst.append(i.split(','))
#     for i in lst:
#             # v=i.count('Vegetables')
#         print(i)
#     # print(i.split(','))
# print(list)
# print(lst)
# print(v)/

# print([i.split(',') for i in list])
# list= list[0].split(',')
# print(list)
# for i in dict:
#   list.append(dict.get(i))
# print(list)
# print(list.split(','))
# str= ', '.join(list).lower()
# # # x = dict.get(0).get('status')
# # print(x)
# # # print(df.saved_data)
# print(str)
# str= str.split(', ')
# print(str)


# # print(['Vegetables', 'Proteins'].count('Vegetables'))
# fat_count= list.count('fats')
# vegetables_count= list.count('Vegetables')
# protein_count= list.count('Proteins')
# grains_count= list.count('Grains')
# dairy_count= list.count('Dairy')
# print("fat serving-> ", fat_count)
# print("veg serving-> ",vegetables_count)
# print("protein serving-> ",protein_count)
# print("grains serving-> ",grains_count)
# print("dairy serving-> ", dairy_count)
# history_data = {}
# history_data['Fats'] = fat_count
# history_data['Vegetables'] = vegetables_count
# history_data['Proteins'] = protein_count
# history_data['Grains'] = grains_count
# history_data['Dairy'] = dairy_count
# json_data = json.dumps(history_data)
# print(json_data)

# # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# # dict = df.dietitian_data.to_dict()
# # # print(dict)

# # list =[]

# # for i in dict:
# #   list.append(dict.get(i))

# # print(list)