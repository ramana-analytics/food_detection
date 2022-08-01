# Note: this still uses FPID with a poor mapping algorithm
# improve by using generic ingredients database and mapping instead

import psycopg2 
from Config.config import config
import pandas as pd
import collections
import openpyxl
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


from Model.fetch_commonfoodgroups import fetch_commonfoodgroups

pd.set_option('display.max_rows', 1000)

# using patient id 1926 for testing purposes, which has 83 paul/jeevan images logged with predictions from the most recent model
patientId = '1926'

def fetch_image_data_by_patientId(patient_id):
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        sql_image = """ SELECT ingredients, patient_id, image_id, image, food_item, food_groups, insert_ts  FROM public."_ModelPredictedGroups" WHERE patient_id in(""" + patient_id + ");"
        df_image= pd.read_sql_query(sql_image, conn)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df_image

image_df = fetch_image_data_by_patientId(patientId)
image_df = image_df[['image', 'food_item', 'food_groups', 'ingredients', 'insert_ts']]

ingredients = []
for ingredient in image_df['ingredients']:
    ingredients += ingredient.keys()

most_common_ingredients = collections.Counter(ingredients)

# uses Buland's common food mapping so could be improved
df_foodgroups_db = fetch_commonfoodgroups()
df_foodgroups_db['ingredient'] = df_foodgroups_db['ingredient'].str.lower()

commonfg_df = pd.DataFrame({'ingredient':[], 'ingredient_category':[], 'food_group':[]})
for ingredient in ingredients:
    df_foodgroups_db['contains'] = df_foodgroups_db['ingredient'].str.contains(r"\b{}\b".format(ingredient))
    ingredient_matches_db = df_foodgroups_db[df_foodgroups_db['contains'] == True]
    
    commonfg_df.loc[len(commonfg_df.index)] = [ingredient, 
                                               ingredient_matches_db['ingredient_category'].drop_duplicates().str.cat(sep=','), 
                                               ingredient_matches_db['food_group'].drop_duplicates().str.cat(sep=',')]
#

def fetch_common_ingredients_by_fg(food_group):
    ingredient_fg_df = commonfg_df
    ingredient_fg_df['contains'] = commonfg_df['food_group'].str.contains(food_group)
    ingredients_by_fg = ingredient_fg_df[ingredient_fg_df['contains'] == True]
    return collections.Counter(ingredients_by_fg['ingredient'])

def fetch_ingredient_categories_by_fg(food_group):
    category_fg_df = commonfg_df
    category_fg_df['contains'] = commonfg_df['food_group'].str.contains(food_group)
    df_foodgroups_db['contains'] = df_foodgroups_db['food_group'].str.contains(food_group)
    categories_by_fg = category_fg_df[category_fg_df['contains'] == True]
    category_matches_db = df_foodgroups_db[df_foodgroups_db['contains'] == True]

    categories_by_fg = []
    for category in category_matches_db['ingredient_category'].drop_duplicates():
        category_fg_df['contains'] = category_fg_df['ingredient_category'].str.contains(category)
        for i in range(len(category_fg_df[category_fg_df['contains'] == True])):
            categories_by_fg += [category]

    return collections.Counter(categories_by_fg)


def fetch_ingredient_category(category):
    fetch_commonfoodgroups()

data = pd.read_excel (r'/Users/michellewang/Desktop/PHRQL/API_DB_CONN_V20/FPID Database.xlsx', sheet_name='FPED') #read file
inflammatory = pd.DataFrame(data, columns= ['DESCRIPTION','F_TOTAL (cup eq.)','G_WHOLE (oz. eq.)','G_REFINED (oz. eq.)','PF_MEAT (oz. eq.)','D_TOTAL (cup eq.)', 'SOLID_FATS (grams)', 'ADD_SUGARS (tsp. eq.)','PF_SEAFD_HI (oz. eq.)', 'PF_SEAFD_LOW (oz. eq.)', 'V_DRKGR (cup eq.)','V_REDOR_TOTAL (cup eq.)','V_REDOR_TOMATO (cup eq.)','V_REDOR_OTHER (cup eq.)','V_OTHER (cup eq.)'])


#find all food that containes the ingredient in FPED
def find_food(ingredient, database): 
    potential_food = []
    if ingredient == None: 
        return potential_food
    for food in database:
        if ingredient.lower() in food.lower():
            potential_food.append(food)
    potential_food.sort(key=len) #find the shortest on in the list
    return potential_food

def find_food_bestmatched(ingredient, data):
    if ingredient == None:
        return []   
    food_list = find_food(ingredient, data)
    best_matched_food = process.extractOne(ingredient, food_list)
    return best_matched_food

#get the catogories and values given ingredient and portion size
def get_category(ingredient, portion): 
    FPED = inflammatory['DESCRIPTION']
    row_index = inflammatory[FPED == ingredient].index[0]
    row = inflammatory.loc[row_index]
    category_and_value={}
    for i in range(1,15):
        category = inflammatory.columns[i]
        value = float(row[i])
        category_and_value[category] = value * portion
    return(category_and_value)

def summary(common_food, portion):
    stats = {}
    for food in common_food:
        ingredient = find_food_bestmatched(food, inflammatory['DESCRIPTION'])
        if ingredient != None:
            stats[food] = get_category(ingredient[0],portion)
        else:
            stats[food] = 'Not Found'
    return stats

#print(summary(most_common_ingredients, 1))
data = summary(most_common_ingredients, 1)
df = pd.DataFrame(data)
df.insert(0, "Category", ['fruit', 'whole grain', 'refined grain', 'meat', 'dairy', 'saturated fat', 'added sugar', 'seafood', 'seafood','non-starchy vegetavbles', 'non-starchy vegetavbles', 'non-starchy vegetavbles', 'non-starchy vegetavbles', 'non-starchy vegetavbles'], True)

df.to_excel(r'/Users/michellewang/Desktop/datanew.xlsx', index=False)
