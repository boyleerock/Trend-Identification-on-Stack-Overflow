import pandas as pd
import request_data
import clear_code
from clear_code import clear_code
from clear_code import clear_tags
import random


# function to process post bodies
# clear code and HTML tags in the texts
# params: df - df to be processed; column - column index containing post bodies
def clear_df(df, column):
    rd = random.randint(0, 100)
    num_row = df.shape[0]  # total number of rows
    if (num_row >= 2):
        # 2 or more rows
        for i in range(0, num_row):  # [0, num_row-1]
            text = df.iat[i, column]  # column = 2
            text = clear_code(text)  # get text between <p> and </p>
            text = clear_tags(text)  # clear HTML tags
            df.iat[i, column] = text  # replace with processed text
    else:
        # only 1 row
        text = df.iat[0, column]  # column = 2
        text = clear_code(text)  # get text between <p> and </p>
        text = clear_tags(text)  # clear HTML tags
        df.iat[0, column] = text  # replace with processed text
    df.to_csv('intermediate_data/clear_df%s.csv' % rd, index=False)  # output processed df
    return df
