def remove_new_line(df, review_col):
    df['clean_review'] = df[review_col].apply(lambda x : str(x).replace("\n", ""))

    return df

def create_combined_df(df, title_col, review_col):
    df['combined_reviews'] = df[title_col] + " " + df[review_col]
    return df

def remove_and_combined(df, title_col, review_col):
    df = remove_new_line(df, review_col) #first remove the `\n` tokens on the reviews column
    df = create_combined_df(df, title_col, "clean_review") #then concat `title` and `clean_review` together
    return df