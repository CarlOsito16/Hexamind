import numpy as np
import pandas as pd 


def create_combined_reviews(titles, reviews):
    if pd.isna(reviews):
        combined_reviews = titles
    else:
        combined_reviews = titles + " " + reviews
        
    return combined_reviews