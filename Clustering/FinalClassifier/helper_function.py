import numpy as np
import pandas as pd 


def create_combined_reviews(titles, reviews):
    if pd.isna(reviews):
        combined_reviews = titles
    else:
        combined_reviews = titles + " " + reviews
        
    return combined_reviews




def chart_df(all_comp_df):
    all_result = []
    clean_superclass_name = ['🛒 Buying Experience', '🥦 Product', '🚚 Delivery Mode', '📞 After Sales']
    for comp in all_comp_df['company_name'].unique():
        selected_df = all_comp_df[(all_comp_df['company_name'] == comp)]
        print(comp, selected_df.ratings.mean(), selected_df.has_respond.mean())
        result = [comp, 'All topics', len(selected_df), selected_df.ratings.mean().round(2), selected_df.has_respond.mean().round(2)]
        all_result.append(result)
        
        clean_superclass = ['clean_BE', 'clean_PD', 'clean_DM', 'clean_AS']
        
        for index, supclass in enumerate(clean_superclass):
            selected_df = all_comp_df[(all_comp_df['company_name'] == comp) &
                                    (all_comp_df[supclass] ==1)]
            
            result = [comp, clean_superclass_name[index], len(selected_df), selected_df.ratings.mean().round(2), selected_df.has_respond.mean().round(2)]
            all_result.append(result)
            
    complete_df = pd.DataFrame(all_result, columns= ['company', 'topic', 'count', 'score', 'response'])
    return complete_df