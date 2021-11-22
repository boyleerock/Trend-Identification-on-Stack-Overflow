# setting up account authentication
# env:GOOGLE_APPLICATION_CREDENTIALS="../mci1603-a6e4483d756b.json"

import pandas as pd
import datetime
from datetime import datetime, timedelta

from google.cloud import bigquery
import google.auth

# passing credentials using code https://cloud.google.com/docs/authentication/production
from google.cloud import storage

# get path for key file
input_file = "static/txt/input.txt"
f = open(input_file, 'r')
lines = f.readlines()
line_split = lines[0].split(" ")
key_path = line_split[7]
key_path = key_path.split(":")[1]
key_path = key_path[1:]

# Explicitly use service account credentials by specifying the private key file.
storage_client = storage.Client.from_service_account_json(
    key_path)
# Create a "Client" object
client = bigquery.Client.from_service_account_json(
    key_path)


# for related questions and answers
def rearrange_df(df, type):
    if (type == "qa"):
        # extract columns
        df_q = df[["score", "creation_date", "body"]]
        df_a = df[["score_1", "creation_date_1", "body_1"]]
        df_a.columns = ['score', 'creation_date', 'body']
        df_concat = df_q.append(df_a, ignore_index=True)
        # remove na and duplicate
        df_concat = df_concat.dropna(subset=['body'])
        df_concat = df_concat.drop_duplicates(subset='body', keep="first")
        # Body is at column 2
        return df_concat
    elif (type == "qc" or type == "ac"):
        # extract columns
        df_q = df[["score", "creation_date", "body"]]
        df_a = df[["score_1", "creation_date_1", "text"]]
        df_a.columns = ['score', 'creation_date', 'body']  # make column names consistent
        df_concat = df_q.append(df_a, ignore_index=True)
        # remove na and duplicate
        df_concat = df_concat.dropna(subset=['body'])
        df_concat = df_concat.drop_duplicates(subset='body', keep="first")
        # Body is at column 2
        return df_concat


# get start&end of each time window
def split_windows(start, end, num_window):
    start_time = datetime.strptime(start, '%Y-%m-%d')
    end_time = datetime.strptime(end, '%Y-%m-%d')

    delta = end_time - start_time
    total_seconds = delta.total_seconds()  # total seconds in between

    interval = total_seconds / num_window  # length of each time window

    end_dates = []
    for i in range(num_window):
        end_dates.append(start_time + timedelta(seconds=interval * (i + 1)))  # end date of each time window
        end_dates[i] = end_dates[i].strftime("%Y-%m-%d, %H:%M:%S")  # convert to string

    # construct a matrix storing start/end time, e.g.,
    # time_window_1 start (excl.) end (incl.)
    # time_window_2 start (excl.) end (incl.)
    # time_window_3 start (excl.) end (incl.)
    # fixme: excl or incl?
    start_end = []
    for i in range(num_window):
        start = ""
        if (i == 0):
            start = start_time.strftime("%Y-%m-%d, %H:%M:%S")
        else:
            start = end_dates[i - 1]
        end = end_dates[i]
        row = [start, end]
        start_end.append(row)

    # print(start_end)

    return start_end


# split_windows("2020-1-1", "2020-1-6", 7)


