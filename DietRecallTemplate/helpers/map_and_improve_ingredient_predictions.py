import pandas as pd
import string

BLACKLIST = ['sweet', 'with', 'or', 'and', 'in', 'the', 'all']

generic_df = pd.read_csv('generic_ingredients.csv')
generic_df['name'] = generic_df['name'].str.lower()

# improves ingredient predictions by factoring in the food title/description that the user inputs
# then maps the candidate words/concepts to our generic ingredients database
# parameter must be a datafram with a column titled 'ingredients' and a column titled 'food_name'
def mapAndImproveIngredientPredictions(df):
    df['ingredient_class'] = df['ingredients'] # this will be overwritten (will represent 'hierarchy' upper level)

    # use user inputted food_name to improve ingredient output
    for i in range(len(df.index)):
        # lowercase, remove punctuation, split into indiv words
        food_name_formatted = df['food_name'].iloc[i].lower().translate(str.maketrans('', '', string.punctuation)).split()

        concepts = list()
        if type(df['ingredients'].iloc[i]) == dict:
            concepts = list(df['ingredients'].iloc[i].keys())

        candidate_words = food_name_formatted + concepts
        candidate_words = [word for word in candidate_words if word not in BLACKLIST]

        # set ingredients as the mapped candidate words
        df['ingredient_class'].iloc[i], df['ingredients'].iloc[i] = matchItemToGeneric(candidate_words)

    return df
 
def matchItemToGeneric(items):
    ingredient_class = list()
    generic_ingredients = list()
    skip = list()

    for item1 in items:
        if item1 not in skip:
            containsItem1 = list()
            containsBoth = list()

            # check ingredient names that contain item1
            generic_df['contains'] = generic_df['name'].str.contains(item1)
            contains_df = generic_df[generic_df['contains'] == True]
            containsItem1 = contains_df['name'].tolist()

            # check ingredient names that are exact matches with item1
            generic_df['equals'] = generic_df['name'] == item1
            equals_df = generic_df[generic_df['equals'] == True]
            gen_ingred = equals_df['name'].tolist()

            # check ingredient names that contain item1 and item2 together
            for item2 in items:
                if item1 != item2 and item1 not in item2 and item2 not in item1:
                    containsItem2 = list()
                    generic_df['contains'] = generic_df['name'].str.contains(item2)
                    contains_df = generic_df[generic_df['contains'] == True]
                    containsItem2 = contains_df['name'].tolist()

                    intersection = list(set(containsItem1).intersection(containsItem2))

                    if (len(intersection) > 0 and 
                        intersection[0] not in containsBoth and 
                        item1 + ' ' + item2 not in ingredient_class and 
                        item2 + ' ' + item1 not in ingredient_class):
                            # determine the order to name the ingredient_class, eg 'sour cream' or 'cream sour' based on how it occurs in the matching ingredient
                            if intersection[0].index(item1) < intersection[0].index(item2):
                                ingredient_class.append(item1 + ' ' + item2)
                            else:
                                ingredient_class.append(item2 + ' ' + item1)

                            containsBoth.extend(intersection)
                            skip.append(item2)

            # if an ingredient name contains item1 and any other items together, add them
            if len(containsBoth) > 0:
                generic_ingredients.extend([containsBoth])
                skip.append(item1)
            else:
                # if there is an exact match with item1, add it
                if len(gen_ingred) == 1 and item1 not in ingredient_class:
                    ingredient_class.append(item1)
                    generic_ingredients.extend([gen_ingred])
                
                # otherwise, add any ingredients that contain item1
                if (len(containsBoth) == 0 and 
                    len(gen_ingred) != 1 and 
                    len(containsItem1) > 0 and 
                    item1 not in ingredient_class):
                        gen_ingred = containsItem1

                        ingredient_class.append(item1)
                        generic_ingredients.extend([gen_ingred])

    return ingredient_class, generic_ingredients
