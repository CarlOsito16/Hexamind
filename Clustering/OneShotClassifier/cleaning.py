import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# from pandas.core.common import SettingWithCopyWarning
# import warnings
# warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)




FILEPATH = "20230220_selected_df_google_sheet.csv"

def boolean_to_int(boolean):
    if boolean:
        value = 1
    else:
        value = 0
    return value

def binary_transform(original_df):

    superclass_cols = ['Buying experience', 'Product', 'Delivery Mode', 'After Sales']

    # original_df = pd.read_csv(FILEPATH, index_col=0, header= [1]).reset_index()
    print(f"Original shape: {original_df.shape}")

    # original_df.columns = original_df.columns.droplevel(0)

    # Now let's make sure we select only the reviews that has some reviewers working on
    have_reviewers = ['Poon', 'Yves', 'Insaf', 'All']
    selected_df = original_df[original_df['reviewer'].isin(have_reviewers)]
    unselected_df = original_df[~original_df['reviewer'].isin(have_reviewers)]
    
    selected_df.shape
    print(F"Selected shape: {selected_df.shape}")
    print(F"Unselected shape: {unselected_df.shape}")


    BE_subclass = ['Buying experience', 'Digital', 'store', 'service', 'product not available']
    PD_subclass = ['Product', 'fresh', 'non fresh', 'value (quality, etc.)', 'price']
    DM_subclass = ['Delivery Mode', 'Drive', 'Delivery']
    AS_subclass = ['After Sales', 'Carrefour', 'Other brand', 'reimbursement']

    selected_df['clean_BE'] = np.any(selected_df.loc[: ,BE_subclass], axis=1)
    selected_df['clean_PD'] = np.any(selected_df.loc[: ,PD_subclass], axis=1)
    selected_df['clean_DM'] = np.any(selected_df.loc[: ,DM_subclass], axis=1)
    selected_df['clean_AS'] = np.any(selected_df.loc[: ,AS_subclass], axis=1)

    clean_superclass = ['clean_BE', 'clean_PD', 'clean_DM', 'clean_AS']

    selected_df['clean_BE'] = selected_df['clean_BE'].apply(lambda x : boolean_to_int(x))
    selected_df['clean_PD'] = selected_df['clean_PD'].apply(lambda x : boolean_to_int(x))
    selected_df['clean_DM'] = selected_df['clean_DM'].apply(lambda x : boolean_to_int(x))
    selected_df['clean_AS'] = selected_df['clean_AS'].apply(lambda x : boolean_to_int(x))

    selected_df.loc[:, superclass_cols].sum().plot(label = 'before checking the subclass')
    selected_df.loc[:, clean_superclass].sum().plot(label = 'after checking the subclass')
    plt.legend()
    plt.title('Changes of number of reviews after looking at the subclass')
    plt.xlabel('4 super classes')
    plt.ylabel('number of reviews')
    plt.show()
    
    return selected_df, unselected_df