# param: [start, end, num_window, limit, types, sort, word]
def request_data(input_arr):
    print("requesting data at", datetime.now())
    start = input_arr[0]
    end = input_arr[1]
    num_window = input_arr[2]
    limit = input_arr[3]
    types = input_arr[4]
    sort = input_arr[5]

    # SQL body
    sql_time = """
       WHERE creation_date >= "{}" AND 
       creation_date <= "{}"
    """.format(start, end)

    order_by = ""  # fixme: ASC or DESC
    if (sort == "creation_date_asc"):
        order_by = "creation_date ASC"
    elif (sort == "creation_date_desc"):
        order_by = "creation_date DESC"
    elif (sort == "score"):
        order_by = "score DESC"
    elif (sort == "random"):
        order_by = "rand()"

    sql_order = """
           ORDER BY {}
        """.format(order_by)

    # pure questions/answers/titles/comments --------------------------------------------------------------------------
    if (types == "questions" or types == "answers" or types == "comments" or types == "titles"):

        print("------------- requesting questions/answers/comments/titles -------------")

        sql_limit = """
           LIMIT {}
        """.format(limit)

        type = ""
        if (types == "questions" or types == "titles"):
            type = "bigquery-public-data.stackoverflow.posts_questions"
        elif (types == "answers"):
            type = "bigquery-public-data.stackoverflow.posts_answers"
        elif (types == "comments"):
            type = "bigquery-public-data.stackoverflow.comments"
        sql_types = """
           SELECT * FROM `{}`
        """.format(type)

        sql = sql_types + sql_time + sql_order + sql_limit
        query_job = client.query(sql)  # Make an API request.

        # save results
        results = query_job.result()
        df = results.to_dataframe()  # convert to dataframe

        # if searching titles ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if (types == "titles"):  # swap title and body
            columns_titles = ["id", "body", "title", "title"]
            df = df.reindex(columns=columns_titles)

        # if searching comments ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if (types == "comments"):  # swap title and body
            columns_titles = ["id", "creation_date", "text", "score"]
            df = df.reindex(columns=columns_titles)

        start_d = start.split(" ")[0]
        df.to_csv('output/raw%s.csv' % start_d)   # todo
        return df

    # unrelated questions and answers ----------------------------------------------------------------------------------
    elif (types == "unrelated_qa"):
        print("------------- requesting unrelated_qa -------------")
        limit = str(int(limit) // 2)
        sql_limit = """
                  LIMIT {}
               """.format(limit)
        sql_q = """
           SELECT * FROM `bigquery-public-data.stackoverflow.posts_questions`
        """ + sql_time + sql_order + sql_limit
        sql_a = """
           SELECT * FROM `bigquery-public-data.stackoverflow.posts_answers`
        """ + sql_time + sql_order + sql_limit

        query_job = client.query(sql_q)  # Make an API request.

        # save results
        results = query_job.result()
        df_q = results.to_dataframe()  # convert to dataframe
        df_q.to_csv('output/raw_q.csv')

        query_job = client.query(sql_a)  # Make an API request.

        # save results
        results = query_job.result()
        df_a = results.to_dataframe()  # convert to dataframe
        df_a.to_csv('output/raw_a.csv')

        df = df_q.append(df_a, ignore_index=True)  # concatenate df
        df.to_csv('output/raw.csv')
        return df

    # related questions and answers ------------------------------------------------------------------------------------
    elif (types == "qa" or types == "qc" or types == "ac"):  # related questions and answers
        print("------------- requesting qa/qc/ac -------------")
        sql = """"""
        if (types == "qa"):
            limit = str(round(15 * int(limit) // 25))  # fixme: every question has 1.5 answers on average
            sql_select = """SELECT * FROM `bigquery-public-data.stackoverflow.posts_questions` AS question 
            LEFT JOIN `bigquery-public-data.stackoverflow.posts_answers` AS answer 
            ON answer.parent_id = question.id"""

            sql_time = """
                          WHERE question.creation_date >= "{}" AND 
                          question.creation_date <= "{}"
                       """.format(start, end)

            sql_limit = """
                               LIMIT {}
                           """.format(limit)

            order_by = ""
            if (sort == "creation_date_asc"):
                order_by = "question.creation_date ASC"
            elif (sort == "creation_date_desc"):
                order_by = "question.creation_date DESC"
            elif (sort == "score"):
                order_by = "question.score DESC"
            elif (sort == "random"):
                order_by = "rand()"
            sql_order = """ORDER BY {} """.format(order_by)
            sql = sql_select + sql_time + sql_order + sql_limit

        elif (types == "qc"):
            limit = str(round(2 * int(limit) // 3))  # fixme: every question has 2 comments on average
            sql_select = """SELECT * FROM `bigquery-public-data.stackoverflow.posts_questions` AS question 
                    LEFT JOIN `bigquery-public-data.stackoverflow.comments` AS comment 
                    ON comment.post_id = question.id"""
            sql_time = """
                          WHERE question.creation_date >= "{}" AND 
                          question.creation_date <= "{}"
                       """.format(start, end)

            sql_limit = """
                           LIMIT {}
                       """.format(limit)

            order_by = ""
            if (sort == "creation_date_asc"):
                order_by = "question.creation_date ASC"
            elif (sort == "creation_date_desc"):
                order_by = "question.creation_date DESC"
            elif (sort == "score"):
                order_by = "question.score DESC"
            elif (sort == "random"):
                order_by = "rand()"  # fixme: question.rand()
            sql_order = """ORDER BY {} """.format(order_by)
            sql = sql_select + sql_time + sql_order + sql_limit

        elif (types == "ac"):
            limit = str(round(12 * int(limit) // 22))  # fixme: every answer has 1.2 comments on average
            sql_select = """SELECT * FROM `bigquery-public-data.stackoverflow.posts_answers` AS answer 
                    LEFT JOIN `bigquery-public-data.stackoverflow.comments` AS comment
                    ON comment.post_id = answer.id"""
            sql_time = """
                          WHERE answer.creation_date >= "{}" AND 
                          answer.creation_date <= "{}"
                       """.format(start, end)

            sql_limit = """
                           LIMIT {}
                       """.format(limit)

            order_by = ""
            if (sort == "creation_date_asc"):
                order_by = "answer.creation_date ASC"
            elif (sort == "creation_date_desc"):
                order_by = "answer.creation_date DESC"
            elif (sort == "score"):
                order_by = "answer.score DESC"
            elif (sort == "random"):
                order_by = "rand()"
            sql_order = """ORDER BY {} """.format(order_by)
            sql = sql_select + sql_time + sql_order + sql_limit

        query_job = client.query(sql)  # Make an API request.

        # save results
        results = query_job.result()
        df = results.to_dataframe()  # convert to dataframe
        df.to_csv('output/raw_qa.csv')
        df = rearrange_df(df, types)
        df.to_csv('output/concat_qa.csv')

        return df

### testing code
# input_arr = ["2020-1-1", "2020-1-2", "7", "50", "titles", "creation_date_desc", ""]
# request_data(input_arr)

# df = pd.read_csv("output/raw_q.csv")
# columns_titles = ["id", "body", "title","title"]
# df = df.reindex(columns=columns_titles)
#
# df.to_csv('output/raw.csv')
