import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from helper_function import create_combined_reviews
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=UserWarning)

    CLF_MODEL_FILEPATH  = "model/clf_bayes.sav"
    loaded_clf = joblib.load(CLF_MODEL_FILEPATH)

    TOKENIZER_FILEPATH = "model/tokenizer.sav"
    loaded_tokenizer = joblib.load(TOKENIZER_FILEPATH)

    print("model and tokenizer downloaded")



CARREFOUR_FILEPATH = "data/final_carrefour_df.csv"
df = pd.read_csv(CARREFOUR_FILEPATH, index_col=0)
print("carrefour data downloaded")